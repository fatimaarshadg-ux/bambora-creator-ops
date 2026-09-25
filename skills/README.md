# EVOLVE skills

Nine Claude Code skills for direct-response copywriting — seven built from the
EVOLVE Master Prompt Doc, plus two native advertising skills built from
Alexander Kemperman's native ad system. Wired into local tooling instead of
generic "go search the internet" instructions.

Install location: `~/.claude/skills/`. They load automatically in any Claude Code
session.

## The pipeline

```
evolve-desires ─────┬──────────────────────────┐
                    │                          │
                    ▼                          ▼
        evolve-new-mechanism ──┐          evolve-angles
                               │               │
        evolve-new-info ───────┤               │
                               ▼               ▼
                        evolve-video-ads   evolve-static-ads

        evolve-call-analysis  (standalone — reads meeting transcripts)
```

| Skill | Stage | Produces |
|---|---|---|
| `evolve-desires` | Research | Mass desires with verbatim quotes, ranked by Scope / Urgency / Staying Power |
| `evolve-new-mechanism` | Strategy | 3–5 new mechanisms that create new hope. Holds the canonical market-sophistication reference |
| `evolve-new-info` | Research | Recent discoveries competitors haven't used, with sources and dates |
| `evolve-angles` | Strategy | 3 angles per sub-avatar, 3 hooks per angle, ranked with a testing priority |
| `evolve-static-ads` | Copy | 9 headlines → your picks → full image ad briefs for editors |
| `evolve-video-ads` | Copy | 3 hooks + 3 bridges + 1 universal hold + 1 universal CTA, 30–45s |
| `evolve-call-analysis` | Ops | Weekly ad learnings call transcript → client-by-client report |

Only two of the seven write copy. The other five are the research and strategy
that make the copy possible — which is the actual shape of the source material.

## Native advertising

Two separate skills for native ads — image ads that look like an organic post,
running on 100% cold traffic, where the click is a belief rather than a purchase.
Both are long-form and both feed a prelander, advertorial, comparicle, or
listicle.

| Skill | Approach | Use when |
|---|---|---|
| `evolve-native-ads` (v1) | Method-driven. Research extraction → copy → country/page checkpoint → three versions | New product, new market, or the angle isn't known yet |
| `evolve-native-ads-v2` | Swipe-driven. Pick a proven template, fit the product to it | The angle is known, or a previous ad worked and you want another in that shape |

v2's four templates, reverse engineered from the swipe bank:

|  | Product-direct CTA | Article / prelander CTA |
|---|---|---|
| **Authority voice** | Practitioner Confession | Soft Handoff |
| **Sufferer voice** | Symptom Checklist | Sufferer Confession |

Ask which version is wanted if the user just says "native ads." Both carry the
method's absolute rule: **no hyphens anywhere in the copy.**

Source PDFs use subset fonts with a character offset (+29 on the prompt doc, +28
on the swipe doc), so plain text extraction returns a cipher. `pdftext.py` in the
session scratchpad handles it if these ever need re-extracting.

## What was changed from the source prompts

**Wired to local tooling.** `evolve-desires` calls
[`voc-miner`](https://github.com/fatimaarshad-blip/voc-miner) for verbatim Reddit
and YouTube quotes rather than instructing a model to "search Reddit."

**Wired to brand context.** Where a `flown-brain/` directory is present, the
skills read the brand's own research, personas, and hard rules instead of asking
the user to attach a product document.

**Market sophistication reconstructed.** The source prompts repeatedly reference
a "Market Sophistication Document" that wasn't included. It was rebuilt from the
fragments quoted across the prompts plus Schwartz, and lives at
`evolve-new-mechanism/references/market-sophistication.md`. If the team's own
version surfaces, replace that file.

**Large prompts split.** The video (67KB) and statics (36KB) prompts became a
lean `SKILL.md` plus `references/` loaded on demand.

## Known gaps in the source material

- **Awareness coverage.** `evolve-video-ads` writes for problem-aware and
  product-aware only — the source prompt refuses unaware and most-aware
  explicitly. Unaware is covered by the separate `unaware-ads` skill;
  most-aware / retargeting is unserved.
- **The statics prompt has no awareness gate**, unlike the video prompt. The two
  disagree about who they're addressing. Each skill follows its own source and
  flags the difference rather than silently harmonising them.
- **Example images were lost.** The Angles doc has 16 angle/hook pairs and the
  statics doc has 11 example ads; the written descriptions survived the export,
  the creative did not.
- The video prompt is marked **V1**. If a V2 exists, it should supersede
  `evolve-video-ads`.

## The Product Prompt

The doc's first tab isn't a copy prompt — it's a system prompt for spinning up a
custom project. It isn't a skill, so it's preserved here:

<details>
<summary>Project Goal Prompt</summary>

Hello, I would like to create a custom project tailored to assist our marketing
agency in creating more effective, data-driven ads for our client, an E-commerce
Brand. Brand name: BRAND. Brand website: YOURWEBSITE. The purpose of this custom
project is to support the following key marketing functions for this brand:

**Customer Understanding & Market Trends:** Analyze customer surveys, buyer
personas, and behavioral data to uncover customer preferences, pain points, and
purchasing motivations. Identify market trends and audience segments relevant to
this brand's products.

**Market Research & Competitive Analysis:** Gather and analyze data on
competitors and broader industry trends. Identify opportunities for
differentiation in the brand's positioning and advertising strategies.

**Creative Ideation & Strategy:** Generate new creative concepts and strategies
for ad campaigns based on insights from market data, customer feedback, and
competitive analysis. Provide feedback on existing ideas, suggesting improvements
grounded in customer insights and market trends.

**Scriptwriting & Copy Development:** Assist with crafting persuasive, targeted
scripts for ads and other marketing materials. Review and critique copywriting to
ensure it resonates with the target audience, incorporating customer pain points
and desires.

**Ad Review & Performance Feedback Loop:** Assist in analyzing post-launch ad
performance by reviewing metrics such as ad spend, ROAS, hook rate, hold rate,
CTR, etc. Provide insights on why certain ads performed well or underperformed,
identifying key learnings from each campaign. Close the feedback loop by
suggesting actionable takeaways from winning and losing ads, incorporating these
learnings into future creative strategies.

**Knowledge Base:** This project should use the attached files as its primary
knowledge base and refer to the information within when providing insights or
recommendations. Whenever this project provides an answer, it should be informed
by the content within the knowledge base.

**Instructions:** Always ground your responses in the content within the
knowledge base. Highlight any recommendations based on specific insights or
principles from the provided data or resources, especially when drawing on
"Breakthrough Advertising." Prioritize relevance to the brand's audience, and use
data to back up your suggestions.

</details>

In Claude Code the equivalent is a `CLAUDE.md` at the project root, or a brand
brain like `flown-brain/`, which the skills already read.

## Credit

Methods: the EVOLVE Master Prompt Doc, and Alexander Kemperman's native
advertising prompt system and swipe bank ([kemperman.com](https://www.kemperman.com/))
for the two native skills. Principles throughout draw on Claude Hopkins
(*Scientific Advertising*), Eugene Schwartz (*Breakthrough Advertising*), John
Caples, Gary Halbert, Robert Cialdini, and Joseph Sugarman.

The native skills teach the *structures* from the swipe bank rather than
reproducing it — the templates are the reusable asset, and lifting the sentences
produces a detectable clone carrying claims you cannot support.
