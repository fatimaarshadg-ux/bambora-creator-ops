"""Arctic Shift — a current, reliable Reddit archive.

This is the primary Reddit source. Compared to PullPush it is fresher (comments
from today, not months ago) and far less prone to rate-limit rejections, which
matters more than raw breadth when you actually need a run to finish.

The one real constraint: full-text search must be scoped to a subreddit (or an
author). There is no global "search all of Reddit for this phrase" here. That
shapes the workflow into two stages — work out which communities discuss your
topic, then harvest those communities deeply. That ordering is usually better
research practice anyway, because it tells you *where* your customers gather,
not just that a phrase exists somewhere.
"""
from __future__ import annotations

import calendar
import datetime

import re

from . import http
from .store import record, utc_iso


def _epoch(v):
    """Accept epoch seconds or YYYY-MM-DD and return an int.

    The API takes either form, but pagination compares the cursor against
    timestamps, so everything has to be normalised before arithmetic.
    """
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return int(v)
    txt = str(v).strip()
    if txt.isdigit():
        return int(txt)
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y/%m/%d"):
        try:
            return calendar.timegm(datetime.datetime.strptime(txt, fmt).timetuple())
        except ValueError:
            continue
    raise ValueError(
        "cannot read %r as a date; use YYYY-MM-DD or epoch seconds" % v
    )

BASE = "https://arctic-shift.photon-reddit.com/api"
DELAY = 1.2  # arctic-shift answers 422 "slow down" if pushed harder

# Ceiling on pages per subreddit per keyword, at 100 records a page. A cap is
# needed because pagination ends only when a subreddit runs out of history,
# which for a large one is a very long time. Raise it for a deep historical
# pull; the throttling in http.py keeps even a large run polite.
MAX_PAGES = 60


def find_subreddits(term, limit=20, allow_nsfw=False):
    """Find subreddits whose *name* starts with a term. Returns dicts with
    display_name and subscribers, biggest first.

    Name-prefix matching is a blunt instrument — r/FineHair will surface for
    "hair" but a community like r/femalehairadvice will not surface for "fine".
    Treat this as one input to picking subreddits, not the whole answer.
    """
    url = http.qs("%s/subreddits/search" % BASE, subreddit_prefix=term,
                  limit=max(limit * 3, 30))
    data = http.fetch_json(url, delay=DELAY)
    rows = data.get("data") or []
    out = []
    for r in rows:
        name = r.get("display_name")
        if not name:
            continue
        # Name-prefix matching on a term like "hair" drags in a lot of adult
        # subreddits that share the stem. They are never customer research.
        if r.get("over18") and not allow_nsfw:
            continue
        out.append({
            "subreddit": name,
            "subscribers": r.get("subscribers") or 0,
            "title": r.get("title") or r.get("public_description") or "",
            "over18": bool(r.get("over18")),
        })
    out.sort(key=lambda x: x["subscribers"], reverse=True)
    return out[:limit]


def search_comments(body, subreddit, limit=200, after=None, before=None,
                    query=None, allow_scan=True, on_note=None,
                    scan_cap=4000, exact_only=False, on_progress=None):
    """Find comments containing a phrase inside one subreddit, newest first.

    Two strategies, because the fast one is not dependable. Arctic Shift runs
    the text filter server-side, which is efficient when it succeeds, but under
    load it answers 422 "Timeout. Maybe slow down" on queries that worked
    minutes earlier. That is a property of the service, not of your query, so
    retrying the same thing harder does not help.

    The fallback pulls the subreddit's recent comments unfiltered — about a
    second per hundred, and it effectively never times out because there is no
    text predicate for the server to evaluate — then matches the phrase here.
    It reads more data to find the same quotes, which is a fair trade for a run
    that actually finishes.
    """
    got, failed = [], False
    try:
        # Two retries: the server-side filter yields roughly an order of
        # magnitude more matches per request than scanning does, so it is
        # worth waiting on before giving up.
        got = _paged("comments/search", "body", body, subreddit, limit,
                     after, before, query or body, "comment", retries=2)
    except http.FetchError as e:
        if not allow_scan or e.status not in (-2, 422, 429, 500, 502, 503, 504):
            raise
        failed = True

    # A short result means the filter died partway through — under load it
    # routinely dies after the first page. Keeping only that page silently
    # capped harvests at a day or two of history, so top the result up by
    # scanning backward from where it left off. Neither strategy alone is
    # dependable; together they are.
    if len(got) >= limit:
        return got[:limit]
    if not failed and got:
        return got  # genuinely ran out of matches, not a failure

    if not allow_scan:
        return got

    if on_note and failed:
        note = "server-side search stopped after %d; scanning for the rest" % len(got)
        on_note(note)

    seen_ids = set(r["id"] for r in got)
    # Resume from the oldest record already held so the scan covers new ground.
    resume = None
    if got:
        stamps = [r.get("created") for r in got if r.get("created")]
        if stamps:
            resume = _epoch(min(stamps)[:10])
    try:
        more = scan_comments(body, subreddit, limit=limit - len(got), after=after,
                             before=resume or before, query=query or body,
                             scan_cap=scan_cap, exact_only=exact_only,
                             on_progress=on_progress)
        got.extend(r for r in more if r["id"] not in seen_ids)
    except http.FetchError:
        # Whatever the first strategy managed is still worth returning.
        pass
    return got[:limit]


def scan_comments(needle, subreddit, limit=200, after=None, before=None,
                  query=None, scan_cap=4000, exact_only=False, on_progress=None):
    """Pull a subreddit's recent comments and filter for the phrase locally.

    `scan_cap` bounds how much gets read while hunting for `limit` matches, so
    a rare phrase degrades into a bounded scan rather than an unbounded crawl.

    Keeps the same two grades of match the server-side search produces: the
    exact phrase, and comments where every word appears but not adjacently
    ("fine, dense, wavy hair" for "fine hair"). Matching only the exact phrase
    here would mean results quietly changed shape depending on which code path
    happened to run, which is a nasty thing for a research tool to do.
    """
    from .store import match, near_match

    after = _epoch(after)
    found, seen, cursor = [], 0, _epoch(before)
    words = [w for w in re.split(r"[^\w]+", needle or "") if len(w) > 2]
    guard = 0
    while len(found) < limit and seen < scan_cap and guard < MAX_PAGES:
        guard += 1
        url = http.qs("%s/comments/search" % BASE, subreddit=subreddit,
                      limit=100, sort="desc", after=after, before=cursor)
        data = http.fetch_json(url, delay=DELAY)
        if data.get("error"):
            raise http.FetchError(-1, url, str(data["error"]))
        rows = data.get("data") or []
        if not rows:
            break
        seen += len(rows)
        for r in rows:
            rec = _norm(r, "comment", query or needle)
            # An empty needle means "take everything" — used for health checks
            # and for pulling a subreddit's raw recent activity.
            if not (needle or "").strip():
                found.append(rec)
                continue
            ok, _ = match(rec, [needle], mode="any")
            if ok:
                rec["exact"] = True
                found.append(rec)
            elif not exact_only and words:
                near, _ = near_match(rec, words)
                if near:
                    rec["exact"] = False
                    found.append(rec)
        if on_progress:
            on_progress(seen, len(found))
        oldest = min(int(r.get("created_utc", 0)) for r in rows)
        if cursor is not None and oldest >= int(cursor):
            break
        cursor = oldest
        if len(rows) < 100:
            break
    return found[:limit]


def search_posts(text, subreddit, limit=100, after=None, before=None, query=None):
    """Search post selftext inside one subreddit."""
    return _paged("posts/search", "selftext", text, subreddit, limit,
                  after, before, query or text, "post")


def _paged(endpoint, field, needle, subreddit, limit, after, before, query, kind,
           retries=http.DEFAULT_RETRIES):
    out = []
    after = _epoch(after)
    cursor = _epoch(before)
    guard = 0
    while len(out) < limit and guard < MAX_PAGES:
        guard += 1
        want = min(100, limit - len(out))
        params = {field: needle, "subreddit": subreddit, "limit": want,
                  "sort": "desc", "after": after, "before": cursor}
        url = http.qs("%s/%s" % (BASE, endpoint), **params)
        try:
            data = http.fetch_json(url, delay=DELAY, retries=retries)
            if data.get("error"):
                raise http.FetchError(-1, url, str(data["error"]))
        except http.FetchError:
            # Losing page 5 is no reason to discard pages 1-4. The server-side
            # filter is an order of magnitude more efficient than scanning, so
            # a partial result from it usually beats a complete scan — and
            # throwing it away was silently capping every harvest at whatever
            # the fallback could read.
            if out:
                return out[:limit]
            raise
        rows = data.get("data") or []
        if not rows:
            break
        for r in rows:
            out.append(_norm(r, kind, query))
        oldest = min(int(r.get("created_utc", 0)) for r in rows)
        if cursor is not None and oldest >= int(cursor):
            break  # cursor not advancing — stop rather than spin
        cursor = oldest
        if len(rows) < want:
            break
    return out[:limit]


def _norm(r, kind, query):
    if kind == "comment":
        text = r.get("body") or ""
        title = r.get("link_title")
    else:
        parts = [r.get("title") or "", r.get("selftext") or ""]
        text = "\n\n".join(p for p in parts if p.strip())
        title = r.get("title")
    perma = r.get("permalink") or ""
    url = ("https://reddit.com" + perma) if perma.startswith("/") else (perma or None)
    return record(
        "reddit", kind, r.get("id"), text,
        author=("u/" + r["author"]) if r.get("author") else None,
        venue=("r/" + r["subreddit"]) if r.get("subreddit") else None,
        title=title, url=url,
        created=utc_iso(r.get("created_utc")) if r.get("created_utc") else None,
        score=r.get("score"), query=query,
        extra={"via": "arctic-shift", "link_id": r.get("link_id")},
    )
