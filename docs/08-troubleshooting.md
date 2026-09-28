# Troubleshooting (by symptom)

First step for almost everything: tell Claude **"run the health check"**, or run it yourself:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\sweep\health.ps1"
```
Background on each piece: `09-background-machinery.md`.

---

### "Clicks do nothing" / Claude says Send didn't work / the message is still in the box
**Cause:** the Trybe tab is in the background, Chrome is minimised, or another window is on top. Chrome drops clicks and key presses in background tabs (reading still works, so the page looks fine).
**Fix:** restore Chrome (don't minimise it). Claude runs `front.ps1` and checks `document.visibilityState` is "visible" before trying again. Do your own browsing in a separate Chrome window.

### "helpers not defined" / "convoScan is not defined" / "g2 is not defined" / "Failed to fetch"
**Cause:** the Trybe page was reloaded (helpers are wiped on reload), or the helper server on port 8765 is not running.
**Fix:** open http://127.0.0.1:8765/chat-helpers.js in Chrome. If it shows code, Claude just reloads the helpers in the page. If it doesn't load, run `work\sweep\start.ps1` (it starts the server), or in PowerShell: `cd "$env:USERPROFILE\claude-setup\work\trybe-chat"; py -3 cors_srv.py` and leave that window open.

### The sweep didn't run / no message from Claude for over 30 minutes
**Causes, most likely first:** the PC slept; the Claude chat was closed (timers die with it); the timer is more than 7 days old; Claude was busy and the watchdog wasn't running.
**Fix:** check the PC's power settings and keep-awake (`keep-awake.ps1 status`). In the same Claude chat, type "start the routines" again: it recreates the timer and watchdog and runs a full sweep now. If Claude says it is busy, it should run the sweep right after its current step (that is a rule).

### A stream shows as stale ("STALE: discovery")
**Fix:** tell Claude "run the stale streams now". A stream is only marked done after its check really ran, so a stale stream means it genuinely hasn't been checked.

### "Drive upload fails" / drive-upload.ps1 can't find the folder
- **"Google Drive for desktop was not found":** open Google Drive from the Start menu and sign in with fatima@bamboraco.com; check File Explorer shows `Google Drive (G:)`.
- **"Could not find the 'Trybe' folder":** run `drive-upload.ps1 -Find` to list folders, then give Claude the right path (for example `G:\Shared drives\Main Media\Trybe`); it saves it in `drive-folders.json`. If "Main Media" isn't there at all, it is probably a folder someone *shared with* Fatima, and Drive for desktop only shows those once they have a shortcut: open https://drive.google.com (Bambora profile), click **Shared with me**, right-click **Main Media**, **Organize** > **Add shortcut** > **My Drive**. After a minute it appears as `G:\My Drive\Main Media\Trybe`, which drive-upload.ps1 finds by itself. Not in "Shared with me" either: ask Fatima.
- **Files copied but not visible in Drive:** they are still uploading (the Drive tray icon shows progress). Wait, then Claude checks with the Drive connector.
- **Renaming fails:** the Google Drive connector isn't connected or has no access. Reconnect it in the Claude app (Settings > Connectors).
- **Browser fallback:** see memory `windows-drive-upload-technique`.

### Trybe API errors (401 or 403) / "Trybe key: NOT FOUND"
- NOT FOUND: run `work\common\store-trybe-key.ps1` and paste the key from Fatima.
- 401/403 with a key stored: the key was probably replaced in Trybe. Ask Fatima for the current key, then `store-trybe-key.ps1 -Force`. Don't create a new key without asking her.
- 403 only from a new script: it must send a normal User-Agent (`curl/8.7.1`); Python's default is blocked.

### Trybe shows a login page
You sign in yourself (in the Bambora Chrome profile). Claude never types passwords.

### The Discovery page freezes
Normal: it renders 222,000+ creators. Claude focuses the Inbox tab through the page and presses a real Enter; if it stays frozen, it reloads the tab and tries again. Don't click around in it while Claude works.

### Claude doesn't seem to know the rules / has no memory
**Cause:** Claude Code was opened in a different folder, so it loaded a different (empty) memory.
**Fix:** always open `C:\Users\<you>\Bombara`. Check `claude-setup\.project-slug` against the folder list in `C:\Users\<you>\.claude\projects\`. Rerunning `install.ps1` repairs it.

### Claude keeps asking permission for every command
Run `settings\apply-settings.ps1` (adds the allowlist). New command in a routine? It should be added to `settings\allowlist.json`; then rerun the script.

### A scheduled task seems stuck
Ask Claude to "check the scheduled task runs". A run stuck in "running" waited for a permission prompt; Claude stops it and names the missing permission.

### Garbled characters (Ã©, ðŸ’™) in script output
`PYTHONUTF8` isn't set in that window. Open a new PowerShell or Claude session (install.ps1 set it for your user), or rerun install.ps1.

### "py is not recognized" / "git is not recognized"
Open a NEW PowerShell window (Windows only sees newly installed programs in new windows). Still missing: rerun install.ps1, or install from the README links.

### Commit blocked: "em dash in added lines"
The repo's pre-commit hook refuses em dashes. Claude rewrites the line (unless it is quoted material) and commits again.

### Push failed
The commit is safe on the PC meanwhile. In PowerShell run `gh auth login` (choose **GitHub.com**, **HTTPS**, **Yes** to authenticate Git, **Login with a web browser**; sign in as Fatima's GitHub account, fatima@bamboraco.com), then `gh auth setup-git`. Then tell Claude to run sync.ps1 again. If it says "pull FAILED", tell Claude "sync.ps1 pull failed, sort out the conflict".

### Media watcher: "not installed" / a video won't open
Rerun `install.ps1` (it resumes the media watcher install). For a Trybe video, the signed link expires in about 20 minutes: Claude fetches a fresh one. Private or removed TikTok/Instagram videos can't be downloaded.

### TikTok "Access denied" (403)
Claude used the browser for TikTok; it must use `tt.py` instead (memory `tiktok-no-browser-tool`). Wait about 20 minutes and the block clears.

### A message went to the wrong person, or said something wrong
Tell Claude right away. Trybe lets you **edit** a sent message (hover it, Edit message, Save changes); deleting is destructive, so ask before deleting. Claude logs the lesson so it doesn't repeat.

### Two Claude chats both running the routine
Close one. Two sweeps fight over the same Chrome tabs.

### Fatima's Mac and this PC both running the routine
Stop one right away (on this PC: tell Claude "stop the sweep timer and the watchdog", or close the chat). Then ask Claude to check the last hour of Trybe chats for double replies and to compare the follow-up ledger with Fatima's, so nothing is sent twice or lost.

---

## Things that go wrong during a shift

### The PC restarted (Windows Update, a power cut, or it crashed)
Everything you saved is safe (the ledger, memory and repo are files). What died: the sweep timer, the watchdog, keep-awake and the helper server. To get going again, in this order:
1. Sign in to Windows.
2. Open Chrome with the **Bambora** profile. If Chrome offers **Restore** pages, click it. If not, don't worry: Claude reopens its Trybe tabs.
3. Check the Google Drive icon is in the taskbar tray (bottom right, maybe under the **^** arrow). It starts by itself; if it isn't there, open **Google Drive** from the Start menu.
4. Open the Claude app, **Code** tab. Your old chat is in the list on the left: click it (or start a new chat in the **Bombara** folder).
5. Type **start the routines**. Claude reruns `start.ps1` (keep-awake, helper server, pull), sets the timers again and runs a full sweep straight away.
6. Many follow-ups will be due at once and replies may be late. That is normal; Claude works through them oldest first. If the PC was off for more than 2 hours of your shift, tell Fatima in one line.

**Stop it happening again:** Start > Settings > **Windows Update** > **Advanced options** > **Active hours**: set it to **Manually**, from **4 PM** to **6 AM** (or your hours plus an hour each side). Windows will not restart for updates during those hours. On a day with a pending update, restart the PC yourself **before** your shift. Also turn off **"Get the latest updates as soon as they're available"** on the Windows Update page.

### The screen locked, or I pressed Windows+L
A locked PC makes Chrome treat every tab as hidden, so Claude can read but **cannot click or send** anything. Sign back in; Claude catches up on the next sweep. Don't lock the PC while the routine runs; if you need privacy, turn the monitor off with its own button instead. To stop it locking by itself: Start > Settings > **Accounts** > **Sign-in options** > "If you've been away, when should Windows require you to sign in again?" > **Never**, and turn **Dynamic lock** off.

### A Trybe tab was closed (by you, or Chrome crashed)
Do nothing. At the next step Claude notices the `cl=` tab is missing and opens it again, then reloads its helpers. If you want it sooner, tell Claude "reopen the Trybe tabs". Only open tabs yourself **without** `cl=` in the address.

### Chrome shows "Relaunch to update", or Chrome restarted
Don't click Relaunch mid-shift; do it before or after. If Chrome restarted anyway: it usually restores tabs; if the Trybe tabs are gone, Claude reopens them. If Trybe asks you to sign in, sign in yourself.

### Tabs keep reloading or go blank ("This page was discarded to save memory")
Chrome's **Memory Saver** throws away tabs you are not looking at, and that wipes Claude's helpers. In the Bambora Chrome profile: **three dots** (top right) > **Settings** > **Performance**: turn **Memory Saver** OFF and **Energy Saver** OFF.

### Claude asks for permission in the middle of a sweep
The sweep waits until you answer. Nothing is lost if you were away; answer when you are back.
- **Allow it** when it is one of Claude's own tools: a command that starts with `py -3 ~/claude-setup/`, `bash ~/claude-setup/`, `powershell ... claude-setup\...`, `git -C ~/claude-setup`, `~/claude-media-watcher/watch`, `ffmpeg`, `yt-dlp`; reading files; the Trybe tools (`trybe_list_submissions`, `get_submission`, `transcribe` and so on); Chrome on jointrybe.com, Google Drive, TikTok, Instagram or YouTube. If the same kind of request keeps coming, choose the "always allow" option, then tell Claude "add that to settings/allowlist.json" and run `settings\apply-settings.ps1` later.
- **Allow only if you already said yes in the chat:** `trybe_approve_submission`, `trybe_reject_submission`, `trybe_request_revision` (these change a creator's video for real).
- **Deny** anything that deletes files (`rm`, `del`), `git push --force` or `git reset --hard`, changes Claude's settings or permissions, types a password, installs a program, or that you simply don't understand. Then type "what was that and why?" Claude explains, and nothing breaks. Still unsure: ask Fatima.
- Never switch Claude to a "bypass permissions" or "skip all permissions" mode.

### The helper server is down ("Failed to fetch", "g2 is not defined")
Tell Claude **"run start.ps1"**; it restarts the helper server and checks it. If that doesn't fix it, open a PowerShell window and paste `cd "$env:USERPROFILE\claude-setup\work\trybe-chat"; py -3 cors_srv.py`, then leave that window open (minimised is fine) for the rest of the shift. Check: http://127.0.0.1:8765/chat-helpers.js in Chrome should show code. If PowerShell says the port is in use, the server is already running, and the problem is the page: tell Claude "reload the helpers".

### I am not sure whether to approve something
Don't approve it yet. Say **"hold 2"** or **"show me 2"** (Claude shows the frames, the transcript, the creator's message or the thread). Then check `11-decision-guide.md`. Anything about money, the 10 protected creators, program settings or a Trybe key: ask Fatima. Waiting one sweep never breaks anything.

### Claude says it hit a usage limit ("limit reached, resets at ...")
This Claude account is Fatima's, so her own use on the Mac counts too. Nothing can run until the time shown. Keep the chat open; at the reset time type **start the routines** (the timers may have stopped). Tell Fatima, so she can avoid heavy use during your shift or change the plan.

### Claude is looking at the wrong Chrome (Fatima's tabs, not yours)
Because you both use Fatima's Claude account, Claude in Chrome may see Fatima's Chrome on her Mac as well as yours. Tell Claude: **"list the connected browsers and use the one on this Windows PC"**. It must never click in Fatima's browser. If it did, tell Fatima right away.

### Claude in Chrome says "not connected" / no browser found
In Chrome, click the Claude icon (puzzle piece > Claude if it isn't pinned) and check you are signed in with Fatima's Claude account. Then in Claude say "try Chrome again". Still nothing: close Chrome completely and reopen it with the Bambora profile.


