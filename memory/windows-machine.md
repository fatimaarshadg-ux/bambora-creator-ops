---
name: windows-machine
description: This is a Windows PC; how the Mac-built routine maps onto it (shell, Python, paths, PowerShell ports, what differs)
metadata:
  type: reference
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

**Keep the PC awake during the work day:** start.ps1 holds a keep-awake request, but closing a laptop lid can still sleep it. Leave the lid open and the charger in.

Related: [[operator-handover]].
