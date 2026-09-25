---
name: operator-handover
description: Who Claude works with now (Fatima's sister, the operator) and how every "Fatima" rule in memory and skills maps onto her
metadata:
  type: user
---

Since the handover (built 2026-09-25), the Bambora creator-ops job on this Windows PC is run by **Fatima's sister, the operator**. Her name, work hours and timezone are in `~/claude-setup/OPERATOR.md`. Read that file at the start of every session.

**How to read the rest of memory and the skills:**
- They were written while working for Fatima. Wherever they say "Fatima's go", "ask Fatima", "tell her", "her green light" or "bring it to her", that now means **the operator**. The operator decides, or checks with Fatima herself.
- A few things stay Fatima's call even now, so the operator should check with her before saying yes: money (retainers, commission rates, the $400 base offer in memory creator-base-retainer-offer), anything about the 10 protected creators' programs, creating a new Trybe API key, and changes to program settings (welcome messages, briefs).
- **Messages to creators still go out as Fatima**, from Fatima's Trybe account, in Fatima's voice (skills `fatima-creator-voice` and `human-messages`, unchanged). Creators know Fatima; never mention a sister, an assistant or a handover to them. Speak as one person: I and me.
- The operator signs in to Chrome with Fatima's Bambora Google account (fatima@bamboraco.com), so Trybe, Google Drive, Notion and Slack open as Fatima. Never type or store any password; the operator signs in herself.
- "Her work day" in older notes means Fatima's (about 5 PM to 5 AM PKT). Use the operator's hours from OPERATOR.md for timers, the end-of-day wrap-up and "today". If OPERATOR.md still has placeholders, ask the operator once and fill it in.

**Ownership (Fatima, 2026-09-25):** the assistant owns the routine. It acts on everything the rules cover, sends every due follow-up in the same sweep instead of listing it, reports only live status (never stale notes), and asks the operator only about irreversible actions (approve, reject, accept, anything that cannot be undone), money, or real unknowns. See [[feedback-take-ownership]] and [[core-rules]].

**Sync:** the operator's private GitHub repo is cloned at `~/claude-setup` (same path as Fatima's, so every path in the notes works). End of session: `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/sync.ps1" -Message "<what changed>"`.

**Taking turns with Fatima (second audit, 2026-09-25):** this repo (`fatimaarshadg-ux/bambora-creator-ops`) is the one live copy of the shift data. Fatima's Mac swaps data with it through `work/backup/handoff-mac.sh take|give`; one machine runs sweeps at a time. Details: `~/claude-setup/docs/12-sync-with-fatima.md`. Who decides what: `docs/11-decision-guide.md`. The operator uses Fatima's Claude account, so pick this PC's Chrome in Claude in Chrome, never hers.

Related: [[windows-machine]], [[core-rules]], [[claude-in-chrome-standing-permission]].
