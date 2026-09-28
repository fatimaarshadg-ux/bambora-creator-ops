#!/usr/bin/env python3
"""TikTok creator check without a browser (no page loads, so no 403 blocks).

  tt.py <handle> [--videos 6] [--comments 15] [--download DIR]

Prints the recent videos (pinned included) with views, likes and comment
counts, plus the first comments on each. Needs yt-dlp. --download saves the
most-viewed recent video for media-watcher.
"""
import json, os, shutil, subprocess, sys, time, urllib.request, argparse
from pathlib import Path
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36'


def ytdlp():
    """Find yt-dlp. A shell started before the PATH entry existed does not have it,
    which used to fail with a bare WinError 2 and no hint about the cause. The media
    watcher ships its own copy, so fall back to that."""
    found = shutil.which('yt-dlp')
    if found:
        return found
    for cand in (Path.home() / 'claude-media-watcher/bin/yt-dlp.exe',
                 Path.home() / 'claude-media-watcher/bin/yt-dlp'):
        if cand.exists():
            return str(cand)
    sys.exit('yt-dlp not found. Install it, or restore ~/claude-media-watcher/bin/yt-dlp.exe')


YTDLP = ytdlp()


def videos(handle, n):
    out = subprocess.run([YTDLP, '--flat-playlist', '-I', f'1:{n}', '--print',
                          '%(id)s\t%(view_count)s\t%(like_count)s\t%(comment_count)s\t%(timestamp)s\t%(title).80s',
                          f'https://www.tiktok.com/@{handle.lstrip("@")}'], capture_output=True, text=True, timeout=180)
    rows = []
    for line in out.stdout.splitlines():
        p = line.split('\t')
        if len(p) >= 6:
            rows.append(dict(id=p[0], views=p[1], likes=p[2], comments=p[3], ts=p[4], title=p[5]))
    return rows, out.stderr[-300:]

def comments(vid, n):
    url = f'https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={vid}&count={n}&cursor=0'
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://www.tiktok.com/'})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=30))
        return [(c['user'].get('unique_id'), c.get('text', '')) for c in (d.get('comments') or [])]
    except Exception as e:
        return [('ERR', str(e)[:100])]

if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('handle'); a.add_argument('--videos', type=int, default=6)
    a.add_argument('--comments', type=int, default=15); a.add_argument('--download')
    o = a.parse_args(); h = o.handle.lstrip('@')
    rows, err = videos(h, o.videos)
    if not rows: print('NO VIDEOS', err); sys.exit(1)
    for r in rows:
        print(f"\n## {r['id']} views={r['views']} likes={r['likes']} comments={r['comments']} :: {r['title']}")
        if o.comments and r['comments'] not in ('0', 'NA', 'None'):
            for u, t in comments(r['id'], o.comments): print(f'  - {u}: {t[:100]}')
            time.sleep(1.5)
    if o.download:
        top = max(rows, key=lambda r: int(r['views']) if r['views'].isdigit() else 0)
        subprocess.run([YTDLP, '-q', '-f', 'b[height<=720]/b', '-o', f"{o.download}/{h}_{top['id']}.%(ext)s",
                        f"https://www.tiktok.com/@{h}/video/{top['id']}"])
        print('\nDOWNLOADED', top['id'])
