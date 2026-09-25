#!/usr/bin/env python3
"""Frames for every video in the creator database, so each creator's style can be watched.

  fetch_media.py            process videos not done yet (safe to rerun daily; only new ones run)
  fetch_media.py --slug X   only one creator

For each submission: 6 frames spread across the video, stitched into one contact sheet
db/media/<slug>/<trybe_id>.jpg, plus duration. ffmpeg reads straight from the short-lived
signed URL, so no full video download is kept. Transcripts already sit in creators.json.
"""
import json, os, subprocess, sys, tempfile, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, 'db'); MEDIA = os.path.join(DB, 'media')
sys.path.insert(0, HERE)
from build_db import api  # same DPAPI key and retry logic

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit('needs Pillow: py -3 -m pip install --user pillow')


def duration(url):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', url],
                         capture_output=True, text=True, timeout=120).stdout.strip()
    try: return float(out)
    except ValueError: return 0.0


def sheet(slug, s):
    dest = os.path.join(MEDIA, slug, s['trybe_id'] + '.jpg')
    if os.path.exists(dest): return 'skip'
    d = api('/submissions/' + s['id'])
    url = ((d or {}).get('asset') or {}).get('url')
    if not url: return 'no-asset'
    dur = duration(url) or 30
    frames = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, t in enumerate([dur * f for f in (0.03, 0.18, 0.35, 0.52, 0.7, 0.88)]):
            f = os.path.join(tmp, f'{i}.jpg')
            try:
                subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', url, '-frames:v', '1',
                                '-vf', 'scale=240:-2,format=yuvj420p', '-strict', 'unofficial', f], timeout=120)
            except subprocess.TimeoutExpired:
                continue  # a slow .mov frame; skip it rather than stop the whole run
            if os.path.exists(f): frames.append((t, Image.open(f).convert('RGB')))
        if not frames: return 'no-frames'
        w = 240; h = max(im.height for _, im in frames)
        out = Image.new('RGB', (w * len(frames), h + 20), 'white'); dr = ImageDraw.Draw(out)
        for k, (t, im) in enumerate(frames):
            out.paste(im, (k * w, 20)); dr.text((k * w + 4, 4), f'{t:.0f}s / {dur:.0f}s', fill='black')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        out.save(dest, quality=70)
    meta = os.path.join(MEDIA, slug, 'durations.json')
    m = json.load(open(meta)) if os.path.exists(meta) else {}
    m[s['trybe_id']] = round(dur, 1); json.dump(m, open(meta, 'w'))
    return 'ok'


def safe_sheet(slug, s):
    # one slow or broken video must never stop the run; it is retried on the next run
    try:
        return sheet(slug, s)
    except Exception as e:
        return 'error: ' + type(e).__name__


def main():
    db = json.load(open(os.path.join(DB, 'creators.json')))
    only = sys.argv[sys.argv.index('--slug') + 1] if '--slug' in sys.argv else None
    jobs = [(c['slug'], s) for c in db.values() if not only or c['slug'] == only for s in c['submissions']]
    with ThreadPoolExecutor(3) as ex:
        res = list(ex.map(lambda j: (j[0], j[1]['trybe_id'], safe_sheet(*j)), jobs))
    from collections import Counter
    print(Counter(r[2] for r in res))
    for r in res:
        if r[2] not in ('ok', 'skip'): print('  ', r)


if __name__ == '__main__':
    main()
