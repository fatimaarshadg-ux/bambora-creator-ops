---
name: core-rules
description: The essential Bambora creator-ops rules in one page; read first every session. Details live in the linked memories and skills
metadata:
  node_type: memory
  type: feedback
  originSessionId: c57db420-bc45-460b-a4ca-2e63128418b9
  modified: 2026-09-23T17:07:13.342Z
---

**NEWEST RULES (Fatima, 2026-09-25 to 09-28). These override any older line in the skills, memory, routines or docs that says otherwise.**
1. **Send window:** no creator message, accept, approval or rejection before 12 PM US Eastern. Check `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/common/us-time.ps1"` before sending anything. Before 12 PM ET: read, review and write what you would send into `work/send-queue/<date>.md`; the first sweep after 12 PM ET sends the queue.
2. **Nothing goes to Liam.** Approved videos only go into Drive, Main Media > Trybe (`file_approved.py`). No Liam sheet, no Liam folder, no Liam links, no Slack to Liam.
3. **Applicants, standing go:** every fit question answered yes (baby or toddler 10 to 50 lbs to film with, OK showing faces, 3 to 5 videos a week) + confident talking-to-camera videos + lives in the US, Canada, UK, Australia, New Zealand or Ireland = ACCEPT without asking, then onboarding (move to V3 if Grandparents, welcome note in the thread, partnership ads request or connect-Instagram ask, sample nudge next day). Asked for a talking video, answers were yes, never sent it (after one follow-up) = REJECT without asking. Conditional answers, borderline delivery and anything else still wait for a go.
4. **Existing creators' submissions (Fatima, 2026-09-28):** a CLEAR-CUT approval (all 6 checklist points pass in every frame, not sale-led, nothing you are unsure of) goes ahead WITHOUT anyone's review: approve, message (inside the send window), file in Drive, and list it under Done. Anything you are not sure about goes to the operator. **Revisions and rejections always wait until FATIMA herself has watched the videos**; the operator's yes is not enough for those, so list them as "for Fatima to watch".
10. **What else runs without review when you're sure:** the standing applicant accepts and rejects (item 3), eligible sample approvals, partnership ads requests and nudges, due follow-ups, and Drive filing.
5. **Sweeps keep running** past any stated end time until the operator types "stop the routines" (then follow the Stop section of routines/START.md). Keep-awake starts with start.ps1; never ask the operator to start it.
6. **Volume ask is 3 to 5 videos a week** (not 4 to 5). Never excuse it; add one natural line about the support they get.
7. **Cooking and stairs are fine** with one hand on the baby. Straps being chewed is fine. Only flag what the checklist says.
8. **No double follow-ups:** never nudge when our last message is unanswered and under about 48 hours old. Exceptions: sample and Meta access nudges go 15 to 20 hours after our last message about it; applicants asked for a talking video get their one follow-up after a full day. Always `ctx(name)` first and write the next line of that conversation.
9. **Creators who want to post their videos on their own page too:** fine; the program is sharing videos on Trybe so we can run them as ads; kindly ask what they had in mind.


Fatima's non-negotiables (collected 2026-09-23). Each links to its full memory.

**Safety**
- The sling fits babies **10 to 50 lbs**. Never suggest or imply use under 10 lbs, from birth, or a "hospital bag" idea. Stand-ins (a friend's or sister's baby in range, or a doll) ONLY for creators with no child in range; anyone with a kid in range films with their own kid, and gets no doll suggestion. Always one hand on baby; never "hands free". Cooking with baby is OK (Fatima 2026-09-26), don't flag it. [[bambora-sling-safety-rules]]

**Submissions**
- No sale-LED videos (opening on, built around, or repeating the sale, like Kia's). A brief sale mention at the end is fine. Flag sale-led ones to Fatima with revise or reject. [[bambora-content-checklist]]

**Every message**
- Load skill `human-messages` before any creator message: it continues the actual conversation, uses first names only, has no stock phrases ("quick favor" and similar), and every draft passes `lint_message.py`. The chat helper refuses robotic text.
- **Sample nudges sell THEIR benefit (Fatima, 2026-09-26):** the sample is a free product for them, never a favor they do me. Say "free sample" + "the sooner it arrives, the sooner you can start making videos". Never "would love to get it to you" / "any luck with the sample request?" as a favor ask.
- **SAMPLE GATE (hard rule, 2026-09-23):** never write anything about a creator's sample ("request your sample", "approved", "when it arrives") until you've checked her ACTUAL sample status in the Samples tab in that same sweep (`work/trybe-chat/sample-status.js`, or her profile modal's sample history). If a request is pending, approve it first (when delegated) and say it's approved. Never tell someone to request a sample they've already requested. (Alison Boutwell was told to request one she already had pending.)
- **Speak as ONE person (Fatima, 2026-09-24, angry):** I/me, never we/us for feelings or actions ("me too", not "us too"; "on my end", not "on our side"). Linted.
- **Never name other creators to a creator (2026-09-25):** example videos are "video 1, video 2" in messages AND in Drive file titles.
- No em dashes, ever. Read the whole thread right before sending. No parroting. Vary the wording and the emoji. Acknowledge life moments (pregnancy, birth). Positive replies get a reaction plus a line. Never paste the same checklist P.S. twice to one person. [[feedback-creator-dm-voice]]
- If it's unclear what a creator means about something of hers, ask Fatima in one line first. [[feedback-ask-before-guessing]]

**Inspo**
- Cast every creator like a casting director: their role (pediatrician, mom of 5, grandma, twin mom) decides the formats; pitch several. [[creator-casting-mindset]]
- Every inspo item (AI or real, any source) gets thought through: how could OUR creators film their own version, and who fits it. [[inspo-message-rules]]
- Only for creators who already have the sling. Say it's just inspo and they should put their own spin on it. Include the checklist (reworded for repeats). No baby in range: tester, rating, authority, pregnancy haul, "the gift I'm saving for when baby's 10 lbs", or a reaction video (always with a link to react to, found last). Come up with angles from the creator's life stage. [[inspo-message-rules]]

**Applicants**
- On camera talking with good delivery = accept (no socials needed). Nothing on camera = hold. Numbers but no on-camera talking = yapper ask. A big Trybe yapper portfolio overrides weak TikTok numbers. Bilingual is fine. [[bambora-creator-acceptance-criteria]]

**Who to ignore**
- Retainer askers: Kia Layton, Krystal Camacho, Andrew Pagliara, Madison Grove. (Tasha Clay: accepted 10% and Fatima moved her herself on 2026-09-25; the move is DONE, never bring it up again. Answer her replies normally. Her videos have a bad thumbstop rate, so don't use them as inspo examples.) Also Emily Seitz and Madison Tanefski. Labourgeoise Bynum (Fatima 2026-09-26: too much trouble; ignore her messages and NEVER approve her sample request). [[trybe-5pct-migration-followup]]

**Autonomy**
- Approve, reject and accept only on her go, except: samples from recently accepted creators (check them, approve, tell her after). Multi-item sample requests from new V3 creators are fine to approve (Fatima, 2026-09-24, Victoria). Creators who already own a Bambora don't need a sample: no sample nudge, tell them to start filming with theirs (her rule, 2026-09-24). Sample addresses can be in ANY English-speaking country (US, Canada, UK, Australia, New Zealand, Ireland), not US-only (Fatima, 2026-09-24: the routine files had wrongly said "US address"). NEVER approve a sample request made before 2026-09-17 (her rule, 2026-09-24); old pending requests (Jasmyn, Kayse, Kristen, Aurora, Megan Devine, Autumn Bailey, Sara, Skyler) stay untouched. Messages follow her rules without asking unless there's a real question. [[creator-response-cadence]]

**System**
- Follow-up ledger `followups.py due` = everything owed; run it every sweep. Quiet creators (14+ days) are added automatically. [[trybe-applicant-followups]]
- EVERY 30-minute sweep is the FULL run (all six streams: chat, samples, partnership, submissions, discovery, ledger), slow reviews in background agents; streams.sh tracks each and the watchdog (`watchdog.sh 30 60`) wakes Claude when any stream is 60+ min stale (2026-09-24).
- Live sweep every 30 minutes, started at the beginning of every work session (session timers die at session close or after 7 days). The session timer SKIPS a run if Claude is busy, so ALSO keep the watchdog running: `bash ~/claude-setup/work/sweep/watchdog.sh 30` in the background (run_in_background). It exits, and wakes Claude, once the last sweep is 30+ minutes old. Every sweep ends with `bash ~/claude-setup/work/sweep/mark.sh`, and the watchdog is restarted after each wake. Run `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/trybe-chat/front.ps1"` before any browser send (Chrome ignores keys in background tabs). [[creator-response-cadence]]
- Anything new becomes a routine in the same step (skill, routines/, ledger), then push to GitHub. [[feedback-new-work-becomes-routine]]
- Solve gaps from the data before asking. [[feedback-solve-from-data-first]]
- **Sweeps are never skipped because I'm busy (Fatima, 2026-09-24, angry):** when a sweep is due (timer fire or watchdog wake) while I'm working on her request, I tell her in one line and run it right after the current step, or hand the slow parts to a background agent. Being busy is never a reason to skip or silently defer any stream.
- **Irreversible actions need an unambiguous go (2026-09-24):** "let's do the 8" was read as "reject the 8" and all 8 were rejected before she asked to see their messages first. For reject, accept, approve or anything that can't be undone, if her words could mean "discuss" instead of "act", ask one line first. Before any reject, show what each person sent (pitch + what's on their videos) unless she's already seen it.
- **Never pause sweeps on an unanswered question (Fatima, 2026-09-25):** questions go on her list; the 30-minute sweeps and all other work continue regardless.

- Labourgeoise Bynum (2026-09-27, Fatima): "just forget about her". She asked for program terms or a contract; don't reply, don't nudge, no inspo. Ignore her like Abbey Way.
- Reese (Discovery inquiry 2026-09-27, $200/video paid-deal ask): ignore, Fatima said so. No reply.
