#!/usr/bin/env python3
"""Find popular TikTok videos (incl. TikTok Shop affiliate videos) without the browser.

TikTok blocks its own search and hashtag pages for scripts, so this finds video URLs
through web search (DuckDuckGo HTML, then Bing as a fallback), then reads each video's
stats with yt-dlp and ranks them by views.

Usage:
  tt_find.py "baby carrier honest review" "mom must haves" --min-views 100000
  tt_find.py --shop "baby carrier" "postpartum"      # TikTok Shop style queries
  tt_find.py ... --seen ~/claude-setup/work/inspo/seen.txt --out results.tsv

Output TSV: views, likes, upload_date, creator, url, title
"""
import argparse, html, json, re, subprocess, sys, time, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"
VID = re.compile(r"https?://(?:www\.)?tiktok\.com/@[\w.\-]+/video/\d+")
SHOP_SUFFIXES = ["tiktok shop", "#tiktokshop review", "tiktok made me buy it"]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "ignore")


def search(q):
    found = []
    for base in ("https://html.duckduckgo.com/html/?q=", "https://www.bing.com/search?count=50&q="):
        try:
            page = html.unescape(urllib.parse.unquote(fetch(base + urllib.parse.quote(f"site:tiktok.com {q}"))))
            found += VID.findall(page)
        except Exception as e:
            print(f"  search failed ({base.split('/')[2]}): {e}", file=sys.stderr)
        time.sleep(1.5)
    return list(dict.fromkeys(u.replace("://tiktok", "://www.tiktok") for u in found))


def stats(url):
    try:
        out = subprocess.run(["yt-dlp", "--socket-timeout", "20", "--skip-download", "-j", url],
                             capture_output=True, text=True, timeout=60).stdout
        d = json.loads(out)
        return [d.get("view_count") or 0, d.get("like_count") or 0, d.get("upload_date", ""),
                d.get("uploader", ""), url, (d.get("title") or "").replace("\t", " ").replace("\n", " ")[:100]]
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("queries", nargs="*")
    ap.add_argument("--urls-file", help="also rank these TikTok URLs (one per line), e.g. from the Brave search tool; "
                                        "DuckDuckGo and Bing often block scripted searches")
    ap.add_argument("--shop", action="store_true", help="add TikTok Shop phrasing to each query")
    ap.add_argument("--min-views", type=int, default=100000)
    ap.add_argument("--seen", help="file of URLs already used; they are skipped")
    ap.add_argument("--out")
    a = ap.parse_args()

    seen = set()
    if a.seen:
        try:
            seen = set(open(a.seen).read().split())
        except FileNotFoundError:
            pass
    qs = [f"{q} {s}" for q in a.queries for s in SHOP_SUFFIXES] if a.shop else a.queries
    urls = []
    for q in qs:
        got = search(q)
        print(f"{len(got):3d} urls  {q}", file=sys.stderr)
        urls += got
    if a.urls_file:
        urls += VID.findall(open(a.urls_file).read())
    urls = [u for u in dict.fromkeys(urls) if u not in seen]
    rows = []
    for u in urls:
        s = stats(u)
        if s and s[0] >= a.min_views:
            rows.append(s)
        time.sleep(1.5)  # normal pace, TikTok rate limits fast callers
    rows.sort(key=lambda r: -r[0])
    lines = ["\t".join(map(str, r)) for r in rows]
    if a.out:
        open(a.out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
