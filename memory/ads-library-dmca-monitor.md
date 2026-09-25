---
name: ads-library-dmca-monitor
description: "Bambora's Meta Ads Library copycat monitor (Apify + Python + Slack); first scan findings incl. the confirmed explicitn.com theft, and the exact pickup point"
metadata: 
  node_type: memory
  type: project
  originSessionId: afbb6282-ff80-4a70-8d42-68dd57edb732
  modified: 2026-09-22T17:03:23.431Z
---

**Status (paused 2026-09-23, she will be back in a few days; open by recapping this):** Fatima approved weekly runs with Slack alerts. The readable chat history of the build session is saved at `work/ads-library-dmca-monitor/findings/2026-09-22-conversation.md` (full export zip in her Downloads folder). Windows Task Scheduler job "Bambora Ads Library monitor" is registered (Mondays 09:00, first run 2026-09-28) and runs `monitor.py`, which now also posts a picture digest of every new sling-category ad (Slack blocks with thumbnails) plus the flagged-ad summary, and posts a plain failure note if Apify refuses (credit exhausted until ~2026-10-22, so the first weekly runs will report that unless she upgrades). Findings from the first review are in `work/ads-library-dmca-monitor/findings/2026-09-22-first-scan.md`. Still pending on her side: store the Slack webhook (channel #copycat-alerts, app "Bambora Copy Cat Hunter" already added; nothing posts until then) and file the Explicitn takedown. Option offered but not built: a scheduled cloud Claude routine that eyeballs the digest itself.

**Headline finding:** explicitn.com (page "Explicitn-ea", ad 2128834464362109) runs Bambora's own 56-second UGC video (frame-identical to Bambora ad 1835818061100628) and its product page clones Bambora's: same 13 colour options in order, 21 of 25 images are Bambora's product photos. Hosted behind Cloudflare, not Shopify. Ownership is clear: Bambora ad 1343534694113082 ran the same video from 2026-07-31, before the copy's 2026-08-07 start. Lookalike-but-not-theft clusters: Zenovap/Windlore (3 stores, one video, AI product images) and the eigoods/luckinwish/outrerbuy mesh-sling funnels. Real competitors with similar design: Mabē, Qookie, Lune & Littles, Senarah, Wildride.

**Tool:** `~/claude-setup/work/ads-library-dmca-monitor/` (synced). `monitor.py` runs Apify actor `apify/facebook-ads-scraper` on Ad Library search URLs from `config.json`; own ads = page IDs 253532267844120 / 61557300960466 or any link to bamboraco.com (that covers Trybe creator ads, which was her rule: if it doesn't mention Bambora or link to our landing page, it's not us); ignore list for same-name businesses (bambora.cl); flags `brand` / `copy` / `visual` (dHash within 10 of Bambora's own creatives, reference set built free from own ads in each scan). Secrets follow [[trybe-api-key-storage]]: `apify_api_token.dpapi` stored and working (FREE plan, monthly $5 credit exhausted by the first scan, resets around 2026-10-22); `slack_webhook.dpapi` NOT stored. `store-secret.ps1` is a WinForms popup (Ctrl+V failed in the console prompt). Config now set for weekly runs on ads newer than 8 days (about 26 ads, roughly $0.15).

**Manual method that worked (no Apify needed for the review):** contact sheets of ad thumbnails (30 per sheet, Pillow) viewed by eye, then dHash of suspects against all own creatives, then Shopify `products/<handle>.json` of suspect stores hashed against bamboraco.com's product JSON. The built-in browser renders the Ad Library search page; harvesting cards via JS worked but only about 26 loaded per page until wheel events were dispatched.

**Why:** she wants copycats selling her exact product surfaced cheaply (Bustem is too expensive) and DMCA-able cases separated from mere lookalikes.

**How to apply:** explain plainly (she asked for "like I'm 5"). Never ask her to paste tokens in chat. For any new copycat question, reuse `state/last_dataset.json` and the sheet method before spending Apify credit.
