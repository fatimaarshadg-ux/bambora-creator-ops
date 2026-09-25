# Handover build report

Built 2026-09-25 on Fatima's Mac from her live setup, for her sister (the operator) on a Windows PC. Built locally only: no GitHub repo was created, nothing was pushed, nobody was invited.

The repo is rebuilt by a script that copies the live sources, applies text ports, then lays hand-written Windows files on top, so it can be refreshed right before publishing if Fatima's setup changes again.

## 1. Sources included

| Source | Went to | Notes |
|---|---|---|
| `~/.claude/skills/*` (19 skills: creator-ops-daily, trybe-portal, trybe-applicant-review incl. scripts and taste profile, fatima-creator-voice incl. lessons.md, human-messages, media-watcher, no-em-dashes, think-before-grinding, voc-miner, bot-forensics, evolve-angles, evolve-call-analysis, evolve-desires, evolve-native-ads, evolve-native-ads-v2, evolve-new-info, evolve-new-mechanism, evolve-static-ads, evolve-video-ads) | `skills/` | Live Mac copies (newest). `.git`, `__pycache__` and any voc-miner corpus left out. media-watcher skill replaced by the current public skill plus a Bambora section. |
| `~/.claude/projects/-Users-fatima-Bombara/memory/*.md` | `memory/` | The live memory (newest), plus 4 files only in claude-setup (ads-library-dmca-monitor, bambora-grandparents-program, claude-media-watcher, feedback-no-oneoff-breakdowns-in-github). MEMORY.md = live index plus the repo-only lines. |
| `~/claude-setup/routines/` | `routines/` | START, full-run (incl. the new Liam batches and Meta access check), live-sweep, README |
| `~/claude-setup/scheduled-tasks/` | `scheduled-tasks/` | All 5 prompts |
| `~/claude-setup/hooks/` | `hooks/` | pre-commit (no em dashes) unchanged; `claude/no-dash-check.py` made UTF-8 safe |
| `~/claude-setup/settings/*.json` | `settings/` | allowlist rewritten for Windows paths; additional-dirs rewritten |
| `~/claude-setup/work/` (every tracked file) | `work/` | Ledger (`followups.json`, 326 items, 174 open), creator-db (profiles, dms, frame sheets, creators.json), trybe-chat helpers and partnership notes, trybe-applicant-review (seen.txt, dated verdicts, scripts, taste profile), trybe-drive-filing (file_approved.py, filed.json, liam_batch.py, liam-sent.json, liam-links), inspo (seen.txt, example-videos-map, authority creators, tags README, dated packs), social-tools (tt.py, tt_find.py), sweep scripts, session logs, 5% migration record, grandparent program, bombara-folder, ads-library-dmca-monitor, ad-analysis, ad-idea-tool, updates-deck, trybe-review. Excluded: applicant media (videos, audio, frame jpgs, saved profile html in `2026-09-23b/`), stream stamps, `server.js.bak`, Mac backup scripts. |
| `~/Bombara/trybe-review/mcp-server/server.js` | `work/bombara-folder/trybe-review/mcp-server/server.js` | The live copy is newer than the repo's (review comment field fix). |
| `~/claude-media-watcher` (commit 0216b35, tracked files) | `tools/claude-media-watcher/` | Vendored, so install needs nothing but this repo. |
| `~/.claude/CLAUDE.md` | `claude/CLAUDE.md` | Rewritten for the operator (see section 2). |
| `~/claude-setup/sync-from-windows.ps1`, `install-mac.sh`, `NEW-MACHINE.md` | `sync.ps1`, `install.ps1`, `README.md` + docs | Ported and extended. |

Not included: anything under `~/.claude/secrets`, Keychain, cookies, `.credentials.json`, API keys (a scan for key-like strings found none; the only long base64 strings are public Facebook Ad Library CDN links and embedded images); `~/Bombara/top-performers` (117 MB of videos, already in Drive), `~/Bombara/trybe-review/tmp` (1.3 GB of downloads), `~/Bombara/trybe-review/inspo-jennifer` (videos), `node_modules`.

## 2. Mac to Windows changes

**Paths and commands (applied to every skill, memory file, routine and task prompt):**
- `/Users/fatima/...` → `~/...` (Git Bash expands `~` to `C:\Users\<name>`, so the same paths work).
- `~/.claude/projects/-Users-fatima-Bombara/memory` → `~/.claude/projects/<PROJECT>/memory`; install.ps1 replaces `<PROJECT>` with the real folder name (for example `C--Users-Sara-Bombara`) when it copies files into `.claude`, and saves it in `.project-slug`.
- `/usr/bin/python3` and `python3` commands → `py -3` (the Windows Python launcher). A `~/bin/python3` shim is also installed for Git Bash, for anything still calling `python3` (the voc-miner wrapper does).
- `~/.local/bin/yt-dlp` → `yt-dlp` on the PATH.
- `bash .../front.sh`, `start.sh`, `apply-*-mac.sh`, `sync_check.sh`, `make_backup_zip.sh` → the PowerShell ports below, called as `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/..."`.
- Keychain wording → DPAPI wording; macOS Drive upload wording → the Windows method.

**Scripts ported (logic kept identical):**
| Mac | Windows |
|---|---|
| `work/sweep/start.sh` (caffeinate, lsof, nohup, /usr/bin/python3) | `work/sweep/start.ps1` (+ `start.sh` now a wrapper that calls it) |
| `caffeinate -dimsu` | `work/sweep/keep-awake.ps1` start/status/stop (SetThreadExecutionState in a hidden process, pid file) |
| `work/sweep/streams.sh`, `mark.sh`, `watchdog.sh`, `every.sh` | unchanged (they run in Git Bash) plus `.ps1` twins sharing the same stamp files |
| `work/trybe-chat/front.sh` (AppleScript: activate Chrome, select the tab whose URL has the marker) | `work/trybe-chat/front.ps1` (restore and foreground the Chrome window, Ctrl+Tab until the title contains "Trybe"; Claude confirms the URL marker in the page) + `front.sh` wrapper |
| `security find-generic-password` in `build_db.py`, `file_approved.py` (and `fetch_media.py` via build_db) | `work/common/trybe_key.py` (env var, then DPAPI via ctypes with a PowerShell fallback, then Keychain) |
| `security` in the Trybe MCP server `server.js` | DPAPI via PowerShell (cached), env var first, Keychain kept for Mac |
| `/opt/homebrew/bin/ffmpeg`, `whisper-cli`, `ls` in `server.js` | `ffmpeg` on PATH via execFileSync, faster-whisper from the media watcher's private Python, `readdirSync` with Windows-safe path handling |
| `/usr/bin/python3` subprocess in `quiet_creators.py` | `sys.executable` |
| `/Users/fatima/Bombara/...` in `build-deck.js` | `os.homedir()` |
| Keychain setup (`security add-generic-password`) | `work/common/store-trybe-key.ps1` (masked popup, DPAPI), called by install.ps1 |
| AppleScript Drive upload (New, key codes, Cmd+Shift+G, Cmd+A) | `work/trybe-drive-filing/drive-upload.ps1` (Google Drive for desktop copy, then connector rename) and `sendkeys.ps1` (real keystrokes for the browser fallback and the Trybe brief upload) |
| `work/backup/sync_check.sh`, `make_backup_zip.sh` | `sync_check.ps1` (restores `<PROJECT>` when copying back), `make_backup_zip.ps1` (Compress-Archive) |
| `settings/apply-allowlist-mac.sh` + `apply-no-dash-hooks-mac.sh` | `settings/apply-settings.ps1` + `apply_settings.py` (Windows allowlist, trusted folders `~/.claude`, `~/claude-setup`, `~/Bombara`, hooks via `py -3`) |
| `install-mac.sh` | `install.ps1` (winget prerequisites, Python packages, PYTHONUTF8, shim, working folder, npm install, media watcher, skills, memory, CLAUDE.md merge, task prompts, git hooks, DPAPI key, permissions, PASS/FAIL self-test) |
| `sync-from-windows.ps1` (Fatima's PC) | `sync.ps1` (runs sync_check.ps1, secret scan incl. the DPAPI blob header, commit, push) |

**Windows robustness fixes:** explicit UTF-8 file reads/writes and UTF-8 stdout in `followups.py`, `lint_message.py`, `new_applicants.py`, `liam_batch.py`, `file_approved.py`, `quiet_creators.py`, `no-dash-check.py`; `PYTHONUTF8=1` set for the user by install.ps1 to cover every other script.

**New for the handover:** `README.md`, `install.ps1`, `sync.ps1`, `FIRST-PROMPT.md`, `OPERATOR.md` (placeholders), `claude/CLAUDE.md` (operator version, ownership rules), `docs/` (manual: ownership, how the job works, every rule, Trybe map, voice guide, where everything lives, ledger and scripts, scheduled tasks, troubleshooting by symptom, background machinery, shift checklists and timeline, first day, glossary), `work/sweep/health.ps1`, memory files `operator-handover.md` and `windows-machine.md`, Windows rewrites of `trybe-api-key-storage.md`, `media-watcher-installed.md`, `claude-media-watcher.md`, `reading-slack-desktop.md`, and `windows-drive-upload-technique.md` (replaces `macos-drive-upload-technique.md`). Routines START, full-run, live-sweep and README carry a short "Windows handover note" at the top.

**Identity:** skills and memory still say "Fatima". Rather than rewriting hundreds of lines, `CLAUDE.md` and memory `operator-handover` map "Fatima's go / tell her" to the operator, keep money, protected creators, program settings and new API keys as Fatima's decisions, and keep every creator message going out as Fatima in her voice (voice skills unchanged).

## 3. Could not port, or not tested

- **Nothing was executed on Windows.** This Mac has no PowerShell, so every `.ps1` was written and reviewed but never run. Python and JavaScript files were syntax-checked, and the Python scripts that don't need Windows were smoke-tested (ledger, linter, applicant check, Liam batch). The first real run is the operator's install; expect small fixes.
- **front.ps1 is weaker than front.sh.** Windows can't read Chrome tab URLs, only the active tab's title. It relies on the Trybe tab title containing "Trybe" (not verified) and cycles with Ctrl+Tab. Claude must confirm the `cl=` marker in the page before any click.
- **Slack desktop driving** (Swift CGEvent clicker, screencapture, AppleScript keys) was not ported. Slack is read in Chrome instead.
- **winget ids** `Anthropic.Claude` and `Google.GoogleDrive` and the Claude app's install path were not verified; README has manual links for every program.
- **Main Media > Trybe in Drive for desktop:** the folder id is known but its local path (shared drive vs My Drive) is not; `drive-upload.ps1` guesses, then asks for `-TargetPath` and remembers it.
- **DPAPI from Python** uses ctypes `CryptUnprotectData` on the `ConvertFrom-SecureString` hex blob; untested on Windows, with a PowerShell fallback (the same method Fatima's dmca monitor already uses on her PC).
- **Trybe MCP server transcription** on Windows uses the media watcher's Python; untested.
- **Claude in Chrome / connectors setup steps** are described in words; exact button names in the Claude app may differ.
- **Connector permission ids** in `settings/allowlist.json` (for example `mcp__1a59c906...__batch`) are Fatima's account's connector ids; on another Claude account they will differ and those lines will do nothing (harmless; she will be asked once per tool).
- **Scheduled tasks** are not created by the installer (they live in the Claude app); FIRST-PROMPT has Claude offer to create them.
- **Session timers** (CronCreate) and background tasks are assumed to behave on Windows as on the Mac.
- `work/ads-library-dmca-monitor/tests/run_test.sh` left as bash (it runs in Git Bash); that tool was already Windows-ready.

## 4. Open questions for Fatima

1. **GitHub:** the sister's GitHub username, which account owns the private repo, and its name (README step 3 has `fatimaarshadg-ux/bambora-creator-ops`).
2. **Claude account:** does the sister use her own Claude account (Pro or Max) or Fatima's? This decides whether the **Bambora Creator Tracker** Claude Doc and the Claude-account connectors (Google Drive, Notion, Claude Docs, Atria) are reachable. Her own account needs the tracker doc shared, and Atria reconnected.
3. **Trybe API key:** give her the current key privately (not a new one; a new key may replace Fatima's). Confirm she should use Fatima's Trybe login through the Bambora Google account, as planned.
4. **Google Drive:** is "Main Media" (with the Trybe folder) a shared drive the Bambora account already sees in Drive for desktop? Same for "Bambora Inspo" and "Claude Backup".
5. **Notion, Slack, Atria:** Slack in Chrome as Fatima is fine? Atria: reconnect under whose login (it is a per-account connector)? Brave search API key: needed on her side?
6. **Messages as Fatima:** confirmed they keep going out as Fatima in her voice. Should anything change if a creator asks to talk on a call or meet?
7. **Her hours and timezone** (for timers and "end of day"), and **who approves** day to day: the sister alone, or Fatima for some categories beyond money, protected creators, settings and keys?
8. **Liam:** does the sister forward Liam's links herself in Slack as Fatima, or does Liam need to know someone else is covering?
9. **Scheduled tasks:** which to run on her PC (inspo every 3 days, end-of-day wrap-up, 4-hourly prep)? Keep the 2-hourly messages task paused?
10. **Both machines running:** will Fatima's Mac keep running routines too? Two live sweeps on one Trybe account would double-message creators. Suggest only one machine runs "start the routines" at a time, and both pull the same ledger (or Fatima's claude-setup stops sweeping).
11. **Fatima's personal ad-writing skills** (evolve-*, voc-miner, bot-forensics) are included because they were in her skills folder; keep or remove for the sister?
12. **ads-library-dmca-monitor** (weekly Task Scheduler job on Fatima's PC, Slack webhook): should the sister run it too?
