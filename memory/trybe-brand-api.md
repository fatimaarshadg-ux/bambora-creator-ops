---
name: trybe-brand-api
description: Trybe Brand API reference: endpoints for listing/getting/reviewing creator UGC submissions
metadata: 
  node_type: memory
  type: reference
  originSessionId: 75f786eb-1c63-4035-b9ff-b5c8fb190005
  modified: 2026-09-16T00:53:38.711Z
---

Trybe (jointrybe.com) has a Brand API, documented at https://jointrybe.com/help/api-reference (bearer-token auth). Relevant to reviewing creator submissions:

- `GET /v1/submissions`: list submissions with filters (status, creator, group, program, product, angle, transcript language).
- `GET /v1/submissions/{id}`: fetch one submission. Response includes `transcript.text`, `creator_comment`, `review_comment`, `angles` (AI-tagged with confidence), `products`, and `asset.url`, a short-lived signed Cloudflare R2 URL to the raw media file (`expires_at` ~20 min out).
- `POST /v1/submissions/{id}/approve|reject|request-revision`: review actions. **Real side effects**: approve fires the creator's earnings, all three notify the creator, and the action is indistinguishable from a manual review in the brand portal. Only works while `status: pending` (400 `invalid_request` otherwise, which also prevents double-review). `request-revision` requires a non-empty `comment`.
- 404s are deliberately ambiguous: deleted, superseded, or still in partner review all read as `not_found`.

See also [[bambora-trybe-submission-review]] for how this fits Fatima's review workflow, and [[claude-in-chrome-standing-permission]] for the operating constraint this interacts with (approve/reject should still be confirmed per-action since they trigger payment + notify a third party).
