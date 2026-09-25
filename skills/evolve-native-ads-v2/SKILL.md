---
name: evolve-native-ads-v2
description: Write long-form native ad copy by modelling a proven structure — the Insider Confession (stylist, engineer, salon owner), the Sufferer Confession, the Symptom Checklist, or the Soft Handoff. Pick the structure that fits the product and audience, then rebuild it beat by beat with real research. Use when the user says "native ads v2", "v2 native", "use the swipe", "swipe file native ad", "advertorial style native ad", "stylist authority ad", "engineer ad", or asks for native copy and names version two. This is the structure-driven version — evolve-native-ads (v1) builds the angle from research instead. If the user just says "native ads" without naming a version, ask which they want.
---

# Native ads — proven structures (v2)

> Structures reverse engineered from a swipe bank of native ads that performed
> (Alexander Kemperman, kemperman.com). Only the skeletons were kept.

**v2 versus v1:**

- **v1 (`evolve-native-ads`)** — start from customer research and build the angle
  from scratch. Use for a new product, a new market, or when the angle isn't
  known yet.
- **v2 (this skill)** — start from a proven structure and fit the product to it.
  Faster, and better when the angle is known or a previous ad worked and you want
  another in that shape.

Both write for **100% cold traffic**, and in both the click is a belief, not a
purchase.

## What a native ad is

An image that looks like an everyday picture of a real problem, a real moment, a
real scene from someone's life. It does not look like an ad. The image stops the
scroll by making the viewer think *that is me, that is my life.*

The copy mirrors the emotional state the image created and carries them to a
click. Cold traffic, no brand awareness, no intent. The copy earns attention from
zero in the first sentence. **The moment it feels like an ad, they are gone.**

---

## How to run this

**1. Pick the structure.** Four are documented in `references/templates.md` with
full beat structures.

| | Product-direct CTA | Article / prelander CTA |
|---|---|---|
| **Insider voice** | Insider Confession | Soft Handoff |
| **Sufferer voice** | Symptom Checklist | Sufferer Confession |

Name the choice and say why before writing. If the user already named one, use
it.

**2. Choose the insider**, if the structure needs one. Stylist, colourist,
engineer, product developer, salon owner, buyer — whoever the reader already
trusts *in this category*. Borrowed prestige from the wrong field reads as a
stretch and costs more trust than it buys.

The **engineer variant** is the strongest mechanism vehicle of the four: an
insider explaining how these things are actually built, what is inside the one
the reader already owns, and why it fails the specific way it does. It needs no
client story at all.

**3. Get the research.** These structures live on lived detail — named products
they tried, prices, times of day, the exact thing a professional told them.
Vague input produces a hollow version of a strong skeleton.

```bash
py -3 ~/.claude/skills/voc-miner/scripts/voc.py discover "<problem phrase>"
py -3 ~/.claude/skills/voc-miner/scripts/voc.py search "<phrase>" \
  --subreddit sub1,sub2 --sources reddit,youtube --limit 400
```

Sanity-check `discover` before harvesting — when its global search is rate
limited it falls back to matching subreddit names and returns nonsense.

If `flown-brain/` is present, `personas/voice-of-customer/` and
`personas/persona-voice-library.md` already hold usable language.

**4. Confirm the fixed inputs.** Ask for whatever is missing:

- **The image** the copy sits with, described in full
- **The destination** — product page, advertorial, listicle, quiz
- **The page identity** running the ad
- **The country**, for any reference to professionals, costs, or product access

**5. Write the beats in order**, then run the checks at the end of
`references/templates.md`.

**6. If the user wants variations**, use three *different* structures rather than
three rewrites of one. That is a real test; three paraphrases are not.

---

## What makes these work

**The confession opener.** Three of the four structures open by admitting
something against the writer's own interest — a professional was wrong for years,
a sufferer names her shame before her symptoms. It buys trust before anything is
claimed, and it does not read like advertising because advertising does not
concede.

**One outside source.** In the insider structures the breakthrough never comes
from the expert. It comes from a client, a friend, a comment thread. The
authority is the **witness, not the discoverer.** This is what keeps the piece
from reading as a pitch, and removing it collapses the structure.

**Defending what failed.** The mechanism reframe protects the reader's past
attempts rather than mocking them — the tools were not bad tools, they were never
designed for what her hair became. Nobody who feels stupid buys anything.

**Fragmented rhythm.** Short lines, sentence fragments as paragraphs, then a
longer passage when something needs explaining, then short again.

> Thinner.
>
> Always thinner.
>
> A little less at the crown every year.

**Specificity as proof.** Named tools, real prices, exact times, exact
temperatures. Numbers do the believing.

---

## Rules for every word

- **No hyphens anywhere.** Not one.
- Short punchy sentences, open loops throughout
- The customer's raw language, not cleaned up, throughout the whole piece
- First person, or the voice of the page running the ad
- No corporate language, no marketing speak, nothing brochure shaped
- Every angle carries one emotional driver: shame, exhaustion, anger, grief,
  hope, fear, or resignation

## Rebuild the skeleton, never the flesh

The source bank reuses its own structures with the specifics swapped — same
beats, different category, different numbers. That is the proof that the
**structure** is the reusable asset. Lifting sentences, stories, or mechanism
names produces a detectable clone of someone else's ad and inherits claims you
cannot support.

## For Flown

The insider-authority format is **the account's proven engine.** "The hairstylist
ranks five tools" is the single highest-spend ad in the account, and every
top-spend ad opening with a professional claim — "I'm a hairstylist," "I've
styled hair for 20 years" — runs this exact mechanic. Default to it.

Three things from the account's own read worth carrying in:

- **Specific voice beats generic authority.** On an identical script, the
  named-customer testimonial format posted 3.02 ROAS against 1.84 for an invented
  authority character. The lever is specificity, not the credential — so give the
  insider a real texture (what she does on a Tuesday, what she keeps in her
  station drawer), never a generic "expert."
- **Both tracked competitors run this mechanic through visibly real, credentialed
  stylists** while the account's version is unverified. A real named stylist is
  an available edge nobody in the set has taken.
- **Age-and-hormone-driven hair change is the account's strongest, most-repeated
  angle** — not haircut length. Build the insider's confession around hair that
  changed, not hair that is short.

Check `brand-lens.md` and `running-notes/brand-notes-from-org.md` before writing.
The brand's voice guide bans inflated claims and fear-based manipulation, and
GoCurl Pro has no citable review volume, so proof has to come from mechanism and
specificity rather than numbers.
