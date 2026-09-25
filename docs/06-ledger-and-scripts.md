# The ledger and the scripts

## The follow-up ledger (the memory of everything owed)

One file holds every promise, check-in and nudge owed to a creator: `work/creator-db/followups.json`, managed with `followups.py`. Fatima chose a single ledger on 2026-09-23 after three separate lists drifted apart. **If it is not in the ledger, it will be forgotten.** Claude runs `due` at the start of every sweep and sends every due item in that same sweep.

```bash
py -3 ~/claude-setup/work/creator-db/followups.py due                        # open items due today or earlier
py -3 ~/claude-setup/work/creator-db/followups.py list                       # every open item, soonest first
py -3 ~/claude-setup/work/creator-db/followups.py add "Kat Chandler" partnership_nudge +3d "PA requested 9/25, nudge if still pending"
py -3 ~/claude-setup/work/creator-db/followups.py done "Kat Chandler" partnership_nudge "nudged 9/28"
py -3 ~/claude-setup/work/creator-db/followups.py snooze "Kat Chandler" partnership_nudge +1d
```

Due dates are `YYYY-MM-DD` or `+Nd` (N days from today). A creator can have one open item per type.

### Item types and when they are added

| Type | Added when | Due |
|---|---|---|
| `sample_nudge` | a creator is accepted and has no sample request yet | +1 day (20h rule) |
| `sample_checkin` | a sample is approved | +14 days |
| `inspo_checkin` | inspo is sent | +3 days if they have the sling, +7 if not |
| `inspo_reply` | inspo sent and no reply yet | +2 days |
| `applicant_followup` | we asked an applicant for a talking video, socials or English content | +1 day |
| `applicant_final` | an applicant still hasn't answered | the day to decide reject or hold |
| `quiet_checkin` | added automatically by `quiet_creators.py`: no video in 14+ days (and joined 14+ days ago) | today |
| `connect_ig` | asked a creator to connect a public Instagram for partnership ads | +2 days |
| `partnership_nudge` | partnership ads requested | +3 days |
| `promise` | something Fatima (now you) promised ("I'll put ideas together", Discord invite) | the date given |
| `reply_owed` | a creator asked something only you or Fatima can answer | today |
| `retake_check` | a revision was requested | when the re-take is expected |
| `note` | anything else worth remembering about a creator | when it matters |

At the time of the handover (2026-09-25) the ledger held **174 open items** (57 sample check-ins, 36 partnership nudges, 16 sample nudges, 15 connect-Instagram asks, 10 replies owed, and more). `followups.py list` shows them all.

### The tracker doc

The **Bambora Creator Tracker** (a Claude Doc) is the human-readable view: Due next, Waiting on applicants, New creators, Promises, Creator profiles. The routines rebuild it from the ledger; nobody edits two lists by hand. People's edits in the doc win.

## The creator database

`work/creator-db/` holds one profile per V3 creator plus the 10 protected ones (94 creators and 242 videos on the first build):
- `db/profiles/<slug>.md`: API facts (rebuilt daily) and `## Notes` (style, DMs so far, inspo that fits her, comments), which is kept across rebuilds. How to fill it: `REVIEW-GUIDE.md`.
- `db/dms/<slug>.md`: DM summary, sample history, full thread.
- `db/media/<slug>/<id>.jpg`: a 6-frame sheet per video.
- `build_db.py` (daily, first sweep): refreshes from the API, then runs `quiet_creators.py`. Warns if a protected creator goes missing.
- `fetch_media.py`: frame sheets for new videos only.

## Every script, what it does, how to run it

All from Git Bash (Claude's shell). PowerShell ones are run as `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/<path>" <args>`.

| Script | What it does | Run |
|---|---|---|
| `work/creator-db/followups.py` | The ledger | see above |
| `work/creator-db/build_db.py` | Refresh the creator database from the Trybe API | `py -3 ~/claude-setup/work/creator-db/build_db.py` |
| `work/creator-db/fetch_media.py` | Frame sheets for new videos | `py -3 ~/claude-setup/work/creator-db/fetch_media.py` |
| `work/creator-db/quiet_creators.py` | Adds quiet creators to the ledger (build_db runs it) | `py -3 ~/claude-setup/work/creator-db/quiet_creators.py` |
| `work/trybe-chat/lint_message.py` | Blocks robotic messages. Exit 1 = rewrite | `py -3 ~/claude-setup/work/trybe-chat/lint_message.py "text"` (or `--file drafts.json`, `--long` for inspo) |
| `work/trybe-chat/cors_srv.py` | Helper server on 127.0.0.1:8765 | started by start.ps1 |
| `work/trybe-chat/chat-helpers.js` | In the Trybe chat page: `convoScan()` (who is waiting), `g2(name)` (guarded open and send; refuses while their newest message is unanswered until `ACK[name]=true`), `qCheck()` (unanswered questions), `open2()`, reactions `rx1()`/`rx2()`, `dFill` (refuses robotic text) | loaded in the page from :8765 |
| `work/trybe-chat/roster-scan.js` | In the Creators page: `badges()`, `collectSamples()`, `rosterScan()` (canRequest, noConnect, pendingPA, noSample), `rosterProps()`, `inboxNames()` | loaded in the page |
| `work/trybe-chat/sample-status.js` | The SAMPLE GATE: `await sampleStatus(['Name'])` in the Samples tab | loaded in the page |
| `work/trybe-chat/front.ps1` | Bring Chrome and the Trybe tab to the front | before any click or send |
| `work/trybe-applicant-review/new_applicants.py` | Which Inbox names are new (not in seen.txt); `--add` records them | `py -3 ... new_applicants.py "Name A" "Name B" --add` |
| `skills/trybe-applicant-review/scripts/*.py` | yap.py (transcribe applicant videos), sheet.py (contact sheets), energy.py (pace, loudness), cscore.py (real comments), taste_metrics.py | paths at the top of each; see the skill |
| `work/social-tools/tt.py` | TikTok creator stats, comments, download (no browser) | `py -3 ~/claude-setup/work/social-tools/tt.py <handle> --videos 6 --comments 15 [--download DIR]` |
| `work/social-tools/tt_find.py` | Find TikTok videos by topic, ranked by views | `py -3 ... tt_find.py "clingy baby" --shop --min-views 100000 --seen ~/claude-setup/work/inspo/seen.txt` |
| `work/trybe-drive-filing/file_approved.py` | Approved videos not yet in Drive: `--list`, `--download DIR`, `--mark IDS`, `--seed` | `py -3 ... file_approved.py --list` |
| `work/trybe-drive-filing/liam_batch.py` | Liam batches: `status`, `message [--any]`, `sent` | `py -3 ... liam_batch.py status` |
| `work/trybe-drive-filing/drive-upload.ps1` | Copy files into a Drive folder via Google Drive for desktop | `-Source <folder> -Target Trybe` |
| `work/trybe-drive-filing/sendkeys.ps1` | Real keystrokes for Drive's upload menu and file dialogs (fallback) | `-Keys "{DOWN}{DOWN}{ENTER}"` |
| `work/sweep/start.ps1` | Start of shift: keep-awake, helper server, pull, ledger, stream ages | no args |
| `work/sweep/keep-awake.ps1` | Keep the PC awake: `start`, `status`, `stop` | |
| `work/sweep/health.ps1` | One-glance check of every background piece | no args |
| `work/sweep/streams.sh` / `.ps1` | Per-stream stamps: `done <streams>`, `status`, `stale 60` | `bash ~/claude-setup/work/sweep/streams.sh done chat` |
| `work/sweep/mark.sh` / `.ps1` | Record that a sweep finished | `bash ~/claude-setup/work/sweep/mark.sh` |
| `work/sweep/watchdog.sh` / `.ps1` | Wake Claude when a sweep or stream is late | `bash ~/claude-setup/work/sweep/watchdog.sh 30 60` (background) |
| `work/sweep/every.sh` / `.ps1` | Timed extras: `due metaaccess 300`, `done metaaccess` | |
| `work/backup/sync_check.ps1` | Copy skills, memory, CLAUDE.md, task prompts from this PC into the repo | sync.ps1 runs it |
| `work/backup/make_backup_zip.ps1` | Zip the repo for the Drive backup | end of day |
| `work/backup/handoff-mac.sh` | Swap the shift data (ledger, seen lists, filing and Liam records, logs) between this repo and Fatima's `claude-setup` | on **Fatima's Mac** only, at each handoff (`12-sync-with-fatima.md`) |
| `work/common/trybe_key.py` | Load the Trybe key (`--check` to test) | `py -3 ... trybe_key.py --check` |
| `work/common/store-trybe-key.ps1` | Store or replace the Trybe key (masked box) | `-Force` to replace |
| `sync.ps1` | Push to GitHub (with a secret check) | `-Message "what changed"` |
| `install.ps1` | Install or repair everything | `-Refresh` to overwrite changed skills and memory |
| `settings/apply-settings.ps1` | Add the permission allowlist and no-dash hooks | rerun when allowlist.json changes |
| `~/claude-media-watcher/watch` | Watch a video or link: frames plus transcript | `~/claude-media-watcher/watch "<file or link>"` |

## The Trybe MCP server

`~/Bombara/trybe-review/mcp-server/server.js` (from `~/Bombara/.mcp.json`) gives Claude tools named `mcp__trybe__*`: list and get submissions, creator performance, download a video, extract frames, transcribe, and approve, reject or request revision. It reads the same DPAPI key. The review actions **dropped the comment once**, so for reject and revision Claude calls the API directly with `{"comment": "..."}` and checks `review_comment` in the answer.
