# Where everything lives in Trybe

Full detail (and every trap learned the hard way) is in the skill `trybe-portal` (`skills/trybe-portal/SKILL.md`). This is the short map.

**Bambora's brand id:** `a8bedbc3-3b30-410d-a09e-2aa3aeb3a8e9`. Every portal URL needs `?b=<brand id>`, or the page may 404 or open the wrong brand.

- Portal: https://jointrybe.com/brand?b=a8bedbc3-3b30-410d-a09e-2aa3aeb3a8e9
- API: `https://api.jointrybe.com/v1` (key from DPAPI; send a normal User-Agent like `curl/8.7.1`, because Python's default gets a 403)

## The portal

| Task | Where |
|---|---|
| Review, approve, reject a video (submission) | `/brand/submissions`, or the API (faster) |
| Sample requests | `/brand/creators` > **Samples** tab > **Pending** filter (narrow windows: the "Roster" dropdown > "Samples (N)") |
| New applicants (join requests) | `/brand/discovery` > **Inbox** tab |
| Applicant pitch messages (before approval) | `/brand/discovery` > **Messages** tab (only the 50 newest) |
| DM a creator | `/brand/chat` |
| Roster, stats, partnership ads status | `/brand/creators` > **Roster** |
| Programs and commission rates | `/brand/creators` > **Programs** |
| Creators you invited | `/brand/discovery` > **Invited** |
| Sales, GMV, ad performance | `/brand/analytics` |
| Shopify and Meta connections, API keys | `/brand/integrations` |

The left-nav **badges** (Chat, Submissions, Creators = pending samples, Discovery = inbox) are read at the start of every sweep (`badges()` in roster-scan.js). The Discovery badge never reaches zero (held applicants stay), so it is not trusted alone: new names are compared with `seen.txt`.

## Programs

| Program | Rate | Notes |
|---|---|---|
| **Bambora Affiliates V3** | 5% of GMV, videos only | "The 5% program". All new creators go here. Id `creator_program_f7523ebb-8206-4da5-9997-4464f77aec58` |
| The Bambora Affiliate Program! | 12% | 6 of the protected creators |
| Ambassador Program! | 10% | |
| Bambora Affiliates v1 | legacy 10% | 4 of the protected creators |
| Bambora Grandparents Program | 5% (V3 clone) | For grandparent creators, since 2026-09-24. Moms sometimes apply here by mistake |

V3 invite link: https://jointrybe.com/auth/program-invite/cmu4sbfi9001jj90xcvcs5smm

**Welcome messages** fire automatically when someone is accepted into a program (Manage > Customize > Chats). An **empty** welcome does not mean silence: Trybe then sends its own generic message, which cannot be deleted. Never clear it; ask Fatima before changing it; test with one creator first.

## Rules of the portal (why things are done the slow careful way)

1. **API first.** The browser only for samples, join requests and chat (the API has no endpoints for those).
2. **Never click by screen position.** Find the element and click it by reference, or focus it and send a real Enter key.
3. **Re-find and verify right before any send or approve.** The chat list re-sorts when a message sends; duplicate accounts share a name (Jenasa Prudhomme has two). Confirm the thread by its history, not the name.
4. **A check that failed is not a "no".** If a click timed out or a page froze, say "could not verify".
5. **Read an applicant's message before approving** (approval moves it out of the Messages tab).
6. **Discovery freezes** (it renders 222,000+ creators). Focus the tab through the page and send a real Enter.
7. **Background tab = dead clicks.** See `09-background-machinery.md` section 5.
8. Chat turns `<3` into `&lt;3`: use emoji hearts.
9. Approving a submission **releases money**; approving a sample **ships a real product**; accepting an applicant **adds a paid creator**. None are cleanly reversible.

## The API in one breath

- `GET /v1/submissions?status=pending` (filters: `status`, `creator_id`, `query` (matches on-screen text too), `program_id`, `limit`; cursor `after`).
- `GET /v1/submissions/<id>` gives a signed video `asset.url` that expires in about 20 minutes, and the transcript.
- `POST /v1/submissions/<id>/approve` with body `{}`; `/reject` and `/request-revision` with `{"comment": "..."}`. Claude uses these directly because the MCP tool dropped the comment once.
- `GET /v1/creators` does NOT list everyone; look up known ids with `GET /v1/creators/<id>` (includes `programs[]`).
- `GET /v1/creator-performance?start_date=2026-06-01` for earnings, GMV, last submission date.
- No chat API. Trybe's internal chat backend with a session token is blocked by Claude's safety checks: read chats through the normal screen.
- Sample tracking numbers are not in Trybe (only the Shopify order number).
