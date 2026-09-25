---
name: feedback-never-overwrite-repo-memory-index
description: When syncing to claude-setup, append or edit lines in memory/MEMORY.md; never copy the Mac's MEMORY.md over it (the PC has entries the Mac doesn't)
metadata:
  type: feedback
---

When syncing memory to ~/claude-setup, never `cp` the Mac's MEMORY.md over `memory/MEMORY.md`. Append new lines, or edit specific lines in place, and check `git diff` for removed lines before committing.

**Why:** on 2026-09-23 a blanket copy silently dropped two PC-only index lines (Claude media watcher, Ads Library DMCA monitor). The two machines' indexes differ. Caught and restored in the next commit.

**How to apply:** memory *files* can be copied individually. The index gets line-level edits only.
