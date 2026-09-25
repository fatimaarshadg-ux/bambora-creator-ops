---
name: no-em-dashes
description: Write without em dashes, and repair text that contains them. Use this skill whenever writing or editing any prose the user will read or send, including chat replies, creator DMs, emails, reports, docs, commit messages, and code comments. Also use it when the user asks to remove em dashes, clean up punctuation, or says their text sounds AI-generated. Default to using it for any drafting task, even when em dashes are not mentioned.
---

# Writing without em dashes

Fatima does not want em dashes in anything you write. This includes text you send on her behalf, which is most of what matters here: creator DMs, emails, anything a real person reads and attributes to her.

## What counts

Remove all of these when they act as a dash:

- `—` the em dash (U+2014)
- `–` the en dash (U+2013) used as a connector between clauses
- `--` two hyphens standing in for a dash
- ` - ` a spaced hyphen standing in for a dash

That last one matters. Swapping `—` for ` - ` is the most common way this rule gets quietly broken. It is the same move wearing a different hat, and it reads worse.

Leave these alone, they are not dashes:
- hyphens inside compound words: `well-known`, `knee-to-knee`, `9:16`
- hyphens in identifiers, paths, flags: `no-em-dashes`, `--verbose`, `creator_program_f752`
- en dashes inside numeric ranges: `1080–1920`, `Aug 9–12`

## Why the rule exists

Em dashes are the fingerprint of AI-written text. Fatima's creators are real people reading messages they believe she typed herself, and a message dense with em dashes reads machine-made. The rule is about her voice sounding like hers.

There is a second reason worth internalising. An em dash is usually a shortcut past a decision. It lets you bolt a thought onto a sentence without working out how the two ideas relate. Removing it forces that decision, and the writing gets clearer.

## What to use instead

The instinct is to find a substitute mark. Usually the better fix is to restructure. Work down this list, in order, and stop at the first one that reads naturally.

**1. Split into two sentences.** This is the right answer far more often than it feels like it should be. If the material after the dash is a complete thought, give it its own sentence.

> Before: The video is lovely — I want to use it.
> After: The video is lovely. I want to use it.

**2. Comma**, for a light aside or a short trailing clause.

> Before: One fix first — around 12s both hands are down.
> After: One fix first, around 12s both hands are down.

**3. Colon**, when the second half explains, reveals, or lists what the first half set up.

> Before: Two things to check — the buckle and the seat depth.
> After: Two things to check: the buckle and the seat depth.

**4. Parentheses**, for a genuine aside the sentence could survive without.

> Before: Her older account — joined July 28 — has all six videos.
> After: Her older account (joined July 28) has all six videos.

**5. Semicolon**, for two independent clauses that are tightly linked. Use sparingly; it is formal, and it reads stiff in a casual DM.

**6. A connecting word.** Often the dash was hiding a relationship you can just name: `because`, `so`, `but`, `which`, `and`.

> Before: I stopped before sending — the name did not match.
> After: I stopped before sending because the name did not match.

## Worked repair

> Before: Good catch — I sent it to the wrong account. She has two — one joined in July with six videos, the other a duplicate from Friday — and both show up identically in search.

Three dashes, three different jobs. Repair each on its own terms:

> After: Good catch, I sent it to the wrong account. She has two: one joined in July with six videos, the other a duplicate from Friday. Both show up identically in search.

The first became a comma (light aside), the second a colon (the list it was introducing), the third a sentence break (the clause stood alone fine).

## Checking your own work

Em dashes do not arrive deliberately. They appear mid-flow, when a sentence is running long and you want to attach one more thought. So the check has to happen after drafting, not during.

Before sending or saving anything, scan the text for `—`, `–`, `--`, and ` - `. If you find one, do not reach for the nearest substitute mark. Reread the sentence and ask what relationship the dash was standing in for, then write that relationship out.

Watch for two failure modes:

- **Comma overload.** Replacing every dash with a comma gives you long, limp, run-on sentences that are harder to read than the original. If a sentence now has three commas doing three different jobs, split it.
- **Mark laundering.** Reaching for ` - ` or `...` or an extra set of parentheses to preserve the exact original rhythm. The rhythm is allowed to change. That is the point.

## Scope

This applies to your own prose. Do not rewrite em dashes inside:

- quoted material from someone else, where you are reproducing their words
- file contents you are reading back to the user verbatim
- text the user wrote and asked you to send as-is, unless they ask you to clean it

If the user's own draft contains em dashes and they have asked you to send it, mention it in one line and let them decide, rather than silently editing their voice.
