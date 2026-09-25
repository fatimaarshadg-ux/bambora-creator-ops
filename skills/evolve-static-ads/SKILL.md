---
name: evolve-static-ads
description: Stage 5 of the EVOLVE ad pipeline — write Facebook and Instagram image ad briefs. Runs a four-question intake, produces nine scroll-stopping headlines (6-8 words max) each with its reference pattern, rationale, and two iterations, then after the user picks their favourites writes complete image ad briefs with visual direction for editors. Use when the user says "run the static ads prompt", "evolve statics", "write me static ads", "image ad brief", "I need headlines for a static", "$100k statics", or wants Meta image ad concepts ready to hand to a designer. Two-step and interactive by design — always stop for the user's headline picks before writing the full briefs.
---

# EVOLVE — Static image ads

Stage 5 of the EVOLVE pipeline. Produces image ad briefs for Facebook and
Instagram, ready to hand to an editor.

**A winning image ad** is a bold, scroll-stopping image with a powerful headline
that lets the company increase spend profitably and acquire new customers.

**These ads are for NEW customers only.** The target avatar has likely never
heard of the brand and does not care who it is. They care about themselves. The
ad has to appeal to them and show them they're understood.

## This skill runs in two steps. Do not merge them.

The source prompt is explicitly interactive. Step 1 produces headlines; the user
picks; only then does Step 2 produce briefs. Writing all nine full briefs
unprompted wastes most of the work and removes the user's judgement from the
one place it matters most.

---

## Intake — ask these one at a time

1. **Research** — the cleaned research document, reviews, and any other
   resources for the brand.
2. **Avatar** — the target avatar for this ad.
3. **Product** — name and a brief description, including unique features and
   benefits.
4. **Confirmation** — confirm they're ready to proceed.

If `flown-brain/` is present, read rather than ask:
`sub-context-docs/brand-profile-narrative.md`,
`sub-context-docs/website-and-product-audit.md`, `personas/personas-profile.md`,
`personas/voice-of-customer/`, `brand-lens.md`. Tell the user what you loaded and
ask only for what's genuinely missing — usually just which product and which
avatar.

Prior EVOLVE stages feed this directly: `evolve-angles` output supplies the
angles, `evolve-desires` supplies the customer language.

---

## Step 1 — Nine headlines

Write **nine** headlines for the ad. Ground them in the research, write them for
the specific avatar and product, follow the brand's tone.

**6–8 words maximum.** One objective: stop the scroll of the target avatar and
get them to want to learn more.

For each headline:

- **The reference example** from `references/example-ads.md` it was built from,
  and why that pattern works for this brand and avatar
- **Why it stops the scroll** for this specific avatar — briefly
- **Two more iterations** of the same idea to choose from

Then **stop and ask the user to pick their top three** (or however many they
want).

---

## Step 2 — Full image ad briefs

For each chosen headline, write the complete concept: describe the image and
provide any additional callout text needed, so it's ready to send to editors.

`references/example-ads.md` shows how to describe an image ad. **Keep the briefs
more condensed than those examples** — they're deliberately exhaustive for
teaching, not a length target.

Cover: layout and background, the main visual elements and their arrangement,
all on-image text and where it sits, branding placement, and the tone the
finished ad should carry.

---

## The four rules

Applied before writing headlines and again before finalising briefs:

1. **Assume the avatar does not know you and does not care about you.**
2. **Imagery must match and emphasise the headline.** Congruency is not
   optional — an image that doesn't reinforce the line splits attention and
   kills both halves.
3. **Make people FEEL something.** Make them feel understood.
4. **Be clear, be concise, keep the language simple.**

---

## Notes

**This prompt has no awareness gate**, unlike `evolve-video-ads`, which writes
only for problem-aware and product-aware audiences. Statics here assume a cold
avatar who has never heard of the brand. If a static is wanted for a warm or
retargeting audience, say that the source method doesn't cover it rather than
silently borrowing the video prompt's rules.

**Don't fabricate proof.** Review counts, ratings, customer numbers, and
clinical results must be real. Same standard as `evolve-video-ads` — if the
number isn't verified, use a percentage, a testimonial pattern, or nothing.

**For Flown:** the brand runs a permanent 50%-off anchor that sits in tension
with its stated pro-aging, non-manipulative identity. Check `brand-lens.md`
before leaning on discount or urgency framing in a headline.
