"""YouTube comments via the official Data API v3.

Free and generous: 10,000 quota units/day with no billing account attached.
The pricing shape matters when planning a run — search.list costs 100 units
per call, while commentThreads.list costs 1 unit for up to 100 comments. So
searching is the expensive part and comment harvesting is nearly free. Find
a handful of relevant videos, then pull their comments exhaustively.

Needs YOUTUBE_API_KEY in the environment; see references/setup.md.
"""
from __future__ import annotations

import html
import os

from . import config, http
from .store import record

API = "https://www.googleapis.com/youtube/v3"


class YouTube:
    def __init__(self, api_key=None):
        self.key = api_key or config.get("YOUTUBE_API_KEY")

    @property
    def configured(self):
        return bool(self.key)

    def _get(self, endpoint, **params):
        if not self.configured:
            raise RuntimeError(
                "YouTube needs YOUTUBE_API_KEY (free, no billing). See references/setup.md."
            )
        url = http.qs("%s/%s" % (API, endpoint), key=self.key, **params)
        return http.fetch_json(url, delay=0.35)

    def search_videos(self, q, limit=10, order="relevance", published_after=None,
                      published_before=None, region=None, language=None):
        """Find videos for a keyword. Costs 100 quota units per 50 results.

        `region` (ISO 3166-1 alpha-2, e.g. "US") and `language` (ISO 639-1,
        e.g. "en") shape which videos come back. Be careful what you conclude
        from them: they bias results toward what is surfaced in that market,
        not toward creators who live there, and they say nothing at all about
        where the commenters are. YouTube exposes no commenter-location field,
        so "US customers only" is not something this can honestly deliver.
        """
        out, token = [], None
        while len(out) < limit:
            data = self._get(
                "search", part="snippet", q=q, type="video",
                maxResults=min(50, limit - len(out)), order=order,
                publishedAfter=published_after, publishedBefore=published_before,
                regionCode=region, relevanceLanguage=language, pageToken=token,
            )
            for it in data.get("items", []):
                vid = it.get("id", {}).get("videoId")
                sn = it.get("snippet", {})
                if not vid:
                    continue
                out.append({
                    "video_id": vid,
                    # Search results arrive HTML-escaped ("doesn&#39;t"), unlike
                    # comment bodies fetched with textFormat=plainText.
                    "title": html.unescape(sn.get("title") or ""),
                    "channel": html.unescape(sn.get("channelTitle") or ""),
                    "published": sn.get("publishedAt"),
                })
            token = data.get("nextPageToken")
            if not token:
                break
        return out[:limit]

    def comments(self, video_id, limit=500, query=None, video_title=None):
        """Pull comments and their replies for one video. ~1 unit per 100."""
        out, token = [], None
        while len(out) < limit:
            try:
                data = self._get(
                    "commentThreads", part="snippet,replies", videoId=video_id,
                    maxResults=100, order="relevance", textFormat="plainText",
                    pageToken=token,
                )
            except http.FetchError as e:
                # Comments disabled on a video is a normal, expected condition —
                # it should skip that video, not abort a whole research run.
                if e.status in (403, 404):
                    break
                raise
            for it in data.get("items", []):
                top = it.get("snippet", {}).get("topLevelComment", {})
                out.append(self._norm(top, video_id, video_title, query, "comment"))
                for rep in (it.get("replies", {}) or {}).get("comments", []):
                    out.append(self._norm(rep, video_id, video_title, query, "reply"))
            token = data.get("nextPageToken")
            if not token:
                break
        return out[:limit]

    def _norm(self, node, video_id, video_title, query, kind):
        sn = node.get("snippet", {}) or {}
        cid = node.get("id") or sn.get("parentId", "") + ":?"
        return record(
            "youtube", kind, cid, sn.get("textOriginal") or sn.get("textDisplay") or "",
            author=sn.get("authorDisplayName"),
            venue="YouTube",
            title=video_title,
            url="https://www.youtube.com/watch?v=%s&lc=%s" % (video_id, cid),
            created=(sn.get("publishedAt") or "").replace(".000Z", "Z") or None,
            score=sn.get("likeCount"), query=query,
            extra={"video_id": video_id, "channel": sn.get("authorChannelUrl")},
        )
