---
name: evolve-desires
description: Stage 1 of the EVOLVE ad pipeline — produce a Desire Research document for a product: the mass desires worth advertising against, each evidenced by verbatim customer quotes with sources, mapped to the permanent forces behind them, and ranked by Scope, Urgency, and Staying Power. Use when the user says "run the desires prompt", "evolve desires", "desire research", "find the mass desires", "what do customers actually want here", "desire power ranking", "map our angles to desires", or is starting EVOLVE research on a product before writing ads. The output is the Customer Data Document that evolve-angles and evolve-video-ads consume, so also use it when a later EVOLVE stage needs that input and it does not exist yet. This is the strategic analysis layer — for raw quote collection alone, use voc-miner directly.
---

# EVOLVE — Desire research

Stage 1 of the EVOLVE pipeline. Its job is to find the **mass desires** a product
can be sold against, and to prove each one exists with the customer's own words.

The deliverable is a document, not a chat answer. Later stages consume it:

```
evolve-desires ─┬─> evolve-angles ──> evolve-static-ads
                └─> evolve-video-ads  (as the Customer Data Document)
```

You are acting as a market research analyst in consumer psychology and
desire-based marketing. The standard to hold: **a desire nobody said out loud is
a hypothesis, not a finding.** Every desire in the final document carries at
least one exact quote and a link.

## What you need before writing anything

Ask for what's missing, one thing at a time. Do not ask for what you can read.

1. **Product and brand.** If `flown-brain/` exists in the working directory, read
   it instead of asking — see *Loading brand context* below.
2. **The angles currently being targeted.** Needed for Section 2. If the user
   doesn't know, check `strategy/messaging-strategy-input.md` and
   `sub-context-docs/ad-account-evaluation.md` in the brain, then confirm what
   you found rather than asking cold.
3. **Confirmation to proceed.** Say what you're about to mine and roughly how
   long it will take before you start.

## Loading brand context

When `flown-brain/` is present, read these before mining. They replace the
"Product Overview Document" the original EVOLVE prompt asks the user to attach:

| Need | File |
|---|---|
| What the product is and who buys it | `sub-context-docs/brand-profile-narrative.md` |
| Product specifics, claims, catalog | `sub-context-docs/website-and-product-audit.md` |
| Existing personas and their language | `personas/personas-profile.md`, `personas/voice-of-customer/` |
| Angles currently running | `sub-context-docs/ad-account-evaluation.md` |
| Brand rules that override generic method | `brand-lens.md`, `running-notes/brand-notes-from-org.md` |

`brand-notes-from-org.md` carries the brand's own corrections in full. Read it
before you commit to any finding — it is the file most likely to contradict a
conclusion the research seems to support.

## Mining the language

Use `voc-miner` (`~/.claude/skills/voc-miner/`). It is already installed, free,
and keeps a compounding corpus at `~/voc-data/corpus.jsonl`.

**Find where the conversation lives** before searching. The most common failure
is searching one subreddit and concluding a topic isn't discussed.

```bash
py -3 ~/.claude/skills/voc-miner/scripts/voc.py discover "<category phrase>"
```

**Sanity-check what `discover` returns before harvesting it.** Its global search
(PullPush) is frequently rate-limited, and when it is, discovery silently falls
back to matching subreddit *names* — which is close to useless for a two-word
product phrase. Verified failure: `discover "curling iron"` returned r/Curling
(the winter sport), r/curlingpuzzles, and r/ironmaiden. Harvesting that list
would have produced a corpus about stones and heavy metal.

The tell is a `global search unavailable` line, or results whose `subs` counts
and topics don't match the category. When it happens, skip discovery and pass
`--subreddit` yourself from brand knowledge and the personas file. For Flown's
category, `HaircareScience,femalehairadvice,Hair,longhair,FancyFollicles` is a
verified-working starting set.

**Harvest those communities**, several phrasings, Reddit and YouTube:

```bash
py -3 ~/.claude/skills/voc-miner/scripts/voc.py search "<phrase>" \
  --subreddit sub1,sub2,sub3 --sources reddit,youtube --limit 400
```

Run it more than once per phrase. Resume checkpoints mean each run reaches
further back rather than re-reading the same recent comments — repeat runs are
how the corpus actually grows.

**Pull the quotes you'll cite**, full text, no truncation:

```bash
py -3 ~/.claude/skills/voc-miner/scripts/voc.py quotes \
  --contains "<phrase>" --min-words 12 --max-chars 0 --sort score
```

Search across several phrasings of the same desire, not one. People describe the
same want in very different words, and the vivid quote is rarely in the obvious
phrasing. `--exact` narrows to the literal phrase; read the related tier before
discarding it, since that is where phrasing variety lives.

### What to search for

- Direct "I want" and "I need" statements
- Recurring complaints and frustrations that reveal an unmet desire
- Emotional language — frustrated, exhausted, embarrassed, finally, obsessed
- Comparative statements: what customers wish the product could do
- Evidence of workarounds people invented for a limitation

Workarounds are the highest-value signal in that list. Someone who built a
workaround has demonstrated the desire with effort, not just words.

Beyond Reddit and YouTube, `references/finding-desires.md` covers the rest of
the source landscape — Amazon Q&A, review mining, Google Trends as a rising-desire
signal, and the customer-interview questions.

## Framing the findings

Every desire gets mapped to the permanent force underneath it: **Mass Instincts**,
**Mass Technological Problems**, or **Forces of Change**. Full taxonomy with
worked examples in `references/desire-frameworks.md`.

The mapping is not decoration. A desire that traces to a Mass Instinct renews
forever; one that traces to a Force of Change has a shelf life. That difference
is what Staying Power in the ranking actually measures.

## The deliverable

Five sections, in this order.

**1. Wants and needs analysis** — specific desires found, each with exact quotes
and sources, categorised by the permanent force it relates to.

**2. Existing angles → desire mapping** — for each angle currently running, which
desire it targets and what evidence supports that. Name the angles that map to
nothing. An angle with no desire underneath it is the most useful finding in
this section.

**3. New desire opportunities** — untapped desires the product can address, each
with quotes and sources as evidence.

**4. Customer voice evidence** — 10 to 15 verbatim snippets with exact sources.
Weight toward complaint patterns and explicit wants/needs statements.

**5. Desire power ranking** — every desire identified, ranked most to least
powerful, with reasoning:

- **Scope** — how many people share it
- **Urgency** — how desperately they want relief
- **Staying Power** — does it renew continuously, or burn out

For each desire, answer: is it widespread enough for mass marketing, strong
enough to drive a purchase, persistent or temporary, how directly the product
addresses it, and what emotional trigger connects to it.

End with a short note on which desires are ready to become angles, so
`evolve-angles` has somewhere to start.

## Rules

**Quote, never paraphrase.** Exact words, original typos, original
capitalisation, original profanity. Never merge several people's phrasing into
one tidy sentence. The persuasive power lives in the specific words people
chose — a smoothed-out summary destroys the only thing this document is for.

**Every quote carries its link.** A quote without a source is not evidence.

**Report counts, never frequencies.** voc-miner is a keyword scrape, not a
survey. Write "14 of 200 comments mentioning X used the word 'embarrassing'" —
never "customers frequently say." Sampling is newest-first unless `--spread` is
used; say so when it matters to the conclusion.

**Filter dropshipping noise.** For Flown specifically, slow delivery, customs,
"made in China," and wrong-address complaints are structurally expected and are
never a creative-strategy finding. They will be loud in the corpus. Exclude
them from every section, including the power ranking.

**Don't resolve live disputes.** For Flown, "built for short hair" is an open
disagreement between this research base and the brand. If the mining touches it,
present both reads and mark it unresolved. Do not rank it as a settled desire.

**Distinguish desire from feature request.** "I wish it had a longer cord" is a
feature request. "I'm tired of being tethered to the wall while my arms ache" is
a desire. Only the second one sells anything.
