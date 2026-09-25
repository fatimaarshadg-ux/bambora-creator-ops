# Audit report

Audited 2026-09-25 on Fatima's Mac, after rerunning the build script so the repo holds tonight's sources. Nothing was pushed, no GitHub repo was created, and none of Fatima's own files were touched. Every fix below is committed locally and was also copied into the build overlay, so a rebuild keeps it (checked: a rebuild after the fixes changed nothing).

**Verdict: NOT READY TO PUSH as a finished handover.** The content is complete and clean, and the scripts are reviewed. But three things only a human can settle block a smooth first day: which repo is the single source of truth (see H1), one real test install on a Windows PC (H2), and the account questions (H3 to H5). Pushing the repo privately so the test install can happen is fine.

## Step 0: sources refreshed

`build.py` only copies into `~/bambora-ops-handover`, so it was run. The repo already matched the live sources. Every item added tonight is present:

| Required item | Present |
|---|---|
| memory `feedback-take-ownership.md`, `creator-base-retainer-offer.md`, `routine-liam-batches-and-meta-access.md` | yes |
| `core-rules.md` with the Tasha Clay line (moved 2026-09-25, never bring it up) | yes |
| `routines/full-run.md` sections "Liam batches" and "Meta access check" | yes |
| `work/trybe-drive-filing/liam_batch.py` and `liam-sent.json` | yes |
| `work/sweep/every.sh` and the Windows port `every.ps1` | yes |
| `work/creator-db/followups.json` | yes, byte-identical to `~/claude-setup` |

## Checklist

| # | Check | Result |
|---|---|---|
| 1 | Completeness against the sources | PASS (after fix) |
| 2 | No Mac leftovers | PASS |
| 3 | No secrets | PASS |
| 4 | install.ps1 and every .ps1 | PASS after 6 script fixes; untested on Windows |
| 5 | "Stupid simple" walk-through | PASS after fixes, with the open items in H3 to H6 |
| 6 | Rules completeness in the docs | PASS (after fix) |
| 7 | No dashes in the builder's prose | PASS |
| 8 | Messages as Fatima, her email, one machine at a time | PASS (after fix; the one-machine warning was missing) |

### 1. Completeness: PASS

- **Skills:** all 19 folders in `~/.claude/skills` are in `skills/`. Only `~/.claude/skills/README.md` (the EVOLVE pipeline overview) was missing. **Fixed:** copied it.
- **Memory:** every live file is in `memory/`. The differences are deliberate: `macos-drive-upload-technique.md` is replaced by `windows-drive-upload-technique.md`; `operator-handover.md` and `windows-machine.md` are new; four files come from the claude-setup copy only.
- **Routines and scheduled tasks:** all of them.
- **work/:** every tracked file except deliberate exclusions: applicant media in `trybe-applicant-review/2026-09-23b/` (videos, replies audio, jpg and html), the Mac-only `backup/*.sh` (they have .ps1 ports), `server.js.bak`, and the runtime stamps.
- **Trybe MCP server:** `server.js` (the newer live copy, ported), `package.json`, and `~/Bombara/.mcp.json`, which install.ps1 copies into `%USERPROFILE%\Bombara`. **Added** a self-test line for it.
- **Media watcher:** vendored in `tools/claude-media-watcher` (only the untracked downloaded `bin/` is left out; the installer downloads it).
- **TikTok tool:** `work/social-tools/tt.py` and `tt_find.py`.
- **Not carried, minor:** `~/Bombara/.claude/settings.json` (project permissions). Every entry in it that matters is already in `settings/allowlist.json`.

### 2. Mac leftovers: PASS

Every remaining hit for `osascript`, `caffeinate`, Keychain, `find-generic-password`, `/usr/bin/python3`, `Cmd+`, AppleScript, `/opt/homebrew` and `screencapture` is one of these: a "the Mac used X" explanation, a macOS-only fallback branch that never runs on Windows (`trybe_key.py`, `server.js`, the dmca monitor), or the media watcher's own Mac installer `install.sh`. `/Users/fatima` appears only in HANDOVER-BUILD-REPORT.md, where it describes the conversion. The `.sh` files still referenced (`streams.sh`, `mark.sh`, `watchdog.sh`, `every.sh`) run in Git Bash, which is Claude Code's shell on Windows. They use only portable commands (`date +%s`, `cat`, arithmetic), and every one has a `.ps1` twin. `front.sh` and `start.sh` are wrappers that call the `.ps1` ports.

### 3. Secrets: PASS

- Scanned every tracked file for GitHub tokens (`gho_`, `ghp_`, `github_pat_`), `sk-`, `sk-ant`, Slack tokens and webhooks, `Bearer` plus a long string, `tk_`, AWS and Google keys, PEM blocks, password assignments, DPAPI blob headers and 48+ character hex runs. The only hits were false positives (`ask-everything` in a file name, the scanner patterns in sync.ps1, base64 JPEGs embedded in the invite HTML).
- The real Trybe key was read from the Keychain and searched for, in the working tree and in the full git history, without ever printing it: **0 hits**.
- No `.credentials.json`, cookie files or `.env` files. `.gitignore` blocks `secrets/`, `*.dpapi`, `.env*`, `*.pem`, `*.key` and cookies.

### 4. PowerShell review: PASS after fixes (never run on Windows)

The install.ps1 read-through:
- **winget ids:** `Git.Git`, `Python.Python.3.12`, `Google.Chrome`, `OpenJS.NodeJS.LTS`, `Gyan.FFmpeg`, `yt-dlp.yt-dlp`, `GitHub.cli` and `Google.GoogleDrive` are the right ids as far as I know. `Anthropic.Claude` is plausible but unverified. The README has a manual link for every program, and `-NoWinget` skips winget.
- **Project memory folder:** `[regex]::Replace($work, '[^a-zA-Z0-9]', '-')` gives `C--Users-hp-Bombara` for `C:\Users\hp\Bombara`. That is correct: Claude Code turns every character that is not a letter or digit into `-`, which covers the colon and the backslashes. The result is saved in `.project-slug` and reused by `sync_check.ps1`. The one assumption is that the operator opens exactly `C:\Users\<name>\Bombara`; FIRST-PROMPT has Claude check this.
- **DPAPI:** `store-trybe-key.ps1` shows a masked WinForms box and stores the key with `ConvertTo-SecureString` and `ConvertFrom-SecureString` (user-scoped DPAPI, hex). `trybe_key.py` decrypts it with `CryptUnprotectData` and reads it as UTF-16LE, which is right for that format, with a PowerShell fallback. `server.js` uses the same PowerShell method.
- **Paths with spaces:** quoted or passed through `Join-Path` everywhere. **Idempotency:** existing files are kept unless `-Refresh` is given, with backups; the memory index only gets lines appended; CLAUDE.md goes between markers. **Encoding:** every .ps1 is pure ASCII (safe for PowerShell 5.1 without a BOM). `.gitattributes` forces LF for `.sh` files and CRLF for `.ps1`, so Git for Windows' autocrlf cannot break the bash scripts.
- **Self-test:** covers programs, Python packages, the working folder, skills, memory, CLAUDE.md, the media watcher, the ledger, the linter, the stream tracker, the key (with a live API call) and PYTHONUTF8. **Added:** a check for `.mcp.json` plus `server.js`.

Bugs found and fixed:
1. **keep-awake.ps1 would never have kept the PC awake.** `[uint32]"0x80000003"` fails in Windows PowerShell 5.1: the hex string parses as a negative Int32, and converting that to UInt32 overflows. The error happens inside the hidden loop, so `status` would still have said RUNNING while the PC went to sleep. Now `[uint32]2147483651` (the same value in decimal).
2. **The PowerShell stamp writers broke the bash watchdog.** `streams.ps1`, `mark.ps1` and `every.ps1` wrote stamps with `Set-Content`, which ends them with CRLF. `watchdog.sh`, `streams.sh` and `every.sh` read those files with `$(cat ...)` into bash arithmetic, which fails on the trailing `\r`. Now they write LF only.
3. **The CLAUDE.md round trip nested itself.** `sync_check.ps1` copied the whole installed `~/.claude/CLAUDE.md`, markers and older content included, into `claude/CLAUDE.md`, and the next `install.ps1` wrapped it in markers again. Now only the text between the markers is synced back.
4. **sync.ps1 never pulled.** Any push from elsewhere made the push fail, and the error wrongly suggested `gh auth login`. It now runs `git pull --rebase --autostash` first and gives a plain message if that pull hits a conflict.
5. **The backup zip had no git history.** `Compress-Archive` skips hidden items, and `.git` is hidden on Windows. The script now uses the built-in `tar.exe -a` and falls back to Compress-Archive.
6. **Allowlist gaps.** `settings/allowlist.json` had no entries for `health.ps1`, `keep-awake.ps1`, `streams.ps1`, `mark.ps1`, `watchdog.ps1`, `every.ps1`, `sendkeys.ps1` or `cors_srv.py`, so an unattended run using any of them would freeze on a permission prompt. Added.

Reviewed, not changed, but risky until tested on Windows:
- **front.ps1** taps Alt before `SetForegroundWindow`. If Chrome is already in front, that Alt can focus Chrome's menu and swallow the next Ctrl+Tab. It also relies on the Trybe tab title containing "Trybe", which nobody has verified.
- **Background processes started from Claude's Bash tool** (the keep-awake loop and `cors_srv.py`, both started with `Start-Process` in `start.ps1`) may be killed when the tool call ends, if Claude Code on Windows runs commands in a job object. `health.ps1` would show it; the fix would be a Task Scheduler "run now" job.

### 5. "Stupid simple" walk-through: PASS after fixes

Walked through the README and FIRST-PROMPT as a non-technical person starting from a blank Windows PC. Well covered: opening and pasting into PowerShell, winget with a manual fallback, the clone path, the installer's prompts in order, the self-test and its fixes, the Chrome extension, Drive for desktop, power and lid settings, keep-awake, the timers, the watchdog, the helper server on 8765, keeping the Trybe tab in front, the cl= markers, permission prompts, the key, backups and push, start and end of shift checklists, troubleshooting by symptom, and the glossary.

Places where she would have got stuck, now fixed:
- No step for **accepting the GitHub invitation**. Without it the clone says "Repository not found". Added.
- **Google sign-in on a new PC** will ask Fatima's phone to approve it (2-Step Verification), which could come up at any hour. Added a heads-up to message Fatima first.
- Chrome said "Turn on sync" in her own profile, which would mix Fatima's Google account into the sister's personal Chrome. Changed to "Add a new profile".
- **Trybe sign-in:** no method was given. Added: use Fatima's Trybe sign-in method (Continue with Google if shown) and ask her before trying passwords.

Still open (a human has to fill these in): `fatimaarshadg-ux/bambora-creator-ops` in README step 3, and the exact button names in the Claude app's Connectors screen, which were written from memory.

### 6. Rules completeness: PASS after fix

`docs/02-rules.md` already covered: safety (10 to 50 lbs, one hand, the seat and M position, the buckle and safety loop), no sale-led videos, the sample gate, I not we, never naming other creators, the ignore list, the 10 protected creators, autonomy, samples only from 9/17 on, English-speaking countries, ownership (docs/README.md), and the $400 base retainer framing. Fixes:
- **Tasha Clay** was listed under "Who to ignore (never message them)" while the same line says to answer her normally. She is now a separate "settled, do not reopen" note, and the stale "any reply about numbers goes to Fatima" line in the money section is updated.
- **Acceptance criteria** were missing: the English-speaking hard requirement as a reject rule, the "talking to camera but small numbers" test (energy plus 3 to 4 real comments), the automatic reject rule, and "no extra DM after accepting, nothing to rejected applicants". Added.
- **Liam batches** and the **Meta access check** were in 01, 05 and 10 but not in the rules page. Added as sections 11 and 12.

### 7. Dashes: PASS

The builder-written files (every overlay file, including README, FIRST-PROMPT, OPERATOR, CLAUDE.md, docs, scripts and the new memory files) contain no em dashes, no en dashes used as connectors, no `--` as punctuation and no spaced hyphens in prose. The only hits are list bullets, command flags, PowerShell minus signs and the dash checker's own pattern. Text copied from Fatima's files is exempt and was left as it is.

### 8. Identity and one machine: PASS after fix

Messages go out as Fatima, in her voice, from her Trybe account. The sister signs in with fatima@bamboraco.com. Creators never hear about the handover. This is stated in CLAUDE.md, the operator-handover memory, OPERATOR.md and docs/README. **What was missing was the one-machine rule.** It appeared only as "don't run two chats". Added in plain words to the top of the README and the daily start step, CLAUDE.md (Claude will not start sweeps if Fatima's Mac is running them), OPERATOR.md, docs/README, docs/02-rules section 13, the start-of-shift checklist, FIRST-DAY and troubleshooting (what to do if both ran).

## Fixes made (one local commit)

1. `work/sweep/keep-awake.ps1`: UInt32 overflow fix (without it the PC was never actually kept awake).
2. `work/sweep/streams.ps1`, `mark.ps1`, `every.ps1`: LF-only stamps, so the bash watchdog can read them.
3. `work/backup/sync_check.ps1`: syncs only the block between the CLAUDE.md markers.
4. `sync.ps1`: `pull --rebase --autostash` before the push, with a plain message on conflict.
5. `work/backup/make_backup_zip.ps1`: `tar.exe` so the zip includes `.git`.
6. `settings/allowlist.json`: 8 missing entries.
7. `install.ps1`: self-test line for `.mcp.json` and the MCP server.
8. `README.md`: one-machine box, GitHub invitation step, Google 2-Step heads-up, a new Chrome profile instead of sync, the Trybe sign-in hint, and the one-machine check at the daily start.
9. `claude/CLAUDE.md`, `OPERATOR.md`, `docs/README.md`, `docs/10-shift-checklists.md`, `docs/FIRST-DAY.md`, `docs/08-troubleshooting.md`: the one-machine rule.
10. `docs/02-rules.md`: Tasha placement, full acceptance criteria, the Liam batch rule, the Meta access check, the one-machine section.
11. `skills/README.md`: copied from `~/.claude/skills`.

All of them were also copied into the build overlay (`scratchpad/overlay`), so `build.py` reproduces them.

## Needs a human decision

- **H1. One source of truth (the biggest one).** This repo is a new repo, separate from Fatima's `claude-setup`. Both are cloned at `~/claude-setup` on their machines. So the ledger (`followups.json`), memory, seen.txt and filed.json will drift apart the moment both machines are used. `start.ps1` and the docs even say "Fatima may have pushed", which only holds if they share one repo. Choose one: (a) Fatima stops running the routine on her Mac and this repo becomes the only live copy, or (b) both machines use one repo, which needs the Mac setup to accept this repo's Windows paths. Until then, whoever takes a shift has to start from the other person's latest ledger.
- **H2. One real test install on Windows** (a spare PC or a VM) before the sister's first day. Nothing here has ever run on Windows. Watch these in particular: the winget ids `Anthropic.Claude` and `Google.GoogleDrive`, `keep-awake` (check `powercfg /requests` shows it), `front.ps1`'s Alt tap and the "Trybe" title match, DPAPI from Python, whether processes started by `start.ps1` survive the tool call, the MCP server's transcription through the media watcher's Python, and `health.ps1` showing all OK.
- **H3. Claude account.** Does she use Fatima's account or her own? This decides whether she can reach the Creator Tracker Claude Doc and the connectors (Drive, Notion, Claude Docs, Atria). With her own account, the connector ids in `settings/allowlist.json` will be different, so those entries do nothing and she will get a permission prompt once per tool.
- **H4. Trybe API key.** Give her the existing key privately. Do not create a new one, because that can replace Fatima's.
- **H5. Google 2-Step Verification** on fatima@bamboraco.com: Fatima has to be reachable to approve the first sign-ins (Google, then maybe Slack and Notion). Consider adding the sister's phone as a second 2-Step method, or backup codes.
- **H6. README placeholders and details:** `fatimaarshadg-ux/bambora-creator-ops`, the sister's GitHub username, her hours and timezone (FIRST-PROMPT asks for these), and whether Liam knows someone else is covering.
- **H7. Scheduled tasks:** keep either the `bambora-end-of-day-wrapup` task or the session end-of-day timer, not both, or the wrap-up runs twice.
- **H8. Skills to keep:** Fatima's personal ad-writing skills (evolve-*, voc-miner, bot-forensics) and the dmca monitor are included. Keep them, or remove them for the sister?
- **H9. Commit identity:** commits are made as `operator@users.noreply.github.com`. That is harmless but anonymous; use her GitHub noreply address if you want her commits linked to her account.

# Second audit

Done 2026-09-25 on Fatima's Mac, with fresh eyes, by role-playing the operator through a first install, a full 5 PM to 5 AM shift and the usual breakages, using only what the repo says. Nothing was pushed and none of Fatima's own files were changed. Every fix is committed locally and copied into the build overlay (or added as a text port in `build.py`), and a rebuild after the fixes changed nothing.

**Verdict: READY TO PUSH and hand over, with one condition:** a real test install on a Windows PC (H2 below) before her first live shift. The content is complete, the account questions are settled by defaults, and every point where she would have had to guess now has a written answer.

## Step 0: data synced

`build.py` only copies sources into the repo, so it was run. The ledger `work/creator-db/followups.json` is byte-identical to `~/claude-setup/work/creator-db/followups.json` and holds tonight's items (Elizabeth Albee, Sandeep kaur, Kaitlyn Cunningham, Jaimie Kunkel, Madilynne Cantrell). Every live memory file is present (only `macos-drive-upload-technique.md` is replaced by its Windows version on purpose), including `feedback-take-ownership`, `creator-base-retainer-offer` and `routine-liam-batches-and-meta-access`. Committed as "Sync tonight's ledger and session log".

**Found while doing it:** the build overlay was behind the repo. Its `README.md` and `HANDOVER-BUILD-REPORT.md` still had the old `OWNER/REPO` placeholder and the "accept the invitation" step, so any rebuild would have undone the two commits that filled in the repo name. The overlay now matches the repo.

## What the role-play found, and what was fixed

### (a) First install on a blank Windows 11 PC
1. **Contradiction about accounts.** The "have these ready" table said she needs her own GitHub account and an invite, and "ask Fatima which Claude account"; Step 3 said to use Fatima's GitHub. Fixed: GitHub and Claude are both Fatima's (fatima@bamboraco.com), no invite, and her Claude use on the Mac shares the usage limit.
2. **Sign-in codes with no email open.** GitHub (Step 3) and Claude (Step 7) can email a code to fatima@bamboraco.com before Chrome exists. Added Step 2b: open Gmail in Microsoft Edge first.
3. **The PC could restart or lock mid-shift.** Nothing covered Windows Update restarts, the automatic lock, or Chrome's Memory Saver (which discards background tabs and wipes the helpers). A locked PC makes Chrome treat tabs as hidden, so Claude cannot click. Added to README Step 6b, FIRST-DAY and troubleshooting: update active hours 4 PM to 6 AM, "require sign-in" Never, Dynamic lock off, never Windows+L, Memory Saver and Energy Saver off.
4. **Permission mode was never mentioned.** Added: keep the normal "ask" mode, never bypass.
5. **Connectors:** with Fatima's Claude account they are probably connected already; the step now says "check each says connected".
6. **OPERATOR.md** asked for a GitHub username she doesn't have. Now prefilled with Fatima's hours, timezone, end-of-day time and accounts; only her first name is left to fill.

### (b) First full shift
7. **"Do I decide this, or does Fatima?"** had no single answer page. Added `docs/11-decision-guide.md`: the four rules, then 38 concrete cases (messages, samples, videos, applicants, partnership ads and Liam, money and programs, permissions), each marked Claude, You, Fatima or Nobody, all taken from memory and skills.
8. **Sending Liam's batch:** "copy it into Slack" had no steps. Added them (new Chrome window, not Claude's tabs; app.slack.com; Liam under Direct messages; paste; Enter), and that `liam_batch.py sent` already ran.
9. **5-hour Meta check and Done items:** she would not know what they look like in the summary. Added a note to the "during the shift" list.
10. **Samples rule contradiction in the routine itself:** `routines/live-sweep.md` (Fatima's text) still said "V3, US", while core-rules says any English-speaking country and that "US address" was a mistake. Fixed through a text port in `build.py`. Fatima's own Mac copy still has the old wording (not touched).
11. **Two end-of-day mechanisms** (H7). Decided: the session timer is the only one on the PC. Its prompt now covers everything the scheduled wrap-up did (Drive filing, Liam links, memory, session log, sync.ps1, repo zip to Drive, stop timer and watchdog). The scheduled task prompt carries a "not used on the Windows PC" note, docs/07 marks it "do NOT create on this PC", and FIRST-PROMPT no longer offers it.

### (c) Something breaks
12. Added troubleshooting sections for: PC restarted overnight (six steps back to running), screen locked, a Trybe tab closed, Chrome relaunch, discarded tabs, **a permission prompt mid-sweep** (what to allow, what to allow only after a yes, what to deny), the helper server down (with the port-in-use case), **unsure whether to approve** ("hold 2", "show me 2"), a Claude usage limit, Claude driving the wrong Chrome, Claude in Chrome not connected, and "Main Media" missing from Drive for desktop (add a shortcut from "Shared with me").
13. **Push failed** advice said `gh auth login` only; git uses its own credential helper, so it also needs `gh auth setup-git`, signed in as Fatima's GitHub. Fixed.
14. **start.ps1 pulled with a plain `git pull`**, which fails whenever the PC has unpushed commits or an edited ledger ("divergent branches"). Now `pull --rebase --autostash`, and it prints who pushed last, so a handoff from Fatima is visible.

### Skills on Windows (step 2)
15. `trybe-applicant-review` ran `~/claude-setup/work/social-tools/tt.py` by its bare path. On Windows the `#!/usr/bin/env python3` line can land on the Microsoft Store alias. Now `py -3 ...` (text port), and CLAUDE.md says to always run `.py` files with `py -3`.
16. **Same Claude account, two Chromes.** Claude in Chrome can list several connected browsers on one account, so Claude on the PC could drive Fatima's Mac Chrome. CLAUDE.md and FIRST-PROMPT now make Claude list the connected browsers and select the Windows one; troubleshooting covers it.
17. Allowlist gaps: the browser selection tools, the Drive `update_file` rename used after every filing, and the applicant review scripts (run by background agents, which would otherwise stop on a prompt). Added.
18. Checked and fine as written: creator-ops-daily (every command is `py -3` or a PowerShell port; Drive filing goes through drive-upload.ps1), trybe-portal, human-messages (`py -3 lint_message.py`), fatima-creator-voice (text only), media-watcher (`~/claude-media-watcher/watch` finds `.venv/Scripts/python.exe` from Git Bash; `watch.cmd` for PowerShell), `tt.py`/`tt_find.py` (standard library plus `yt-dlp` on the PATH), the applicant scripts (`ffmpeg` on the PATH; Pillow, numpy and faster-whisper installed for `py -3` by install.ps1; `PYTHONUTF8=1` covers their plain `open()` calls), `fetch_media.py` (`ffprobe`, `ffmpeg`, Pillow). The scheduled wrap-up prompt pointed at a `NEW-MACHINE.md` the repo does not have; it now points at `docs/05-where-everything-lives.md`.

### Sync with Fatima (H1, step 3)
19. **Decided and documented** in `docs/12-sync-with-fatima.md`: this repo is the one live copy of the shift data from handover day. Fatima's `claude-setup` keeps the Mac versions of skills and scripts. Only data moves between them, with a new script for her Mac, `work/backup/handoff-mac.sh take|give|diff` (ledger, creator database, seen lists, filing and Liam records, session logs, applicant verdict notes, voice lessons). One machine at a time, with a written handoff in both directions; new rules travel through the session logs. The script was tested end to end on throwaway clones (give, push, take) and changes nothing unless run on her Mac.

## "Needs a human" list from the first audit: where each stands

| # | Default chosen and documented | Still needs a human? |
|---|---|---|
| H1 one source of truth | This repo is the live copy; handoff script for the Mac (docs/12) | Fatima clones the repo on her Mac once (`git clone ... ~/bambora-creator-ops`) |
| H2 real Windows test | none possible | **Yes.** One install on a spare PC or VM before the first shift (list of things to watch is in the first audit) |
| H3 Claude account | Fatima's account; shared usage limit and the two-Chrome risk are handled in the docs | no |
| H4 Trybe key | Fatima gives the existing key privately; never a new one | Fatima sends it |
| H5 Google 2-Step | Fatima reachable for the first sign-ins; Gmail open in Edge for codes | Optional: add the sister's phone as a second 2-Step method (Fatima's choice) |
| H6 placeholders | repo name, accounts and hours filled in; Liam gets messages as Fatima, like everything else | only her first name, at first run |
| H7 end of day | session timer only | no |
| H8 personal ad skills | keep: they only trigger on ad-writing requests and cost nothing | no |
| H9 commit identity | keep her first name with the noreply email, so Fatima can tell whose commits are whose | no |

## Checks re-run
- **Secrets:** the real Trybe key (read from the Keychain, never printed) has 0 hits in the tree and in the full history; the token and key pattern scan finds only the scanner patterns themselves; no credential files are tracked.
- **Dashes:** every line added in this audit was checked for em dashes, en dash connectors, `--` as punctuation and spaced hyphens. The only hits are git's `--` pathspec separator in `handoff-mac.sh` (command syntax) and list bullets.

## Still open
- **H2, the Windows test install.** Nothing has run on Windows yet. Beyond the first audit's list, also check: that the Claude app's permission prompt wording matches troubleshooting's description, that a locked screen really stops clicks (written from how Chrome treats a locked session, not tested), and that Claude in Chrome shows both browsers when Fatima's Mac is connected too.
- **Fatima's own Mac files** still say "V3, US" for samples (`~/claude-setup/routines/live-sweep.md`). Only the handover copy was fixed.
- **Exact button names** in the Claude app (Connectors, permission modes, Claude in Chrome) are still written from memory.
- The first audit's risks for `front.ps1` (the Alt tap, the "Trybe" title match) and for background processes started by `start.ps1` stay open until H2.
