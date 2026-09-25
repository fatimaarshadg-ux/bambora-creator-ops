---
name: trybe-api-capabilities
description: Trybe Brand API has a creator-performance endpoint and an on-screen-text search; the local MCP server had invented filters (now fixed)
metadata:
  type: project
---

Trybe's Brand API (`https://api.jointrybe.com/v1`, docs at
jointrybe.com/help/api-reference, login required, so use Claude in Chrome) does
far more than the local MCP server originally exposed:

- **`GET /v1/creator-performance`** returns the creator leaderboard directly:
  earnings, trybe_conversions, trybe_gmv, new/active submissions, ads, spend,
  purchases, purchase_value, roas. Date-bounded, `sort_by` any metric,
  cursor-paged. Defaults to last 30 days, so pass `start_date` for lifetime.
  Capped at 90 days when `sort_by` is a metric or `active_only` is set.
- **`GET /v1/submissions?query=...`** substring-matches the transcript, **the
  on-screen text**, and the creator's note. This finds burned-in captions that
  transcripts miss entirely.

The local server at `~/Bombara/trybe-review/mcp-server/server.js` originally
passed `creator` and `product` params that the API rejects, and had no cursor
support, which led to a wrong conclusion that the API couldn't do this analysis.
Fixed 2026-09-17: real filter names, `after`/`before` cursors, and a new
`trybe_creator_performance` tool. Backup at `server.js.bak`.

**Lesson:** check the vendor's API reference before concluding an API can't do
something. The local wrapper is not the API. Related:
[[feedback-use-chrome-extension-for-logged-in-sites]], [[bambora-brand-basics]]
