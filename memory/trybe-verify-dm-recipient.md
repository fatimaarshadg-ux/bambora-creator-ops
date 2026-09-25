---
name: trybe-verify-dm-recipient
description: Always confirm which Trybe chat thread is open before sending, because duplicate creator accounts make name-matching unsafe
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e246c4f3-5aec-4721-b2f1-930d009ebb61
  modified: 2026-09-20T14:37:58.365Z
---

Before sending any DM in the Trybe brand portal, confirm the open thread is the right one by its **conversation history**, not by the creator's name or avatar.

**A conversation list preview is not a thread.** The list shows one line per conversation, the most recent message only. On 2026-09-20 a click meant to open Laura Daniels' thread silently timed out, the conversation list got read instead, and her video introduction was reported to Fatima as not existing. She had written that she is a pediatric physical therapist who evaluates baby wearing and infant positioning for a living, which is a strong credential for this brand. Fatima's templated welcome, which goes out to a new creator within a minute or two of approval, was the only thing in the preview line. Because that welcome sends on its own, a newly approved creator already has a reply; check the thread before offering to draft one. Confirm a thread actually opened, by its header and history, before stating anything about what it contains, and when a tool call fails say "could not verify" rather than reporting an absence.

**Why:** on 2026-09-20 an approval DM for Jenasa Prudhomme went to the wrong account. She has two: `creator_f8f3ad99` (joined Jul 28, photo avatar, 6 submissions, the real one) and `creator_75eada6b` (joined Sep 19, initials avatar, zero submissions, a duplicate she created by signing up through the V3 invite link instead of joining with her existing account). Both show identically as "Jenasa Prudhomme (DM)" in chat search. The conversation list also re-sorts the moment a message sends, so a `ref` or coordinate captured a few seconds earlier can point at a different row by the time it's clicked. Fatima caught it; I did not.

**How to apply:**
- Re-`find` the conversation immediately before clicking, click by `ref`, then screenshot and read the thread history to confirm identity before typing a single character.
- Duplicate accounts are distinguishable by history: the real account has prior back-and-forth; the duplicate usually holds only the generic onboarding message.
- Cross-check against the API when stakes are real: `GET /v1/creators/{id}` returns `avatar_url` (null = initials avatar in the UI) and `joined_at`, which together identify the row.
- Watch for the avatar in a thread header being clickable: clicking it opens the creator profile modal instead of switching threads.
- A sent DM cannot be unsent; hovering a message reveals edit/delete controls, but deleting is destructive, so ask Fatima before removing a misdirected message.

Related: [[trybe-sample-request-workflow]], [[bambora-trybe-submission-review]].
