---
name: evolve-new-info
description: Stage 3 of the EVOLVE ad pipeline — research genuinely NEW INFORMATION for a product: recent studies, emerging discoveries, novel mechanisms of action, regulatory or industry shifts, and untapped angles from the last 12-24 months that competitors have not yet used in their marketing. Use when the user says "run the new info prompt", "evolve new information", "find new information", "what's the latest research on X", "we need a fresh angle for a saturated market", "what are competitors not saying", or is working through Stage 4 market sophistication. Produces the New Information Document that evolve-video-ads requires as a named input. Output is science-first educational positioning with sources, dates, and non-fear-mongering hooks.
---

# EVOLVE — New information

Stage 3 of the EVOLVE pipeline. Finds knowledge the market hasn't heard yet.

```
evolve-new-mechanism ──┐
                       ├──> evolve-video-ads
evolve-new-info ───────┘
```

The output is the **New Information Document**, a named required input of
`evolve-video-ads`.

## When this is the right move

At Stage 4 sophistication, every competitor already has a mechanism and the
audience believes none of them. Escalating claims fails. What still works is
telling people something they genuinely did not know — recent research, a newly
identified cause, a discovery that reframes the problem itself.

Stage detail in
`~/.claude/skills/evolve-new-mechanism/references/market-sophistication.md`.

New information and new mechanism are strongest **together**: the information is
the hook (*here's something you didn't know*), the mechanism is the resolution
(*and here's what acts on it*). The information alone is a problem with no
solution; the mechanism alone solves a problem nobody knew they had.

## What counts as new information

- Recently published scientific research
- Newly identified mechanisms of action
- Emerging use cases and unexpected demographic adoption
- Breakthrough manufacturing or processing methods
- Regulatory changes and approvals
- Technological advances in the category
- Newly discovered synergistic effects
- Consumer behaviour shifts backed by data

**Recency bar:** published or discovered in the last **12–24 months**, and not
yet widely used in marketing. Something true but old isn't new information —
it's a feature. The whole value is the gap between what's known in the
literature and what's been said in the category.

## Where to look

Peer-reviewed studies, industry reports, patent filings, regulatory approvals,
expert interviews, emerging consumer-behaviour data.

Use `WebSearch` and `WebFetch` for the literature. Use
`~/.claude/skills/voc-miner/` when the question is whether consumers have started
noticing something — an emerging use case usually shows up in customer language
before it shows up in a study.

Check what competitors are already saying before calling anything new.
`competitors/` in `flown-brain/`, or a competitive ad sweep. Information already
running in a competitor's ads is not an opening.

## Output format

For each finding:

**Source** — publication and date, specifically. A finding without a citable
source cannot be used.

**Why it's new** — the market sophistication gap. What is the category saying
instead, and what does this fill?

**How to use it ethically** — educational positioning. Explain the finding;
don't weaponise it.

**Three marketing hooks** — that educate and pique curiosity without fear
mongering.

Group findings under: Recent Scientific Discoveries, Emerging Market Trends,
Industry Developments, Novel Mechanisms or Benefits, Untapped Angles.

### Worked example of the shape

> **DPP-4 enzyme surge under chronic stress accelerates aging**
>
> **Source:** Multiple 2024 studies including *Advanced Science* (December 2024)
> and *Frontiers in Pharmacology* on DPP-4 and stress-induced vascular aging.
>
> **Why it's new:** 2024 research shows chronic stress upregulates DPP-4
> production, creating a cycle where stress breaks down natural GLP-1 faster
> than the body can use it. Most competitors haven't found this yet.
>
> **How to use it ethically:** Educate that stress isn't only a feeling — it
> measurably affects appetite regulation at the cellular level.
>
> **Hooks:**
> - "Scientists just discovered why stress makes you gain weight even when eating the same foods"
> - "NEW 2024 study: your stress is breaking down your appetite control system"
> - "Why chronic stress ages you twice as fast (hint: it's not just cortisol)"

## Rules

**Educate, don't frighten.** The line: explaining a mechanism the reader didn't
know about is education. Implying harm to manufacture urgency is fear mongering.
The first builds authority; the second buys a click and loses the customer. For
Flown this is also a brand rule — the voice guide explicitly bans fear-based
manipulation.

**Cite or drop it.** Every finding needs a real, checkable source with a date. If
a claim can't be traced to a specific publication, it does not go in the
document. Everything here flows downstream into ad copy that has to survive a
compliance check.

**Don't overstate what a study found.** A finding in mice is not a finding in
people. A correlation is not a mechanism. An n=40 pilot is not established
science. State what was actually measured — the specificity makes the copy
*more* persuasive, not less.

**New to the market, not new to you.** The test isn't whether you just learned
it. It's whether the category is already saying it. Check competitor ads before
classifying anything as untapped.
