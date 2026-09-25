---
name: evolve-video-ads
description: Stage 5 of the EVOLVE ad pipeline — write production-ready Facebook and Instagram video ad scripts. Produces three hooks, three matched bridges, ONE universal hold and ONE universal CTA, with timing markers, AI voiceover copy and B-roll visual instructions, targeting 30-45 seconds for problem-aware or product-aware audiences. Use when the user says "run the video prompt", "evolve video ads", "write me a video script", "VSL script", "write ad scripts for this angle", "3 hooks and a script", or wants Meta video creative built on the EVOLVE method. Runs a mandatory feedback-loop intake about previous script performance before writing. Execution model is B-roll compilation plus AI voiceover — no talking heads.
---

# EVOLVE — Video ad scripts

Stage 5 of the EVOLVE pipeline. Production-ready Meta video scripts.

**Core operating principle:** *It's not what you say, it's what you communicate.*

**Human first, formula second.** The frameworks here are tools for thinking, not
templates to complete. Hitting 2–3 elements powerfully beats forcing all four
awkwardly. The goal is natural, flowing copy — not copy that checks boxes.

**Execution model:** B-roll compilation + AI voiceover. No talking heads, no
direct-to-camera. Strategic footage plus narration that creates a slippery
slope — once they start watching, they can't stop until the CTA.

## Reference files

| File | Contents |
|---|---|
| `references/frameworks.md` | The Big 4, the Four U's, Hopkins' principles, slippery slope, the categorisation ban |
| `references/section-playbook.md` | Hook / Bridge / Hold / CTA requirements, awareness branches, the visual system |
| `references/proof-and-checks.md` | Social proof tiers, borrowed proof, compliance, the final checklists |

---

## Step 1 — Feedback loop. Mandatory, before any writing.

Ask these five, and wait for answers. This is what makes the system compound
instead of generating variations forever.

1. **Have you tested video scripts for this angle before?** If yes, paste them
   and say which were winners (got spend, hit KPI) and which were losers (no
   spend, or missed KPI). If no, "N/A".
2. **Which performed best and worst?** Of the hooks tested, which one got the
   spend?
3. **Were any metrics off?** If it never got spend, say "did not get significant
   spend". Otherwise: CTR under 1%, hook rate under 25%, hold rate under 5%, no
   conversions.
4. **Why do you think people did or didn't care about this ad?**
5. **Any new learnings to share before I write?**

Then adjust:

| Problem | Fix |
|---|---|
| Low CTR / hook rate | Stronger, more contrarian hooks; better visuals |
| Low hold rate | Simplify the mechanism, tighten the slippery slope, faster b-roll pacing |
| Low conversion | Strengthen the offer or build more trust |

If nothing has been tested, proceed on best practice and build three distinct
emotional entry points. Briefly say how the feedback shaped the strategy before
writing.

## Step 2 — Read the input documents

Required, and analysed with active reading for subtext before a word is written:

| Document | Source |
|---|---|
| Product Document | `evolve-desires` output, or `sub-context-docs/website-and-product-audit.md` |
| New Mechanism Document | `evolve-new-mechanism` output |
| New Information Document | `evolve-new-info` output |
| Customer Data Document | `evolve-desires` output, `personas/voice-of-customer/` |

Extract: the one mechanism that creates new hope, exact customer language for
pain and transformation, specific numbers and credibility markers, the
sophistication stage, contrarian angles, and at least three distinct emotional
entry points for hooks.

## Step 3 — Pick the awareness level

**Problem-aware or product-aware only.** Do not write unaware hooks or
most-aware retargeting.

| | Problem-aware | Product-aware |
|---|---|---|
| They | Feel the pain, may not know solutions exist | Have tried competitors, are skeptical |
| Hook | State the problem directly | Pattern interrupt / contrarian |
| Bridge | Agitate, explain why it exists | Quick problem reminder |
| Hold | Educate — your mechanism as *the* solution | Heavy on why *yours* is different |
| CTA | Make it easy to try | Risk reversal |
| Length | 40–45s | 30–40s |

Problem-aware: *"Here's the problem and here's THE solution."*
Product-aware: *"Here's why other solutions failed and why THIS one works."*

If the audience is unaware, `anthropic-skills:unaware-ads` covers that stage.

## Step 4 — Write

Four sections: Hook (0–3s), Bridge (3–8s), Hold (8–35s), CTA (35–45s). Hard cap
45 seconds. Per-section requirements in `references/section-playbook.md`.

Voiceover at a **fifth-to-seventh grade reading level**, conversational, with
contractions and natural speech rhythm. Test every line: *would someone actually
say this out loud?*

---

## Output structure — you are testing HOOKS + BRIDGES

**The hold and CTA are identical across all three scripts.** This is what
isolates hook/bridge performance. Vary the hold or CTA too and you learn nothing
from the test.

Present in five parts:

**Part 1 — Three hook variations.** Each with its framework type, in a
TIMING / AI VOICEOVER / VISUAL INSTRUCTION table at 0–3s.

**Part 2 — Three bridges**, one matched to each hook, 3–8s.

**Part 3 — One universal hold**, 8–35s. Not Hold A/B/C. One.

**Part 4 — One universal CTA**, 35–45s. Not CTA A/B/C. One.

**Part 5 — How they combine:**

```
SCRIPT 1 = Hook A + Bridge A + Universal Hold + Universal CTA
SCRIPT 2 = Hook B + Bridge B + Universal Hold + Universal CTA
SCRIPT 3 = Hook C + Bridge C + Universal Hold + Universal CTA
```

Then a **strategic explanation**: the Big 4 analysis per section, which
mechanism creates new hope, target awareness level and why, how the
Objection → Claim → Proof → Benefit cycle runs, where show-don't-tell replaced
benefit lists, and how curiosity gaps were created line to line.

---

## The rules that override style

**Never categorise.** If you say what the product *is* — massage gun, collagen,
curler — you've made it a commodity. Say what it *does* that nothing else does.
Non-negotiable; full treatment in `references/frameworks.md`.

**One central proposition.** Hammer it throughout. A script with one message
penetrates; a script with ten dilutes.

**Show, don't tell.** "When you're telling, you aren't selling." Behavioural
transformation, not benefit lists.

**Slippery slope.** Every sentence creates a curiosity gap pulling to the next.
No natural stopping point before the CTA.

**One Objection → Claim → Proof → Benefit cycle.** Once, cleanly, in the hold.
Not multiple cycles.

**Specific over vague.** Hopkins: vague claims are ignored, specific claims are
believed.

**Never fabricate proof.** If a number isn't verified, don't use it. Tiers and
the borrowed-proof protocol in `references/proof-and-checks.md`.

**For Flown:** AI-produced creative outperforms UGC for this brand — never
propose "hire a real presenter" as a generic authenticity fix. Never present
"built for short hair" as settled. Filter shipping and logistics complaints out
of customer language. See `brand-lens.md` and
`running-notes/brand-notes-from-org.md`.
