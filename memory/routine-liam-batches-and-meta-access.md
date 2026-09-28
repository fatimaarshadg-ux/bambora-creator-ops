---
name: routine-liam-batches-and-meta-access
description: "Liam part RETIRED 2026-09-27 (nothing goes to Liam); the Meta (partnership ads) access check every ~5 hours"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 671421c3-23ff-4c9a-a09e-71661b766efe
  modified: 2026-09-25T13:56:26.959Z
---

**Liam's sheet RETIRED (Fatima, 2026-09-27):** item 1 below no longer applies. Approved videos only go into Main Media > Trybe. The Meta access check (item 2) still runs.

1. **Liam's ad-launcher sheet (Fatima + Liam, 2026-09-25):** Liam launches ads from a Google Sheet wired to an ad launcher ("10000x faster"). Every approved Trybe video, right after its Main Media filing, is copied into his Drive folder "Fatima - Trybe > Trybe creator ads" (`1tUaOf_HOrAUsxfWhBJXRxGFkPyHfHt3h`) and gets a row in "Creative Tracker - Bambora 2026" (`1W13Eqz3iBqvlUbgvdZMbPhKveTXpEOEODbtOInazmkI`, tab "Bambora - Internal"): `Trybe - <Creator> - <id>` | Video Ad | Pending | Bambora | copy's Drive link | PDP | blank ad copy. Tool: `work/liam-launch/liam_launch.py` (pending / tsv / done), steps in its README. The old links list and liam_batch.py are RETIRED: no Liam links message to Fatima, daily or in batches.
2. **Meta access check every ~5 hours:** `work/sweep/every.sh due metaaccess 300`; when due, roster scan V3 creators needing partnership ads access (Request available, no Instagram connected, Pending 3+ days) and ask them, per the partnership rules in routines/full-run.md.

**Why:** Liam asked for ready creatives in his drive + sheet instead of Slack links, and Fatima said to build it so it happens automatically.
**How to apply:** both are steps in routines/full-run.md; check them every sweep. First batch (Ellie, Aubrie, Jodi, Cambria) added 2026-09-25, rows 301-304. Sheet writes: insert rows below the last row, then a real paste of the TSV (synthetic paste not used), then verify via CSV export. Related: [[core-rules]], [[bambora-drive-approved-videos]].
