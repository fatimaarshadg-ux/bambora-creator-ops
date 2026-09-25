"""Work out which subreddits actually discuss a topic.

Arctic Shift needs a subreddit to search inside, so this stage answers "where
is this conversation happening?" before harvesting. Three signals get merged,
strongest first:

  1. Real occurrences  — a global search that returns the subreddits where the
     phrase genuinely appears. This is by far the best signal because it is
     evidence rather than inference, but the only free global-search source
     (PullPush) is flaky, so it is treated as a bonus, not a dependency.
  2. Official search   — Reddit's own post search, if credentials are set.
     Also evidence-based, and current.
  3. Name matching     — subreddits whose names start with a word from the
     query. Weakest signal, but it never fails and it surfaces the obvious
     hubs (r/Haircare for "hair") that occurrence search can miss.

Communities found by more than one signal rank highest, which is a decent proxy
for "this is really where the topic lives".
"""
from __future__ import annotations

import re
import sys

from . import arctic, http

STOP = {"the", "a", "an", "and", "or", "for", "of", "my", "is", "to", "in",
        "with", "on", "it", "that", "this", "best", "good", "how", "why"}


def _tokens(query):
    words = [w for w in re.split(r"[^a-z0-9]+", query.lower()) if w]
    return [w for w in words if w not in STOP and len(w) > 2]


def phrase_query(query):
    """Quote multi-word queries so the search engine matches the phrase.

    This matters more than it looks. Unquoted, "fine hair" matches any comment
    containing "fine" OR "hair", which on Reddit means the results drown in
    promo spam that stuffs common words. Quoted, the same search comes back
    almost entirely on-topic.
    """
    q = query.strip()
    if " " in q and not (q.startswith('"') and q.endswith('"')):
        return '"%s"' % q
    return q


def _pullpush_subs(query, sample=100):
    """Global comment search purely to learn which subreddits show up."""
    url = http.qs("https://api.pullpush.io/reddit/search/comment/",
                  q=phrase_query(query), size=min(sample, 100), sort="desc")
    data = http.fetch_json(url, delay=1.6, retries=1)
    needle = query.strip().lower()
    counts = {}
    for r in data.get("data") or []:
        sub = r.get("subreddit")
        # Trust only rows that really contain the phrase; the index is fuzzy
        # at the edges and this keeps the subreddit tally honest.
        if sub and needle in (r.get("body") or "").lower():
            counts[sub] = counts.get(sub, 0) + 1
    return counts


# Adult and promo subreddits share word stems with ordinary product topics
# ("hair", "skin", "body"), so they surface in both name matching and global
# search. Quoting the phrase removes most of them; this catches the rest by
# name, at zero request cost, which matters because the archive rate-limits
# and a screening pass that needs one lookup per candidate is exactly the kind
# of overhead that turns a 20-second discovery into a three-minute one.
_ADULT = re.compile(
    r"onlyfans|gonewild|nsfw|porn|nude|nudes|sexy|hentai|escort|camgirl"
    r"|boobs|tits|ass_|_ass|milf|fetish|kink|bdsm|thick|booty|lewd",
    re.I,
)

_sub_cache = {}


def _screen(names, verbose=True, lookups=4):
    """Drop adult/promo subreddits and attach subscriber counts where known.

    Name patterns handle it for free. A small budget of API lookups is spent
    only on the top candidates, and a failed lookup keeps the subreddit rather
    than dropping it — a rate-limited archive should not silently shrink your
    research.
    """
    keep, dropped = [], []
    budget = lookups
    for n in names:
        if _ADULT.search(n):
            dropped.append(n)
            continue
        subs = _sub_cache.get(n.lower(), "unknown")
        if subs == "unknown" and budget > 0:
            budget -= 1
            try:
                rows = arctic.find_subreddits(n, limit=1, allow_nsfw=True)
                hit = next((r for r in rows if r["subreddit"].lower() == n.lower()), None)
                if hit and hit.get("over18"):
                    _sub_cache[n.lower()] = None
                    dropped.append(n)
                    continue
                subs = hit.get("subscribers") if hit else None
                _sub_cache[n.lower()] = subs
            except Exception:
                subs = None
        if subs == "unknown":
            subs = None
        keep.append((n, subs))
    if verbose and dropped:
        print("      screened out %d adult/promo subreddit(s)" % len(dropped))
    return keep


def discover(query, limit=12, live=None, verbose=True):
    scored = {}
    meta = {}

    def bump(sub, points, why):
        key = sub.lower()
        scored[key] = scored.get(key, 0) + points
        m = meta.setdefault(key, {"subreddit": sub, "why": set()})
        m["why"].add(why)

    # 1. real occurrences via global search
    try:
        counts = _pullpush_subs(query)
        for sub, n in counts.items():
            bump(sub, 10 + min(n, 20), "mentions")
        if verbose and counts:
            print("      global search: %d subreddits with real mentions" % len(counts))
    except Exception as e:
        if verbose:
            print("      global search unavailable (%s) — using name + official search"
                  % str(e)[:60])

    # 2. official search, when credentials exist
    if live is not None and getattr(live, "configured", False):
        try:
            posts = live.search_posts(query, limit=100)
            counts = {}
            for p in posts:
                v = (p.get("venue") or "")[2:]
                if v:
                    counts[v] = counts.get(v, 0) + 1
            for sub, n in counts.items():
                bump(sub, 8 + min(n, 15), "posts")
            if verbose and counts:
                print("      official search: %d subreddits" % len(counts))
        except Exception as e:
            if verbose:
                print("      official search failed (%s)" % str(e)[:60])

    # 3. name matching — always works, catches the obvious hubs
    for tok in _tokens(query)[:3]:
        try:
            for s in arctic.find_subreddits(tok, limit=8):
                # popularity is a weak tiebreak, deliberately compressed so a
                # huge generic sub cannot outrank a small on-topic one
                bump(s["subreddit"], 3 + min(s["subscribers"] // 500000, 4), "name")
                meta[s["subreddit"].lower()]["subscribers"] = s["subscribers"]
        except Exception:
            pass

    ranked = sorted(
        scored.items(),
        key=lambda kv: (len(meta[kv[0]]["why"]), kv[1]),
        reverse=True,
    )
    shortlist = [meta[k]["subreddit"] for k, _ in ranked[: limit + 4]]
    screened = _screen(shortlist, verbose=verbose)

    rows = []
    for name, subscribers in screened:
        key = name.lower()
        m = meta[key]
        rows.append({
            "subreddit": name,
            "score": scored[key],
            "signals": sorted(m["why"]),
            "subscribers": subscribers if subscribers is not None else m.get("subscribers"),
        })
    rows.sort(key=lambda r: (len(r["signals"]), r["score"]), reverse=True)
    return rows[:limit]
