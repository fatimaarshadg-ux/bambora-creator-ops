# Bambora creator-ops routines

> **Windows handover note:** clock times here are Fatima's (Pakistan time, shift about 5 PM to 5 AM). Use the operator's hours and end-of-day time from `~/claude-setup/OPERATOR.md`. "Fatima", "her go" and "tell her" mean the operator (memory `operator-handover`); messages still go out as Fatima. If anything in the background looks off, run `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/sweep/health.ps1"`.

Every routine that runs the operation, so this whole system can be set up on a new device or for a new brand from this repo alone.

**"Run the routines" = `routines/full-run.md`**, the single ordered checklist that covers every stream below in one pass.

| Routine | Where it runs | Cadence | What it does | Prompt |
|---|---|---|---|---|
| Live creator sweep (30 min) | In an open Claude Code session on this PC (session cron) | every 30 minutes during the work day (changed from 2 hours on 2026-09-23) | The only routine that can SEND. It runs `followups.py due`, answers creator replies (reaction plus a line), sends due follow-ups, and brings questions and submission verdicts to Fatima | `routines/live-sweep.md` |
| Full cycle | Scheduled task `bambora-full-cycle-every-4h` | every 4 hours | Refreshes the creator DB (which runs the quiet-creator check), reviews submissions, applicants and samples, and drafts everything into the tracker. Sends nothing | `scheduled-tasks/bambora-full-cycle-every-4h/SKILL.md` |
| Messages drafts | Scheduled task `bambora-messages-every-2h` | PAUSED since 2026-09-23 (the live sweep replaced it) | Drafts replies only; re-enable for days with no live session | `scheduled-tasks/bambora-messages-every-2h/SKILL.md` |
| Inspo research | Scheduled task `bambora-inspo-research-every-3-days` | every 3 days | Builds the Atria, YouTube, TikTok and IG inspo pack, puts it in Drive, and TAGS every item (baby in shot, format, who) | `scheduled-tasks/bambora-inspo-research-every-3-days/SKILL.md` |
| End of day | Fatima's Mac only: scheduled task `bambora-end-of-day-wrapup`. **On the Windows PC the end-of-day session timer in START.md does this instead; don't create the task.** | daily 04:15 (end of her 5 PM to 5 AM day) | Session log, tracker tidy, push to GitHub, repo zip to Drive | `scheduled-tasks/bambora-end-of-day-wrapup/SKILL.md` |

The brain behind all of them is the `creator-ops-daily` skill (`skills/creator-ops-daily/SKILL.md`). The memory of everything owed is the follow-up ledger (`work/creator-db/followups.py` and `followups.json`).

## Starting the live sweep on a new session
In Claude Code, in the Bombara folder, with Chrome logged into Trybe:
```
/loop 30m <the prompt in routines/live-sweep.md>
```
Session loops stop when the session closes, and after 7 days at most, so restart it at the start of each work day. Unattended scheduled tasks can't send messages, which is why sending lives here.

## Permissions (so unattended runs never freeze)
Run `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/settings/apply-settings.ps1"` after any change to `settings/allowlist.json` or `settings/additional-dirs.json`.

**Start of every work day:** Fatima says "start the routines", then Claude follows `routines/START.md`: setup (`work/sweep/start.ps1`), timers (full sweep at :07/:37, end of day at 4:12), watchdog, then the first full sweep right away.
