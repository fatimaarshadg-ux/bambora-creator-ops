---
name: creator-database
description: Per-creator database for the 5% program (V3) plus the protected 10: where it lives, what it holds, how it refreshes daily
metadata:
  type: project
---

Built 2026-09-23 at Fatima's request: "build a database on each creator, run this daily based on any new inspo... you should know everything about them just as much as I do", and "it's important for you to know what we've talked with the creators about, and to watch those videos... don't miss anything".

**Scope:** every active creator in Bambora Affiliates V3 (the 5% program) plus the 10 protected creators ([[bambora-protected-creators]]). 94 creators and 242 videos on the first build.

**Where:** `~/claude-setup/work/creator-db/` (so it's pushed to GitHub with everything else).
- `build_db.py`: API refresh into `db/creators.json` and `db/profiles/<slug>.md`. Programs, performance (earnings, GMV, ads, ROAS) and every submission with its transcript. `/creators` does not list every creator, so the protected ids are hard-coded; it warns if one goes missing. `creator-performance` rejects `start_date` values before about mid 2026, so use 2026-06-01.
- `fetch_media.py`: a 6-frame contact sheet per video in `db/media/<slug>/`. ffmpeg reads the signed URL directly.
- `db/dms/<slug>.md`: DM summary, sample history (from the profile modal) and the full thread, read through the normal chat screen.
- The profile's `## Notes` section survives rebuilds: Style, DMs so far, Inspo that fits her, Fatima's comments.

**Blocked routes (safety check, 2026-09-23):** calling Trybe's internal `/backend/api/channels/<id>/messages` with her session token, and zipping the whole repo for Drive, were both refused even after she approved. Don't retry them unless she changes the permission mode herself.

**Daily:** step 0 of the `creator-ops-daily` skill.

**In the tracker too (her rule, 2026-09-23: "the profile should have been in creator tracker too"):** tab "Creator profiles" in the Bambora Creator Tracker (tab id 0ffd89e9-8438, body node dc383477-3b0f) holds one section per creator, linked from the main tab. Keep it in step with the database every day. Anything built about creators goes where she looks (the tracker), not only in GitHub.
