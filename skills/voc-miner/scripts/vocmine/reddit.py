"""Reddit access via two complementary free paths.

These are not redundant, and picking the wrong one is the most common way to
come back empty-handed:

  archive (PullPush)  — the ONLY free way to keyword-search *comment bodies*
                        across all of Reddit. No auth. Rate-limited hard, and
                        the archive lags real time by months. This is where
                        verbatim customer quotes actually live, because people
                        describe their problems in comments, not post titles.

  live (official API) — Reddit's own search only indexes post titles and
                        selftext, never comment bodies. What it is good for is
                        current data and pulling a complete thread (every
                        comment, nested) once you know its id. Needs free
                        credentials; see references/setup.md.

Typical flow: search the archive for the phrase to find where the conversation
happens, then use live thread fetches to read those discussions in full and
current form.
"""
from __future__ import annotations

import base64
import os
import sys

from . import config, http
from .store import record, utc_iso

ARCHIVE = "https://api.pullpush.io/reddit/search"
# PullPush is a volunteer-run archive. Going faster than this gets you 429s
# and, sustained, hurts a resource the whole research community depends on.
ARCHIVE_DELAY = 1.6


# ---------------------------------------------------------------- archive ---

def _archive_page(kind, q, subreddit=None, before=None, after=None, size=100):
    url = http.qs(
        "%s/%s/" % (ARCHIVE, kind),
        q=q, subreddit=subreddit, before=before, after=after,
        size=min(size, 100), sort="desc",
    )
    data = http.fetch_json(url, delay=ARCHIVE_DELAY)
    return data.get("data") or []


def search_archive(q, kind="comment", subreddit=None, limit=200,
                   before=None, after=None, on_page=None):
    """Keyword-search Reddit comments or submissions across the archive.

    Pages backward in time using the oldest result's timestamp as the next
    `before` cursor, which is how PullPush expects to be paginated.
    """
    out = []
    cursor = before
    while len(out) < limit:
        want = min(100, limit - len(out))
        page = _archive_page(kind, q, subreddit=subreddit,
                             before=cursor, after=after, size=want)
        if not page:
            break
        for item in page:
            out.append(_norm_archive(item, kind, q))
        if on_page:
            on_page(len(out))
        oldest = min(int(i.get("created_utc", 0)) for i in page)
        if cursor is not None and oldest >= int(cursor):
            break  # not advancing; stop rather than loop forever
        cursor = oldest
        if len(page) < want:
            break
    return out[:limit]


def _norm_archive(item, kind, q):
    if kind == "comment":
        text = item.get("body") or ""
        title = item.get("link_title")
        uid = item.get("id")
        rkind = "comment"
    else:
        # A submission's customer language can be in either field; keep both.
        parts = [item.get("title") or "", item.get("selftext") or ""]
        text = "\n\n".join(p for p in parts if p.strip())
        title = item.get("title")
        uid = item.get("id")
        rkind = "post"
    perma = item.get("permalink") or ""
    url = ("https://reddit.com" + perma) if perma.startswith("/") else (perma or None)
    return record(
        "reddit", rkind, uid, text,
        author=("u/" + item["author"]) if item.get("author") else None,
        venue=("r/" + item["subreddit"]) if item.get("subreddit") else None,
        title=title, url=url,
        created=utc_iso(item.get("created_utc")) if item.get("created_utc") else None,
        score=item.get("score"), query=q,
        extra={"link_id": item.get("link_id"), "via": "pullpush"},
    )


# ------------------------------------------------------------------- live ---

class RedditLive:
    """Official Reddit API, app-only (read) auth.

    Credentials come from env: REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET.
    Registering a free 'script' app takes about two minutes — see
    references/setup.md. Without them, archive search still works.
    """

    def __init__(self, client_id=None, client_secret=None):
        self.cid = client_id or config.get("REDDIT_CLIENT_ID")
        self.csec = client_secret or config.get("REDDIT_CLIENT_SECRET")
        self._token = None

    @property
    def configured(self):
        return bool(self.cid and self.csec)

    def token(self):
        if self._token:
            return self._token
        if not self.configured:
            raise RuntimeError(
                "Reddit live API needs REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET. "
                "See references/setup.md, or use --source archive which needs no keys."
            )
        basic = base64.b64encode(("%s:%s" % (self.cid, self.csec)).encode()).decode()
        data = http.fetch_json(
            "https://www.reddit.com/api/v1/access_token",
            headers={"Authorization": "Basic " + basic,
                     "Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"},
            delay=0.6,
        )
        self._token = data.get("access_token")
        if not self._token:
            raise RuntimeError("Reddit did not return a token: %s" % data)
        return self._token

    def _get(self, path, **params):
        url = http.qs("https://oauth.reddit.com" + path, raw_json=1, **params)
        return http.fetch_json(
            url, headers={"Authorization": "Bearer " + self.token()}, delay=0.65
        )

    def search_posts(self, q, subreddit=None, limit=100, sort="relevance", t="all"):
        """Search post titles/selftext. Reddit does not index comment bodies here."""
        path = ("/r/%s/search" % subreddit) if subreddit else "/search"
        params = dict(q=q, limit=min(limit, 100), sort=sort, t=t)
        if subreddit:
            params["restrict_sr"] = 1
        out, after, seen = [], None, 0
        while seen < limit:
            data = self._get(path, after=after, **params)
            kids = data.get("data", {}).get("children", [])
            if not kids:
                break
            for c in kids:
                d = c["data"]
                body = "\n\n".join(p for p in [d.get("title", ""), d.get("selftext", "")] if p.strip())
                out.append(record(
                    "reddit", "post", d.get("id"), body,
                    author=("u/" + d["author"]) if d.get("author") else None,
                    venue=("r/" + d["subreddit"]) if d.get("subreddit") else None,
                    title=d.get("title"),
                    url="https://reddit.com" + d.get("permalink", ""),
                    created=utc_iso(d.get("created_utc")),
                    score=d.get("score"), query=q,
                    extra={"num_comments": d.get("num_comments"), "via": "oauth"},
                ))
            seen += len(kids)
            after = data.get("data", {}).get("after")
            if not after:
                break
        return out[:limit]

    def thread(self, post_id, subreddit=None, limit=500, query=None):
        """Fetch a complete thread: the post plus every comment, nested."""
        pid = post_id.split("_")[-1]
        path = "/r/%s/comments/%s" % (subreddit, pid) if subreddit else "/comments/%s" % pid
        data = self._get(path, limit=limit, depth=20)
        out = []
        if isinstance(data, list) and data:
            post = data[0].get("data", {}).get("children", [])
            title = None
            if post:
                d = post[0]["data"]
                title = d.get("title")
                body = "\n\n".join(p for p in [d.get("title", ""), d.get("selftext", "")] if p.strip())
                out.append(record(
                    "reddit", "post", d.get("id"), body,
                    author=("u/" + d["author"]) if d.get("author") else None,
                    venue=("r/" + d["subreddit"]) if d.get("subreddit") else None,
                    title=title, url="https://reddit.com" + d.get("permalink", ""),
                    created=utc_iso(d.get("created_utc")), score=d.get("score"),
                    query=query, extra={"via": "oauth"},
                ))
            for listing in data[1:]:
                _walk_comments(listing, out, title, query)
        return out


def _walk_comments(node, out, title, query):
    """Recursively collect t1 (comment) nodes from Reddit's nested listing."""
    if isinstance(node, list):
        for n in node:
            _walk_comments(n, out, title, query)
        return
    if not isinstance(node, dict):
        return
    if node.get("kind") == "t1":
        d = node.get("data", {}) or {}
        out.append(record(
            "reddit", "comment", d.get("id"), d.get("body") or "",
            author=("u/" + d["author"]) if d.get("author") else None,
            venue=("r/" + d["subreddit"]) if d.get("subreddit") else None,
            title=title,
            url="https://reddit.com" + d.get("permalink", "") if d.get("permalink") else None,
            created=utc_iso(d.get("created_utc")) if d.get("created_utc") else None,
            score=d.get("score"), query=query,
            extra={"depth": d.get("depth"), "via": "oauth"},
        ))
        _walk_comments(d.get("replies"), out, title, query)
        return
    for key in ("data", "children", "replies"):
        if key in node:
            _walk_comments(node[key], out, title, query)
