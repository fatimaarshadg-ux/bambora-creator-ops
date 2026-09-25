# How the job works

Bambora (https://bamboraco.com) sells a baby sling carrier. Creators (mostly moms) film short UGC videos with the sling on **Trybe**, a creator platform. Bambora pays them commission on sales, and the best videos become Meta ads. The job is to keep that machine running: answer creators fast, get them samples, approve good videos, recruit good new creators, keep everyone filming, and feed approved videos to Liam (the media buyer).

Source files Claude follows: `routines/START.md`, `routines/full-run.md`, `routines/live-sweep.md`, skill `creator-ops-daily`.

## The shape of a work day

Fatima's day ran from about **5 PM to 5 AM Pakistan time**, which matches US daytime for the creators. Yours is in `OPERATOR.md`.

1. **Start:** you type `start the routines`. Claude:
   - reads the core rules and the voice cheat sheet;
   - runs `start.ps1` (keeps the PC awake, starts the little helper server Chrome loads scripts from, pulls the repo, prints what is owed today and how fresh each stream is);
   - makes sure the three Trybe tabs are open in Chrome: Chat (`&cl=3`), Discovery (`&cl=1`), Creators (`&cl=4`);
   - sets the timers: a full sweep at :07 and :37 past every hour, and the end-of-day job;
   - starts the **watchdog**, which wakes Claude if a sweep is 30+ minutes late or any stream is 60+ minutes stale;
   - runs the first full sweep right away.
2. **Every 30 minutes: a full sweep** of all six streams (below). Slow work (watching applicant videos, checking submission frames) goes to background helpers so chat never waits.
3. **After each sweep:** ONE message to you: what was done (counts and names), "Needs your go" (numbered, each with a recommendation), "Questions" (only what no rule answers), and a line like `chat 3m · samples 3m · partnership 3m · submissions 4m · discovery 5m · ledger 3m`.
4. **Every ~5 hours:** the Meta (partnership ads) access check.
5. **End of day** (about 45 minutes before you stop): file any approved videos not yet in Drive, send you the Liam links, write the session log, push to GitHub, stop the timer.

## The six streams (every sweep, in this order)

### 1. Chat (Trybe DMs)
- Claude reads every thread where the creator's message is the last one (oldest first), **the whole thread**, then replies in Fatima's voice.
- Positive replies ("thank you!", "so excited!") always get a heart reaction plus a short warm line.
- Real questions get answered if a rule answers them; otherwise they come to you. Never a "let me check" holding line.
- It never opens and sends in one step. The chat helper refuses to send while the creator's newest message is unanswered.
- It does not touch a thread you (or Fatima) are actively handling (your own messages in the last hour).

### 2. Samples
- Creators request a free sling (a "sample") through Trybe. Claude approves requests that are: from **V3** creators, requested **on or after 2026-09-17**, shipping to an **English-speaking country** (US, Canada, UK, Australia, New Zealand, Ireland). Multiple items are fine. Then it sends the approval message.
- **Never** approves a request made before 2026-09-17 (those stay untouched).
- Creators accepted 20+ hours ago with no sample request get one nudge. Creators who already own a Bambora get "no need to request a sample, you can start filming whenever you're ready" instead.

### 3. Partnership ads (Meta access)
- For V3 creators, Bambora asks for "partnership ads" permission so their videos can run as ads from their Instagram.
- On the Creators roster: **Request** where it is available (then a tiny note); creators showing "--" are asked to connect a **public** Instagram (or Facebook) in their Trybe profile; requests pending 3+ days get one gentle nudge.
- The full check runs every ~5 hours (`every.sh due metaaccess 300`).

### 4. Submissions (videos)
- Claude pulls pending videos from the Trybe API, watches each (frames plus transcript) against the 6-point checklist and the no-sale-led rule, and brings you a verdict: approve, revise or reject, with the reason.
- **Nothing is approved or rejected without your yes.** After your yes: it acts, messages the creator, files the video in Google Drive straight away, and adds it to the Liam list.

### 5. Discovery (new applicants)
- New creators apply in Trybe's Discovery Inbox. Every sweep Claude lists the Inbox names and compares them with `seen.txt`; any new name gets a full review in the background.
- The deciding rule: **can we see them on camera, talking to camera?** Good delivery and a clear English accent = accept. Nothing on camera = hold. Big numbers but no talking = ask them for talking-head ("yapper") content.
- **Accepting or rejecting waits for your yes.** After accepting: request partnership ads, and a sample nudge is scheduled for the next day.

### 6. Ledger and follow-ups
- `followups.py due` lists everything owed today: sample check-ins, inspo check-ins, applicant follow-ups, quiet-creator check-ins, promises, replies owed. Claude sends each one in this sweep and closes it.
- Creators who went quiet (our message last, 2+ days) get one gentle follow-up that fits the thread.
- Once per shift (first sweep after 11 PM in Fatima's day) a **check-in audit**: every V3 and protected creator must have a ledger item or a recent message.

## The other routines

| Routine | When | What |
|---|---|---|
| Liam batches | after every Drive filing | When 5 or more filed videos have not gone to Liam, Claude gives you a ready-to-forward message ("hey Liam, here are 5 more videos you can add to Meta:" plus one link each). You forward it to Liam on Slack. |
| Creator database refresh | first sweep of the day | `build_db.py` refreshes every creator's profile from the API and adds quiet creators (no video in 14+ days) to the ledger; `fetch_media.py` makes frame sheets of new videos. |
| Inspo research | every 3 days (scheduled task) | Top human video ads from Atria plus popular mom videos on TikTok, YouTube and Instagram, saved to Drive "Bambora Inspo / Week of ...", tagged, then matched to creators. |
| Personal inspo messages | every 3 days | 3 to 5 ideas per creator who already has the sling, in Fatima's voice, "just inspo, put your own spin on it", checklist link, warm close. |
| End-of-day wrap-up | daily, ~45 min before you stop | Session log, tracker tidy, Liam links, push, repo zip to Drive. |

## What waits for you, and what does not

| Claude does it on its own | Claude asks you first |
|---|---|
| Replies to creators under the voice rules | Approve, reject or request revision on a video |
| Approving eligible sample requests, then the message | Accept or reject an applicant |
| Partnership ads requests, connect-Instagram asks, nudges | Anything about money, retainers or commission |
| Every due follow-up, quiet check-in, sample check-in | Anything about the 10 protected creators' programs |
| Filing approved videos in Drive, Liam lists | Program settings (welcome messages, briefs) |
| Updating the ledger, database, tracker, session log, GitHub | A creator question no rule answers |

## Why each rule exists

Almost every rule came from a real mistake: a message to the wrong duplicate account, a sample request someone had already made, a generic welcome message sent to six creators, Discovery going unchecked all night. The rules file (`02-rules.md`) keeps the reason next to each rule so it makes sense.
