---
name: core-rules
description: The essential Bambora creator-ops rules in one page; read first every session. Details live in the linked memories and skills
metadata:
  node_type: memory
  type: feedback
  originSessionId: c57db420-bc45-460b-a4ca-2e63128418b9
  modified: 2026-09-23T17:07:13.342Z
---

Fatima's non-negotiables (collected 2026-09-23). Each links to its full memory.

**Safety**
- The sling fits babies **10 to 50 lbs**. Never suggest or imply use under 10 lbs, from birth, or a "hospital bag" idea. Stand-ins (a friend's or sister's baby in range, or a doll) ONLY for creators with no child in range; anyone with a kid in range films with their own kid, and gets no doll suggestion. Always one hand on baby; never "hands free". [[bambora-sling-safety-rules]]

**Submissions**
- No sale-LED videos (opening on, built around, or repeating the sale, like Kia's). A brief sale mention at the end is fine. Flag sale-led ones to Fatima with revise or reject. [[bambora-content-checklist]]

**Every message**
- Load skill `human-messages` before any creator message: it continues the actual conversation, uses first names only, has no stock phrases ("quick favor" and similar), and every draft passes `lint_message.py`. The chat helper refuses robotic text.
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
- Retainer askers: Kia Layton, Krystal Camacho, Andrew Pagliara, Madison Grove. (Tasha Clay: accepted 10% and Fatima moved her herself on 2026-09-25; the move is DONE, never bring it up again. Answer her replies normally. Her videos have a bad thumbstop rate, so don't use them as inspo examples.) Also Emily Seitz and Madison Tanefski. [[trybe-5pct-migration-followup]]

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
