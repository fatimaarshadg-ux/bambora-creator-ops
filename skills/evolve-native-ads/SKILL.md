---
name: evolve-native-ads
description: Write native ad copy for cold traffic — the copy that sits above or below a native image ad and carries the reader to a click on a prelander, advertorial, comparicle, or listicle. Runs the full four-stage method: research extraction from real customer comments, then copy built as hook, agitation, aha moment, transformation, CTA, then a country and page-identity checkpoint, then three genuinely different versions. Use when the user says "native ad", "native ads", "native copy", "write native ad copy", "prelander ad copy", "advertorial ad copy", "cold traffic ad copy", or references Kemperman's native prompt. This is v1, the method-driven version — evolve-native-ads-v2 writes from the proven swipe bank instead. If the user just says "native ads" without naming a version, ask which they want.
---

# Native ads — the method (v1)

> Built from Alexander Kemperman's native advertising prompt system
> (kemperman.com). Adapted to run inside Claude Code with local research tooling.

There is a **v2** of this skill that works from the proven swipe bank instead of
from research. If the user hasn't named a version, ask which they want:

- **v1 (this skill)** — start from customer research, build the angle from
  scratch. Best when you have a new product, a new market, or no idea what the
  angle is yet.
- **v2** — start from a proven structural template and fit the product to it.
  Faster, and better when the angle is already known.

## What a native ad actually is

A native ad is an image that looks like an everyday picture of a real problem, a
real moment, a real scene from someone's life. It does not look like an ad. It
looks like something a person would post on Facebook or find organically in a
feed. The image stops the scroll by making the viewer think *that is me, that is
my life, that is the exact thing I have been dealing with.*

The copy above or below that image has one job: mirror the emotional state the
image just created, and carry the reader from that moment of recognition all the
way through to a click.

**The click is not a purchase. The click is a belief** — a belief that what is
on the other side is going to change something real.

**Traffic is 100% cold.** These people have never heard of the brand, were not
looking for a solution, and were scrolling to kill time. The copy earns
attention from zero in the first sentence and holds it to the CTA without ever
feeling like an ad. The moment it feels like an ad, they are gone.

It reads like an editorial, a confession, a message from a friend, an article
they stumbled onto.

## How to work

Go deeper than the obvious pain point and find the embarrassing truth
underneath. Think in real human moments, not marketing concepts. Write what a
real person said at 11pm to their best friend, not what a brand said in a
boardroom.

Always ask: **what is the emotion nobody is talking about publicly but everyone
is feeling privately?**

Never settle for the first angle. Push until you find the one that makes someone
feel seen in a way they did not expect.

---

## Stage 1 — Research extraction

**Do not skip this and do not do it from the outside.** Everything downstream is
only as good as this step.

Read real customer comments and become the prospect. Not a marketer observing
them from a distance — adapt your entire frame of reference to theirs. Think the
way they think, feel the weight they carry, understand the texture of their
daily frustration, their shame, their exhaustion from things that did not work.

The source prompt assumes Reddit comment CSVs. **Use `voc-miner` instead** — it
produces the same raw material with links:

```bash
py -3 ~/.claude/skills/voc-miner/scripts/voc.py discover "<problem phrase>"
py -3 ~/.claude/skills/voc-miner/scripts/voc.py search "<phrase>" \
  --subreddit sub1,sub2 --sources reddit,youtube --limit 400
py -3 ~/.claude/skills/voc-miner/scripts/voc.py quotes \
  --contains "<phrase>" --min-words 12 --max-chars 0 --sort score
```

Sanity-check `discover` before harvesting — when its global search is rate
limited it silently falls back to matching subreddit *names* and returns
nonsense. If the user already has CSVs or a corpus, read those instead.

Extract four things. **Do not paraphrase. Do not clean anything up.** Raw words —
the messy, unfiltered, late-night language people use when they are not
performing for anyone.

**1. The top 5 emotional tensions.** Not symptoms. Not physical complaints. The
feelings underneath — shame, fear, isolation, hopelessness, grief. Rank them
biggest to smallest, number one carrying the heaviest emotional load. Under each,
paste the exact phrases people use, word for word.

**2. The 3 most common things they already tried that failed.** Ranked by
emotional load, starting with the one they feel worst about — the one that cost
the most money, time, or hope. Capture not just what they tried but *why the
failure stung.*

**3. The single specific moment in the day when the problem hits hardest.** Not
a general time of day. The actual moment: what they are doing, where they are,
who they are with or not with, what triggered it.

**4. The thing they are most ashamed of.** What they would not say out loud at a
dinner table. What they only write anonymously at 1am. The thing that makes them
feel like less of a person.

Hold all of it. Stage 2 builds directly on top.

---

## Stage 2 — The copy

Three inputs before writing a word:

1. **The emotional driver the image is built around**
2. **A full description of the image** — what is shown, the scene, any text on
   it, the emotional reaction it is designed to create
3. **The prelander**, read in full

### Congruence is the whole game

**Copy ↔ prelander.** The person who clicks lands on that page. If the ad and the
prelander tell a different story, use different language, introduce a different
mechanism, or carry a different emotional tone, the reader feels the disconnect
the moment they arrive and they leave. *The ad copy is the door. The prelander is
the room behind it. They have to feel like the same place.*

**Copy ↔ image.** The image stops the scroll; the copy mirrors the exact
emotional state it created. If they are not telling the same emotional story in
the same emotional language, nobody clicks. They have to feel like one
continuous thing — the image was the first sentence, the copy is everything
that follows.

### The six-part structure, in this exact order

Full detail and worked patterns in `references/copy-anatomy.md`.

1. **Hook** — either mirrors the image so precisely that the reader feels they
   describe the same moment in their own life, creating an open loop that is
   uncomfortable to leave unclosed; or opens with a statement so bluntly true and
   unexpected they are stopped before consciously deciding to engage. If the hook
   fails, nothing else matters.
2. **Agitation** — go deeper using the exact research language. The moment in the
   bathroom. The thing they said to their partner. The thing they stopped doing
   because it got too hard.
3. **Let the fear breathe** — the cost of doing nothing, truthfully, not
   manipulatively.
4. **The aha moment** — the most important structural element. One mechanism,
   one reframe they have genuinely never heard, explained so plainly they will
   repeat it to someone else. It explains why everything they already tried could
   not have worked — not because they did something wrong, but because those
   things were never designed to address the actual root cause. **Must be the
   same mechanism as the prelander**, told at a different depth.
5. **Transformation** — specific, close, believable. A timeline. Small moments
   that add up to a different life. Earned by everything before it, not dropped
   in. Mirror the prelander's transformation language.
6. **CTA** — not a command, not a sales line. A gentle, inevitable continuation.
   By now, clicking should feel like the only logical thing left and *not*
   clicking should feel like the stranger choice. Point at whatever the prelander
   offers as the next step.

---

## Stage 3 — Country and page checkpoint

Before finalising, check two things and report what changed.

**Country/countries targeted.** Make sure references to doctors, healthcare
systems, costs, product access, and cultural context match that audience. If a
reference works everywhere, leave it.

**The page it runs from.** Ask what the page is — a community page where people
share what worked, a page running from a stylist's or an engineer's point of
view, an editorial brand. The voice, authority, and framing must match who is
telling the story. Adjust first-person language, implied credentials, and CTA
framing to fit.

Flag anything changed and why. If nothing needs changing, say so.

---

## Stage 4 — Three versions

Same product, same mechanism, same CTA destination, same emotional driver.
**Everything else completely different** — hook, story, narrative voice,
emotional angle, opening scene, aha framing, transformation sequence, CTA
language.

They should feel like they were written by three different people who each lived
a slightly different version of the same problem and found the same way out. A
reader should be able to read all three and not realise they are for the same
product until the very end.

Do not change a few sentences and call it a version. Start from scratch each
time: go back to the research, lead with a different emotional tension, open on a
different moment in the day, agitate a different failure, frame the mechanism
from a different angle.

Write three that all have a genuine shot at winning — not one strong version and
two backups. Label them `VERSION 01`, `VERSION 02`, `VERSION 03`.

---

## Rules for every word

- **Write in first person**, or from the perspective of the page running the ad,
  whichever is more congruent with the image
- **Sound like a real human** who lived this problem and found a way through —
  not a brand, not a marketer, not a copywriter
- **Use the research language throughout**, not only in the agitation
- **Short punchy sentences** that create rhythm and forward momentum
- **Open loops throughout** — small unresolved gaps the brain is compelled to
  close by reading on
- **No hyphens anywhere.** Not a single one. This is stated as an absolute in the
  source method
- **No corporate language**, marketing speak, or anything brochure-shaped
- Make it read like a drama they cannot put down

Every angle must have a clear emotional driver: **shame, exhaustion, anger,
grief, hope, fear, or resignation.** It must have a moment that feels lived in
rather than constructed, and a hook that works in under two seconds mid-scroll.

## Choosing the authority

Where the copy speaks from a professional's point of view, pick the one the
reader already trusts **in this category** — a stylist or colourist on hair, an
engineer or product developer on how a tool is built, a salon owner on what
actually gets used. Borrowed prestige from an unrelated field reads as a stretch
and costs more trust than it buys.

Give that person real texture — what they do on a Tuesday, what is in their
station drawer, the thing they say to every client. On an identical script, a
specific named voice has outperformed a generic "expert" character by a wide
margin in this account. **The specificity is the lever, not the credential.**

Composite and anonymised client stories are normal in this format. Keep the
credential itself something the page can stand behind, and keep results claims
traceable to something real — a fabricated credential or an invented named
testimonial is what gets ad accounts restricted, which is a deliverability
concern rather than a legal one.
