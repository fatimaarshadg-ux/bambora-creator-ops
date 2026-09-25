# Trybe creative audit — runbook

Re-runs the "which creators actually perform without a sale" analysis.

**Start with the API** — `trybe_creator_performance` gives you the whole
leaderboard in one call, and `trybe_list_submissions` with `query:"sale"`
shortlists the sale ads. The browser steps below are the fallback for judging
*where* the sale sits in each ad, which the API can't tell you.

## Files
| File | What |
|---|---|
| `trybe-helpers.js` | Browser console helpers — scrape the table, open an ad, scrub the video |
| `rank.py` | Classification TSV → creator rankings |
| `creative-classification.tsv` | The verdicts (rank, creator, sales, spend, verdict, evidence) |
| `creatives-lifetime-page1.tsv` | Raw metrics for the top 42 creatives |

## Steps

**1. Set the range.** jointrybe.com → Brand Portal → Analytics.
Analytics has **no all-time preset** — only 7/14/30 days and Custom. Click the
date button → "Edit custom range…" → page the calendar back to Jan 2025 → click
the 1st → Apply. It resets on every reload, so redo it each session.
(The Creators/Roster page *does* have "All time". Analytics does not.)

**2. Set the table.** "Group by Creative", sort by Trybe Sales desc, 48/page.

**3. Scrape.** Paste `trybe-helpers.js` into the console, then:
```
__sweep(0,3400,55)     // run 2-3x with different step sizes
__acc.size             // poll this; one pass misses ~25% of rows
copy(__tsv())          // clipboard → creatives-lifetime-page1.tsv
```

**4. Classify.** For each creative, top-down:
```
__closeModal(); __open('Cambria R.','$7.98K',1)
__seek(0.1)   // screenshot the region __box() returns
__seek(0.5)
__seek(0.9)
```
Read the **burned-in captions**. Record a verdict per the scale in `rank.py`.

**5. Rank.** `python3 rank.py`

## Gotchas that cost time

- **Transcripts are useless for this.** The sale copy is on-screen text, not
  speech. A transcript-based pass called Kia's ads clean; they are the most
  sale-led ads on the platform.
- **The table is a windowing virtualiser** — it discards rows as it scrolls.
  Jumping to the bottom loses the top. Sweep in small steps and accumulate.
- **There are two `<video>` elements** in the modal. The first is 0x0; seeking
  it silently does nothing and every frame looks identical. Use `__vid()`.
- **Screenshot coords ≠ CSS coords.** Multiply by `1568/innerWidth` (~0.836).
  `__box()` does it.
- **The JS bridge times out on awaited calls** (~45s) but the work continues.
  Fire `__sweep` without awaiting and poll `__acc.size`.
- **The API can do most of this — prefer it over the UI now.** The old MCP
  server only wrapped two endpoints and invented filter names, which is why the
  first pass concluded otherwise. Both are fixed in
  `trybe-review/mcp-server/server.js`:
  - `trybe_creator_performance` (`GET /v1/creator-performance`) returns the
    creator leaderboard directly — earnings, GMV, conversions, submissions, ads,
    spend, purchases, ROAS — date-bounded, sortable by any metric, cursor-paged.
    **This replaces steps 1–3 entirely.**
  - `trybe_list_submissions` now has the real filters, including **`query`**,
    which substring-matches the transcript, **the on-screen text** and the
    creator's note. `query:"sale"` finds burned-in sale captions directly, which
    is what step 4 does by hand.
  Caveats: `creator-performance` defaults to the last 30 days (pass
  `start_date`), and is capped at 90 days when `sort_by` is a metric.
  Video scrubbing is still the only way to judge *how* sale-heavy an ad is —
  where the sale sits, hook vs end-card — which `query` cannot tell you.
- **Stop at ~42 creatives.** They carry 87% of lifetime sales; the remaining
  164 split $11.5k and won't move the top of the ranking.
- **Roster totals disagree with themselves** — header cards said 347/269, the
  panel below said 343/267, same screen, same filter.

## Definitions
- `CLEAN` — no sale/discount language anywhere
- `SALE-AT-END` — organic ad, sale named only in the closing seconds
- `SALE-HEAVY` — sale carried through a substantial part of the ad
- `SALE-LED` — the hook itself is the sale (Kia-style)

`rank.py` prints both cuts: end-mention allowed, and strict.
