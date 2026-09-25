# START: what Claude does when Fatima says "start the routines"

> **Windows handover note:** clock times here are Fatima's (Pakistan time, shift about 5 PM to 5 AM). Use the operator's hours and end-of-day time from `~/claude-setup/OPERATOR.md`. "Fatima", "her go" and "tell her" mean the operator (memory `operator-handover`); messages still go out as Fatima. If anything in the background looks off, run `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/sweep/health.ps1"`.

Her work day runs from about 5 PM to 5 AM PKT. From "start the routines" until 5 AM, everything below runs on its own. She only hears from Claude for approvals, accepts, and questions no rule answers.

## 1. Set up (first 5 minutes, no questions)
1. Read memory `core-rules`, then the cheat sheet in skill `human-messages` (section 7), then `routines/full-run.md`.
2. `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/sweep/start.ps1"`. It starts keep-awake and the helper server, pulls the repo, and prints what's due in the ledger plus how fresh each stream is.
3. Chrome: make sure the three Trybe tabs exist (chat `&cl=3`, Discovery `&cl=1`, Creators `&cl=4`); open any that are missing. Load `chat-helpers.js` and `roster-scan.js` from `http://127.0.0.1:8765/`.
4. Timers (session-only, so recreate them every day):
   - CronCreate `7,37 * * * *`, recurring: "FULL SWEEP: follow ~/claude-setup/routines/full-run.md for ALL six streams. Slow reviews go to background agents. Mark each stream with streams.sh done, then mark.sh, restart watchdog.sh 30 60, push. If you're mid-task for Fatima, tell her in one line and run it right after the current step. Never skip."
   - CronCreate `12 4 * * *`, recurring: "END OF DAY: send Fatima the Links for Liam list (work/trybe-drive-filing/liam-links-<day>.md), file any approved videos not yet in Drive, write the session log, push, and stop the sweep timer for the night."
   - `bash ~/claude-setup/work/sweep/watchdog.sh 30 60` in the background.
5. Run the first full sweep right away (don't wait for :07).

## 2. Every sweep (full-run.md, in this order)
1. **Chat:** the `convoScan()` needsUs list (their message is last), oldest first. Read, then reply per the cheat sheet. `qCheck()` flags unanswered questions. Don't touch threads Fatima is handling.
2. **Samples:** approve eligible requests (V3, requested on or after 2026-09-17, shipping to an English-speaking country such as the US, Canada, UK, Australia, New Zealand or Ireland; multiple items are fine), then send the approval message. Nudge anyone 20+ hours without a request, except Bambora owners, who are told to start filming.
3. **Partnership ads:** request everyone the roster shows as requestable, ask "--" creators to connect a public Instagram or Facebook, and nudge requests still pending after 3 days.
4. **Submissions:** review, then bring verdicts. After her go: approve and message the creator, then file the video in Drive right away and add it to the Liam links list.
5. **Discovery:** new names (not in seen.txt) get reviewed in a background agent, and the verdicts come to her. After her go: accept, request partnership ads, schedule the sample nudge.
6. **Follow-ups:** `followups.py due`, plus the `convoScan()` waiting list:
   - **Creators who didn't reply** (our last message, 2+ days old): one gentle follow-up that fits the thread.
   - **Inspo sent, no reply after 2 days:** "hey [name]! what did you think of the inspo I sent? need any help? really looking forward to seeing what you put together 💗" (vary the wording per person).
   - **Applicants we asked for a talking video or socials:** one follow-up after a full day. If there's still nothing 3 days later, it goes to Fatima as reject or hold.
   - **Quiet creators** (no video in 14+ days): her model message. Notice the gap, ask how they are, offer ideas.
   - **Sample check-ins 2 weeks after approval**, and inspo check-ins.
7. **Finish:** streams.sh done for each stream, mark.sh, push, then ONE message: what was done, what needs her go (each with a recommendation), real questions only, and the stream line `chat Xm · samples Xm · partnership Xm · submissions Xm · discovery Xm · ledger Xm`.

## 3. Every 3 days (scheduled task)
The inspo research pack. Per-creator inspo messages are drafted from it and go to her for a look before sending, until she says they can go straight out.

## 4. End of day (4:12 AM timer)
The Links for Liam list, the session log, and the push. Before stopping, name anything still open in the ledger so the next day starts from it.

## Never
- Skip or silently put off a stream because of being busy.
- Report status from memory without re-checking the portal.
- Open and send in one step.
- Approve sample requests from before Sep 17.
- Message ignore-list creators.
- Pretend credentials in inspo ideas.
