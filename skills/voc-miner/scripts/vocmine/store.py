"""Normalized record schema + append-only JSONL store.

Every source gets flattened into one record shape so that quote extraction,
filtering, and export work the same whether the text came from a Reddit
comment or a YouTube reply. The store is append-only and deduped by id, so
re-running a search that overlaps a previous one is cheap and safe.
"""
from __future__ import annotations

import datetime
import json
import os
import re


def utc_iso(ts=None):
    if ts is None:
        dt = datetime.datetime.utcnow()
    else:
        dt = datetime.datetime.utcfromtimestamp(float(ts))
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def record(source, kind, uid, text, author=None, venue=None, title=None,
           url=None, created=None, score=None, query=None, extra=None):
    """Build one normalized record.

    `text` is stored exactly as the platform returned it. Never clean, trim,
    or 'fix' it here — the whole point of this tool is verbatim customer
    language, and normalizing away a typo or an ALL-CAPS rant destroys the
    signal you came for.
    """
    r = {
        "id": "%s:%s" % (source, uid),
        "source": source,
        "kind": kind,
        "text": text or "",
        "author": author,
        "venue": venue,
        "title": title,
        "url": url,
        "created": created,
        "score": score,
        "query": query,
        "fetched_at": utc_iso(),
    }
    if extra:
        r["extra"] = extra
    return r


class Store:
    def __init__(self, path):
        self.path = path
        d = os.path.dirname(os.path.abspath(path))
        if d:
            os.makedirs(d, exist_ok=True)
        self._seen = set()
        if os.path.exists(path):
            for r in self.read():
                self._seen.add(r.get("id"))

    def read(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except ValueError:
                    continue

    def add_many(self, records):
        """Append records, skipping ids already stored. Returns count added."""
        added = 0
        with open(self.path, "a", encoding="utf-8") as f:
            for r in records:
                rid = r.get("id")
                if not rid or rid in self._seen:
                    continue
                if not (r.get("text") or "").strip():
                    continue
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                self._seen.add(rid)
                added += 1
        return added

    def __len__(self):
        return len(self._seen)


# Reddit marks removed/deleted content with these exact bodies. They carry no
# customer language, so they are noise in every downstream view.
DEAD_BODIES = {"[deleted]", "[removed]", "", "[unavailable]"}


def is_dead(rec):
    return (rec.get("text") or "").strip().lower() in DEAD_BODIES


# Automated accounts post on-topic text constantly — AutoModerator alone will
# reply "it seems like you may be looking for information about dark circles"
# to every relevant thread. That is a perfect keyword match and worthless as
# customer language, so it has to go before it reaches a quote export.
_BOT_NAMES = re.compile(r"^u?/?(automoderator|.*[-_]?bot|botrank|remindme.*)$", re.I)

# The disclaimer has to end a clause to count. Matching "i am a bot" loose
# would also catch a real person writing "I am a bot enthusiast honestly",
# and dropping genuine customer language is the more costly error here.
_BOT_DISCLAIMER = re.compile(
    r"\bi(?:'m| am) a bot\b\s*(?:[.,;!)\]]|$)"
    r"|\bthis action was performed automatically\b"
    r"|\bbeep boop\b"
    r"|\bplease contact the moderators of this subreddit\b",
    re.I | re.M,
)


def is_bot(rec):
    """True when a record was written by an automated account."""
    author = (rec.get("author") or "").strip()
    if author and _BOT_NAMES.match(author):
        return True
    return bool(_BOT_DISCLAIMER.search(rec.get("text") or ""))


def _norm_ws(text):
    """Flatten exotic whitespace for matching purposes only.

    YouTube in particular returns non-breaking spaces inside ordinary prose, so
    "fine\xa0hair" would silently fail a search for "fine hair". The stored
    text is never touched — only the copy used for comparison — because the
    verbatim record is the product here.
    """
    return (text or "").replace("\xa0", " ").replace("\u200b", "")


def near_match(rec, words, slack=1):
    """True when the query's words appear in order, in one tight span.

    Plain AND-matching is far too loose to be useful. Searching "fine hair"
    against "Cantu was created for Black hair, so it's fine for 4A-C types"
    succeeds, even though "fine" there means "acceptable". Distance alone does
    not save it either — the words sit four tokens apart there, versus three in
    "fine, dense, wavy hair", which is a phrasing you would want to keep.

    What actually separates them is order. Real variants of a phrase keep the
    words in the order the phrase has them ("fine ... hair"), while
    coincidental co-occurrence usually reverses or scatters them. Requiring
    original order inside a span of len(words) + slack keeps the genuine
    rewordings and drops the accidents.
    """
    wanted = [w.lower() for w in words if w]
    if not wanted:
        return False, []
    span_limit = len(wanted) + slack

    # Confine the search to a single sentence. "fine, dense, wavy hair" and
    # "that is fine. anyway my hair" put the words the same distance apart, so
    # position alone cannot tell them apart — but the second crosses a full
    # stop, and a phrase never spans one. This is what makes the tier reliable.
    for sentence in re.split(r"[.!?\n]+", _norm_ws(rec.get("text")).lower()):
        toks = re.findall(r"\w+", sentence)
        if not toks:
            continue
        positions = {}
        for i, t in enumerate(toks):
            if t in wanted:
                positions.setdefault(t, []).append(i)
        if any(w not in positions for w in wanted):
            continue
        # Walk each occurrence of the first word and try to pick a strictly
        # increasing position for every following word within the span.
        for start in positions[wanted[0]]:
            cur = start
            ok = True
            for w in wanted[1:]:
                nxt = next((p for p in positions[w] if p > cur), None)
                if nxt is None or nxt - start > span_limit:
                    ok = False
                    break
                cur = nxt
            if ok:
                return True, wanted
    return False, []


def match(rec, terms, mode="any"):
    """Case-insensitive whole-phrase match against a record's text.

    Uses word boundaries so 'fine hair' does not match 'superfine hairline',
    but phrases with punctuation still work.
    """
    text = _norm_ws(rec.get("text")).lower()
    hits = []
    for t in terms:
        t = t.strip().lower()
        if not t:
            continue
        pat = r"(?<!\w)" + re.escape(t).replace(r"\ ", r"\s+") + r"(?!\w)"
        if re.search(pat, text):
            hits.append(t)
    if not terms:
        return True, []
    ok = bool(hits) if mode == "any" else len(hits) == len([t for t in terms if t.strip()])
    return ok, hits
