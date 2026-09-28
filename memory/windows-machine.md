---
name: windows-machine
description: "This is a Windows PC; how the Mac-built routine maps onto it (shell, Python, paths, PowerShell ports, what differs)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 69a3b3e5-e78c-4da3-971b-bbee6481f79a
  modified: 2026-09-28T12:11:42.003Z
---

The whole routine was built on Fatima's Mac and ported for this Windows PC on 2026-09-25 (repo `~/claude-setup`, see its HANDOVER-BUILD-REPORT.md for every change).

**Shell and paths**
- Claude Code's Bash tool runs **Git Bash**. `~` is `C:\Users\<name>`, so `~/claude-setup/...`, `~/Bombara/...` and `~/.claude/...` all work as written.
- Python is `py -3` (the Windows launcher), never `/usr/bin/python3`. A `python3` shim in `~/bin` exists too, but `py -3` is the documented form.
- `PYTHONUTF8=1` is set for the user so scripts read and print emoji and creator names correctly. If a script prints garbled characters, check that variable.
- ffmpeg, ffprobe and yt-dlp are on the PATH (winget, with the media-watcher's copies in `~/claude-media-watcher/bin` as a fallback).
- The working folder is `~/Bombara` (misspelt on purpose so every note matches; the brand is Bambora). Its memory folder is `~/.claude/projects/<PROJECT>/memory`, where `<PROJECT>` is the folder name install.ps1 computed and saved in `~/claude-setup/.project-slug`.

**Mac piece → Windows piece**
- `front.sh` (AppleScript tab fronting) → `work/trybe-chat/front.ps1` (brings Chrome forward, Ctrl+Tab until the Trybe tab is active; confirm `location.href` has the marker with javascript_tool).
- `start.sh` (caffeinate, lsof, nohup) → `work/sweep/start.ps1` (hidden keep-awake process, helper server, pull, ledger, stream ages).
- `streams.sh`, `mark.sh`, `watchdog.sh`, `every.sh` run unchanged in Git Bash; `.ps1` twins exist and share the same stamp files.
- Keychain → Windows DPAPI (`~/.claude/secrets/trybe_api_key.dpapi`), loaded by `work/common/trybe_key.py`. See [[trybe-api-key-storage]].
- AppleScript Drive upload → Google Drive for desktop copy (`work/trybe-drive-filing/drive-upload.ps1`). See [[windows-drive-upload-technique]].
- `osascript ... key code` → `work/trybe-drive-filing/sendkeys.ps1` (real keystrokes for file dialogs and menus only).
- `sync_check.sh`, `make_backup_zip.sh` → `work/backup/*.ps1`. `apply-allowlist-mac.sh` + `apply-no-dash-hooks-mac.sh` → `settings/apply-settings.ps1`.
- Slack desktop driving (Swift clicker, screencapture) was not ported: read Slack in Chrome instead ([[reading-slack-desktop]]).

**Keep the PC awake during the work day:** start.ps1 holds a keep-awake request, but closing a laptop lid can still sleep it. Leave the lid open and the charger in. Say this to the operator every time a routine starts ([[play-the-routines]]).

**The PC clock is US Pacific, not Pakistan time** (found 2026-09-28). `Get-TimeZone` says Pacific Standard Time, so during the shift local time runs 9 hours behind Ikra's PKT wall clock (PKT 5 PM = 5 AM local). Anything that uses the machine's local time has to be converted:
- CronCreate fires on local (Pacific) time. Her 6:12 AM PKT end of day is `12 18 * * *`, not `12 4 * * *`.
- The send window is safe either way, because `work/common/us-time.ps1` computes US Eastern itself. 12 PM ET is 9 AM on this clock.
- A session-log filename taken from the local date stays on one date through her whole shift, while the PKT date rolls over at 12 AM PKT (2 PM local). Use the PKT date for logs so they line up with Fatima's Mac.

**`py` can vanish from PATH** (found 2026-09-28). The launcher lives in `%LOCALAPPDATA%\Programs\Python\Launcher\py.exe` and is on the user PATH, but a Claude session started before that entry existed inherits the old PATH, so `py` is not found and the ledger and helper server fail with nothing obvious in the output. Fixes now in place: a `py` shell shim in `~/bin` for Git Bash, and `start.ps1` resolves `py.exe` by full path when `Get-Command py` misses (it ignores the `~/bin` shim, which PowerShell cannot execute). If `py` fails again, restart the Claude app first, since that picks up the real PATH.

**There is a second clone of the repo at `D:\Projects\bambora-creator-ops`.** It is a spare from handover setup day and is not wired to anything. The live copy is `C:\Users\Hp\claude-setup`: it holds Ikra's filled-in OPERATOR.md, and every script, memory path and doc points at it. Both clones push to the same single GitHub repo, `fatimaarshadg-ux/bambora-creator-ops`. Ikra's instruction (2026-09-28): keep only one up to date. Never sweep or sync from the D copy.

Related: [[operator-handover]], [[play-the-routines]].
