# Trybe applicant review

How new creators in Discovery > Inbox get reviewed. Rules live in memory: `bambora-creator-acceptance-criteria.md`. Follow-ups are tracked in `trybe-applicant-followups.md`.

## Routine
1. Open Discovery > Inbox, set Per page to 100.
2. Read every card's creator object from React props (country, IG/TikTok URLs, languagesSpoken). Open each profile modal by script to get `portfolioItems` (featured video URLs on cdn.jointrybe.com, public, no auth needed). Use a MessageChannel-based sleep: background tabs throttle setTimeout.
3. Export by prepending an `<article>` with the text and reading it with get_page_text (javascript_tool output truncates around 1,000 chars). Remove the article afterwards.
4. Discovery > Messages: the full text is in each row's second `td` (textContent). Only the 50 most recent are listed.
5. `scripts/yap.py`: first 25s of audio from each creator's first 2 featured videos, transcribed with faster-whisper small, plus 3 frames per video. `scripts/sheet.py` builds contact sheets. `scripts/energy.py` gives words per second plus loudness and pitch variation.
6. Social stats: TikTok profile `[data-e2e=followers-count]` / `likes-count`; Instagram `og:description` meta. Load pages at a normal pace (3 seconds or more). Loading TikTok video URLs directly got a 403.
7. yt-dlp returns TikTok video view, like and comment counts without a browser, but not the comment text.

`2026-09-23/`: the first run (78 applicants): apps.tsv, transcripts (yap.jsonl), energy.txt.
