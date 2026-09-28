# Timers and scheduled tasks

There are two kinds of automatic runs. Knowing the difference saves a lot of confusion.

| | Session timers | Scheduled tasks |
|---|---|---|
| What | Timers Claude sets inside the open chat (CronCreate), plus the watchdog | Tasks saved in the Claude app (Scheduled section, or the scheduled-tasks tool) |
| Survive closing the chat? | **No.** Gone when the chat or app closes, and after 7 days at most | Yes |
| Can send messages and approve? | **Yes** (the only runs that can) | **No.** Unattended runs are refused sends and approvals; they only draft and report |
| Needs | the chat open | the PC awake, the Claude app open, Chrome signed in |
| Recreated | every work day by "start the routines" | once, then they keep running |

## Session timers (set by "start the routines")

1. **Full sweep:** cron `7,37 * * * *`, recurring. Prompt: "FULL SWEEP: follow ~/claude-setup/routines/full-run.md for ALL six streams. Slow reviews go to background agents. Mark each stream with streams.sh done, then mark.sh, restart watchdog.sh 30 60, push. If you're mid-task, say so in one line and run it right after the current step. Never skip."
2. **End of day:** cron at your end-of-day time (Fatima's was `12 4 * * *`, 4:12 AM PKT), recurring. Prompt: "END OF DAY: follow the END OF SHIFT list in ~/claude-setup/docs/10-shift-checklists.md: file any approved videos not yet in Drive (Main Media > Trybe; nothing goes to Liam anymore), save new rules to memory, write the session log, run sync.ps1, upload the repo zip to Drive, The sweeps keep running after this until the operator types stop the routines." **This is the only end-of-day job on this PC** (decided in the second audit, 2026-09-25): it runs inside the live session, so it can do everything, and the scheduled wrap-up task below is not created. Two wrap-ups would file, push and message twice.
3. **Watchdog:** `bash ~/claude-setup/work/sweep/watchdog.sh 30 60` in the background.

Timer times are in the PC's local time. If your timezone is not Pakistan time, Claude converts the end-of-day time from `OPERATOR.md`.

## Scheduled tasks (create once)

Prompts are in `scheduled-tasks/<name>/SKILL.md` (install.ps1 also copied them to `%USERPROFILE%\.claude\scheduled-tasks`). To create them, tell Claude: "create the scheduled tasks from docs/07-scheduled-tasks.md in my timezone" and say yes when it asks. It uses the scheduled-tasks tool with the same name, schedule and prompt.

| Task | Schedule (Fatima's, PKT) | What it does | Status at handover |
|---|---|---|---|
| `bambora-inspo-research-every-3-days` | every 3 days | Atria + TikTok + YouTube + Instagram inspo pack to Drive "Bambora Inspo / Week of ...", tagged (`tags.tsv`), links doc, matched to creators | **create on this PC** |
| `bambora-end-of-day-wrapup` | daily ~4:15 AM (end of shift) | session log, tracker tidy, sync_check + push, repo zip to Drive | **do NOT create on this PC**: the end-of-day session timer does this job. Kept for Fatima's Mac. |
| `bambora-full-cycle-every-4h` | every 4 hours | prep only: submission verdicts, applicant verdicts, sample list, database refresh, "Needs your go" in the tracker | optional: only for days with no live session, and only if Fatima is not running her routine (one machine at a time) |
| `bambora-messages-every-2h` | every 2 hours | drafts replies only | **PAUSED** since 2026-09-23 (the live sweep replaced it); enable only for days with no live session |
| `trybe-5pct-replies-report` | one-off | read-only report on replies to the September 5% migration message | historical; don't recreate unless Fatima asks |

**Before creating any task:** run `settings\apply-settings.ps1` (the allowlist), because an unattended run freezes on the first permission prompt and blocks every later run of that task. Each prompt carries a "TOOL RULES FOR UNATTENDED RUNS" block (one simple command per call, absolute paths, no `cd`, `&&`, pipes or loops); keep it.

**Daily check:** at the start of each shift Claude lists recent task runs. A run still "running" long after it started is frozen: Claude reads it, stops it, and tells you which command needs adding to `settings/allowlist.json` (then you rerun `apply-settings.ps1`).
