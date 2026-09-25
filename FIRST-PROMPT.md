# First prompt

Copy everything inside the box below and paste it into Claude (Claude app, **Code** tab, folder `C:\Users\<you>\Bombara`). Use it once, right after `install.ps1` finished. You can paste it again any time something seems off; it only checks and fixes.

```
Hi Claude. I'm taking over Fatima's Bambora creator-ops job on this Windows PC. Everything you need is in my repo at ~/claude-setup (installed with install.ps1). Please get fully set up before we do any real work:

1. Read, in this order: ~/claude-setup/OPERATOR.md, ~/.claude/CLAUDE.md, your memory index MEMORY.md and the memory files operator-handover, windows-machine, core-rules and open-work (the newest "open-work" file), then ~/claude-setup/docs/README.md, docs/01-how-the-job-works.md, docs/02-rules.md, routines/START.md and routines/full-run.md, and the skills creator-ops-daily, trybe-portal, trybe-applicant-review, fatima-creator-voice (with lessons.md), human-messages and media-watcher.

2. Verify the install and fix anything small yourself (tell me what you fixed). Check each and give me a PASS/FAIL list:
   - py -3 works; py -3 ~/claude-setup/work/creator-db/followups.py due runs and prints the ledger
   - py -3 ~/claude-setup/work/trybe-chat/lint_message.py "awesome!! thank you" prints ok
   - py -3 ~/claude-setup/work/common/trybe_key.py --check says the key works (never print the key; if it is missing, tell me to run work/common/store-trybe-key.ps1, do NOT ask me to paste it here)
   - ffmpeg, ffprobe and yt-dlp run; ~/claude-media-watcher/watch exists and the media-watcher skill is loaded
   - your memory folder is the one install.ps1 made (see ~/claude-setup/.project-slug) and MEMORY.md is loaded in this session; if not, find the right folder under ~/.claude/projects and copy the memory there
   - bash ~/claude-setup/work/sweep/streams.sh status and the PowerShell start.ps1 both run
   - the Trybe MCP server (tools named mcp__trybe__*) is available; if not, tell me what to click
   - Claude in Chrome can see my Chrome (list the tabs) and the Trybe brand portal opens logged in; Google Drive, Notion, Claude Docs (the Bambora Creator Tracker) and Atria connectors answer
   - git -C ~/claude-setup status is clean or explainable, and git can push (dry run is fine)

3. If OPERATOR.md still has <placeholders>, ask me for my name, work hours, timezone, end-of-day time and GitHub username in ONE message, then fill it in.

4. Tell me in plain words: what the job is, what you will do on your own, and what will always wait for my yes. Then list anything still missing that only I can do (sign-ins, connectors, permissions), each as one simple instruction.

5. Offer to create the scheduled tasks from ~/claude-setup/docs/07-scheduled-tasks.md with times in my timezone, and wait for my yes before creating them.

6. Run sync.ps1 to push the filled-in OPERATOR.md. Then say "ready" and tell me that each work day I just type: start the routines

Do not message any creator, approve, reject or accept anything during this setup.
```
