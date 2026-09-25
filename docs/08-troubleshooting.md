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
- **"Could not find the 'Trybe' folder":** run `drive-upload.ps1 -Find` to list folders, then give Claude the right path (for example `G:\Shared drives\Main Media\Trybe`); it saves it in `drive-folders.json`. If "Main Media" isn't there at all, the Bambora account may not have that shared drive added: ask Fatima.
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
Run `gh auth login` in PowerShell (choose GitHub.com, HTTPS, sign in with browser), then tell Claude to run sync.ps1 again. The commit is safe on the PC meanwhile.

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
