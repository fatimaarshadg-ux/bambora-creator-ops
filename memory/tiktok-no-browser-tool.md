---
name: tiktok-no-browser-tool
description: Read TikTok creators with ~/claude-setup/work/social-tools/tt.py (yt-dlp + public comment API), not the browser; browser page loads get 403-blocked
metadata:
  type: reference
---

For any TikTok check (recent videos, views, likes, comment counts, comment text, downloading a video to watch), use:

`py -3 ~/claude-setup/work/social-tools/tt.py <handle> --videos 6 --comments 15 [--download DIR]`

- Listing, stats and downloads go through yt-dlp (on the PATH). Comment text comes from `https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id=<id>&count=N`, which needs a normal User-Agent and Referer and no login.
- A downloaded video can be watched with media-watcher (see [[media-watcher-installed]]), with sound, frames and a transcript.
- **Don't use the browser for TikTok.** On 2026-09-23 fast page loads, and especially loading /video/ URLs directly, got an HTTP 403 "Access denied" for about 20 minutes, twice.
- Profile follower and like counts are still easiest from the profile page (`[data-e2e=followers-count]`, `likes-count`) if one visit is enough. Otherwise sum from yt-dlp.
- Instagram profile counts: loading `instagram.com/<handle>/` in her logged-in Chrome and reading the `og:description` meta works, at a pace of 3 seconds or more. No blocks yet.

Related: [[bambora-creator-acceptance-criteria]]

**Finding videos by topic (added 2026-09-23):** `tt_find.py` in the same folder searches the web for TikTok video URLs (DuckDuckGo then Bing, `site:tiktok.com <topic>`), reads views with yt-dlp, and ranks them. `--shop` adds TikTok Shop phrasing ("tiktok shop", "#tiktokshop review", "tiktok made me buy it"), `--seen` skips URLs already used. TikTok's own /tag/ and search pages fail in yt-dlp ("No working app info"), so don't bother with them. Fatima asked for this so TikTok Shop videos can feed the inspo runs.
