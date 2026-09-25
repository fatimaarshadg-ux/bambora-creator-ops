---
name: bambora-trybe-submission-review
description: "Fatima is exploring a Claude Code skill/plugin to review UGC submissions from Trybe against Bambora's correct/wrong-way usage guidance"
metadata: 
  node_type: memory
  type: project
  originSessionId: 75f786eb-1c63-4035-b9ff-b5c8fb190005
  modified: 2026-09-20T13:49:11.970Z
---

Fatima (fatima@bamboraco.com, Bambora) wants a Claude Code skill/plugin that reviews creator UGC submissions coming through Trybe (jointrybe.com) against her "correct way vs wrong way to use the product" guidance (originally going to be shown to Claude via a video, not yet reviewed since there's no video-playback tool available locally).

Trybe turned out to have a Brand API (see [[trybe-brand-api]]), not just a dashboard, which makes an API-driven skill viable instead of pure browser-automation-only.

**Visual review IS possible as of 2026-09-20**: ffmpeg is now installed (winget Gyan.FFmpeg, on PATH), so the earlier "no video-watching capability" limitation is resolved. Working recipe: fetch the submission by id for a fresh `asset.url` (they expire ~20 min), download the .mov, `ffprobe` for dimensions/rotation/duration (covers checklist point 5; all Bambora submissions so far are 9:16 1080p+), then `ffmpeg -vf "fps=1/2,scale=540:-2"` for frames every 2s and Read them. Crop-and-zoom (`crop=w:h:x:y,scale=800:-2`) for buckle/seat close-ups where checklist points 1 and 3 need detail.

**How to apply:** transcript + metadata (`creator_comment`, `angles`, `products`) still frame the verbal review, but frames now carry checklist points 1–4 and 6. Two honest caveats to state in any report: 2s sampling can miss a brief hands-off lapse (point 2 findings are "at least this bad", not exhaustive), and the safety loop (point 3) is often obscured by the wearer's arm in every frame. Treat `approve`/`reject`/`request-revision` API calls as consequential actions (see [[trybe-brand-api]]) requiring per-action confirmation, not something the skill should auto-fire.

**API gotchas:** list-submissions filters are `program_id` (not `program`) and the forward cursor is `after` (not `cursor`). `POST /approve` needs an explicit empty JSON body (`-Body "{}"` with `-ContentType application/json`) or it 400s on "Malformed JSON". `program_id` filters by the program the submission was *pinned to at upload*, which is NOT the same as the creator's current enrollment. To find "all submissions from people in program X", enumerate creators, check each one's `programs[]`, then query by `creator_id`.
