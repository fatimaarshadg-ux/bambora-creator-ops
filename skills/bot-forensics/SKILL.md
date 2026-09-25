---
name: bot-forensics
description: Archive every paid Genesis bot call with full provenance, record what actually shipped, and mine the difference to reverse-engineer what the bots do — so a free replacement can be built. Use whenever a Genesis bot is called ("run the bot", "call MarioBot", "get me a floor"), whenever a piece is finished and shipped ("this is the final", "I'm happy with this now"), when Fatima reacts to bot copy, or when she asks how the reverse-engineering project is going ("what have we learned", "bot forensics report", "are we ready to drop the bots"). Portable and user-level — works in any project on this machine. Free.
---

# Bot forensics

**Goal, agreed 2026-08-29, running from Sunday 2026-08-30 for about a month:**
Genesis bots are expensive. Archive everything they produce, learn what they
actually do that is worth paying for, and build a free skill that beats them.
By the end of the month, reduce dependence on the bots.

Portable by design: lives at `~/.claude/skills/bot-forensics/`, archive at
`~/.claude/bot-forensics/`, no project paths anywhere. Works from any project and
any Claude session on this machine. Override the archive with
`$BOT_FORENSICS_HOME`; point at a specific Genesis install with `$GENESIS_STREAM`.

## Log my drafts too, not just the bots'

Fatima's point, 2026-08-29: nothing Claude has shipped has survived at 100%
either. She is right, and measuring only the bot would rig the comparison. **Every
draft written here goes into the archive with `--source claude`**, judged by the
same survival metric. If the free replacement is worse, the archive should be able
to say so.

## How to spend the research budget (agreed 2026-08-29)

Fatima authorised extra API spend for one month specifically to learn from the
bots. Spend it on controlled comparisons, not raw volume:

| Call type | What it isolates | Cost |
|---|---|---|
| **Probe** — minimal input | The bot's hidden system prompt, almost undiluted. The closest thing to reading the recipe. | Cheapest — tiny input |
| **Paired** — one brief, 2-3 bots | What each bot actually contributes, so per-bot keep/drop decisions become possible | Medium |
| **Repeat** — same brief, same bot, twice | Fixed structure vs run-to-run variance. Tells us whether "the bot's method" is even stable. | Medium |
| **Real work** | Survival data — the only calls that feed the metric | Normal |

**Use Haiku for probes.** The point is to expose the hidden prompt, not to get
good copy, so the cheap model is the right one. Note that heavy-taxonomy bots
carry ~34K-token hidden prompts, so those calls cost real money whatever the
output length — probe them once, not repeatedly.

**The binding constraint is her editing, not the calling.** "Better = fewer edits"
needs a shipped `final` attached to each floor. Twenty floors with two finals is
worth less than eight floors with eight finals. If calls pile up without finals,
say so rather than quietly banking useless data.

## The one rule

**Every paid bot call goes through this.** A call made outside it is a lost data
point, and lost data points are the main thing that can kill this project. There
is no way to reconstruct provenance afterwards — the existing backfilled runs are
all logged as `unknown-bot` because nothing recorded which bot or model produced
them.

## Commands

```bash
B=~/.claude/skills/bot-forensics/scripts/botlog.py

# Call a bot AND archive it in one step (preferred)
py -3 $B call ad-tagging-bot-@claude-sonnet-4-6 prompt.md

# Probe a bot: minimal input, so the output is mostly its HIDDEN system prompt
py -3 $B probe BOT_SLUG@claude-haiku-4-5 "GoCurl Pro, a curling iron for fine bobs"

# Archive a call that was already made another way
py -3 $B ingest BOT_SLUG@model prompt.md output.md

# Log a draft written HERE, so it is measured the same way as the bot's
py -3 $B ingest claude-code prompt.md draft.md --source claude

# Attach what actually shipped, once she is happy with it
py -3 $B final <run-id> final.md

# Record WHY - the most valuable field in the archive
py -3 $B verdict <run-id> "cut the whole opening, kept the stylist line, the bot's hook was generic"

# See the archive / mine it
py -3 $B list
py -3 $B report
```

`final` prints the survival rate immediately — what fraction of the bot's words
made it into the shipped piece. That single number is the project's core metric.

## What each phase needs

**On every bot call:** nothing extra from Fatima beyond using `call` instead of
invoking genesis-stream directly.

**When a piece is done:** `final` plus a one-line `verdict`. Thirty seconds. The
diff shows *what* changed; only she knows *why*, and the why is the signal.

**Never:** invent a rubric rule from the report without her confirming it. The
report is descriptive statistics, not findings.

## Reading the report honestly

The report is weak until there are roughly **10-15 pairs**. Below that it cannot
separate a bot habit from the vocabulary of whichever paragraph happened to be
cut. Say so rather than over-reading it.

What to watch as pairs accumulate:

- **Survival rate.** Low survival = the bot's words are being thrown away, so what
  is being bought is structure, not prose. High survival = the prose itself is the
  value, and beating it is harder.
- **Recurring cut words** that are *not* topic words — those are genuine bot tics.
- **Em-dashes and banned words** in the floors: pure waste the free side must fix
  every time.
- **Which bots** produce high-survival output versus low. Some may be worth their
  cost and others not. That is a per-bot decision, not a blanket one.

## Current state, 2026-08-29

Four runs backfilled from `genesis-refine/runs`, all `unknown-bot`. Two have
shipped versions attached:

| Pair | Floor | Shipped | Survival |
|---|---|---|---|
| claire-bob | 1,755w | 855w | **8%** |
| claire-bob v4 | 1,013w | 1,013w | **100%** |

Two data points pointing in opposite directions, so **no conclusion yet**. The 8%
case is encouraging for the project — nearly all of the bot's prose was discarded
and the shipped piece was built in the free local pass. The 100% case is the
opposite. This is exactly why volume matters.

## The final test must be blind

When a candidate free skill exists, the comparison has to be blind: same brief,
bot writes one, skill writes one, Fatima judges without knowing which is which.
Anything less and the skill's author is grading its own homework. **Do not declare
the free version better on the basis of my own read.**

## Open items

- **Success metric.** Fatima to choose: fewer edits to reach her taste (measurable
  now) versus better in-market performance (the real arbiter, needs ad data and
  probably longer than a month). Working assumption is the first.
- **Volume.** If she runs only a handful of concepts a month, the sample stays too
  small to reverse-engineer anything. Ask, and say plainly if the timeline is
  unrealistic.
- **Older outputs.** Any bot outputs in Downloads, Drive, Notion or old chats are
  worth ingesting — the archive currently starts 2026-08-28.
- **Cost.** Record what the bots actually cost so the saving can be stated at the
  end.

## What cannot be done

The bots' system prompts are not readable — genesis-refine notes some carry
~34K-token hidden prompts. Everything here is inference from input/output pairs,
never the recipe itself. Do not claim otherwise.
