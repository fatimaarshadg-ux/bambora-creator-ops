# Ads Library DMCA monitor

Scans the Meta Ads Library (Facebook and Instagram ads) through Apify and reports ads that look like they are trading on Bambora: brand name in the ad, Bambora's own copy reused, or Bambora's own creative reused. Each hit comes with the Ad Library link and ad ID you need for a DMCA or trademark report.

## One-time setup (Windows PC)

1. Create an Apify account at apify.com and copy the API token from Settings, Integrations.
2. Store it (the prompt hides what you type):
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File .\store-secret.ps1 -Name apify_api_token
   ```
3. Optional, for Slack DMs: in Slack, Create an app (From scratch), enable Incoming Webhooks, Add New Webhook, choose your own DM as the channel, copy the URL, then:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File .\store-secret.ps1 -Name slack_webhook
   ```
4. Optional, run every Monday 09:00 automatically:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File .\schedule-weekly.ps1
   ```

Requires Python 3 with Pillow (already installed on the PC). Nothing else.

## Run it

```
python monitor.py
```

The first run also downloads Bambora's own ads once to build the visual reference set (`state/reference_hashes.json`). Refresh it every month or two, or after a big creative push, with `--refresh-reference`.

Output: `reports/<date>.html` (open in a browser) and `.csv`. Rows highlighted NEW were not in any previous run; `state/seen.json` remembers them.

Useful flags: `--new-only`, `--no-visual`, `--estimate` (worst-case cost), `--from-json state/last_dataset.json` (re-score the last download after editing keywords, free).

## What it searches (config.json)

- `brand_terms`: exact-phrase searches. Any ad from a non-Bambora page that mentions these is flagged `brand`.
- `copy_phrases`: distinctive sentences from bamboraco.com and Bambora ads. Flagged `copy` when reused.
- `category_searches`: broad product searches (baby sling carrier, hip carry sling...). These are not flagged on their own. They exist to surface ads whose images or video thumbnails match Bambora's own creatives (`visual`). This is the check that catches stolen footage, which keyword search alone cannot.
- `own_page_ids`: Bambora's Facebook page ID(s), excluded from results. Pages are deliberately not excluded by name, so a copycat calling itself "Bambora Outlet" still shows up.

Edit the lists freely. Add a phrase whenever a creator or ad produces a line that gets copied.

## Visual matching

Each image and video thumbnail is reduced to a 64-bit difference hash. Re-encoding, resizing, light cropping and colour tweaks barely change it (a test copy scored distance 3, an unrelated image 26). Anything within `visual.max_distance` (10) of one of Bambora's own creatives is flagged. Always open the ad and eyeball it before filing.

## Cost

Apify charges per ad returned, about $0.0058 per ad on the free plan and $0.005 on Starter ($19/month, includes $19 of usage; free plan includes $5). `python monitor.py --estimate` prints the worst case for the current config. In practice exact-phrase brand and copy searches return few ads, so a weekly run is typically a few dollars.

## Self-test (no token needed)

```
bash tests/run_test.sh
```
