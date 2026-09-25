---
name: evolve-angles
description: Stage 4 of the EVOLVE ad pipeline — turn sub-avatars into marketing angles and hooks. For each sub-avatar, produces 3 angles (each a concrete reason to buy, written from the customer's perspective) and 3 hooks/headlines per angle, ranked strongest-first with a testing priority. Use when the user says "run the angles prompt", "evolve angles", "identify the angle", "what angle should we run", "turn these avatars into angles", "give me angles and hooks for X", or is confused about whether something is a concept or an angle. Follows the EVOLVE definition where an angle is the customer's reason to buy, not the marketer's test idea.
---

# EVOLVE — Angles and hooks

Stage 4 of the EVOLVE pipeline. Converts sub-avatars into the specific reasons
those people would buy, and the lines that communicate them.

```
evolve-desires ──> evolve-angles ──> evolve-static-ads
                                 └─> evolve-video-ads
```

## The distinction this skill exists to enforce

Most bad ads come from confusing a **concept** with an **angle**.

**Concept** = the big idea you're testing. About *you* and your test strategy.
**Angle** = how you're choosing to sell the product. About *the customer* and
their reason to buy.

These are all concepts pretending to be angles:

| Looks like an angle | Actually a concept | The missing part |
|---|---|---|
| "Us vs Them" | Comparison test | Comparing *what*? |
| "Before & After" | Transformation test | Transformation of *what*? |
| "Problem-aware ads" | Awareness test | *Which* problem? |
| "Post-it note ads" | A format | No angle considered at all |

The "what" is the angle. **If it doesn't give the customer a reason to buy, it
isn't an angle yet.**

Sometimes the concept *is* to test an angle — "Test Buy It For Life" → angle
"Buy It For Life." That's why people use the words interchangeably. It's still
worth writing the angle down explicitly for every concept, because that's the
line that catches the ones that don't have one.

Angles live on a spectrum from broad to specific, exactly like avatars do.
"Want better sleep?" is technically an angle — it's just a weak one, because
it's broad. Broad avatars force broad angles, which is why sub-avatar work makes
angle work easy. **Keep them actionable.**

Fuller treatment, with the full worked example set, in
`references/angle-craft.md`.

## Inputs

1. **Sub-avatars.** From `evolve-desires` output, or `personas/personas-profile.md`
   and `personas/voice-of-customer/` in `flown-brain/`. If only a core avatar
   exists, break it into sub-avatars first — you cannot write specific angles
   from a broad avatar.
2. **Product information.** `sub-context-docs/website-and-product-audit.md`.
3. **Winning ad references.** `references/angle-craft.md` carries the proven
   hook set; `idea-bank/` and `sprints/` in the brain carry brand-specific ones.

## Method

For each sub-avatar:

1. Find their **most painful or most specific attribute** — the thing true of
   them that isn't true of the broad avatar.
2. **Frame it as a problem from their perspective**, in their words.
3. **Convert it into a reason to buy** that a person would recognise as their
   own.
4. Write **three hooks** that communicate that angle.

Do this three times per sub-avatar, for three angles each.

### Hooks

The hook is how you communicate the angle — how you get attention in order to
sell. Until you're at an advanced level, **hooks should be direct, not
indirect**: the hook should say the angle plainly.

| Angle | Direct hook |
|---|---|
| Stops swelling | "14+ Hours. No Swelling" |
| Keeps you full like a meal | "This is a meal. Not a protein shake" |
| Stops you snapping at people | "5 minutes to install. No more snapping" |

Each hook should name which proven pattern it was built from — that's what makes
it repeatable rather than a one-off.

## Output

Ranked **strongest first** — strongest sub-avatar, strongest angle, strongest
hook at the top. Structure per angle:

> **Angle 1: [name]**
> **Reason to Buy:** [one or two sentences, customer's perspective]
> **Hook:** "[the line]"
> **Inspired by:** "[proven hook]" — [the pattern it uses]

Open the document with a **priority note** and close it with a **testing
priority**.

The priority note must tell the user, explicitly, that **they do not have to
test each angle separately** — a single concept can test multiple angles using
the best hook. This is stated in the source prompt as a requirement and it
matters: treating every angle as its own test is how people burn a month
learning nothing.

The testing priority names which single hook to test first and what to do next
depending on whether it hits.

## Rules

**Write from the customer's side.** An angle that describes what the product
does is a feature. An angle that describes why their life is worse without it
is an angle.

**Specific beats broad, every time.** "Want better sleep?" versus "5 minutes to
install. No more snapping." Both are angles. Only one of them is worth running.

**Rank honestly.** The strongest angle goes first, and the reasoning is stated.
A ranked list where everything is "strong" is an unranked list.

**For Flown, two brand rules bind here.** "Built for short hair" is a live
unresolved dispute — do not produce it as a confident angle; present both reads
and mark it open. And the dexterity-limited buyer (arthritis, reduced grip
strength) is the most evidence-backed unaddressed sub-avatar on file with zero
dedicated spend — check whether she belongs in the set before finalising.
