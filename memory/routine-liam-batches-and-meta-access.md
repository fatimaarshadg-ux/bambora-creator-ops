---
name: routine-liam-batches-and-meta-access
description: Two routines Fatima added 2026-09-25: send her a forward-ready Liam message at 5+ new videos, and a Meta (partnership ads) access check every ~5 hours
metadata:
  type: feedback
---

1. **Liam batches:** whenever 5 or more approved videos are filed in Drive and not yet sent to Liam, send Fatima the links with "now you can send this to Liam", as a forward-ready text: "hey Liam, here are N more videos you can add to Meta:" plus one link per video. Tracked by `work/trybe-drive-filing/liam_batch.py` (status / message / sent). Never resend what Liam already has.
2. **Meta access check every ~5 hours:** `work/sweep/every.sh due metaaccess 300`; when due, roster scan V3 creators needing partnership ads access (Request available, no Instagram connected, Pending 3+ days) and ask them, per the partnership rules in routines/full-run.md.

**Why:** she wants Liam fed in batches without asking, and Meta access chased on a schedule rather than when she remembers.
**How to apply:** both are steps in routines/full-run.md; check them every sweep. Related: [[core-rules]], [[bambora-drive-approved-videos]], [[trybe-5pct-migration-followup]].
