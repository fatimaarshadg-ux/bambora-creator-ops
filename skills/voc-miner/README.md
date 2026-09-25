# voc-miner

Free voice-of-customer mining. Pulls **verbatim** customer comments from Reddit
and YouTube, with a link back to every source.

Built as a no-cost replacement for Apify-style scraping tools. Standard-library
Python 3.9+ — no `pip install`, no account needed for the default Reddit path.

## Quick start

```bash
py -3 scripts/voc.py doctor                 # what's working
py -3 scripts/voc.py discover "fine hair"   # where is this discussed?
py -3 scripts/voc.py search "fine hair" --spread 8 --limit 400
py -3 scripts/voc.py quotes --contains "fine hair" --sort score
py -3 scripts/voc.py export --contains "fine hair" --format csv -o quotes.csv
```

Results accumulate in `~/voc-data/corpus.jsonl`, deduped, so the corpus
compounds and re-querying it is instant and offline.

## Sources

| Source | Cost | Setup | Coverage |
|---|---|---|---|
| Reddit (Arctic Shift) | free | none | today back to ~2010 |
| Reddit (PullPush) | free | none | subreddit discovery |
| Reddit official API | free | ~2 min | full threads |
| YouTube Data API | free | ~5 min | 10k units/day, no billing |
| X / Twitter | — | — | **no free tier exists** |

Optional credentials go in the environment, never in this repo:

```bash
export YOUTUBE_API_KEY="..."
export REDDIT_CLIENT_ID="..."
export REDDIT_CLIENT_SECRET="..."
```

## As a Claude Code skill

Copy this directory to `~/.claude/skills/voc-miner/` and Claude picks it up
automatically. `SKILL.md` carries the full workflow and the caveats worth
knowing before you trust a result.

## Notes worth reading before relying on it

- Results are **not a representative sample** — see the sampling section in
  `SKILL.md`. Use `--spread` for anything time-comparative.
- Rate limiting is deliberately conservative because Arctic Shift and PullPush
  are volunteer-run archives. Don't raise it; narrow the query instead.
- No user-agent rotation, no proxies, no evasion — this reads public content
  through published interfaces and identifies itself honestly.
