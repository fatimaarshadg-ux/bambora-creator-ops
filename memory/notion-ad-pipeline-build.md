---
name: notion-ad-pipeline-build
description: "How the Bambora Notion \"Ad Pipeline\" briefs database and its monthly master are wired (template, automation) and the tricks needed to edit them"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1174535f-0b9e-4b56-a78f-afc304c09e52
  modified: 2026-09-20T22:29:32.665Z
---

Two databases under Bambora - Central Operating Hub / Systems / 🎨 Creative Engine:

- **Ad Pipeline** (live): `collection://f1b45d16-5407-8233-bc2c-07f5924165c7`, title column "Brief", formula "Ad Name". Default template `a0b45d1654078387873681485c3819e8`.
- **Replicate this every month** (master): `collection://85545d16-5407-8389-85cd-07059ed8c09f`, database page `eb945d1654078334be48811e94aebae3`. OLDER schema: title column "Concept", formula "Concept Code"/"Seq", Status is a select with different options, Editor is a select, and it lacks Details/Desire/Learnings/Kill-Keep/Winner-Loser and the Learnings view. Default template `65145d16540782f888b9015e18246e15`. Schema drift vs live was flagged to Fatima on 2026-09-21, not fixed (not requested).

State as of 2026-09-21 (manager's request, applied to BOTH):
- Template titled "Brief Here"; body = ⚠️IMPORTANT⚠️ line → safe-zones paragraph → 2-column safe-zone images (Notion-hosted, file ids 12d15966… and 912979c2…) → "INSPO VIDEO:" h3 → empty video embed.
- Single automation per DB ("Fatima G's automation"): When page added → Set title to formula `"Brief Here"` (was `Trigger page.Ad Name` / `Trigger page.Concept Code`). Ad Name / Concept Code formula columns untouched.
- Title column tooltip updated via `ALTER COLUMN "X" SET TITLE COMMENT '...'` (works). Formula-column tooltips still mention "feeds the automation that titles the page"; left alone to avoid touching formulas.

**How to apply:**
- Automations are invisible to the Notion connector, so use Claude in Chrome ([[feedback_use_chrome_extension_for_logged_in_sites]]), ⚡ icon in the view toolbar.
- The connector cannot write Notion-hosted images (signed or unsigned S3 URLs become empty image blocks). To copy blocks with uploaded images between pages: in Chrome click into the first block, Shift+Down until the selection spans the blocks, dispatch a synthetic `ClipboardEvent('copy')` with a `DataTransfer`, stash the payload in sessionStorage, then on the target page select a placeholder text and dispatch a synthetic `paste`. System clipboard (cmd+c/v) does not work from the background tab. The first/last text blocks come through partial, so fix them afterwards with connector `update_content`.
- The Chrome tab's DOM can be STALE after connector edits. Never do keyboard merges based on it; reload and verify with a connector fetch. (A stale "empty" block caused a doubled IMPORTANT line once.)
- Take a screenshot right before coordinate clicks; Notion shifts scroll after load.
- Page URLs need the `/p/<id>` form in the browser. Test rows: create via "+ New page", verify, then ⋯ → Move to Trash.
- Fatima does not review this work, so verify end-to-end and leave no placeholders/test rows. See [[feedback-no-review-leave-nothing-behind]].
- The manager reviews this build via screen recordings; pull frames with ffmpeg + whisper-cli (model at ~/whisper-models/ggml-base.en.bin).
