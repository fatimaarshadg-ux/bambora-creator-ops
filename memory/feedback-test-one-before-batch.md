---
name: feedback-test-one-before-batch
description: After changing any setting that affects what creators receive, run ONE real case and read the result before doing the rest
metadata:
  type: feedback
---

When a setting or template that affects outbound messages has changed, do the action for one creator, open their thread, read what actually landed, and only then continue with the batch. Never assume what a setting does from its label.

**Why:** On 2026-09-21 the V3 welcome message was cleared so moved creators would get no automatic DM. "Empty" was never tested. On 2026-09-22 six creators were moved in one go and every one of them received Trybe's generic fallback ("Welcome to our creator program! You can use this chat...") from Bambora Admin. It cannot be edited or deleted. Fatima saw it live and was angry ("you are sending a shitty message"). A check after the first move had even been planned and was skipped.

**How to apply:** this is the "run one first" step from [[think-before-grinding]], applied to messaging. It holds even when the user is pushing for speed, because the cost of the check is one thread read and the cost of skipping it is a message to real people that cannot be recalled. Also see the welcome-message warning in the `trybe-portal` skill and [[feedback-no-review-leave-nothing-behind]].
