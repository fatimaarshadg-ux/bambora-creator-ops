---
name: inspo-sources-and-style
description: Where to find creator inspo and what kind; broad scope (any category's formats adapted to the sling), sources, and her reference YouTube Short; Atria MCP address
metadata:
  type: reference
---

**Scope (her words, 2026-09-23):** not just babywearing. That was one example. Look broadly: mom and parenting life, top UGC ads in any category (beauty, home, kitchen, gadgets), TikTok Shop and Amazon-finds formats, weekly trends and sounds, competitors and adjacent baby gear. Each item becomes "here's the format, here's how you'd do it with the sling", matched to the creator, with a safety note when a baby is in shot.

**Reference style for YouTube:** https://www.youtube.com/shorts/KvikgsaZomc ("look for inspo like this on yt"). Watch it with media-watcher before the first YouTube search.

**Sources:**
- Trybe top performers (API).
- TikTok via ~/claude-setup/work/social-tools/tt.py (no browser).
- YouTube Shorts via yt-dlp `ytsearch`.
- Instagram through her logged-in Chrome, light and read-only (no likes, follows or comments) so her account isn't flagged. Apify for scale.
- **Atria: CONNECTED 2026-09-23** (custom connector, official MCP `https://api.tryatria.com/mcp`, OAuth). Its tools appear as `mcp__<id>__search_library_ads` and similar; the id prefix may differ per machine, so find them with ToolSearch "atria" or "search_library_ads". Useful calls: `search_library_ads` (filter by industry, theme=UGC, media_format=video, order=most_impressions, impression_trend=rising), `get_library_ad_creative_tags` (hooks, angles), `transcribe_library_ad`, `save_library_ad` to a board. Workspace state on connect: no owned brand, no followed advertisers, only the default boards; set up on 2026-09-23 on her go:
  - **Board:** "Bambora Creator Inspo", id `6252eeab-7896-45f8-9dbf-78b60cb6d240`. Save the best finds here every 3 days.
  - **Newly followed (22):** competitors Tushbaby, Solly Baby, Konny Baby, Baby Tula, Ergobaby; baby brands Happiest Baby, Kyte Baby, Coterie Baby, Frida ("fridamom"); hook sources Histrips (Hi Strips), Hume Health, Root'd (prenatal), KiddoSpace-UK, EllaOla, Sutera Home Goods, FFS Beauty, Nailboo, Bare Bones, Brevite. She already followed Bambora, Smooche, Rise Science, Koriderm, Resilia, Ankhway, Lymphoria, RYZE, Lullahug, HIKE, Hears, KittySpout and others.
  - **Also followed 2026-09-23 (her request):** Baby Bunting (AU retailer, only 30 ads), Colugo Strollers, plus Wildride (toddler carrier competitor found via the Baby Bunting domain). Baby Tula was already followed.
  - **Quota:** 46 of 50 used (it is a concurrent cap on followed brands, not daily; unfollowing frees a slot). Quiet older follows she may want to drop: Moongrade, Liven, Your Relationship Advisor, Quasico. Keep a few free, and ask before using the last ones.
  - **Her guidance:** follow competitors AND brands in other niches that use real humans in their videos (hooks, formats), e.g. Histrips, Hume Health, Smooche. She's fine with Claude finding and following relevant brands.
  - "Hi Strips" only resolves by domain (histrips.com). Use resolve_advertiser with the domain when a name misses.
- Apify: pay-per-use, token would be stored with DPAPI like the Trybe key (not set up yet).

**Cadence:** every 3 days (see [[creator-response-cadence]]). Before building a brand or handle watch list, verify each handle exists; show her the list first. She interrupted a handle-verification run to connect Atria first, so the list is still to do.

**Research cadence (her spec, 2026-09-23, run without asking):** every 3 days, (1) Atria followed brands' top-impression human videos over the last 7 days (lifetime on the first run), (2) Atria trending ads over the last 7 days (14 on the first run), human ones only, downloaded to Drive "Bambora Inspo / Week of YYYY-MM-DD", (3) YouTube, Instagram and TikTok popular human videos for moms (links are fine if downloading is hard), plus an index doc. She reviews and gives suggestions. Full steps: skill creator-ops-daily, section 7a.

**Drive (from 2026-09-23):** weekly packs go in "Bambora Inspo" (`1HleYAep0n7C5gFGt3RhRsgy0dmiQEb8Y`), one subfolder per week. The Sep 23 week is `1s3Sfr56gxT-vNfFDyAc07ByDz5XZ6uOM`. Fatima hasn't reviewed the first pack yet; learn her taste from her picks.
