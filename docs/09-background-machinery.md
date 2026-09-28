# The invisible machinery, explained

The routine only works if a handful of things keep running quietly in the background all shift. None of them are visible, and if one stops, nothing warns you loudly: sweeps just stop happening. This page explains each piece in plain words: **what it is, why it exists, how to start it on Windows, how to check it is running, and what breaks without it.**

Quick check of everything at once (safe any time, changes nothing):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\sweep\health.ps1"
```

Every line should say **OK**. Anything saying **PROBLEM** shows what to do next to it. You can also just tell Claude "run the health check".

---

## 1. Keeping the PC awake

**What it is.** A tiny hidden program (`work/sweep/keep-awake.ps1`) that tells Windows "don't sleep, don't turn the screen off" every 50 seconds. It is the Windows version of the Mac's `caffeinate`.

**Why it exists.** Everything runs *on this PC*: Claude, Chrome, the timers. When Windows goes to sleep, all of it freezes. A sleeping PC means **missed sweeps**: creators wait hours for replies, samples sit unapproved, follow-ups slip, and Fatima's Trybe "brand health" score (which tracks reply time) drops.

**How to start it.** Claude starts it as part of `start.ps1` when you say "start the routines". By hand:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\sweep\keep-awake.ps1" start
```

**How to check it.** `keep-awake.ps1 status` says RUNNING or NOT running. The health check shows it too.

**How to stop it (end of shift).** `keep-awake.ps1 stop`. It also stops when you restart or sign out.

**Also change these Windows settings once** (keep-awake covers them while it runs, but these make it safe if keep-awake ever stops):
1. **Start** > **Settings** > **System** > **Power & battery** (Windows 11) or **Power & sleep** (Windows 10).
2. Under **Screen and sleep**: set **"When plugged in, put my device to sleep after"** to **Never**. (Turning the *screen* off after a while is fine, but see note 4.)
3. **Laptops: the lid.** Start, type `Control Panel`, open it, **Hardware and Sound** > **Power Options** > **Choose what closing the lid does** (left side). Set **"When I close the lid"** under **Plugged in** to **Do nothing**. Click **Save changes**. Otherwise closing the lid sleeps the PC no matter what.
4. **Keep the charger in** all shift. On battery, Windows may sleep anyway to save power.
5. Prefer an app? Microsoft **PowerToys** has an "Awake" tool that does the same thing with a tray icon (`winget install Microsoft.PowerToys`). Either works; you don't need both.

**What breaks without it.** Sweeps stop the moment the PC sleeps. When it wakes, the watchdog (section 3) notices the gap and Claude catches up, but everything in between was late.

---

## 2. The 30-minute sweep timer

**What it is.** A timer inside the Claude session that fires at **:07 and :37 past every hour** and tells Claude "FULL SWEEP: follow routines/full-run.md for all six streams". Claude sets it with its CronCreate tool when you say "start the routines".

**Why it exists.** Creators expect fast replies, and every stream (chat, samples, partnership ads, submissions, Discovery, ledger) needs checking all day. The timer makes it happen every 30 minutes without you asking.

**The catch: session timers are fragile.**
- They live **only inside the open Claude Code session**. Close the Claude app, close that chat, or restart the PC, and the timer is gone.
- They **expire after 7 days** at most, even if the session stays open.
- If Claude is busy with something when the timer fires, that run can be **skipped**.
That is why the timer is recreated **every work day** (it is step 1 of "start the routines") and why the watchdog exists.

**How to check it.** Ask Claude "is the sweep timer running?" (it checks CronList). The health check's "last full sweep" line should be under 45 minutes.

**What breaks without it.** Nothing happens until you ask. The watchdog would still wake Claude, but only if the watchdog is running.

---

## 3. The watchdog

**What it is.** A small script (`work/sweep/watchdog.sh`, PowerShell twin `watchdog.ps1`) that Claude runs **in the background**. Every 60 seconds it looks at two things: when the last full sweep finished (`work/sweep/last_sweep`), and when each of the six streams last ran (`work/sweep/streams/`). The moment the last sweep is **30+ minutes old**, or any stream is **60+ minutes stale**, it exits, and that exit **wakes Claude** with a message naming what is late.

**Why it exists.** The timer can skip runs when Claude is busy; the watchdog cannot be skipped. It was added on 2026-09-23/24 after Discovery went unreviewed all night while only chat was being swept.

**How it works day to day.** Claude starts it (`bash ~/claude-setup/work/sweep/watchdog.sh 30 60`, in the background). When it fires, Claude runs the late streams, marks each with `streams.sh done <stream>`, runs `mark.sh`, and **starts the watchdog again**. Every sweep ends that way.

**How to check it.** Health check line "watchdog". Or ask Claude "is the watchdog running?".

**What breaks without it.** A skipped timer run goes unnoticed; a stream can go stale for hours.

---

## 4. The helper server (cors_srv.py on port 8765)

**What it is.** A tiny local web server (`work/trybe-chat/cors_srv.py`) that serves Claude's JavaScript helper files from `work/trybe-chat/` at `http://127.0.0.1:8765/`: `chat-helpers.js` (reading threads, the guarded send `g2()`, `qCheck()` for unanswered questions, `convoScan()` for who is waiting), `roster-scan.js` (samples, partnership ads status, left-nav badges, `inboxNames()`), `sample-status.js` (the SAMPLE GATE).

**Why it exists.** Trybe has no API for chat, samples or applicants, so Claude works those through the real Trybe page in Chrome, using these helpers. The page loads them fresh from this server each time (`eval(await fetch('http://127.0.0.1:8765/chat-helpers.js').then(r => r.text()))`), so it always runs the **current** version from the repo, never a stale copy. The server only answers the Trybe site (`jointrybe.com`) and only on this PC (127.0.0.1).

**How to start it.** `start.ps1` starts it hidden. By hand, in PowerShell:
```powershell
cd "$env:USERPROFILE\claude-setup\work\trybe-chat"; py -3 cors_srv.py
```
(leave that window open).

**How to check it.** Open http://127.0.0.1:8765/chat-helpers.js in Chrome: you should see JavaScript text. Or the health check.

**What breaks without it.** In the Trybe page Claude sees errors like "`convoScan is not defined`" or "`g2 is not defined`" / "helpers not defined", or "Failed to fetch". Chat, samples and Discovery streams cannot run.

**Note:** reloading a Trybe page wipes the loaded helpers. Claude reloads them after any reload (that is normal).

---

## 5. Keeping the Trybe tab in front (front.ps1)

**What it is.** `work/trybe-chat/front.ps1` brings Chrome to the front and switches to the Trybe tab. It is the Windows version of the Mac's `front.sh` (which used AppleScript).

**Why it exists.** **Chrome ignores clicks and key presses in background tabs and minimised windows.** Reading still works, which makes it look like the page is broken: Claude clicks Send and nothing happens. On 2026-09-21 this cost about 25 attempts before it was understood. So before every click or send, Claude runs front.ps1.

**What you should do.**
- **Don't minimise Chrome** during the shift. Other windows on top are OK-ish, but minimised is not.
- If you want to use Chrome yourself, **use a different Chrome window** (Ctrl+N), not the Trybe tabs Claude is using, and don't close them.
- Better still: keep the Bambora Chrome window on its own, and do your own browsing in another profile or browser.

**How Claude checks.** In the page: `({vis: document.visibilityState, focus: document.hasFocus()})`. `vis: "hidden"` means the tab is in the background; Claude runs front.ps1 and checks again before any irreversible click.

**Windows limitation.** Windows can only see the title of each window's *active* tab, not the URLs (the Mac could read every tab's URL). front.ps1 therefore presses Ctrl+Tab until the active tab's title contains "Trybe", then Claude confirms the exact tab by its URL marker (next section).

---

## 6. The "cl=3" tab marker

**What it is.** A harmless extra bit Claude adds to the end of a Trybe URL, like `&cl=3`. Trybe ignores it.

**Why it exists.** You (or Fatima) often have your own Trybe tabs open with almost identical URLs. The marker lets Claude find **its own** tab without touching yours. The three working tabs:
- `&cl=3`: Chat
- `&cl=1`: Discovery (applicants)
- `&cl=4`: Creators (roster, samples, partnership ads)

**What you should do.** Leave tabs with `cl=` in the URL alone; they are Claude's. Open your own tabs without it.

---

## 7. Permission prompts (the allowlist)

**What it is.** Claude Code asks "Allow this command?" before running anything not on its allowlist. The allowlist for this routine is in `settings/allowlist.json`; `settings/apply-settings.ps1` adds it (plus the trusted folders `~/.claude`, `~/claude-setup`, `~/Bombara` and the no-em-dash hooks) to `%USERPROFILE%\.claude\settings.json`. install.ps1 offered to do this.

**Why it matters.** When you are there, a prompt just waits for your click. But **scheduled tasks run unattended**: one prompt and the run freezes forever, and while it is "running", **no later run of that task fires either**. On 2026-09-23 a single prompt silently stopped the whole routine until morning.

**Rules that prevent it.**
- Scheduled task prompts use only simple, allowlisted commands (one command per call, absolute paths, no `cd`, `&&`, pipes or loops). Each task prompt carries a "TOOL RULES" block saying so.
- Reading outside the working folder prompts unless the folder is in "additionalDirectories" (apply-settings.ps1 adds them).
- Whenever a routine gains a new command, it is added to `settings/allowlist.json` the same day, and **you** rerun `apply-settings.ps1` (Claude is not allowed to change its own permissions).

**How to check.** Ask Claude to "check the scheduled task runs": any run still "running" long after it started is frozen; Claude reads it, stops it and tells you which command needs allowing.

---

## 8. The Trybe API key (DPAPI)

**What it is.** The password-like key that lets scripts talk to Trybe's API (submissions, creators, earnings, approvals). It lives in `%USERPROFILE%\.claude\secrets\trybe_api_key.dpapi`, **encrypted with Windows DPAPI**: only your Windows account on this PC can read it. It is never in the repo, the chat or the screen.

**To enter or replace it** (a small hidden box opens; paste with Ctrl+V):
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\common\store-trybe-key.ps1" -Force
```

**To test it:** `py -3 "$env:USERPROFILE\claude-setup\work\common\trybe_key.py" --check` (prints "found (N characters)" and "the key works").

**If Trybe answers 401 or 403:** the key was probably replaced in Trybe. Ask Fatima for the current one. **Never create a new key yourself without asking Fatima** (Trybe, Integrations, API): a new key can replace the old one and break her setup.

---

## 9. Where files go, and the daily backup

| What | Where |
|---|---|
| The repo (skills, memory, routines, scripts, ledger, creator database) | `C:\Users\<you>\claude-setup` (and your private GitHub repo) |
| The working folder Claude Code opens | `C:\Users\<you>\Bombara` |
| Claude's installed skills, memory, settings | `C:\Users\<you>\.claude\` |
| The Trybe key | `C:\Users\<you>\.claude\secrets\trybe_api_key.dpapi` (never pushed) |
| Media watcher | `C:\Users\<you>\claude-media-watcher` |
| Approved videos, inspo packs, backups | Google Drive (see `05-where-everything-lives.md`) |
| Downloads for Drive filing | `C:\Users\<you>\Downloads\trybe-filing-YYYY-MM-DD` (deleted after filing) |

**Daily push.** At the end of every session Claude runs `sync.ps1`: it copies what it learned (skills, memory, CLAUDE.md, task prompts) back into the repo, refuses anything that looks like a secret, then commits and pushes. The end-of-day job also zips the repo and uploads it to Drive "Claude Backup / Repo snapshots" (newest 7 kept). If GitHub ever says "push failed", Claude tells you; usually `gh auth login` in PowerShell fixes it.

---

## 10. Keeping Claude Code open all shift

**What it is.** The Claude app's **Code** tab, open on the `Bombara` folder, with the chat where you typed "start the routines".

**Why it matters.** The sweep timer and the watchdog live *inside that session*. Close the app, close that chat, or start a new chat, and they are gone (the ledger and all memory survive; only the timers stop).

**What to do.**
- Keep that one chat open all shift. Talk to Claude in the same chat.
- If you had to close it: open it again in the `Bombara` folder and type `start the routines`. It picks up from the ledger.
- Don't start a second "start the routines" chat at the same time (two sweeps would fight over the same Chrome tabs).

---

## 11. Scheduled tasks (outside the session)

A few jobs run as **scheduled tasks** in the Claude app instead of the session timer: the inspo research every 3 days and optionally the 4-hourly full-cycle prep. They survive closing the chat, but need **the PC awake, the Claude app open, and Chrome signed in**. **They cannot send messages or approve anything** (the permission layer refuses unattended sends), so they only prepare drafts and reports; sending always happens in the live session. How to create them: `07-scheduled-tasks.md`.
