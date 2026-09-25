# Source coverage, costs, and honest limits

## What this tool covers

| Source | Cost | Account | Freshness | What it searches |
|---|---|---|---|---|
| Arctic Shift | free | none | today, back to ~2010 | comment + post bodies, scoped to a subreddit |
| PullPush | free | none | lags months | global comment search — used to find subreddits |
| Reddit official API | free | free app | live | post titles/selftext; full threads by id |
| YouTube Data API | free | free key | live | video comments and replies |

## How far back the data goes

Sampling r/beauty (created 2008) by year returns comments from 2010 onward,
and nothing for 2008. So roughly **2010 to today** is retrievable, with the
usual caveat that a subreddit cannot predate its own creation — an empty 2019
for r/finehair means that community did not exist yet, not that the archive
stops there. Comments deleted or removed by moderators are absent regardless
of date.

Depth per run is capped at 60 pages (~6,000 records) per subreddit per keyword.
Prefer narrowing `--after` / `--before` over raising that cap.

## Why Reddit needs two sources

Reddit's own search has never indexed comment bodies, and the free global
comment search that researchers relied on (Pushshift) was shut off to the
public in 2023. What remains:

- **Arctic Shift** is current and reliable but requires a subreddit or author
  scope for text search. No global "search all of Reddit" endpoint.
- **PullPush** does offer global search, but the archive lags real time by
  months and it rate-limits aggressively.

Hence the two-stage design: PullPush (or the official API) answers *where* the
conversation happens, Arctic Shift harvests those places deeply and freshly.
When PullPush is rate-limited, discovery degrades to subreddit-name matching —
weaker, but the harvest itself is unaffected.

**Arctic Shift's server-side text filter times out unpredictably** under load,
returning 422 "Timeout. Maybe slow down a bit" on queries that worked minutes
earlier. This is a property of the service, not of the query, so retrying
harder doesn't help. The tool falls back to pulling recent comments unfiltered
(about a second per hundred, essentially never times out) and matching the
phrase locally. Slower per quote, but runs finish.

## X / Twitter — no free path

There is no honest way to give you free X search. Laying out the options so
the tradeoff is yours:

| Option | Cost | Verdict |
|---|---|---|
| X API free tier | $0 | Post-only. **Zero** read/search access. Useless here. |
| X API Basic | ~$200/mo | 10k posts/month read. The only sanctioned search path. |
| X API Pro | ~$5,000/mo | Full search. Enterprise pricing. |
| Nitter mirrors | $0 | Almost all dead since 2024. Not dependable. |
| Scraping x.com | $0 | Against their terms, login-walled, actively blocked. Not built here, and not recommended. |

If X specifically matters, the realistic options are paying for Basic, or
using X's own search in a browser and copying quotes manually for low volume.
This is also, notably, the main thing Apify was actually selling — the proxy
infrastructure to get at sources that block automated access. That part is
genuinely hard to replace for free, and it's fair to say so rather than
pretend otherwise.

## Sources deliberately not included

Amazon, Sephora, Ulta, Trustpilot and similar review sites are excluded on
purpose. They block automated access aggressively and their terms prohibit
scraping; getting through reliably requires rotating residential proxies,
which is the expensive part of the commercial tools and not something to
reimplement casually. If review-site data matters, the Adlicio connector's
`scrape_url` already covers several of these and is the cleaner route.

## What "free" means here

No card, no billing account, no trial clock, no per-request charge on any path
described in this document. The optional credentials in `setup.md` are free
tiers that do not convert to paid without an explicit upgrade you would have
to seek out. The real costs are time (runs are rate-limited by courtesy to
volunteer-run archives) and coverage (no X, no review sites).
