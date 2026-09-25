---
name: creator-response-cadence
description: Fatima's rules for how fast and how often to respond to creators. Check chat every 2 hours in a work day, positive replies always get a 💙 reaction plus a warm line, 1-working-day follow-ups, sample check-in about 2 weeks after approval
metadata:
  type: feedback
---

How often and how fast to answer creators (stated by Fatima on 2026-09-23; her brand health score tracks reply time):

- **Start of every work day:** run the `creator-ops-daily` sweep. Read chat first, oldest waiting first.
- **Confirmed 2026-09-23:** messages every 2 hours, full cycle (submissions, Drive filing, applicants, samples, tracker) every 4 hours, her green light on EACH approval, rejection and acceptance, and a session kept open during her work day. Details in skill `creator-ops-daily` under "The work-day rhythm".
- **Every 30 minutes during the work day** (changed from 2 hours on 2026-09-23): the live sweep in the open session checks the ledger and Trybe chat (Unread first) and answers. The prompt is in ~/claude-setup/routines/live-sweep.md.
- **Positive replies** ("thanks!", "so excited!"): always react with 💙 and send a short, warm, human line that fits the thread ("Of course, I'm always here for you 😊💙"). Never skip these.
- **Questions or problems** (revision confusion, rejected videos, retainer): don't improvise. Bring them to her with a suggested reply the same day.
- **No reply to our ask** (applicant DMs, yapper or English content): one gentle follow-up after 1 working day.
- **Accepted but no sample request:** nudge after about 1 day, fitted to the thread.
- **Inspo packs:** every 3 days, personalised per creator (skill creator-ops-daily step 7).
- **Sample approved:** check in about 2 weeks later ("hope it arrives soon if it hasn't, let me know when it does so I can share ideas").
- **Made a few videos, then stopped:** check in, with her point that creators posting 20-30 videos a month do best.
- **Retainer askers from the 5% migration:** don't chase (see [[trybe-5pct-migration-followup]]).
- Messages go in her voice ([[feedback-creator-dm-voice]], skill `fatima-creator-voice`), each unique to its thread. Emoji: 💙 and 😊.

Related: [[bambora-creator-tracker-doc]], [[trybe-applicant-followups]]
- **Samples from newly accepted creators: approve without asking (delegated by Fatima, 2026-09-23).** Check the product (one item), the address and the note first, then approve on the next 30-minute sweep, send a sample message fitted to the thread, and tell her after. Anything else (an older creator, several items, an odd note, duplicate names) goes to her first. Sample requests are checked on EVERY sweep, not just the 2-hour pass.
