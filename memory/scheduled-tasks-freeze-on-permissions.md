---
name: scheduled-tasks-freeze-on-permissions
description: Scheduled task runs freeze on any permission prompt and block every later run; keep the allowlist covering every command a task uses, and check runs daily
metadata:
  type: feedback
---

On 2026-09-23 the 2-hourly and 4-hourly Bambora tasks both started (03:12 and 03:47) and froze seconds in, each waiting on a Bash permission prompt in its own session. While a run sits in "running", no later run fires, so a single prompt silently stopped the whole routine until morning.

**Why:** unattended runs can't answer prompts. Any command a task prompt uses that isn't on the allowlist stops everything.

**How to apply:**
- Whenever a task prompt gains a new command or tool, add it to `~/claude-setup/settings/allowlist.json` in the same change and ask Fatima to run `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/settings/apply-settings.ps1"` (Claude can't change its own permissions).
- At the start of each session, run `list_task_runs` for each Bambora task. A run still "running" long after it started means it's frozen: read it with `list_events`, stop it with `stop_session`, and fix the allowlist gap.
- 2026-09-23 14:13 UTC: it happened again. Each task fired twice (four runs), and all four froze on their first Bash call, a chained `cd ... && for f in ...; do cat` read. Fix: every task prompt now carries a TOOL RULES block (one simple command per Bash call, no cd, &&, loops or pipes; `git -C`; Trybe via MCP tools), and `Bash(git -C ~/claude-setup *)` plus Read rules for ~/.claude and ~/claude-setup were added to allowlist.json. Fatima still needs to run apply-settings.ps1.
Related: [[creator-response-cadence]], [[creator-database]]
- **Real root cause (found 2026-09-23 20:45 PKT):** the 20:12 run froze on a plain `cat` of absolute paths, which IS allowlisted. Reads outside the task's working folder (~/Bombara) prompt no matter what the Bash rules say. Fix: `permissions.additionalDirectories` = ~/.claude and ~/claude-setup, kept in ~/claude-setup/settings/additional-dirs.json and applied by apply-settings.ps1. If a new routine reads another folder, add it there.
