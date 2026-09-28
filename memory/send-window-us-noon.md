---
name: send-window-us-noon
description: Creator messages only go out from 12 PM US Eastern (9 PM PKT); before that, review and draft only
metadata:
  type: feedback
---

No creator messages before 12 PM US Eastern (21:00 in Pakistan; check the US time, not this PC's clock) (Fatima, 2026-09-27, after quiet check-ins went out at ~7 AM ET: "it's pretty early in the US right now"). Before that time every sweep only reads, reviews and drafts into `work/send-queue/<date>.md`; at 12 PM ET send the queue, then normal sending until her day ends.

**Why:** messages landing at 6 or 7 AM US time feel off and get buried.
**How to apply:** check `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/common/us-time.ps1"` before any send. If it's before 12:00, queue it. Accepts, approvals and rejections follow the same window since they notify the creator. Related: [[core-rules]].
