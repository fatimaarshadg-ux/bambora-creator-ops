# Where everything lives

Add any new tool, folder or cloud location here the day it appears (Claude does this as part of the end-of-day wrap-up).

## On this PC

| What | Path |
|---|---|
| This repo (skills, memory, routines, scripts, ledger, creator database, logs) | `C:\Users\<you>\claude-setup` |
| Working folder Claude Code opens (brief, checklist, Trybe data, Trybe MCP server) | `C:\Users\<you>\Bombara` (spelled "Bombara" on purpose to match every note; the brand is **Bambora**) |
| Claude's installed skills | `C:\Users\<you>\.claude\skills\` |
| Claude's memory for this folder | `C:\Users\<you>\.claude\projects\<PROJECT>\memory\` (`<PROJECT>` is in `claude-setup\.project-slug`, for example `C--Users-Sara-Bombara`) |
| Claude's global instructions | `C:\Users\<you>\.claude\CLAUDE.md` (source: `claude-setup\claude\CLAUDE.md`) |
| Claude's settings (permissions, hooks) | `C:\Users\<you>\.claude\settings.json` |
| Trybe API key (encrypted) | `C:\Users\<you>\.claude\secrets\trybe_api_key.dpapi` |
| Media watcher | `C:\Users\<you>\claude-media-watcher` |
| Google Drive (via Drive for desktop) | `G:\My Drive`, `G:\Shared drives` |

**How Claude Code names the memory folder:** it takes the full path of the folder you open (`C:\Users\Sara\Bombara`) and turns every character that is not a letter or digit into `-`: `C--Users-Sara-Bombara`. That is why you must always open the same folder: a different folder means a different (empty) memory.

## Inside the repo

| Path | What |
|---|---|
| `routines/` | START.md (start of shift), full-run.md (every sweep), live-sweep.md (the sweep prompt), README.md |
| `skills/` | creator-ops-daily, trybe-portal, trybe-applicant-review, fatima-creator-voice, human-messages, media-watcher, no-em-dashes, think-before-grinding, plus Fatima's ad-writing skills (evolve-*, voc-miner, bot-forensics) |
| `memory/` | every rule and fact (MEMORY.md is the index) |
| `scheduled-tasks/` | prompts for the scheduled tasks |
| `work/creator-db/` | the follow-up ledger (`followups.py`, `followups.json`), the creator database (`db/profiles`, `db/dms`, `db/media`, `db/creators.json`), `build_db.py`, `fetch_media.py`, `quiet_creators.py` |
| `work/trybe-chat/` | browser helpers (`chat-helpers.js`, `roster-scan.js`, `sample-status.js`), `lint_message.py`, `cors_srv.py`, `front.ps1` |
| `work/trybe-applicant-review/` | `seen.txt` (every applicant name already reviewed), dated verdict files, `new_applicants.py`, the taste profile |
| `work/trybe-drive-filing/` | `file_approved.py`, `filed.json`, `liam_batch.py`, `liam-sent.json`, `liam-links-<date>.md`, `drive-upload.ps1`, `sendkeys.ps1` |
| `work/inspo/` | `seen.txt` (no repeats), `example-videos-map.md` (which anonymous Video 1 to 7 is whose), `authority-creators-*.md`, tag rules, dated packs |
| `work/social-tools/` | `tt.py` (TikTok creator check), `tt_find.py` (find TikTok videos by topic) |
| `work/sweep/` | `start.ps1`, `keep-awake.ps1`, `health.ps1`, `streams.sh/.ps1`, `mark.sh/.ps1`, `watchdog.sh/.ps1`, `every.sh/.ps1` |
| `work/session-logs/` | one log per work day |
| `work/trybe-5pct-migration/` | the September 2026 move of creators to the 5% program (who was messaged, who moved) |
| `work/trybe-grandparent-program/` | the Grandparents Program setup and welcome text |
| `work/bombara-folder/` | the source of `C:\Users\<you>\Bombara` |
| `work/backup/` | `sync_check.ps1`, `make_backup_zip.ps1`, `handoff-mac.sh` (Fatima's Mac only) |
| `work/common/` | `trybe_key.py`, `store-trybe-key.ps1` |
| `tools/claude-media-watcher/` | the media watcher, vendored |
| `docs/` | this manual |

## Google Drive (signed in as fatima@bamboraco.com)

| Folder | Id | What goes there |
|---|---|---|
| **Main Media > Trybe** | `1kleoyEuzTGxftUvYKwSK3aVUDTKkG53R` | ONLY approved Trybe submissions. The media buyers' drive. |
| **My Drive > Bambora Inspo** | `1HleYAep0n7C5gFGt3RhRsgy0dmiQEb8Y` | Weekly inspo packs (`Week of YYYY-MM-DD` subfolders, link-shared) and anonymous example videos. Never Main Media. |
| **Bambora Creator Brief** | `1QRX-mhJiKirwNOznaYGOwC8Fqo7BsI3_` | The 15 top-performer videos used in the brief |
| **Claude Backup / Bambora top-performers** | `1Hy_RKKus0SL17j19oSqllq__6PGgDNYW` | Backup of the same 15 videos |
| **Claude Backup / Repo snapshots** | `1FHhB0_QemdOFsdAMr2j7tLBDRYaBF5Yx` | Nightly zip of the repo, newest 7 kept |

**Approved video naming:** `CreatorFullNameNoSpaces/fatima/trybe=<8-char id>`, for example `BrittanyArchutowski/fatima/trybe=6c916aab`. The 8-char id is the last 8 characters of the submission id. The "fatima" part is the buyers' convention; keep it. Windows cannot put "/" in a file name, so files are copied as `BrittanyArchutowski__fatima__trybe=6c916aab.mp4` and renamed in Drive afterwards.

**Filing steps** (Claude does these right after each approval):
1. `py -3 ~/claude-setup/work/trybe-drive-filing/file_approved.py --list` (what is approved but not filed)
2. `--download ~/Downloads/trybe-filing-YYYY-MM-DD` (Windows-safe names plus `manifest.json`)
3. `drive-upload.ps1 -Source <that folder> -Target Trybe` (Google Drive for desktop)
4. Drive connector: `search_files` in the Trybe folder, `update_file` to rename each to its `drive_name`
5. `file_approved.py --mark <ids>`, then delete the download folder
6. Add the line to `liam-links-<date>.md`, then `liam_batch.py status`

Fatima's Google Docs "Bambora_Trybe_DM_History" and "Tasks for Trybe Management" are **not** for Claude to use.

## Liam links

Liam is the media buyer; he puts approved videos into Meta ads. He gets the individual Drive links:
- **Batches:** when `liam_batch.py status` says READY (5+ unsent), Claude gives you: "Now you can send this to Liam:" plus "hey Liam, here are N more videos you can add to Meta:" and one line per video (creator, id, link). You paste it to Liam in Slack. Then Claude runs `liam_batch.py sent`.
- **End of day:** whatever is left (`liam_batch.py message --any`).
- Never resend a video he already got (`liam-sent.json` remembers).

## Other places

| What | Where |
|---|---|
| **Bambora Creator Tracker** (the human-readable view: Due next, applicants, new creators, promises, Creator profiles tab) | Claude Doc https://claude.ai/code/artifact/3db72f36-d656-451e-8ddb-ec6f39609238 (needs the Claude Docs connector and access from Fatima's Claude account) |
| Filming checklist (public, send to creators) | https://bamborachecklist.netlify.app/ |
| How-to-use tutorial | https://bamboraco.com/pages/how-to-use |
| Atria (ad library, inspo) | connector `https://api.tryatria.com/mcp`; board "Bambora Creator Inspo" (id `6252eeab-7896-45f8-9dbf-78b60cb6d240`); 46 of 50 followed-brand slots used |
| Notion | Ad pipeline pages (memory `notion-ad-pipeline-build`) |
| Slack | Liam and the team; read in Chrome |
| Media watcher (public) | https://github.com/fatimaarshadg-ux/claude-media-watcher |
| Brave web search (optional, for finding TikTok/IG/YouTube links) | Claude app MCP server `brave-search` with your own Brave API key (never in the repo) |
