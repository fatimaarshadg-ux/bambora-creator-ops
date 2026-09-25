---
name: feedback-no-review-leave-nothing-behind
description: "Fatima doesn't review changes to shared team tools: finish 100%, verify end-to-end, leave no placeholders, notes-to-self or test artifacts"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1174535f-0b9e-4b56-a78f-afc304c09e52
  modified: 2026-09-20T22:29:38.228Z
---

When changing shared workspaces (Notion, etc.), Fatima will not review the result, and her manager/team see it directly. Work must be fully done and self-verified: no "delete me later" notes, no messages addressed to her inside the workspace, no placeholder text, no leftover test rows, no stale descriptions contradicting the change.

**Why:** Said explicitly on 2026-09-21 after the Notion Ad Pipeline change, because she passes work straight to her manager and wants zero handholding.

**How to apply:** After any such change, run a sweep: search for placeholder strings, verify on the server (not just the browser DOM), test the real user flow, trash test artifacts, and fix adjacent stale text. Report honestly in chat what was done and any mistakes caught. Just never leave loose ends in the workspace itself. Related: [[notion-ad-pipeline-build]].
