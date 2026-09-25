# Optional free credentials

The default Reddit path needs nothing. These two add coverage and both are
genuinely free — no card, no billing account, no trial that expires.

## Reddit official API (~2 minutes)

Adds current data and complete thread fetches (every comment in a discussion,
nested). Reddit's own search only indexes post titles and selftext, never
comment bodies — so this complements the archive rather than replacing it.

1. Sign in at <https://www.reddit.com/prefs/apps>
2. **create another app…** at the bottom
3. Name it anything. Choose type **script**.
4. Redirect URI: `http://localhost:8080` (unused, but required)
5. **create app**
6. The client id is the string under the app name; the secret is labelled
   `secret`.

```bash
echo 'export REDDIT_CLIENT_ID="your_id"'     >> ~/.zshrc
echo 'export REDDIT_CLIENT_SECRET="secret"'  >> ~/.zshrc
source ~/.zshrc
```

Free tier is 100 requests/minute, which is far more than this tool uses.
There is no paid upgrade prompt and no usage bill.

## YouTube Data API v3 (~5 minutes)

10,000 quota units per day, free, **with no billing account attached**. If a
page ever asks for a card, you have wandered into a different Google product —
back out; YouTube Data API v3 does not require one.

1. <https://console.cloud.google.com/> → create a project
2. **APIs & Services → Library** → search "YouTube Data API v3" → **Enable**
3. **APIs & Services → Credentials** → **Create credentials → API key**
4. Restrict the key to YouTube Data API v3 (good hygiene; optional)

```bash
echo 'export YOUTUBE_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc
```

Budgeting the quota is worth understanding, because the two operations differ
by a factor of a hundred:

| Operation | Units | Meaning |
|---|---|---|
| `search.list` | 100 | finding videos is the expensive part |
| `commentThreads.list` | 1 | up to 100 comments per unit |

So 10,000 units/day is roughly 100 video searches, *or* a handful of searches
plus hundreds of thousands of comments. Find a few relevant videos, then
harvest their comments exhaustively — that pattern barely dents the quota.

## Where to put credentials

`~/voc-data/credentials.env` (mode 600) is the recommended home:

```
YOUTUBE_API_KEY=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
```

Shell config works too, but only for shells that read it. `~/.zshrc` is loaded
by interactive shells only, so a key set there vanishes under cron, launchd, or
any script — and the tool keeps running, quietly minus that source. The config
file is read in every context. Environment variables still win when both exist,
so one-off overrides remain easy.

Verify either one with:

```bash
py -3 ~/.claude/skills/voc-miner/scripts/voc.py doctor
```
