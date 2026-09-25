---
name: think-before-grinding
description: Find the structural shortcut before doing a task the slow way. Use this skill whenever work looks repetitive or bulk (hundreds of records, many pages, "do this for all of them"), whenever the same action has failed twice in a row, whenever a tool or page keeps timing out, and before starting anything that would take many near-identical steps. Also use it when you catch yourself saying something cannot be done. Read it before grinding, not after.
---

# Think before grinding

Most slow work is not hard. It is a fast problem being solved the slow way because nobody looked for the shortcut first.

The cost of looking is about two minutes. The cost of not looking, on 2026-09-20, was roughly an hour of Fatima's time watching a page get clicked at, and her eventually supplying the insight herself. Her words: "there are so many smart ways of doing things, always look at all the ways of doing things."

## Before starting repetitive work, spend two minutes here

Do not start the first approach that occurs to you. Generate several, then pick.

**Ask what the data already knows.** The strongest shortcuts come from structure in the data, not from better tooling.

The worked example: the task was rejecting several hundred join requests belonging to two old programs while sparing applicants to a new one. The plan was to inspect all 483 by hand. Fatima pointed out that the new program had only just launched, so *every* request older than its launch date necessarily belonged to an old program. One API call fixed the launch date at 2026-09-18, and a "sort by oldest" turned an inspect-everything problem into a safe bulk operation with a clean cutoff.

Nothing about that required new tools. It required asking what was already true about the data.

Questions that surface this kind of structure:
- What changed recently, and does that date partition the set?
- Is there an ordering that groups what I care about together?
- Is one category rare? Then enumerate the rare one and treat the rest as the default.
- Can a cheap query answer what I was about to establish by inspection?
- Does an API expose this, when I was about to do it through a UI?

**Ask whether the problem can be made smaller before it is solved.** A page that freezes under 483 rendered cards is not a broken page. It is an overloaded one. Typing a nonsense string into its search box emptied the grid, and every control that had been unresponsive for twenty minutes started working immediately. Shrink first, then act.

**Enumerate approaches out loud, then choose.** Three or four candidates, with a one-line reason each for why it might be fastest or safest. Picking the best of four beats perfecting the first.

## When something fails twice, stop

Two failures of the same action is the signal. Not five, not ten.

At two, stop and change category. Do not retry with a slightly different coordinate, a slightly longer wait, or a slightly different selector. Ask instead:

- **What is the actual failure?** "Clicks do not work on this page" and "clicks do not work while this page is rendering 483 cards" lead to completely different fixes. The first is a dead end. The second is solved by shrinking the page. A general claim about a whole tool or page is almost always the wrong diagnosis, and it is seductive because it feels like a conclusion while actually being surrender. Name the specific mechanism or you have not diagnosed anything.
- **Have I already seen this work?** Earlier that same session, a click on a search-filtered page with one result had worked instantly. That was the whole answer, an hour before it got used. When something intermittently works, the difference between the working and failing cases *is* the diagnosis. Go looking for a case where it worked before theorising about why it cannot.
- **Am I confusing "cannot" with "have not found how yet"?** Reporting an obstacle is only honest after genuinely enumerating alternatives. Otherwise it is giving up dressed as diligence.

## Separate the probe from the commit

Before asking a person to resolve an unknown, check whether you can resolve it yourself with a **reversible** action.

The mistake, from the same session: a bulk control labelled "Reject All" sat beside a "Select All". The scope of Select All was unknown, so the plan became "ask Fatima whether it selects the page or everything." She pointed out the obvious: **just click Select All and read the counter.** Selecting is reversible. Rejecting is not. The information was one free click away, and the question wasted her time on something answerable in three seconds.

The error was treating a harmless probe as if it carried the risk of the destructive action it sits next to. Proximity to danger is not danger.

So, before escalating an unknown:
- Is there an action that reveals the answer without committing anything? Selecting, filtering, sorting, hovering, opening a dropdown, previewing, expanding a row, a dry run, a GET request. All free.
- Can I do it to a single item first and watch what happens, rather than to all of them?
- Can I undo it if I am wrong? If yes, just do it.

Take the calculated risk when the calculation says the risk is zero. Reserve questions for what is genuinely irreversible or genuinely ambiguous.

The same applies to claims about capability. "The API has no endpoint for this" was asserted from reading a docs index. The honest version came from firing thirteen candidate URLs and getting thirteen `not_found` responses. Probing took one call. Assert after probing, not before.

## Match the effort to the stakes

Cheap and reversible: just try it. Trying is faster than planning.

Expensive, irreversible, or touching other people: the two minutes of thinking are mandatory, and so is verifying scope before acting. "This operates on N things" must be a fact you have checked, not an assumption. A bulk control labelled "Reject All" sitting next to per-item buttons might mean everything or might mean the selection; if you cannot tell which, you cannot use it.

When scope is genuinely unverifiable, say so and ask. One question costs a minute. Rejecting four hundred people who should have been spared cannot be undone at all.

## A failed check is not a negative result

If a call timed out, a page froze, or a read returned something other than what you asked for, the check did not happen. Say "I could not verify this," never "it is not there." Absence of evidence from a broken check is not evidence of absence, and a confident wrong "no" does more damage than an honest "I don't know."

The trap has a general shape: **a summary view is not the thing it summarises.** A conversation list shows one preview line per thread and tells you nothing about a thread's history. A search index is not the document. A directory listing is not a file's contents. On 2026-09-20 a click to open someone's message thread silently failed, the list was read instead, and her introduction was reported to Fatima as non-existent. She had written that she assesses baby wearing professionally, which was the single most relevant fact about her.

So before concluding something is absent, confirm the thing you meant to open actually opened.

## Doing irreversible bulk work safely

When hundreds of irreversible actions have to run against records that must not all be treated alike, the danger is not the volume. It is that a plan made from a sample gets applied to records nobody looked at.

The pattern that works, and that made 391 rejections safe with zero errors:

**1. Order the set so the protected class clusters at one end.** Sorting by oldest worked because the category to spare was new. Look for the ordering that separates the groups instead of interleaving them.

**2. Act on the head of the list, and re-read the page every iteration.** Do not collect references up front and work through them. They go stale the moment the list changes, which it does after every action.

**3. Check each record's own text immediately before acting on it, inside the loop.** This is the actual safety mechanism. It means the code physically cannot act on a record it has not just read, so the protection does not depend on the plan being right.

**4. Let the loop stop itself** when the guard matches, rather than counting iterations. Then the stopping point is evidence: it stopped on the exact name expected at the boundary.

**5. Run one first.** One action, then verify the count moved by exactly one and the right record disappeared. Then scale.

**6. Verify both ends when finished.** Not just "I did 391" but also "the 48 that remain are all, without exception, the protected class, and zero unprotected records are left." Checking only the side you acted on misses the failure where you did the right number of the wrong things.

Keep batches inside whatever timeout the environment imposes. When a batch does time out, the work may well have continued anyway, so re-read the state rather than assuming nothing happened.

## The honest failure mode this exists to prevent

Grinding feels like working. Each retry feels like progress because it is an action. It is easy to spend an hour in a loop of small variations and produce nothing, while the person watching can see the shortcut.

Two habits prevent it:

1. Before repetitive work starts, ask what makes this set easy. Two minutes.
2. After two identical failures, stop and re-derive from what the failures have in common.

Neither requires being cleverer in the moment. Both just require not skipping the step.

## The one-line version

Across a long session of getting this wrong and then right, the difference was never effort. It was always this:

**Read the structure of the problem before choosing a method. Once a method is chosen, the pull is to make it work rather than to ask whether it is the right one.**

Every failure that day came from picking a method and grinding. Every success came from reading the data first and letting the method fall out of what the data was already shaped like. The person watching could see the shortcut the whole time, which is the reliable sign that the shortcut was visible and simply was not looked for.
