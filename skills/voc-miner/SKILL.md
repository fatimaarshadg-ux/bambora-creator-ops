---
name: voc-miner
description: Mine verbatim customer language from public discussion sources — Reddit comments and YouTube comments — for free, with no API costs, no scraping subscription, and no account required for the default path. Use this whenever the user wants to know what real customers say about a topic, product, ingredient, symptom, or competitor: "what are people saying about X", "find me real quotes about X", "customer pain points for Y", "voice of customer research", "what do people complain about with Z", "I need real customer language for this ad", "pull comments about X", "what's the chatter on X". Works for any topic or vertical — skincare, supplements, SaaS, fitness, finance, pets — the keyword is entirely yours; nothing about any category is built in. Also use it when the user mentions Apify, Brandwatch, Sprout, Talkwalker, Bright Data, or any paid scraping/social-listening tool and wants a free alternative. Strongly prefer this over ad-hoc curl or WebFetch for customer-language research — it handles rate limits, failover, dedupe, and keeps a reusable corpus, none of which one-off fetching does.
---

# voc-miner

Pull what real people actually said, word for word, from public discussions —
and keep it in a corpus you can query again without re-scraping.

The output is always **verbatim customer language with a link back to the
source**. That constraint is the whole point of the tool: a summary of what
customers feel is worth very little for copywriting or positioning work,
because the persuasive power lives in the specific words people chose. When
you present findings, quote exactly and attribute; never smooth out typos,
capitalisation, or profanity, and never merge several people's phrasing into
one tidy sentence.

## Setup

Nothing to install — standard library Python 3.9+, no pip, no keys for the
default path. The CLI lives at `scripts/voc.py`.

```bash
py -3 ~/.claude/skills/voc-miner/scripts/voc.py doctor
```

Run `doctor` first when anything looks wrong; it reports which sources are
live and which optional credentials are missing. Two sources are optional
upgrades, both free — see `references/setup.md`.

## How searching actually works

Reddit has no free global comment search any more, so this works in two stages.
Understanding the split prevents the most common failure, which is searching
one subreddit and concluding a topic isn't discussed.

**Stage 1 — find where the conversation lives.**

```bash
voc.py discover "fine hair"
```

Merges three signals: subreddits where the phrase genuinely appears, Reddit's
own post search if credentials are set, and subreddit name matching. Adult and
promo subreddits are screened out. Save the good ones — for a given brand the
list stabilises fast, and reusing it makes every later run quicker and better
targeted than re-discovering each time.

**Stage 2 — harvest those communities.**

```bash
voc.py search "fine hair" --subreddit finehair,Haircare,curlyhair --limit 400
```

Omit `--subreddit` and it auto-discovers first.

Results append to `~/voc-data/corpus.jsonl`, deduped by id, so overlapping
runs are cheap and the corpus compounds over time.

### Two grades of match, and why both are kept

The archive's own text filter matches all of a query's words anywhere in a
comment, not the phrase — so it happily returns "Cantu was created for Black
hair, so it's fine for 4A-C types" for `"fine hair"`. Results are therefore
graded locally rather than trusted as returned:

- **exact** — the literal phrase, case-insensitive, on word boundaries. Catches
  "I have fine hair", not "superfine hairline".
- **related** — the same words, in the same order, inside one sentence:
  "fine, dense, wavy hair", "very fine, low porosity hair". These are usually
  the same customer saying the same thing with an adjective in the way, and
  they are frequently the more vivid quotes.
- everything else is discarded, because a corpus that fills with coincidental
  word overlap stops being evidence of anything.

Both grades are kept and labelled. `--exact` narrows to the phrase alone when
precision matters more than reach — but read the related tier before dropping
it; that is where phrasing variety tends to live.

### What gets filtered out automatically

Deleted and removed comments, and automated accounts. AutoModerator alone
replies "it seems like you may be looking for information about X" to every
relevant thread — a perfect keyword match and worthless as customer language.
Bots are filtered on read as well as on write, so corpora built earlier still
come out clean. Detection is deliberately conservative about the disclaimer
phrase: "I am a bot." is filtered, "I am a bot enthusiast" is not, because
dropping a real customer is the more costly mistake.

### Run it again to get more

Repeat runs are the main way to build a corpus. Each one remembers how far back
it reached and starts the next run just before that point, so running the same
command five times gives five batches of new material rather than the same
batch five times:

```bash
voc.py search "fine hair" --subreddit finehair --sources reddit,youtube
```

Measured over three identical runs: 1,066 records, **zero duplicates**, with
Reddit walking backward 08-27 → 08-24 → 08-21 and YouTube moving through six
different videos. `--limit` is the target per source, so the default gives 200
Reddit plus 200 YouTube each time.

This matters more than deduplication does. Dedup stops repeats being *stored*,
but without resume state every run re-reads the same recent comments and throws
them away — the corpus stops growing while the request count climbs, which
looks exactly like the archive being empty.

Resume state lives beside the corpus in `checkpoints.json`. `--no-resume`
ignores it for one run; `--reset` forgets a keyword's progress and starts over.
Because it needs no arguments to keep working, the plain command is safe to
schedule.

Two honest limits: a niche keyword will eventually exhaust a subreddit, and
YouTube will run out of matching videos — the tool says so rather than
returning less and looking successful. Try `--yt-order date`, more subreddits,
or a neighbouring phrase at that point.

### How much you can pull, and sampling bias

**Reddit** is bounded by `--limit` (a target per keyword, divided across the
subreddits in play) and by `MAX_PAGES` — 60 pages of 100, so ~6,000 records per
subreddit per keyword before it stops.

**YouTube** is bounded by the 10,000 free quota units/day, and the two
operations are priced a hundred-fold apart: finding videos costs 100 units per
call, pulling comments costs 1 unit per 100 comments. Five video searches plus
comment harvesting leaves headroom for hundreds of thousands of comments a day.
In practice you run out of *comments that exist* long before quota.

The bias worth knowing about: **the archive returns newest first and stops at
the limit.** A plain 240-record run came back entirely from a single month. It
is a good snapshot of how people talk right now, and misleading if read as the
whole picture. `--spread N` fixes it by dividing the date range into N windows
and taking a share from each:

```bash
voc.py search "fine hair" --subreddit finehair --spread 8 --after 2022-01-01 --limit 240
```

Measured on the same subreddit: without it, 182 records all inside one month;
with `--spread 8`, 184 records across 21 months of 2022–2026. Same cost, four
years of coverage. Use it for any "is this changing?" question. Reddit only —
YouTube's comment ordering can't be steered by date.

Neither source is a representative sample. It is "the most recent N that
matched" and "the most-engaged N on topical videos". Good for finding phrasing
and pain points; not a basis for "most customers think X". Say so when
reporting, and prefer counts over adverbs: "11 of 340 comments mention X" is
honest, "customers frequently mention X" is not.

### Geographic and language filters

YouTube search accepts `--region US` (ISO country code) and `--language en`.
Both bias which videos surface, and neither does what people usually want:
they say nothing about where the *commenters* are, because YouTube exposes no
commenter-location field. A live check showed `--region US` and `--region GB`
returning two of the same three videos, so treat it as a nudge, not a filter.

Reddit has no geographic filter at all — but subreddit choice is a far better
proxy than any API flag. `discover` surfaced r/TeenIndia and r/indiasocial for
"dark circles", and r/AskWomenOver40 and r/GenXWomen for "fine hair". Picking
communities is how you target a demographic here.

### Depth and date range

The archive reaches back to at least **2010**, so year-over-year comparisons
are possible. Bound a run with `--after` / `--before`, which take `YYYY-MM-DD`
or epoch seconds:

```bash
voc.py search "fine hair" --subreddit finehair --after 2024-01-01
```

Paging stops at `MAX_PAGES` (60) per subreddit per keyword — about 6,000
records — or when the subreddit runs out of history, whichever comes first.
Raise it in `vocmine/arctic.py` for a deep historical pull, but prefer
narrowing the date window: it gets the same data with far less load on a
service nobody is paying for. When the archive falls back to scanning,
`scan_cap` (4,000 comments read per subreddit) bounds the hunt so a rare
phrase degrades into a bounded scan rather than an endless crawl.

### When a search returns little

Work through these before concluding the topic is quiet:

- **Wrong subreddits.** Re-run `discover`, or name them explicitly. This is
  the cause most of the time.
- **Phrase too specific.** "fine limp hair" is rarer than "fine hair". Search
  the broad phrase, then filter the corpus locally with `quotes --contains`,
  which costs nothing because the data is already downloaded.
- **Try the customer's words, not the brand's.** People write "my hair looks
  greasy by lunch", not "sebum management". Search several phrasings; each
  one is cheap.

## Getting quotes back out

The corpus is queried locally, so this is instant and repeatable:

```bash
voc.py quotes --contains "fine hair" --min-score 5 --sort score
voc.py quotes --contains "flat" "limp" "greasy" --mode any --format markdown
voc.py export --contains "fine hair" --format csv -o quotes.csv
```

`--max-chars 0` (the default) never truncates. Keep it that way when the
quotes are going into research — a cut-off quote can invert the meaning of
what someone said, and mid-sentence is often exactly where the objection is.

Useful filters: `--min-score` for community-endorsed opinions (a +200 comment
is one many people agreed with), `--min-words` to drop noise like "same",
`--venue r/finehair` to isolate one community, `--sort date` for what's
current versus `--sort score` for what resonated.

## Reporting findings to the user

Group quotes by the theme they reveal, and let the quotes carry the argument:

```
### Pain: hair goes flat by midday
> "washed it this morning and by 2pm it looks like i haven't showered in days"
— r/finehair · u/example · 2026-08-14 · score 340 · [source](url)
```

Two habits that keep this honest and useful:

- **Quote, then interpret** — never the reverse, and never interpretation
  alone. The user asked for verbatim language because they intend to use these
  words; your synthesis is a navigation aid, not the deliverable.
- **Say how much you looked at.** "Across 340 comments in 6 subreddits, 11
  mention X" is actionable. "Customers frequently mention X" is not, and
  quietly overstates what a keyword scrape can support.

Watch for sampling skew and mention it when relevant: subreddits are not a
representative sample of your customers, high-score comments are popular
rather than typical, and people post about problems far more than about
things that simply worked.

## Sources and their limits

`references/coverage.md` has the full picture, including what X/Twitter costs
now and why no free path exists there. The short version:

| Source | Cost | Setup | Notes |
|---|---|---|---|
| Reddit via Arctic Shift | free | none | primary; current to today |
| Reddit global search (PullPush) | free | none | discovery only; often rate-limited |
| Reddit official API | free | ~2 min | current data, full threads |
| YouTube Data API | free | ~5 min | 10k units/day, no billing (see note) |
| X / Twitter | **not free** | — | no free search tier exists |

**YouTube is written but unverified end to end.** The request shapes are
confirmed correct against Google's API — it accepts every parameter and
rejects only a dummy key — but the response parsing has never run against a
real key, because there wasn't one available when this was built. Treat the
first real YouTube run as a test: check that comment text, author, and
timestamps land correctly, and fix `vocmine/youtube.py` if they don't. The
Reddit paths are fully exercised and can be trusted.

If a source is down, say so plainly rather than quietly returning less. A
thin result that looks complete is worse than a clear "PullPush is rate-limited
right now, so I searched by subreddit name instead."

## Staying unblocked

`vocmine/http.py` runs three defences, escalating in severity. They exist so
the tool never becomes a problem for the services it reads from, which is also
the only reliable way to keep it working:

- **throttle** — a minimum gap between requests to a host.
- **adaptive delay** — when a host signals overload (429, or Arctic Shift's
  422 "slow down"), that host's gap widens for the rest of the session and
  narrows again only after sustained success. `Retry-After` is obeyed when
  sent, since a server that states its own limit knows better than any formula.
- **circuit breaker** — after six consecutive failures a host is left alone for
  two minutes rather than kept under load.

Inspect the current state with `vocmine.http.host_status()`.

What this deliberately does **not** do is rotate user agents, cycle proxies, or
otherwise disguise the client. Those techniques exist to defeat blocking rather
than to avoid causing it, they breach the terms of every service involved, and
in practice they turn a temporary rate limit into a permanent ban. Identifying
honestly and slowing down is both the better-behaved option and the one that
keeps working. If a run feels slow, narrow the subreddits or the date window —
do not raise the rate limits.

All of this reads public content through published interfaces. It does not
touch private messages, non-public groups, or anything behind a login, and it
shouldn't be extended to.

## Files

- `scripts/voc.py` — the CLI (doctor, discover, search, thread, quotes, export)
- `scripts/vocmine/` — http (rate limiting, backoff), arctic, reddit, youtube,
  discover, store
- `references/setup.md` — free credentials for the two optional sources
- `references/coverage.md` — what each source covers, costs, and the X situation
