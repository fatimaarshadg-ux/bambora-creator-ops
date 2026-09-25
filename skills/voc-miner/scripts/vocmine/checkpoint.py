"""Resume state, so consecutive runs reach new material instead of re-reading.

Deduplication alone is not enough. Without a memory of how far back a previous
run got, every run starts at "now" and re-reads the same recent comments, then
discards them as duplicates — the corpus stops growing while the request count
keeps climbing. That looks exactly like the archive being empty, when really
the tool is walking the same ground.

So each (source, keyword, venue) triple remembers the oldest timestamp already
harvested. The next run starts just before it, which makes "run it again to get
more" genuinely work, and makes the whole thing safe to schedule.

For YouTube the unit is the video rather than a timestamp: comment ordering
cannot be steered by date, so progress means "which videos have been mined",
and a later run picks up videos it has not seen.
"""
from __future__ import annotations

import json
import os

DEFAULT_PATH = os.path.expanduser("~/voc-data/checkpoints.json")


class Checkpoints:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.data = {}
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except (ValueError, OSError):
                # A corrupt checkpoint should cost you one redundant run, not
                # the whole harvest.
                self.data = {}

    @staticmethod
    def _key(source, query, venue):
        return "%s|%s|%s" % (source, (query or "").strip().lower(), venue or "")

    def oldest(self, source, query, venue):
        """Epoch seconds of the oldest record a previous run reached, or None."""
        return self.data.get(self._key(source, query, venue), {}).get("oldest")

    def note(self, source, query, venue, oldest_epoch, added=0):
        if not oldest_epoch:
            return
        k = self._key(source, query, venue)
        cur = self.data.get(k, {})
        prev = cur.get("oldest")
        # Only ever move backward in time; a run that happened to fetch newer
        # material must not erase how far back we already are.
        cur["oldest"] = min(prev, oldest_epoch) if prev else oldest_epoch
        cur["runs"] = cur.get("runs", 0) + 1
        cur["total"] = cur.get("total", 0) + added
        self.data[k] = cur

    def seen_videos(self, query):
        return set(self.data.get(self._key("youtube_videos", query, ""), {}).get("ids", []))

    def add_videos(self, query, ids):
        k = self._key("youtube_videos", query, "")
        cur = self.data.setdefault(k, {"ids": []})
        have = set(cur["ids"])
        for i in ids:
            if i not in have:
                cur["ids"].append(i)
                have.add(i)

    def reset(self, query=None):
        if query is None:
            self.data = {}
            return
        needle = (query or "").strip().lower()
        self.data = {k: v for k, v in self.data.items()
                     if k.split("|")[1] != needle}

    def save(self):
        d = os.path.dirname(os.path.abspath(self.path))
        if d:
            os.makedirs(d, exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)
        os.replace(tmp, self.path)

    def summary(self, query=None):
        rows = []
        for k, v in sorted(self.data.items()):
            src, q, venue = k.split("|", 2)
            if src == "youtube_videos":
                continue
            if query and q != query.strip().lower():
                continue
            rows.append({"source": src, "query": q, "venue": venue,
                         "oldest": v.get("oldest"), "runs": v.get("runs", 0),
                         "total": v.get("total", 0)})
        return rows
