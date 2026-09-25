# "Run the routines": the full run, start to finish

> **Windows handover note:** clock times here are Fatima's (Pakistan time, shift about 5 PM to 5 AM). Use the operator's hours and end-of-day time from `~/claude-setup/OPERATOR.md`. "Fatima", "her go" and "tell her" mean the operator (memory `operator-handover`); messages still go out as Fatima. If anything in the background looks off, run `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/sweep/health.ps1"`.

Built 2026-09-24 after a night of back-and-forth. When Fatima says "run the routines" (or "let's start", "good morning"), do ALL of this without asking, in this order. Only true decisions go to her, batched into ONE message at the end with a recommendation each. Everything else gets done, not reported as "left to do".

Before starting: read memory core-rules, the voice cheat sheet (skill human-messages section 7) and `followups.py due`. Start the keep-awake (start.ps1), the 30-minute live sweep and the watchdog if they aren't running. `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/trybe-chat/front.ps1"` before any browser step. Serve helpers with `py -3 cors_srv.py` from `~/claude-setup/work/trybe-chat` (so the page always loads the CURRENT helpers, never a stale scratchpad copy).

Always use LIVE state. Never report a creator's status from memory notes or earlier in the chat without re-checking the portal (Sam Macsai was listed after Fatima had already rejected her).

## 1. Chat (sends)
- NEVER open and send in one step. Open, read (the last 10 messages at least), then write. `g2()` refuses to send while the creator's newest message is unanswered, until `ACK[name]=true` is set after reading it and the draft answers it first (life moments like pregnancy always acknowledged).
- Unread first. Read the whole thread, then reply per the voice cheat sheet: continue the thread, tiny thank-yous, no bio remarks, reaction plus a line for positive replies.
- Run `qCheck()` (chat-helpers.js) on every thread opened. Any unanswered creator question: answer it if the answer is known (rules in memory and skills); otherwise it goes in the end-of-run questions list. Never a "let me check" holding line.
- Don't touch a thread Fatima is actively handling (her own messages in the last hour).

## 2. Samples (approve and nudge)
- Samples tab, load `roster-scan.js`, run `await collectSamples()`.
- Pending requests dated 2026-09-17 or later from V3 creators: check the product and that the address is in an English-speaking country (US, Canada, UK, Australia, New Zealand, Ireland; not US-only, Fatima 2026-09-24), approve, then send the approval message ("your sample request is approved! let me know when it arrives and I'll share some ideas to get you started 💗", adapted to the thread). Requests before 2026-09-17: NEVER approve; leave them.
- Roster page: `rosterScan()`. `noSample` creators get one nudge 20h+ after accepting, unless they already own a Bambora (then: "no need to request a sample, you can start filming whenever you're ready"). If our last message to them is unanswered and under ~12h old, hold the nudge to the next day (ledger `sample_nudge`).

## 3. Partnership ads (V3 only)
- `canRequest`: click Request (scripted `.click()`, one at a time, check the cell shows Pending), then a tiny note that continues the thread.
- `noConnect` ("--" = no Instagram/Meta connected to Trybe): ask them to connect their Instagram in their Trybe profile so we can send the request. Once it shows Request, click it.
- `pendingPA` 3+ days: one nudge ("just a little reminder about the partnership ads request on Instagram whenever you get a sec 😊"). Creators accept on Instagram or Facebook (FB needs a Page or professional mode).

## 4. Submissions
- File every approved video in Drive RIGHT AFTER approving it (file_approved.py --list/--download, upload, rename, --mark). Fatima's rule 2026-09-24. The Liam links list still goes at the end of the day.
- API `status=pending`. Review each against the checklist (frames plus transcript, safety, sale-led). Verdicts go in the end-of-run list; approve, reject or revise only on her go. After her go: act, then one message per creator (first approval: "your first video is approved!! 🥳 keep them coming, can't wait to see the next one 💗"; revision: fix plus checklist link).

## 5. Discovery (applicants)
- NEW applicants = Inbox names (inboxNames()) not in work/trybe-applicant-review/seen.txt. Review them every sweep, never only in the full run. The badge is always non-zero, so don't trust it.
- Discovery, Inbox (narrow window: focus the "Discovery" dropdown, Return, focus "Inbox (N)", Return). Review every applicant by skill trybe-applicant-review; verdicts in the end-of-run list. Accept only on her go; after accepting: Request partnership ads, add `sample_nudge` for tomorrow.
- Check Messages tab replies from applicants we asked for yapper content.

## 6. Ledger and follow-ups
- Chat list `convoScan()`: `needsUs` (their message last, 14 days) goes into step 1; `waiting` (ours last, 2+ days, no reply) gets one gentle follow-up fitted to the thread. Inspo with no reply after 2 days: "hey [name]! what did you think of the inspo I sent? need any help? really looking forward to seeing what you put together 💗" (vary it). Applicants asked for talking videos: one follow-up after a day; still nothing 3 days later means reject or hold, and that goes to Fatima.
- Handle every `due` line (applicant follow-ups after a full day, quiet check-ins with her model: notice, ask how they are, offer ideas; inspo check-ins; reply_owed). Close with `done`, add new items with `add`.

## 7. End of the work day only (about 4:15 AM, her day is 5 PM to 5 AM)
- File approved videos in Drive, then send her the Drive links for Liam. Session log, push, backup.

## 8. Finish
- After each stream above: `bash ~/claude-setup/work/sweep/streams.sh done <chat|samples|partnership|submissions|discovery|ledger>`.
- `bash ~/claude-setup/work/sweep/mark.sh`, restart the watchdog (`watchdog.sh 30 60`, background), push the repo.
- ONE message to Fatima: what was done (counts plus names), then "Needs your go" (numbered, each with my recommendation), then "Questions" (only things no rule answers). Nothing else.

- Links for Liam: each filing appends a line to ~/claude-setup/work/trybe-drive-filing/liam-links-<work day start>.md; the 4:15 AM wrap-up sends that list to Fatima.

- Mark a stream with streams.sh ONLY right after its check actually ran in this sweep (twice on 2026-09-24 samples was marked done without checking, and three new requests were waiting).

- **Discovery is marked done ONLY after the new-applicant check ran** (Fatima, 2026-09-24: "always run that"): Inbox, every page, `inboxNames()`, then `py -3 ~/claude-setup/work/trybe-applicant-review/new_applicants.py <names...> --add`. Any NEW name gets a background review agent the same sweep. Follow-ups alone never count as the Discovery stream.

## Liam batches (Fatima, 2026-09-25)
- After every Drive filing, run `py -3 ~/claude-setup/work/trybe-drive-filing/liam_batch.py status`. When it says READY (5 or more filed videos not yet sent to Liam), put the output of `liam_batch.py message` in the end-of-sweep message to Fatima with the line "Now you can send this to Liam:" and the forward-ready text ("hey Liam, here are N more videos you can add to Meta:" plus one link per video). Then run `liam_batch.py sent`.
- The end-of-day wrap-up still sends whatever is unsent (`liam_batch.py message --any`, then `sent`). Never resend videos Liam already got.

## Meta access check, every ~5 hours (Fatima, 2026-09-25)
- Each sweep: `bash ~/claude-setup/work/sweep/every.sh due metaaccess 300`. If DUE: on the Creators roster run `rosterScan()` and go through every V3 creator who still needs partnership ads (Meta) access:
  - `canRequest`: click Request (one at a time, confirm Pending), then a tiny note continuing the thread.
  - `noConnect` ("--"): ask them to connect a PUBLIC Instagram (or Facebook) in their Trybe profile so the request can be sent. Skip anyone asked in the last 2 days (check the thread and the ledger `connect_ig` item); otherwise one light reminder.
  - `pendingPA` 3+ days since the request: one nudge ("just a little reminder about the partnership ads request on Instagram whenever you get a sec 😊", varied).
  - Same message rules as always (read the thread first, g2(), lint, SAMPLE GATE, no one on the ignore list).
- Log each ask in the ledger (`connect_ig` / `partnership_nudge`), then `every.sh done metaaccess`. Report counts and names in the sweep summary.

## Check-in audit (added 2026-09-24 after Fatima asked "what creators haven't you checked in with")
Once per shift (first sweep after 11 PM): roster `rosterProps().filteredCreators`, V3 + protected, vs the chat list and the ledger. For every creator with no ledger item: open the thread and add the right one (sample_checkin 14 days after approval, quiet check-in, reply_owed). Also confirm every sample approved this shift got its approval message (Jordan Murray's didn't on 9/24: approve and message in the SAME step). Unanswered creator messages in threads Fatima handles go to her as a question, never left silent.
