---
name: evolve-new-mechanism
description: Stage 2 of the EVOLVE ad pipeline — identify 3-5 NEW MECHANISMS for a product: the fresh process, technology, ingredient, or delivery system that makes a familiar promise believable again, positioned so it creates new hope rather than another feature claim. Use when the user says "run the new mechanism prompt", "evolve new mechanism", "find the mechanism", "what's our unique mechanism", "why does this product work differently", "we need a mechanism for this angle", or is working through Stage 3 market sophistication. Produces the New Mechanism Document that evolve-video-ads requires as a named input. Also holds the canonical market-sophistication reference the other EVOLVE skills cite.
---

# EVOLVE — New mechanism

Stage 2 of the EVOLVE pipeline. Finds the **reason why** the product works —
the specific thing that lets a tired promise land as though it were new.

```
evolve-desires ──> evolve-new-mechanism ──> evolve-video-ads
                                        └─> evolve-angles
```

The output is the **New Mechanism Document**, a named required input of
`evolve-video-ads`.

## The one thing this skill is for

Markets get harder to sell to as they mature. By Stage 3, benefit claims alone
stop working, because the audience has heard every version of the promise and
believed none of them. A new mechanism restores belief by changing *why* the
promise is credible, without changing the promise itself.

**The test that matters:** does this mechanism give someone new hope that their
problem will finally be solved? A mechanism that is merely true, merely
technical, or merely different fails. It has to make a person who has already
given up consider trying again.

Full stage-by-stage detail in `references/market-sophistication.md`.

## Inputs

1. **Product name and URL, or the brand's own product documentation.** If
   `flown-brain/` is present, read `sub-context-docs/website-and-product-audit.md`
   and `sub-context-docs/brand-profile-narrative.md` rather than asking.
2. **The desire being targeted**, ideally from `evolve-desires` output. A
   mechanism with no desire attached is trivia.
3. **What the market has already heard** — `competitors/` in the brain, or
   `sub-context-docs/competitive-landscape.md`. A mechanism is only new relative
   to what competitors are already saying.

## What to look for

Examine the product for:

- **New delivery methods or formats** — how it gets to the customer or into the body
- **Innovative approaches** to an existing problem
- **Uncommon ingredients, technologies, or methodologies**
- **Specific combinations** of existing elements that make it improved
- **Contrarian approaches** that challenge conventional wisdom

The last one is the most underused. A mechanism that says *the thing everyone
does is the thing making it worse* carries more energy than one that says
*we added something new*, because it explains the audience's past failures
instead of asking them to forget them.

## What to produce

For each of 3–5 mechanisms:

1. **The mechanism**, stated plainly at a 6th-grade level
2. **Why it's new to this market** — what the audience has heard instead, and
   what gap this fills
3. **How it positions as "the reason why"** or "the secret thing" that makes the
   product work differently
4. **A Facebook/Instagram hook or headline** built on it
5. **Whether it works as contrarian or "anti-" positioning**

Rank them. Lead with the one that creates the most hope, not the one that is
most technically impressive — they are rarely the same mechanism.

## Rules

**Never categorise.** This is the rule that outranks everything else here, and
it carries through to `evolve-video-ads`. The moment you say what the product is
*like*, it becomes a commodity version of that thing.

| Categorises — kills it | Owns a new category |
|---|---|
| "Like Ozempic but natural" | "The first supplement that blocks the enzyme destroying your appetite hormone" |
| "Better than other collagens" | "The only formula that rebuilds from the inside out" |
| "The best massage gun" | "The only device that reads muscle tension and adjusts pressure automatically" |

The check: if you named the product's category — massage gun, collagen, curler,
protein powder — you have categorised it. Describe what it **does** that nothing
else does.

**Name the mechanism where you can.** A proprietary name makes a mechanism feel
ownable and repeatable: "The Alpine Ice Hack," "The Dyglomera Effect," "The
5-Second Water Method." A named mechanism survives being retold by a customer;
an unnamed one doesn't.

**Every claim needs a reason.** Don't state what it does — explain why that
works. "It reduces appetite" is a claim. "It blocks the enzyme that destroys
your appetite hormone every two minutes, so your brain finally gets the stop
signal" is a mechanism.

**Don't invent capability.** The mechanism must be something the product
genuinely does. If the product documentation doesn't support it, it isn't a
mechanism — it's a fabrication, and it will fail the compliance check in
`evolve-video-ads` downstream. Where a mechanism is plausible but unverified,
mark it as needing confirmation rather than presenting it as established.

**For Flown:** the brand's own voice guide bans inflated claims and fear-based
manipulation. A mechanism built on fear of damage would contradict the brand's
stated identity — check `brand-lens.md` before committing to one. Note also that
no competitor in this category answers "will this damage my hair" with proof;
a mechanism that does is the largest open opportunity on file.
