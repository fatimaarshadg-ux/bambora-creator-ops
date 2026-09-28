---
name: play-the-routines
description: "Play the routines" is Ikra's phrase for "start the routines"; every routine start also tells her to plug in the laptop and keep the lid open
metadata:
  type: feedback
---

Ikra (the operator) says **"play the routines"** to mean "start the routines" (2026-09-28). Treat it, and any close variant like "play the routine", as the full start: load skill `creator-ops-daily` and follow `~/claude-setup/routines/START.md` without asking anything first.

**Every time a routine starts, tell her in one line to caffeinate the laptop: plug in the charger and leave the lid open.** Her words, 2026-09-28.

**Why:** she wants to start the whole day with two words instead of a checklist, and the sweeps run for twelve hours, so a laptop that sleeps or runs flat stops the routine silently. The software side (`keep-awake.ps1`, started by `start.ps1`) cannot stop a closed lid or an empty battery, so that part has to be asked of her.

**How to apply:** on "play the routines", run the START.md setup, then make the confirmation line read: keep-awake RUNNING, timers set, watchdog on, US Eastern time with the send window OPEN or CLOSED, and "plug the laptop in and leave the lid open". This does not change the older rule that Claude never asks her to *start* keep-awake itself ([[core-rules]]); Claude starts that, and only the physical charger and lid are hers.

Related: [[operator-handover]], [[windows-machine]], [[feedback-keep-routines-running]].
