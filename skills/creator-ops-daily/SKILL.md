---
name: creator-ops-daily
description: Fatima's daily creator-management routine for Bambora on Trybe. Run it at the start of every working session ("let's start", "good morning", "what's on today", "start the day") and whenever she asks what needs doing with creators. Covers submission reviews plus approval/rejection messages, Drive filing, new applicants, sample requests, post-sample check-ins, follow-ups on DMs, top-performer monitoring, and weekly personalised inspo.
---

# Creator ops: the daily loop

Treat this like a full-time job. Nothing a creator was promised gets forgotten, and no message sounds like a robot. Load `fatima-creator-voice` before writing any message, `trybe-portal` for navigation, and `trybe-applicant-review` for step 3.

**Before every message:** open that creator's DM history and read it. Never send the same wording you sent them last time. Match the relationship: a first-timer gets the standard message, someone you've been chatting with gets a message that fits the conversation. Use a fitting emoji (💙 is the default, not a rule). Never an em dash.

**Autonomy:** approvals, rejections and sends wait for her go unless she has explicitly delegated that action type (record delegations in memory). Scheduled or unattended runs only read and draft. Batch drafts and ask once.

## First step of every work session: start the live sweep
In-session timers die when the session closes and expire after 7 days anyway, so at the start of EVERY work session (and whenever CronList shows no sweep job), create the 30-minute sweep: CronCreate with cron `7,37 * * * *`, recurring, and a prompt that runs `~/claude-setup/routines/live-sweep.md`. Check CronList first so there's never two of them running. ALSO start the watchdog in the background (`bash ~/claude-setup/work/sweep/watchdog.sh 30`, run_in_background), because the session timer skips a run whenever Claude is busy. When the watchdog exits it wakes you: run the sweep, end it with `bash ~/claude-setup/work/sweep/mark.sh`, and start the watchdog again. Tell Fatima in one line that both are running.

## The work-day rhythm (confirmed by Fatima, 2026-09-23)
A session stays open on this PC during the work day (Chrome logged in).

**Every 30 minutes: messages** (live sweep, `routines/live-sweep.md`; changed from 2 hours on 2026-09-23). Trybe chat, Unread first. Positive replies get a 💙 reaction plus a warm line. Send due follow-ups (1-day no-reply, sample nudges, 2-week sample check-ins, migration yeses: move, accept, invite message). Real questions or problems go to her with a suggested reply.

**Every 4 hours: the full cycle.**
1. New submissions: review against the checklist and give her verdicts with reasons. **Approve, reject or revise only after her green light on each one.** Then one combined message per creator, written after reading her thread.
2. File the approved videos in Drive (`file_approved.py`), named `CreatorName/fatima/trybe=<id>`, verified.
3. New applicants: full review, and **accept or reject only on her green light for each one**. Applicant asks (yapper content, socials, English) also wait for her go.
4. Sample requests: approve only from recently accepted creators (checked product and address), each with a sample DM that fits her thread. Everyone else's requests are hers.
5. Update the tracker doc and memory, then push.

**Green-light rule:** every approval, rejection and acceptance needs her explicit go per creator, even clear-cut ones. Messages follow her rules without asking, except real questions or problems.

## Follow-up ledger (the memory of everything owed; built 2026-09-23 so she needs minimum handholding)
`~/claude-setup/work/creator-db/followups.py` + `followups.json`. At the start of every sweep run `followups.py due` and handle every line. After EVERY message that creates an obligation, add it in the same step:
- inspo sent: `inspo_checkin`, +3d. Inspo only goes to creators who already have the sling. New creators still waiting on a sample get the sample check-in first, then inspo once it has arrived.
- sample approved: `sample_checkin`, +14d
- applicant ask sent: `applicant_followup`, +1d
- accepted, no sample request yet: `sample_nudge`, +1d
- Fatima promises something ("I'll put something together", Discord): `promise`, with the date she gave
- a creator asks something only Fatima can answer: `reply_owed`, today
Close items with `done` once sent. If it isn't in the ledger, it will be forgotten.

## Inspo messages (her rules, 2026-09-23; see memory inspo-message-rules)
Order: incoming submissions and messages first, then inspo. For each creator: watch their past videos (frame sheets + transcripts), read their DM history and look at their socials style, then give 3-4 specific ideas with links (Drive inspo files are link-shared; TikTok, YT and IG links are fine). Every message says these are only inspiration and they should put their own spin on it (creators who do, do really well), includes the checklist link https://bamborachecklist.netlify.app/, and ends warmly ("hope you like it, I'm always here for any questions"), worded differently each time. For the 2026-09-23 run every inspo draft goes through her first.



**Idea generation, not only pack-matching (2026-09-23):** for each creator, brainstorm 2 or 3 angles from their life stage and real moments (see memory inspo-message-rules, "Come up with angles yourself"), then back each one with a pack example. For pregnant creators or newborns under 10 lbs, include no-baby angles: a pregnancy shopping haul, the best baby shower gift, registry picks (never a hospital bag or anything implying use from birth, because newborns are under 10 lbs), a reaction or stitch to a viral clingy-baby video (always with the exact video link, found LAST), tester or rating videos.

**Match inspo to the creator's situation with the pack tags, not by hand (her lesson, 2026-09-23: "look at the inspo and see what inspo doesn't have a baby in it").** Before drafting, read the creator's constraints from her profile (pregnant, newborn under 10 lbs, toddler, dad, grandparent, multi-kid, no sling yet) and filter `tags.tsv`: no baby to wear means fits_no_baby_creators=yes (tester, rating, authority, comparison formats); a dad means who_on_camera=dad; prefer sale_led=no. Anything the tags can't answer gets fixed in the tags, not worked around in the draft. Try to work out the answer yourself from the data first, and only ask Fatima about taste or real decisions.

## 0. Creator database (daily, first thing; her ask 2026-09-23: "know everything about them just as much as I do")
Covers every creator in the 5% program (Bambora Affiliates V3) plus the 10 protected creators. Lives in `~/claude-setup/work/creator-db/`:
- `db/creators.json` and `db/profiles/<slug>.md`: API facts (programs, stats, every video with transcript, status, ads). The facts block is rebuilt; everything under `## Notes` (Style, DMs so far, Inspo that fits her, Fatima's comments) is kept and is where Claude writes what it learns.
- `db/media/<slug>/<trybe_id>.jpg`: a 6-frame sheet per video, so her style can be watched.
- `db/dms/<slug>.md`: DM summary, sample history from the profile modal, and the full thread.

Daily steps:
1. `py -3 ~/claude-setup/work/creator-db/build_db.py` (API refresh; warns if a protected creator goes missing).
2. `py -3 ~/claude-setup/work/creator-db/fetch_media.py` (frames for new videos only).
3. Watch every new sheet plus transcript and update that creator's `### Style` notes: yapper or voiceover, setting, energy, hooks she uses, baby age and setup, safety issues, what performed.
4. DMs: for every thread with new messages since yesterday (the 2-hourly chat sweep sees them), append to `db/dms/<slug>.md` and refresh `### DMs so far` (open promises, questions, sample status). Read through the normal chat screen. Calling Trybe's internal chat API with her session token is blocked by the safety check, so don't try it.
5. When an inspo pack lands (7a), match items to creators in `### Inspo that fits her` (why it fits; never her own videos; respect the protected ten). The per-creator inspo messages (step 7) are drafted from these notes.
6. Keep the tracker's **Creator profiles** tab current (tracker doc 3db72f36-d656-451e-8ddb-ec6f39609238, tab id 0ffd89e9-8438, body node dc383477-3b0f). Every creator in the database has a section there (stats line, who they are, best next move). When a profile's quick read, stats or open items change, update that creator's section with a guarded replace. When a new creator joins V3, add a section. Fatima's rule (2026-09-23): the profiles belong in the tracker, not only in GitHub.
7. Commit and push the repo (the database is backed up with everything else).

## 1. Submissions from roster creators (since the last session)
**No sale-led videos (2026-09-23).** For every pending submission, check the transcript and on-screen text for sale language (the API `query=sale` / `deal` / `discount` matches on-screen text). A brief mention at the end is fine. Flag only sale-LED videos (opening on the sale, built around it, or 2+ mentions, like Kia's) with a revise or reject recommendation.
1. List pending submissions (API `status=pending`) and review each one against `bambora-content-checklist` (frames plus transcript), and in the first 30 days write the feedback she promises (see promises below).
2. Present verdicts; on her go approve, reject or request revision.
3. Message each creator ONE combined note covering everything decided for them in this pass:
   - Approved: a short, warm confirmation ("your video is approved!! 🥳"). A specific thing that worked only when it helps them repeat it (first approvals, coaching); routine approvals stay one line (her correction, 2026-09-24).
   - Rejected: what happened and exactly what to fix, framed as coaching.
   - Mixed: "approved X, one didn't make it, here's why and how to fix it".
   Check the DM history so the wording differs from previous approval notes.
4. File approved videos in the Drive folder with the naming convention (see Open questions).

## 2. Replies and follow-ups
- Run `followups.py due` (the ledger is the only follow-up list). For everyone who replied (for example, sent yapper videos or socials), review what they sent and recommend accept or reject with evidence. For no reply after 1 working day, draft a follow-up.
- Scan Trybe chat for creators waiting on us, oldest first (her brand health score tracks reply time).
- Open promises due today (from the ledger): "Fatima said she'd send inspo", "Discord invite next week", and so on.

## 3. New applicants
Run `trybe-applicant-review` end to end.

## 4. Newly accepted creators
Remind her of the onboarding chain for each one: V3 welcome (automatic, verify it arrived), watch for the sample request, then approve it and send the sample DM. If no sample request arrives within a few days, nudge.

## 5. Samples
- **20-hour sample nudge (her ask, 2026-09-23):** anyone accepted or invited 20+ hours ago with no sample request gets one follow-up fitted to their thread (SAMPLE GATE first). Every accept adds `sample_nudge` to the ledger for the next day.
- Pending sample requests: check product, address and note, and on her go approve them and send a short, context-aware sample DM (history first).
- About 2 weeks after approval: check in ("hope the sling arrives soon if it hasn't already, let me know when it does so I can share some ideas you can work on").
- After delivery with no submission: nudge with ideas.

## 6. Top performers ($500+ in sales)
Weekly: list creators with $500+ in sales (see Open questions for which metric and window). For each, count submissions this week against their usual rate. If they've gone quiet, look at their recent videos and draft feedback or ideas for her to send.

## 6b. Quiet creators (her thresholds, 2026-09-23)
**Automated:** `build_db.py` runs `quiet_creators.py`, which adds a `quiet_checkin` to the ledger for every quiet creator, so `followups.py due` always lists them. Skipping this step on 2026-09-23 meant 11 quiet creators went uncontacted until she noticed.
Every day: from the API (`creator-performance`, `activity.last_submission_at`), list creators whose last submission is **more than 14 days ago**. Exclude new creators until they've been with us **2 weeks** (joined or sample approved less than 14 days ago). Sort by past sales, best first. Before writing, read her thread and past videos. The first check-in notices the gap, asks how they are and OFFERS ideas (her model, 2026-09-24: "Hey Cheylene, I noticed you haven't made a video in a while, I hope everything is good on your end? Happy to put together a few ideas to help you create some winners."). Ideas and the 20-30 videos a month point come after they reply. Never message the protected ten about money; retainer askers from the migration are dropped.

## 7a. Inspo research run, every 3 days (her exact spec, 2026-09-23). Run it without asking her questions.
Goal: capture top-performing ads and videos **that show real humans** (formats she can copy), industry-wide. They do not need to match our product.

1. **Atria, followed brands:** for every followed advertiser, take the top ads by impressions from the **last 7 days** (`scope=followed_advertisers`, `media_format=video`, `order=most_impressions`, `active_since=<today-7>`, `collapse_variants=true`). Keep only videos that show a human (check the preview frame or the creative tags). *First run (week of 2026-09-23): lifetime, with no date filter.*
2. **Atria trending:** the trending ads of the **last 7 days** (Atria's trending page; via MCP, `order=most_saved` plus `impression_trend=rising`, `launched_after=<today-7>`, video). Keep those with humans; these are the replicable ones. *First run: last 14 days.*
3. **Download** the Atria videos (`get_library_ad`, asset URL) and upload them to Google Drive: folder **"Bambora Inspo"**, with a **new subfolder each week** named `Week of YYYY-MM-DD`. Name files `NN Brand, short hook.mp4` (no spaced hyphens; her no-dash rule covers file names). Upload the whole week in one go: stage all files in one local folder, then copy them into the Google Drive for desktop folder for "Bambora Inspo / Week of ..." (or use the browser fallback in memory windows-drive-upload-technique). 56 videos, 680MB took about 5 minutes on the Mac. Save the best to the Atria board "Bambora Creator Inspo" and tag them `inspo-YYYY-MM-DD`.
   Traps: judge humans from a frame of the actual mp4 (ffmpeg at 3s), or from freshly downloaded previews into an EMPTY folder. A reused preview folder from an earlier run shifted every label by one. `get_library_ad` for many ads is best delegated to a subagent that writes a TSV and downloads with curl (keeps the main context small).
4. **YouTube, Instagram, TikTok:** popular videos (clearly high views and engagement for the account) that use humans and are **for moms**, formats she can copy. Download where easy (yt-dlp for YouTube and TikTok); otherwise just links.
   - **YouTube:** `yt-dlp --flat-playlist` on `https://www.youtube.com/results?search_query=<q>&sp=CAMSAhgB` (Shorts sorted by views) or `sp=EgQIBRgB` (Shorts this year). Plain `ytsearch` returns old long-form junk. Her reference style is Chrissy Horton (mom of 7, honest reviews to camera): check `@chrissyhorton/shorts` each run.
   - **TikTok (incl. TikTok Shop):** `py -3 ~/claude-setup/work/social-tools/tt_find.py "<topic>" ... [--shop] --min-views 100000 --seen ~/claude-setup/work/inspo/seen.txt`. It finds video URLs through web search and ranks them by views with yt-dlp, no browser. TikTok's own hashtag and search pages are blocked for scripts. The Brave search tool with `site:tiktok.com <topic>` also works for finding URLs.
   - **Instagram:** find reel URLs with web search (`site:instagram.com/reel <topic>`), then read likes and comments with `yt-dlp --skip-download --print "%(like_count)s ..."` at a 3s pace. No browser needed, so her account is never touched.
5. **Write the links doc** "Inspo links, Week of YYYY-MM-DD" in that week's Drive folder, with a clickable link for EVERY item (Drive file plus original ad or post link). One line per item: source, brand or creator, links, views or impressions, the hook in one line, why it's copyable.
   **No repeats across weeks:** skip anything already in `~/claude-setup/work/inspo/seen.txt`; append this run's items and push. Then tell her it's ready. She reviews it and sends suggestions; record her picks and taste notes in memory.
6. These packs feed the per-creator inspo messages (step 7).

## 7. Personalised inspo, every 3 days (her cadence, 2026-09-23)
Pull the top-performing videos from Trybe, Atria and anything she shares. Then for each creator:
- profile each creator first: who she is (mom, dad, grandma, twins, pregnant, plus-size), baby's age, setting, style (yapper or voiceover, calm or bubbly), and what already worked for her;
- 3-5 videos per creator from Trybe top performers, Atria and Apify, each with a "copy this, skip that" safety note;
- a short message in her voice with one line on why these fit this creator (never a generic blast);
- never send them their own videos;
- match their situation: a dad (for example Jacob with his daughter), a grandmother, twins, a toddler rather than a newborn, plus-size, pregnant;
- prefer non-sale creatives as inspo (sale-led ads skew the numbers; see `trybe-final-top-creators.md` in ~/Bombara);
- flag anything that breaks the updated safety guidelines ("copy the bones, not the mistakes", as in `bambora-top-performer-briefs.md`).

## 8. Close the day
**File approved videos in Drive (every day, before closing):**
1. `py -3 ~/claude-setup/work/trybe-drive-filing/file_approved.py --list` shows approved videos not yet filed (tracked in `filed.json`, so a missed day is caught the next day).
2. `--download ~/Downloads/trybe-filing-YYYY-MM-DD` saves them with Windows-safe names plus `manifest.json`.
3. Upload that folder to the Drive "Trybe" folder with `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/trybe-drive-filing/drive-upload.ps1" -Source <that folder> -Target Trybe` (Google Drive for desktop; the browser fallback is in memory `windows-drive-upload-technique`).
4. Verify with Drive `search_files parentId = '1kleoyEuzTGxftUvYKwSK3aVUDTKkG53R'`, then rename each file to its manifest `drive_name` (`CreatorName/fatima/trybe=<id>`) with `update_file`.
5. Only after the rename is verified: `--mark <ids>`, then delete the local download folder.
6. **Links for Liam (her ask, 2026-09-23):** send Fatima ONE message listing every video filed today, one line each: creator, trybe id, and the individual Drive link (https://drive.google.com/file/d/<id>/view, from search_files on the Trybe folder), so she can forward it to Liam on Slack. Do this every day there are new approvals.

Then update the tracker (its follow-up section is a view of followups.py), log voice lessons, and push memory and skills to claude-setup.

## Standing rules added 2026-09-23 (from Fatima)
- **Every open conversation stays tracked until it's resolved.** That covers campaigns like the 5% migration (see memory `trybe-5pct-migration-followup`): check the silent creators in every sweep. A yes means move, accept, then her invite message. Retainer askers are dropped (including Kia Layton). She had to remind me about this one, so never let an open thread fall out of the tracker.
- **Check for new replies every 2 hours during the work day** (Trybe chat, the Unread filter first), especially from creators we messaged earlier, and answer them. Use `/loop 2h` or ScheduleWakeup in-session; unattended scheduled tasks can only read and draft, not send.
- **Lapsed creators:** anyone who made a few videos for us and then stopped gets a check-in in her words, including her point that creators who post 20-30 videos a month do much better (with her emoji). Look at their videos and history first.
- **Every message is unique to its context.** Read the thread and write for that person; never paste one text to everyone when their situations differ. Positive replies ("thanks, can't wait!") ALWAYS get a heart reaction plus a short warm reply fitted to the thread (see fatima-creator-voice rule 9). Correction from her on 2026-09-23: my earlier "no answer needed" was wrong.
- **Be human and ask her when unsure** (for example, dropping the #1 seller: ask first). She likes being asked the right question at the right time.
- **Promise spotting:** when the chat list or a thread shows her promising something ("I will put something together for you", "Discord invite"), add it to Promises we owe with a date.

## Promises Bambora has made to creators (must be kept)
- The V3 welcome promises: weekly inspo and angles, a Discord invite "next week", and "message me anytime".
- The welcome doc in ~/Bombara (`creator-welcome-message.md`) also promises feedback on every video in the first 30 days, a Calendly link, and the checklist. Confirm with her which of these are live commitments.

## Open questions (ask her; delete each once answered and recorded in memory)
- Drive: DECIDED, see memory bambora-drive-approved-videos.
- The $500 threshold: Trybe GMV or ad purchase value, and lifetime or last 90 days?
- Atria: how to access it (connector, login, exports).
- Ledger: DECIDED, a Claude Doc (see memory bambora-creator-tracker-doc). Still open: sweep timing; which actions are delegated; the nudge interval after delivery.

## Inspo additions (Fatima, 2026-09-24)
- **Nivaro** (Atria advertiser m650969541435421, followed): every inspo run includes 3 to 5 of their top video ads. Label AI-made ones "AI video" and tell creators they can film their own version of that format (not make AI videos). Their grandparent angle pairs with our grandparent creators.
- **Authority and persona creators** (grandparents, a pediatrician, nurses, dads, twin moms and so on): list in `~/claude-setup/work/inspo/authority-creators-*.md`. Use them for authority angles in inspo ("what I tell parents as a pediatrician", "the carrier I keep at Grandma's house"), get creative, and keep the safety rules.

- **Replicate every idea for our people (Fatima, 2026-09-24):** for EVERY inspo item, from any source (Atria, TikTok, YouTube, IG, Nivaro, AI-made or real), think it through like a smart human: what makes it work (hook, format, emotion, who is on camera), and how one of OUR creators could film their own version with their real life, kids and setting. Name which creators it fits and why (casting: [[creator-casting-mindset]]), and write the one-line version they would shoot. If an idea can't be replicated safely or believably by anyone on our roster, drop it.

- **Samples (her rules, 2026-09-24):** never approve a request made before 2026-09-17. Creators who already own a Bambora need no sample and get no sample nudge; tell them to start filming with theirs.
- **Drive filing right after approval (Fatima, 2026-09-24):** file each approved video in the Drive "Trybe" folder as soon as it's approved, not at the end of the day. The Liam links list still goes to her at the end of the day (about 4:15 AM).
- **Abbey Way (V3, not protected):** Fatima said to ignore her questions (2026-09-24).

## Liam batches and Meta access (Fatima, 2026-09-25)
- After every Drive filing: `liam_batch.py status`. At 5+ unsent, message Fatima "now you can send this to Liam:" with the output of `liam_batch.py message` ("hey Liam, here are N more videos you can add to Meta:" + links), then `liam_batch.py sent`.
- Every ~5 hours (`every.sh due metaaccess 300`): roster scan for V3 creators needing partnership ads access; Request / ask to connect a public Instagram / nudge Pending 3+ days. Details in routines/full-run.md.
