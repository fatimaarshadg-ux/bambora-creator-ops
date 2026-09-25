# The manual

## OWNERSHIP (read this first)

**Claude owns the routine.** You (the operator) do not have to remember anything; the system does.

- Claude **acts on everything the rules cover**. If a rule says what to do, it does it in this sweep and reports it as done.
- Claude **sends every due follow-up in the same sweep** it comes due. It never hands you a list of "things to send later".
- Claude **reports only live status**: it re-checks the Trybe portal or API right before saying anything about a creator. Never stale notes, never "according to my notes".
- Claude **asks you only about**:
  1. **irreversible actions**: approving or rejecting a video, accepting or rejecting an applicant, anything that cannot be undone;
  2. **money**: retainers, commission rates, offers;
  3. **real unknowns**: something no rule answers, or something about Fatima's own assets it cannot be sure of.
- Every question comes batched into **one message per sweep**, each with Claude's recommendation and a ready draft, so you can answer "yes 1, 3; no 2".
- When you answer, Claude acts straight away and closes the loop in the same turn.

**One computer at a time:** only this PC or Fatima's Mac runs the routine at any moment, never both (same Trybe account). Check with her before you start.

Your job: start it each work day ("start the routines"), answer the one message per sweep, keep Chrome and the PC awake, and pass anything about money or the 10 protected creators to Fatima.

**Who the creators think they are talking to:** Fatima. Messages go out from Fatima's Trybe account, in Fatima's voice. Never mention a sister, an assistant or a handover to a creator.

## The chapters

| File | Read it when |
|---|---|
| [FIRST-DAY.md](FIRST-DAY.md) | Before your first real work day |
| [01-how-the-job-works.md](01-how-the-job-works.md) | To understand the daily loop and the six streams |
| [02-rules.md](02-rules.md) | Every rule in one place: safety, messages, samples, applicants, who to ignore, autonomy |
| [03-trybe-map.md](03-trybe-map.md) | Where everything lives in the Trybe portal and API |
| [04-voice-guide.md](04-voice-guide.md) | How messages must sound (Fatima's voice), with her templates |
| [05-where-everything-lives.md](05-where-everything-lives.md) | Drive folders and file naming, Liam links, the tracker, Notion, Atria, local folders |
| [06-ledger-and-scripts.md](06-ledger-and-scripts.md) | The follow-up ledger commands and every script |
| [07-scheduled-tasks.md](07-scheduled-tasks.md) | The timers and scheduled tasks, and how to set them up on Windows |
| [08-troubleshooting.md](08-troubleshooting.md) | When something breaks (by symptom) |
| [09-background-machinery.md](09-background-machinery.md) | Every invisible piece (keep-awake, timer, watchdog, helper server, tab fronting, cl= markers, permissions, the key, backups): what, why, how to start and check it |
| [10-shift-checklists.md](10-shift-checklists.md) | START OF SHIFT and END OF SHIFT checklists, and the "what runs when" timeline |
| [GLOSSARY.md](GLOSSARY.md) | Every word and name you will hear |

The chapters are a readable summary. The **source of truth** Claude actually follows is in `routines/` (the run order), `skills/` (methods) and `memory/` (rules and facts). If a chapter and a skill ever disagree, the skill or memory file wins; tell Claude so it fixes the chapter.
