**NEWEST RULES (Fatima, 2026-09-25 to 09-28). These override any older line in the skills, memory, routines or docs that says otherwise.**
1. **Send window:** no creator message, accept, approval or rejection before 12 PM US Eastern. Check `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/common/us-time.ps1"` before sending anything. Before 12 PM ET: read, review and write what you would send into `work/send-queue/<date>.md`; the first sweep after 12 PM ET sends the queue.
2. **Nothing goes to Liam.** Approved videos only go into Drive, Main Media > Trybe (`file_approved.py`). No Liam sheet, no Liam folder, no Liam links, no Slack to Liam.
3. **Applicants, standing go:** every fit question answered yes (baby or toddler 10 to 50 lbs to film with, OK showing faces, 3 to 5 videos a week) + confident talking-to-camera videos + lives in the US, Canada, UK, Australia, New Zealand or Ireland = ACCEPT without asking, then onboarding (move to V3 if Grandparents, welcome note in the thread, partnership ads request or connect-Instagram ask, sample nudge next day). Asked for a talking video, answers were yes, never sent it (after one follow-up) = REJECT without asking. Conditional answers, borderline delivery and anything else still wait for a go.
4. **Existing creators' submissions (Fatima, 2026-09-28):** a CLEAR-CUT approval (all 6 checklist points pass in every frame, not sale-led, nothing you are unsure of) goes ahead WITHOUT anyone's review: approve, message (inside the send window), file in Drive, and list it under Done. Anything you are not sure about goes to the operator. **Revisions and rejections always wait until FATIMA herself has watched the videos**; the operator's yes is not enough for those, so list them as "for Fatima to watch".
10. **What else runs without review when you're sure:** the standing applicant accepts and rejects (item 3), eligible sample approvals, partnership ads requests and nudges, due follow-ups, and Drive filing.
11. **Volume commitments:** record every answer to the volume question with `py -3 ~/claude-setup/work/creator-db/commitments.py add` (exact words), and run `commitments.py get "<name>"` before any message or inspo so it builds on what they agreed to (inspo sized to their number, warm reminders, never guilt).
5. **Sweeps keep running** past any stated end time until the operator types "stop the routines" (then follow the Stop section of routines/START.md). Keep-awake starts with start.ps1; never ask the operator to start it.
6. **Volume ask is 3 to 5 videos a week** (not 4 to 5). Never excuse it; add one natural line about the support they get.
7. **Cooking and stairs are fine** with one hand on the baby. Straps being chewed is fine. Only flag what the checklist says.
8. **No double follow-ups:** never nudge when our last message is unanswered and under about 48 hours old. Exceptions: sample and Meta access nudges go 15 to 20 hours after our last message about it; applicants asked for a talking video get their one follow-up after a full day. Always `ctx(name)` first and write the next line of that conversation.
9. **Creators who want to post their videos on their own page too:** fine; the program is sharing videos on Trybe so we can run them as ads; kindly ask what they had in mind.

**Liam's sheet RETIRED (Fatima, 2026-09-27): approved videos only go into Main Media > Trybe (the Drive "Trybe" folder). Skip every Liam sheet / liam_launch.py step below.**

# "Run the routines": the full run, start to finish

> **Windows handover note:** clock times here are Fatima's (Pakistan time, shift about 5 PM to 5 AM). Use the operator's hours and end-of-day time from `~/claude-setup/OPERATOR.md`. "Fatima", "her go" and "tell her" mean the operator (memory `operator-handover`); messages still go out as Fatima. If anything in the background looks off, run `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/sweep/health.ps1"`.

Built 2026-09-24 after a night of back-and-forth. When Fatima says "run the routines" (or "let's start", "good morning"), do ALL of this without asking, in this order. Only true decisions go to her, batched into ONE message at the end with a recommendation each. Everything else gets done, not reported as "left to do".

Before starting: read memory core-rules, the voice cheat sheet (skill human-messages section 7) and `followups.py due`. Start the keep-awake (start.ps1), the 30-minute live sweep and the watchdog if they aren't running. `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/trybe-chat/front.ps1"` before any browser step. Serve helpers with `py -3 cors_srv.py` from `~/claude-setup/work/trybe-chat` (so the page always loads the CURRENT helpers, never a stale scratchpad copy).

Always use LIVE state. Never report a creator's status from memory notes or earlier in the chat without re-checking the portal (Sam Macsai was listed after Fatima had already rejected her).

**Volume commitments (Fatima, 2026-09-28): always remember what each creator agreed to.** Every answer to the volume question ("3 to 5 videos a week, would that work for you?") goes into `~/claude-setup/work/creator-db/commitments.py add "<name>" --agreed "..." --quote "<their exact words>" --verified` the moment it arrives, before accepting. Before ANY message or inspo to a creator, run `commitments.py get "<name>"` and write with it in mind: inspo is sized and framed to help them hit the number THEY agreed to ("since you said 3 a week works, here are 3 ideas for this week"), check-ins can warmly remind them of it, and the support line (weekly inspo, hooks, help when stuck) is tied to it. Never guilt-trip; never lower the ask. Anyone marked "below" (agreed to fewer than 3) or "soft" gets gentle encouragement toward 3. Entries marked "[quote to verify]" get their exact words copied from the thread the next time that thread is open.


## 1. Chat (sends)
- NEVER open and send in one step. Open, read (the last 10 messages at least), then write. `g2()` refuses to send while the creator's newest message is unanswered, until `ACK[name]=true` is set after reading it and the draft answers it first (life moments like pregnancy always acknowledged).
- Unread first. Read the whole thread, then reply per the voice cheat sheet: continue the thread, tiny thank-yous, no bio remarks, reaction plus a line for positive replies.
- Run `qCheck()` (chat-helpers.js) on every thread opened. Any unanswered creator question: answer it if the answer is known (rules in memory and skills); otherwise it goes in the end-of-run questions list. Never a "let me check" holding line.
- Don't touch a thread Fatima is actively handling (her own messages in the last hour).

## 2. Samples (approve and nudge)
- Samples tab, load `roster-scan.js`, run `await collectSamples()`.
- Pending requests dated 2026-09-17 or later from V3 creators: check the product and that the address is in an English-speaking country (US, Canada, UK, Australia, New Zealand, Ireland; not US-only, Fatima 2026-09-24), approve, then send the approval message ("your sample request is approved! let me know when it arrives and I'll share some ideas to get you started 💗", adapted to the thread). Requests before 2026-09-17: NEVER approve; leave them.
- Roster page: `rosterScan()`. `noSample` creators get one nudge 15 to 20 hours after our last message (usually the welcome), unless they already own a Bambora (then: "no need to request a sample, you can start filming whenever you're ready"). Sample nudge wording (Fatima 2026-09-26): it is their FREE product, not a favor to me: "hey [name]! did you get a chance to request your free sample yet? the sooner it arrives, the sooner you can start making videos 😊" (fit it to the thread). If our last message to them is unanswered and under ~12h old, hold the nudge to the next day (ledger `sample_nudge`).

## 3. Partnership ads (V3 only)
- `canRequest`: click Request (scripted `.click()`, one at a time, check the cell shows Pending), then a tiny note that continues the thread.
- `noConnect` ("--" = no Instagram/Meta connected to Trybe): ask them to connect their Instagram in their Trybe profile so we can send the request. Once it shows Request, click it.
- `pendingPA` 3+ days: one nudge ("just a little reminder about the partnership ads request on Instagram whenever you get a sec 😊"). Creators accept on Instagram or Facebook (FB needs a Page or professional mode).

## 4. Submissions
- File every approved video in Drive RIGHT AFTER approving it (file_approved.py --list/--download, upload, rename, --mark). Fatima's rule 2026-09-24. Nothing goes to Liam (Fatima, 2026-09-27): no Liam sheet, no Liam folder copy, no Liam links, no Slack message to Liam. Filing in Main Media > Trybe is the whole job.
- API `status=pending`. Review each against the checklist (frames plus transcript, safety, sale-led). Verdicts go in the end-of-run list; approve, reject or revise only on her go. After her go: act, then one message per creator (first approval: "your first video is approved!! 🥳 keep them coming, can't wait to see the next one 💗"; revision: fix plus checklist link).

## 5. Discovery (applicants)
- NEW applicants = Inbox names (inboxNames()) not in work/trybe-applicant-review/seen.txt. Review them every sweep, never only in the full run. The badge is always non-zero, so don't trust it.
- Discovery, Inbox (narrow window: focus the "Discovery" dropdown, Return, focus "Inbox (N)", Return). Review every applicant by skill trybe-applicant-review; verdicts in the end-of-run list. Accept only on her go; after accepting: Request partnership ads, add `sample_nudge` for tomorrow.
- Check Messages tab replies from applicants we asked for yapper content.


- **First message to every new applicant (Fatima, 2026-09-26):** after the background review, every NEW 5% applicant (V3 or Grandparents) gets the message in `work/trybe-applicant-review/first-message.md` (baby/toddler to film with, OK on camera, 3 to 5 videos a week, I invest in my creators). Verdicts still go to Fatima; accept only after their answer and her go. Every reply to an applicant includes the next step, never a bare congrats.
- **Standing accept go (Fatima, 2026-09-26):** accept, without asking, any applicant who answered ALL the first-message questions yes, has confident talking-to-camera content, and lives in an English-speaking country. Conditional answers (no faces, pace unsure, half faceless) go to her with a recommendation. Grandparents mix-ups: accept, move to V3, accept the move, then the "ignore that first message about grandparents" note. Then partnership ads request + `sample_nudge`.
- **Nudge timing for Meta access and sample requests (Fatima, 2026-09-26):** follow up once 15 to 20 hours have passed since our last message about it (not 48h for these two).

## 6. Ledger and follow-ups
- **Follow-ups must read as follow-ups (Fatima, 2026-09-26):** read the last 2 to 3 messages first and write the nudge as the next line of that thread, referencing the earlier ask ("did you get a chance to..."). No generic batch templates, no fresh openers, never contradict the last message.
- Chat list `convoScan()`: `needsUs` (their message last, 14 days) goes into step 1; `waiting` (ours last, 2+ days, no reply) gets one gentle follow-up fitted to the thread. Inspo with no reply after 2 days: "hey [name]! what did you think of the inspo I sent? need any help? really looking forward to seeing what you put together 💗" (vary it). Applicants asked for talking videos: one follow-up after a day; still nothing 3 days later means reject or hold, and that goes to Fatima.
- Handle every `due` line (applicant follow-ups after a full day, quiet check-ins with her model: notice, ask how they are, offer ideas; inspo check-ins; reply_owed). Close with `done`, add new items with `add`.

## 7. End of the work day only (about 4:15 AM, her day is 5 PM to 5 AM)
- Catch any approved video not yet filed in Drive (`file_approved.py --list`). Session log, push, backup.

## 8. Finish
- After each stream above: `bash ~/claude-setup/work/sweep/streams.sh done <chat|samples|partnership|submissions|discovery|ledger>`.
- `bash ~/claude-setup/work/sweep/mark.sh`, restart the watchdog (`watchdog.sh 30 60`, background), push the repo.
- ONE message to Fatima: what was done (counts plus names), then "Needs your go" (numbered, each with my recommendation), then "Questions" (only things no rule answers). Nothing else.


- Mark a stream with streams.sh ONLY right after its check actually ran in this sweep (twice on 2026-09-24 samples was marked done without checking, and three new requests were waiting).

- **Discovery helpers (2026-09-27):** for messaging and accepting applicants in the Discovery Inbox, load `discovery-helpers.js` from `http://127.0.0.1:8765/` after chat-helpers.js and roster-scan.js: `dGo(name, first, text, expectTail)` arms a message in the applicant's chat (then a real Return key, then `dVer()`), `findCard(name)` gives program, country, pitch and the Approve button, `attVideo()` gets a video they sent in chat.
- **Discovery is marked done ONLY after the new-applicant check ran** (Fatima, 2026-09-24: "always run that"): Inbox, every page, `inboxNames()`, then `py -3 ~/claude-setup/work/trybe-applicant-review/new_applicants.py <names...> --add`. Any NEW name gets a background review agent the same sweep. Follow-ups alone never count as the Discovery stream.

## Meta access check, every ~5 hours (Fatima, 2026-09-25)
- Each sweep: `bash ~/claude-setup/work/sweep/every.sh due metaaccess 300`. If DUE: on the Creators roster run `rosterScan()` and go through every V3 creator who still needs partnership ads (Meta) access:
  - `canRequest`: click Request (one at a time, confirm Pending), then a tiny note continuing the thread.
  - `noConnect` ("--"): ask them to connect a PUBLIC Instagram (or Facebook) in their Trybe profile so the request can be sent. Skip anyone asked in the last 2 days (check the thread and the ledger `connect_ig` item); otherwise one light reminder.
  - `pendingPA` 3+ days since the request: one nudge ("just a little reminder about the partnership ads request on Instagram whenever you get a sec 😊", varied).
  - Same message rules as always (read the thread first, g2(), lint, SAMPLE GATE, no one on the ignore list).
- Log each ask in the ledger (`connect_ig` / `partnership_nudge`), then `every.sh done metaaccess`. Report counts and names in the sweep summary.

## Check-in audit (added 2026-09-24 after Fatima asked "what creators haven't you checked in with")
Once per shift (first sweep after 11 PM): roster `rosterProps().filteredCreators`, V3 + protected, vs the chat list and the ledger. For every creator with no ledger item: open the thread and add the right one (sample_checkin 14 days after approval, quiet check-in, reply_owed). Also confirm every sample approved this shift got its approval message (Jordan Murray's didn't on 9/24: approve and message in the SAME step). Unanswered creator messages in threads Fatima handles go to her as a question, never left silent.
