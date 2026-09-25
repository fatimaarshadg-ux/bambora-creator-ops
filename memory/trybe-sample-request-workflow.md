---
name: trybe-sample-request-workflow
description: "How to approve Trybe sample requests in the brand portal, and the welcome message Fatima always sends afterwards"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e246c4f3-5aec-4721-b2f1-930d009ebb61
  modified: 2026-09-21T12:32:12.734Z
---

When Fatima asks to accept/approve sample requests on Trybe, do it in the brand portal via Claude in Chrome (the Brand API has no sample-request endpoint; see [[trybe-brand-api]]).

**Where it lives:** Brand Portal → **Creators** (`/brand/creators?b=a8bedbc3-3b30-410d-a09e-2aa3aeb3a8e9`) → **Samples** tab → **Pending** filter. The `b=` param is Bambora's brand id. Each row has a "Toggle details" chevron that expands to show product, variant, quantity, shipping address, an optional creator note, and **Approve N item(s)** / **Reject All**. A green check in the Status column plus a "Sample request approved" toast confirms it.

**Always follow each approval with this DM** (Chat → find the creator's DM → composer; use shift+Enter for line breaks, then the "Send message" button). Fill in the creator's real first name:

```
Hey {firstname}, I just accepted your sample request.

reallyyy excited to do this together! I will always be a message away, whenever you hit a wall with new ideas, or want to run anything by me, message me and I will help you with it.

Letsgoo ❤️
```

**That DM is for NEW creators only.** Before sending, check the creator's Bambora history (API: `GET /v1/submissions?creator_id=...`, and the thread history). If they already have Bambora submissions, the onboarding wording reads like a template, so draft a tailored version and show Fatima before sending. The shape she approved for Sophia Lease on 2026-09-21 (10 Bambora videos in Aug, none since, high volume for other brands):

```
Hey {firstname}, I just accepted your sample request.

you have been on fireee lately, I see how much you are putting out on Trybe and it is reallyyy paying off. Your videos from August are still bringing in sales too, so I think there is a lot more here for you!

I have noticed creators who are putting out 20-30 videos a month for us are making really good commissions. If you are down to do that much volume, I can help you out by sending you weekly inspo/angles/hooks etc. how does that sound?

Can't wait to see what you make with the sample. Letsgoo ❤️
```

Her wording preferences from that edit: keep the warmth ("on fireee", "reallyyy"); the 20-30 videos a month volume pitch plus the weekly inspo/angles/hooks offer is hers; do not name "Bambora" inside a Bambora DM (redundant); no vague references like "this one", say "the sample". Only state things that are true of the creator (the compliment said "on Trybe" because her recent volume was for other brands).

**Trap, Samples table columns:** 30D GMV and 30D SUBM. each have two sub-columns, **Brand** then **Trybe**. The Trybe number is the creator's activity across all brands, not Bambora. On 2026-09-21 I reported Sophia's Trybe-wide 68 submissions as if they were Bambora's (real figure: 0 in 30 days). Confirm Bambora activity through the API before describing a creator. See [[feedback-never-mix-metric-scopes]].

**Why:** Fatima gave this as a standing instruction on 2026-09-20, because approving a sample without the follow-up leaves the creator with no acknowledgement, and the warm "message me anytime" framing is how she onboards. Her brand health score tracks chat reply time.

**How to apply:** approve, then send. Don't batch the messages for later. If the list has more pending requests than she named, show her the list and confirm which ones rather than guessing (approving ships real product to a real address). Check the creator's DM thread before sending. If she already messaged them manually in the last few minutes, flag the overlap.

Related: [[bambora-content-checklist]], [[claude-in-chrome-standing-permission]].

**Scope rule (Fatima, 2026-09-23): only approve sample requests from creators we recently accepted** (new joiners in the current batch). Never bulk-approve everyone pending; older pending requests (from other creators) are hers to decide.

**Mechanics that work (2026-09-23):** on the Samples tab, filter Pending. Only one row's details stay open at a time. Open a row by focusing its "Toggle details" button and sending a real Return; read product/variant/address; then focus "Approve 1 item" and send Return. Scripted `.click()` does nothing here. Verify with the Approved filter afterwards. Bring the tab forward by matching its own URL (`tab=samples`), not the shared `cl=1` marker (another tab may carry it).
