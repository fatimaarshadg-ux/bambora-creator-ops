#!/usr/bin/env python3
"""voc — free voice-of-customer mining from public discussion sources.

Standard library only. No pip install, no API costs, no account required for
the default Reddit archive path.

  voc.py doctor
  voc.py search "fine hair" --limit 300
  voc.py search "fine hair" --subreddit HaircareScience --sources archive,youtube
  voc.py thread https://reddit.com/r/x/comments/abc123/...
  voc.py quotes --contains "fine hair" --min-score 5
  voc.py export --format csv -o quotes.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

import time  # noqa: E402

from vocmine import arctic, discover as disc, http, reddit  # noqa: E402
from vocmine.checkpoint import Checkpoints  # noqa: E402
from vocmine.store import Store, is_bot, is_dead, match, near_match  # noqa: E402
from vocmine.youtube import YouTube  # noqa: E402

DEFAULT_STORE = os.path.expanduser("~/voc-data/corpus.jsonl")


def c(s, code):
    return s if not sys.stdout.isatty() else "\033[%sm%s\033[0m" % (code, s)


def bold(s):
    return c(s, "1")


def dim(s):
    return c(s, "2")


# ------------------------------------------------------------------ doctor ---

def cmd_doctor(args):
    print(bold("voc-miner source check"))
    print()
    ok = True

    print("  " + bold("Arctic Shift") + dim("  — primary source, no account needed"))
    sys.stdout.flush()
    try:
        # No text predicate: this is the one query shape that never times out.
        rows = arctic.scan_comments("", "AskReddit", limit=1, scan_cap=100)
        when = (rows[0].get("created") or "?")[:10] if rows else "?"
        print("    " + c("working", "32") + "  newest comment available: %s" % when)
        print(dim("    searches comment bodies inside a subreddit; current to today"))
    except Exception as e:
        ok = False
        print("    " + c("unreachable", "31") + "  %s" % str(e)[:90])
    print()

    print("  " + bold("PullPush") + dim("  — global search, used only to find subreddits"))
    sys.stdout.flush()
    try:
        http.fetch_json(
            "https://api.pullpush.io/reddit/search/comment/?q=test&size=1",
            delay=0.1, retries=0, timeout=20,
        )
        print("    " + c("working", "32"))
    except Exception as e:
        # Not fatal: discovery falls back to name matching, and every harvest
        # runs through Arctic Shift regardless.
        print("    " + c("rate-limited or down", "33") + dim("  (%s)" % str(e)[:50]))
        print(dim("    discovery still works via name matching; harvesting unaffected"))
    print()

    r = reddit.RedditLive()
    print("  " + bold("Reddit live API") + dim("  — free credentials, 100 req/min"))
    if not r.configured:
        print("    " + c("not configured", "33") + "  set REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET")
        print(dim("    optional. adds current data + complete thread fetches."))
        print(dim("    setup: references/setup.md (about 2 minutes, free)"))
    else:
        try:
            r.token()
            print("    " + c("authenticated", "32"))
        except Exception as e:
            ok = False
            print("    " + c("failed", "31") + "  %s" % e)
    print()

    y = YouTube()
    print("  " + bold("YouTube Data API v3") + dim("  — free key, 10k units/day, no billing"))
    if not y.configured:
        print("    " + c("not configured", "33") + "  set YOUTUBE_API_KEY")
        print(dim("    setup: references/setup.md (about 5 minutes, free)"))
    else:
        try:
            y.search_videos("test", limit=1)
            print("    " + c("authenticated", "32"))
        except Exception as e:
            ok = False
            print("    " + c("failed", "31") + "  %s" % e)
    print()

    print("  " + bold("X / Twitter"))
    print("    " + c("no free path", "31"))
    print(dim("    X removed free search access. See references/coverage.md for"))
    print(dim("    what the remaining options cost and which are worth it."))
    print()

    store = args.store
    if os.path.exists(store):
        s = Store(store)
        print("  " + bold("corpus") + "  %s  (%d records)" % (store, len(s)))
    else:
        print("  " + bold("corpus") + dim("  none yet at %s" % store))
    return 0 if ok else 1


# ------------------------------------------------------------------ search ---

def _resolve_subreddits(args, q, live):
    if args.subreddit:
        subs = [x.strip().lstrip("r/") for x in args.subreddit.replace(",", " ").split() if x.strip()]
        print(dim("    using %d subreddit(s) you specified" % len(subs)))
        return subs
    print(dim("    finding subreddits that discuss this…"))
    sys.stdout.flush()
    rows = disc.discover(q, limit=args.subs, live=live, verbose=True)
    subs = [r["subreddit"] for r in rows]
    for r in rows:
        n = format(r["subscribers"], ",") if r.get("subscribers") else "?"
        print(dim("      r/%-24s %10s  (%s)" % (r["subreddit"], n, ",".join(r["signals"]))))
    return subs


def cmd_discover(args):
    live = reddit.RedditLive()
    for q in args.query:
        print(bold("\nsubreddits discussing %r" % q))
        rows = disc.discover(q, limit=args.subs, live=live, verbose=True)
        if not rows:
            print("  nothing found — try a broader phrase")
            continue
        print()
        for r in rows:
            n = format(r["subscribers"], ",") if r.get("subscribers") else "?"
            print("  r/%-26s %12s subs   %s" % (r["subreddit"], n, ",".join(r["signals"])))
        print(dim("\n  harvest them with:"))
        print(dim("    voc.py search %r --subreddit %s" % (q, ",".join(r["subreddit"] for r in rows[:6]))))
    return 0


def _windows(after, before, n):
    """Split a date range into n equal windows, newest first.

    Sampling matters more than it first appears. The archive returns newest
    first and stops at the limit, so a plain run of 240 records came back
    entirely from a single month — a fine snapshot of current language, but
    useless for "is this complaint growing?" and quietly unrepresentative if
    you read it as the whole picture. Splitting the range and taking a share
    from each window gives an even spread across time for the same total.
    """
    end = arctic._epoch(before) or int(time.time())
    start = arctic._epoch(after)
    if start is None:
        # Three years covers most product-cycle questions without reaching
        # back into eras where the vocabulary has drifted too far to compare.
        start = end - (3 * 365 * 24 * 3600)
    if n < 2 or end <= start:
        return [(after, before)]
    step = (end - start) // n
    out = []
    for i in range(n):
        w_start = start + i * step
        w_end = start + (i + 1) * step if i < n - 1 else end
        out.append((w_start, w_end))
    return list(reversed(out))


def _grade(recs, phrase):
    """Sort records into exact hits, near phrasings, and things to discard.

    The archive's text filter matches all the query's words anywhere in a
    comment, so "fine hair" also returns "Cantu was created for Black hair, so
    it's fine for 4A-C types" — where "fine" means "acceptable". Grading here
    rather than trusting the server is what keeps the related tier worth
    reading: a near hit has to keep the words in order inside one sentence,
    which admits "fine, dense, wavy hair" and rejects the coincidences.

    Returns (kept, n_exact). Records that are neither are dropped, because a
    corpus that quietly fills with coincidental word overlap stops being
    evidence of anything.
    """
    words = _words([phrase])
    kept, exact = [], 0
    for r in recs:
        ok, _ = match(r, [phrase], mode="any")
        if ok:
            r["exact"] = True
            exact += 1
            kept.append(r)
            continue
        near, _ = near_match(r, words)
        if near:
            r["exact"] = False
            kept.append(r)
    return kept, exact


def cmd_search(args):
    store = Store(args.store)
    cks = Checkpoints(args.checkpoints)
    if args.reset:
        for q in args.query:
            cks.reset(q)
        cks.save()
        print(dim("checkpoints cleared for %s" % ", ".join(repr(q) for q in args.query)))
    live = reddit.RedditLive()
    total_added = 0
    total_exact = 0
    reddit_added = reddit_exact = 0
    yt_added = yt_exact = 0

    sources = [x.strip().lower() for x in (args.sources or "").split(",") if x.strip()]

    for q in args.query:
        print(bold("\n· %r" % q))

        subs = []
        if "reddit" in sources:
            subs = _resolve_subreddits(args, q, live)
            if not subs:
                print(c("    no subreddits to search — pass --subreddit explicitly", "33"))
            print()

        per = max(1, args.limit // max(len(subs), 1))
        for sub in subs:
            got = 0
            def _prog(seen, hits, _sub=sub):
                # Scanning reads far more than it keeps, so without this a
                # subreddit with few matches looks identical to a hung process.
                # In a terminal the line rewrites itself; piped to a log, a
                # carriage return renders as noise, so throttle to milestones.
                if sys.stdout.isatty():
                    sys.stdout.write("\r    r/%-24s scanning… %d read, %d kept"
                                     % (_sub, seen, hits))
                    sys.stdout.flush()
                elif seen % 1000 == 0:
                    print("    r/%-24s scanning… %d read, %d kept" % (_sub, seen, hits))

            resume_before = args.before
            if args.resume and args.spread < 2:
                # Picking up where the last run stopped is what makes repeat
                # runs productive; with --spread the windows already dictate
                # where to look, so resuming would fight them.
                ck = cks.oldest("reddit", q, sub)
                if ck:
                    resume_before = ck
                    print(dim("    r/%-24s resuming before %s"
                              % (sub, arctic.utc_iso(ck)[:10])))

            try:
                wins = _windows(args.after, resume_before, args.spread)
                per_win = max(1, per // len(wins))
                recs = []
                for w_after, w_before in wins:
                    recs += arctic.search_comments(
                        q, sub, limit=per_win, after=w_after,
                        before=w_before if args.spread > 1 else resume_before,
                        query=q, scan_cap=max(600, args.scan_cap // len(wins)),
                        on_progress=_prog)
                recs = [r for r in recs if not is_dead(r) and not is_bot(r)]
                if args.include_posts:
                    recs += [r for r in arctic.search_posts(
                        q, sub, limit=max(20, per // 4), after=args.after,
                        before=args.before, query=q)
                        if not is_dead(r) and not is_bot(r)]
                recs, ex = _grade(recs, q)
                if args.exact:
                    recs = [r for r in recs if r["exact"]]
                    ex = len(recs)
                got = store.add_many(recs)
                stamps = [r.get("created") for r in recs if r.get("created")]
                if stamps:
                    cks.note("reddit", q, sub, arctic._epoch(min(stamps)[:10]), got)
                total_added += got
                total_exact += min(ex, got)
                reddit_added += got
                reddit_exact += min(ex, got)
                near = got - min(ex, got)
                extra = dim("  (%d exact, %d related)" % (min(ex, got), near)) if near else ""
                print("%s    r/%-24s +%d%s%s"
                      % ("\r" if sys.stdout.isatty() else "", sub, got, extra, " " * 20))
            except Exception as e:
                print("%s    r/%-24s %s%s"
                      % ("\r" if sys.stdout.isatty() else "", sub, c(str(e)[:60], "31"), " " * 20))

        if "youtube" in sources:
            y = YouTube()
            if not y.configured:
                print(dim("    youtube: skipped (no YOUTUBE_API_KEY — see references/setup.md)"))
            else:
                try:
                    seen_v = cks.seen_videos(q) if args.resume else set()
                    # Over-fetch, then drop what previous runs already mined,
                    # so a repeat run lands on genuinely new videos rather
                    # than re-downloading the same comment threads.
                    pool = y.search_videos(q, limit=args.videos + len(seen_v) + 10,
                                           region=args.region,
                                           language=args.language,
                                           order=args.yt_order)
                    vids = [v for v in pool if v["video_id"] not in seen_v][: args.videos]
                    if seen_v and not vids:
                        print(dim("    youtube: every matching video already mined; "
                                  "try --yt-order date, a new keyword, or --reset"))
                    cks.add_videos(q, [v["video_id"] for v in vids])
                    print(dim("    youtube: %d videos" % len(vids)))
                    # --limit is the target for the source as a whole, so a
                    # run with 4 videos does not quietly return four times what
                    # was asked for.
                    per_video = max(20, args.limit // max(len(vids), 1))
                    for v in vids:
                        recs = y.comments(v["video_id"], limit=per_video,
                                          query=q, video_title=v["title"])
                        recs = [x for x in recs if not is_dead(x) and not is_bot(x)]
                        # Unlike Reddit, the video itself is the topical filter,
                        # so a reply like "same, mine goes flat by noon" is real
                        # customer language even without the keyword in it. Keep
                        # everything, but grade it so the keyword hits stay
                        # findable and the counts stay honest.
                        graded, ex = _grade(recs, q)
                        if args.exact:
                            recs = graded
                        n = store.add_many(recs)
                        total_added += n
                        yt_added += n
                        yt_exact += ex
                        total_exact += ex
                        print("      %-46s +%-4d (%d mention it)"
                              % ((v["title"] or "")[:46], n, ex))
                except Exception as e:
                    print("    " + c("youtube: %s" % str(e)[:70], "31"))

    cks.save()

    print(bold("\n%d new records" % total_added)
          + dim("  → %s  (corpus: %d)" % (args.store, len(store))))

    # The two sources mean different things by "did not match", so reporting a
    # single blended number would misrepresent both. Reddit results are all
    # keyword hits of one grade or another; YouTube keeps every comment on a
    # topical video, most of which never say the phrase.
    if reddit_added:
        near = reddit_added - reddit_exact
        print(dim("  reddit:  %d hits — %d exact, %d related phrasings like"
                  % (reddit_added, reddit_exact, near)))
        print(dim("           \"fine, dense, wavy hair\" for \"fine hair\""))
    if yt_added:
        print(dim("  youtube: %d comments from topical videos — %d actually say your phrase"
                  % (yt_added, yt_exact)))
        print(dim("           (the rest are on-topic context; --exact keeps only the mentions)"))

    if total_added and not args.quiet:
        print(dim("\ntop quotes (full text via `voc.py quotes`):\n"))
        cmd_quotes(argparse.Namespace(
            store=args.store, contains=list(args.query), mode="any", min_score=None,
            source=None, venue=None, limit=6, max_chars=300, sort="score",
            format="text", output=None, min_words=12,
        ))
    return 0


# ------------------------------------------------------------------ thread ---

def cmd_thread(args):
    # Validate the input before complaining about credentials — a typo'd URL
    # should say so, not send you off to set up an API key you may already have.
    m = re.search(r"/comments/([a-z0-9]+)", args.url)
    if not m:
        print(c("That does not look like a Reddit thread URL.", "31"))
        print(dim("expected something like https://reddit.com/r/sub/comments/abc123/title/"))
        return 1
    r = reddit.RedditLive()
    if not r.configured:
        print(c("Full-thread fetch needs free Reddit credentials.", "31"))
        print("See references/setup.md — about 2 minutes, no cost.")
        return 1
    sub = re.search(r"/r/([^/]+)/", args.url)
    store = Store(args.store)
    recs = r.thread(m.group(1), subreddit=sub.group(1) if sub else None, limit=args.limit)
    recs = [x for x in recs if not is_dead(x) and not is_bot(x)]
    n = store.add_many(recs)
    print("%d comments fetched, %d new → %s" % (len(recs), n, args.store))
    return 0


# ------------------------------------------------------------------ quotes ---

def _words(terms):
    out = []
    for t in terms:
        out.extend(w for w in re.split(r"[^\w]+", t) if len(w) > 2)
    return out


def _iter_filtered(args):
    store = Store(args.store)
    rows = []
    terms = args.contains or []
    for rec in store.read():
        # Filter on read as well as on write, so corpora built before bot
        # detection existed still come out clean.
        if is_dead(rec) or is_bot(rec):
            continue
        if args.source and rec.get("source") != args.source:
            continue
        if args.venue and (rec.get("venue") or "").lower() != args.venue.lower():
            continue
        if args.min_score is not None and (rec.get("score") or 0) < args.min_score:
            continue
        if args.min_words and len((rec.get("text") or "").split()) < args.min_words:
            continue
        ok, hits = match(rec, terms, mode=args.mode)
        # A record stored as "related" has the words apart, so a phrase match
        # fails on it here. Keep it unless the caller asked for exact only —
        # the near-misses are frequently the most vivid customer language.
        if not ok:
            if getattr(args, "exact", False) or not terms:
                continue
            if rec.get("exact") is not False:
                continue
            near_ok, hits = near_match(rec, _words(terms))
            if not near_ok:
                continue
            rec["_related"] = True
        rec["_hits"] = hits
        rows.append(rec)

    if args.sort == "score":
        rows.sort(key=lambda r: (r.get("score") or 0), reverse=True)
    elif args.sort == "date":
        rows.sort(key=lambda r: (r.get("created") or ""), reverse=True)
    elif args.sort == "length":
        rows.sort(key=lambda r: len(r.get("text") or ""), reverse=True)
    return rows


def cmd_quotes(args):
    rows = _iter_filtered(args)
    shown = rows[: args.limit] if args.limit else rows

    if args.format == "json":
        out = json.dumps(shown, ensure_ascii=False, indent=2)
        _emit(out, args.output)
        return 0

    lines = []
    for r in shown:
        text = r.get("text") or ""
        if args.max_chars and len(text) > args.max_chars:
            text = text[: args.max_chars].rstrip() + "…"
        head = "  ".join(x for x in [
            r.get("venue") or r.get("source"),
            r.get("author") or "",
            (r.get("created") or "")[:10],
            ("%s likes" % r["score"]) if r.get("source") == "youtube"
            and r.get("score") is not None
            else (("score %s" % r["score"]) if r.get("score") is not None else ""),
            "· related" if r.get("_related") else "",
        ] if x)
        # Without this a YouTube quote is unattributable without opening the
        # link, and on Reddit the thread title is often what makes a short
        # comment make sense at all.
        context = (r.get("title") or "").strip()
        if args.format == "markdown":
            lines.append("> " + text.replace("\n", "\n> "))
            lines.append("")
            src = "— %s" % head
            if context:
                src += "\n  on: *%s*" % context[:100]
            lines.append(src + " · [source](%s)" % (r.get("url") or ""))
            lines.append("")
        else:
            lines.append(bold(head))
            if context:
                lines.append(dim("on: " + context[:95]))
            lines.append(text)
            lines.append(dim(r.get("url") or ""))
            lines.append("")
    body = "\n".join(lines)
    _emit(body, args.output)
    if not args.output:
        print(dim("%d of %d matching quotes" % (len(shown), len(rows))))
    return 0


def cmd_export(args):
    rows = _iter_filtered(args)
    if args.format == "csv":
        path = args.output or "voc-quotes.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["text", "author", "venue", "source", "kind",
                        "created", "score", "url", "matched_query", "title"])
            for r in rows:
                w.writerow([r.get("text"), r.get("author"), r.get("venue"),
                            r.get("source"), r.get("kind"), r.get("created"),
                            r.get("score"), r.get("url"), r.get("query"), r.get("title")])
        print("%d quotes → %s" % (len(rows), path))
    else:
        args.limit = 0
        return cmd_quotes(args)
    return 0


def _emit(text, path):
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print("written → %s" % path)
    else:
        print(text)


# -------------------------------------------------------------------- main ---

def main(argv=None):
    # Long harvests print progress as they go. Without line buffering Python
    # holds that output whenever stdout is not a terminal — a pipe, a log file,
    # a background run — and a working ten-minute scrape looks like a hang.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass


    p = argparse.ArgumentParser(prog="voc", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--store", default=DEFAULT_STORE, help="JSONL corpus path")
    p.add_argument("--checkpoints", default=None,
                   help="resume-state file (default ~/voc-data/checkpoints.json)")
    sub = p.add_subparsers(dest="cmd")

    d = sub.add_parser("doctor", help="check which sources are working")
    d.set_defaults(func=cmd_doctor)

    dv = sub.add_parser("discover", help="find subreddits that discuss a topic")
    dv.add_argument("query", nargs="+")
    dv.add_argument("--subs", type=int, default=12)
    dv.set_defaults(func=cmd_discover)

    s = sub.add_parser("search", help="keyword-search Reddit (+YouTube) and store results")
    s.add_argument("query", nargs="+", help="one or more keywords/phrases")
    s.add_argument("--subreddit", default=None,
                   help="comma/space separated; omit to auto-discover")
    s.add_argument("--subs", type=int, default=8, help="how many subreddits to auto-discover")
    s.add_argument("--limit", type=int, default=200,
                   help="target records per SOURCE per keyword "
                        "(200 reddit + 200 youtube by default)")
    s.add_argument("--sources", default="reddit", help="add ,youtube to include YouTube")
    s.add_argument("--include-posts", action="store_true", help="also search post bodies")
    s.add_argument("--videos", type=int, default=5, help="YouTube videos per keyword")
    s.add_argument("--region", default=None, metavar="CC",
                   help="YouTube: bias video search to a market, e.g. US, GB, AU. "
                        "Note this does NOT filter who commented.")
    s.add_argument("--language", default=None, metavar="LANG",
                   help="YouTube: bias video search to a language, e.g. en, es")
    s.add_argument("--yt-order", default="relevance",
                   choices=["relevance", "date", "viewCount", "rating"],
                   help="YouTube video ranking (default relevance)")
    s.add_argument("--after", default=None, help="epoch seconds or YYYY-MM-DD")
    s.add_argument("--before", default=None)
    s.add_argument("--spread", type=int, default=1, metavar="N",
                   help="sample evenly across N time windows instead of taking "
                        "the newest N; e.g. --spread 12 over 3 years gives a "
                        "quarterly spread. Reddit only.")
    s.add_argument("--scan-cap", type=int, default=2500,
                   help="max comments read per subreddit when the archive's "
                        "own search is unavailable (default 2500)")
    s.add_argument("--exact", action="store_true",
                   help="keep only the exact phrase; by default related "
                        "phrasings like 'fine, dense, wavy hair' are kept too")
    s.add_argument("--no-resume", dest="resume", action="store_false",
                   help="ignore saved progress and start from the newest again")
    s.add_argument("--reset", action="store_true",
                   help="forget saved progress for these keywords, then run")
    s.add_argument("--quiet", action="store_true")
    s.set_defaults(func=cmd_search, resume=True)

    t = sub.add_parser("thread", help="fetch one Reddit thread in full")
    t.add_argument("url")
    t.add_argument("--limit", type=int, default=500)
    t.set_defaults(func=cmd_thread)

    for name, fn, helptext in (("quotes", cmd_quotes, "show verbatim quotes from the corpus"),
                               ("export", cmd_export, "write quotes to csv/markdown")):
        q = sub.add_parser(name, help=helptext)
        q.add_argument("--contains", nargs="*", default=None)
        q.add_argument("--mode", choices=["any", "all"], default="any")
        q.add_argument("--source", default=None)
        q.add_argument("--venue", default=None)
        q.add_argument("--min-score", type=int, default=None)
        q.add_argument("--exact", action="store_true",
                       help="only exact-phrase hits; omit to include related phrasings")
        q.add_argument("--min-words", type=int, default=6,
                       help="drop one-liners with no substance")
        q.add_argument("--limit", type=int, default=25 if name == "quotes" else 0)
        q.add_argument("--max-chars", type=int, default=0,
                       help="0 = full verbatim text, never truncated")
        q.add_argument("--sort", choices=["score", "date", "length"], default="score")
        q.add_argument("--format", default="text" if name == "quotes" else "csv",
                       choices=["text", "markdown", "json", "csv"])
        q.add_argument("-o", "--output", default=None)
        q.set_defaults(func=fn)

    args = p.parse_args(argv)
    if getattr(args, "checkpoints", None) is None:
        # Keep resume state beside its corpus: two different corpora are two
        # different research projects and must not share progress.
        args.checkpoints = os.path.join(
            os.path.dirname(os.path.abspath(args.store)) or ".", "checkpoints.json")
    if not getattr(args, "cmd", None):
        p.print_help()
        return 0
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\ninterrupted — records already stored are safe")
        return 130


if __name__ == "__main__":
    sys.exit(main())
