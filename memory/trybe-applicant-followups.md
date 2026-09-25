---
name: trybe-applicant-followups
description: Retired as a list on 2026-09-23. Every follow-up (applicants, samples, inspo check-ins, promises, replies owed) now lives in the follow-up ledger; this file only points there
metadata:
  type: project
---

**The follow-up ledger is the single source of truth** (Fatima chose this on 2026-09-23 to stop three lists drifting apart):
`py -3 ~/claude-setup/work/creator-db/followups.py due` shows what's due, `list` shows everything open, and `add`, `done` and `snooze` keep it current. The data is in `~/claude-setup/work/creator-db/followups.json`.

The applicant asks from 2026-09-23 (Emily Martines, Michelle Thode, Hazel Vargas, Ashley Sanocki, Casey Muniz, Kristen Smith, Maddie Tesimale, Yaritzacruz, Cassie Burris, Cammy Lyons, Kenzie Thomas, Bailey Schneider) are in the ledger as `applicant_followup`, due 2026-09-24.

The tracker doc shows a view of the ledger for Fatima. The routines rebuild it; nobody edits two lists by hand.
Related: [[creator-response-cadence]], [[bambora-creator-tracker-doc]]
