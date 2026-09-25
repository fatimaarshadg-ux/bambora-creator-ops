# Shift checklists and "what runs when"

Print this page or keep it open. Times below use Fatima's day (about 5 PM to 5 AM Pakistan time); shift them to your hours in `OPERATOR.md`.

## START OF SHIFT (about 5 minutes)

1. **Power:** charger plugged in, laptop lid open.
2. **Chrome:** open the Bambora Chrome profile (fatima@bamboraco.com). Check you are still signed in to Trybe (https://jointrybe.com/brand?b=a8bedbc3-3b30-410d-a09e-2aa3aeb3a8e9). If Trybe shows a login page, sign in yourself.
3. **Google Drive for desktop:** the Drive icon is in the taskbar tray (bottom right, maybe under the ^ arrow) and File Explorer shows `Google Drive (G:)`.
4. **Claude:** open the Claude app, **Code** tab, folder **Bombara**. Use one chat for the whole shift.
5. Type: **`start the routines`**
6. Claude then does all of this by itself (you just watch for its first message):
   - reads the core rules, the voice cheat sheet, the ledger;
   - runs `start.ps1`: keep-awake ON, helper server ON, repo pulled, "due today" list, stream ages;
   - opens or finds the three Trybe tabs (`cl=3` chat, `cl=1` Discovery, `cl=4` Creators) and loads the helpers;
   - sets the sweep timer (:07 and :37) and the end-of-day timer;
   - starts the watchdog in the background;
   - runs the first full sweep right away (on the first sweep of the day it also refreshes the creator database).
7. **Check:** Claude's first message says the timer and watchdog are running. If you want to be sure: tell Claude "run the health check" (everything OK).
8. Don't minimise Chrome from now on. Use another window or browser for your own browsing.

## DURING THE SHIFT

- Every ~30 minutes, one message from Claude: **Done**, **Needs your go** (numbered, with recommendations), **Questions**. Answer like "yes 1 and 3, no 2 because ...".
- Money, retainers, protected creators, program settings, new Trybe key → check with Fatima before you say yes.
- When 5+ videos are ready for Liam, Claude gives you a ready message: copy it into Slack to Liam.
- If you step away: leave everything open. The keep-awake keeps the PC on.

## END OF SHIFT (Claude runs most of it at the end-of-day time; you finish the last 3 steps)

1. Claude: files any approved videos not yet in Drive (download, upload, rename, mark).
2. Claude: gives you the remaining **Liam links** (`liam_batch.py message --any`); you forward them to Liam on Slack.
3. Claude: writes the session log `work/session-logs/YYYY-MM-DD.md` (what got done, new rules, what's open), updates memory and skills with anything new.
4. Claude: makes sure the ledger holds everything still open, so tomorrow starts from it.
5. Claude: runs `sync.ps1` (push to GitHub) and the repo zip to Drive; stops the sweep timer for the night.
6. **You:** read Claude's wrap-up message. Check it says "Pushed".
7. **You (optional):** stop keep-awake (`keep-awake.ps1 stop`) if you want the PC to sleep normally overnight.
8. **You:** you can close the Claude app now. Tomorrow, "start the routines" rebuilds the timers.

## WHAT RUNS WHEN (one page)

| When | What | Where it is defined |
|---|---|---|
| Start of shift | Setup: keep-awake, helper server, pull, ledger, tabs, timers, watchdog, first sweep | `routines/START.md`, `work/sweep/start.ps1` |
| First sweep of the day | Creator database refresh (`build_db.py`, adds quiet creators to the ledger) and new frame sheets (`fetch_media.py`) | `routines/live-sweep.md` step 1 |
| **Every 30 min** (:07 and :37) | **Full sweep, all six streams**: chat, samples, partnership ads, submissions, Discovery, ledger. Then ONE message | `routines/full-run.md` |
| Every minute (background) | Watchdog: wakes Claude if the last sweep is 30+ min old or a stream is 60+ min stale | `work/sweep/watchdog.sh` |
| After every Drive filing | Liam batch check: 5+ unsent videos → forward-ready message | `work/trybe-drive-filing/liam_batch.py` |
| Every ~5 hours | Meta (partnership ads) access check across the V3 roster | `routines/full-run.md`, `work/sweep/every.sh due metaaccess 300` |
| Once per shift (first sweep after 11 PM in Fatima's day) | Check-in audit: every V3 and protected creator has a ledger item or recent message | `routines/full-run.md` |
| Every 3 days (scheduled task) | Inspo research pack to Drive, tagged, matched to creators | `scheduled-tasks/bambora-inspo-research-every-3-days` |
| Every 3 days | Personal inspo messages (drafts to you first) | skill `creator-ops-daily` section 7 |
| Every 4 hours (optional scheduled task) | Full-cycle prep for days without a live session (drafts only) | `scheduled-tasks/bambora-full-cycle-every-4h` |
| End of day (~45 min before you stop) | Drive filing, Liam links, session log, push, repo zip to Drive, stop timer | `routines/START.md` section 4, `scheduled-tasks/bambora-end-of-day-wrapup` |
| Weekly | Top performers ($500+) check; taste profile refresh every month or two | skill `creator-ops-daily` section 6, skill `trybe-applicant-review` |
