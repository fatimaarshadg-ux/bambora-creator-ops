#!/usr/bin/env python3
"""End-of-day Drive filing for approved Trybe videos.

  file_approved.py --list          show approved submissions not yet filed
  file_approved.py --download DIR  download them into DIR with Windows-safe names + manifest.json
  file_approved.py --mark ID ...   record trybe_ids as filed (after upload + rename are verified)
  file_approved.py --seed          mark every currently approved video as filed without downloading

Drive name: {CreatorNameNoSpaces}/fatima/trybe={trybe_id}. "/" isn't allowed in Windows (or Mac) filenames,
so files download as {Name}__fatima__trybe={id}.{ext}; rename in Drive after upload.
Filed ids live in filed.json next to this script (synced via claude-setup).
"""
import json, os, re, subprocess, sys, urllib.error, urllib.request
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')  # emoji and names print on Windows consoles
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__)); LEDGER = os.path.join(HERE, 'filed.json')
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
from trybe_key import get_key  # Windows DPAPI (or env TRYBE_API_KEY); never printed
KEY = get_key()

def api(path):
    r = urllib.request.Request('https://api.jointrybe.com/v1' + path, headers={'Authorization': 'Bearer ' + KEY, 'User-Agent': 'curl/8.7.1'})
    try:
        return json.load(urllib.request.urlopen(r, timeout=60))
    except urllib.error.HTTPError as e:
        hint = ' (the key was rejected: check it with work/common/trybe_key.py --check, ask Fatima whether it was replaced)' if e.code in (401, 403) else ''
        sys.exit(f'Trybe API: HTTP {e.code} on {path.split("?")[0]}{hint}. Nothing was filed.')
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        sys.exit(f'Trybe API: could not connect ({str(e)[:80]}). Check the internet connection and rerun. Nothing was filed.')

def approved():
    out, after = [], None
    while True:
        d = api('/submissions?status=approved&limit=100' + (f'&after={after}' if after else ''))
        out += d.get('data', [])
        if not d.get('has_more'): return out
        after = d.get('next_cursor')

def filed():
    return set(json.load(open(LEDGER, encoding='utf-8'))) if os.path.exists(LEDGER) else set()

def save(ids):
    json.dump(sorted(ids), open(LEDGER, 'w', encoding='utf-8'), indent=0)

def drive_name(s):
    return ''.join(w[:1].upper() + w[1:] for w in re.sub(r'[^A-Za-z0-9 ]', '', s['creator']['name']).split()) + '/fatima/trybe=' + s['trybe_id']

a = sys.argv[1:]
if not a or a[0] == '--list':
    done = filed(); todo = [s for s in approved() if s['trybe_id'] not in done]
    for s in todo: print(s['trybe_id'], drive_name(s), s['created_at'][:10])
    print(len(todo), 'to file')
elif a[0] == '--seed':
    ids = filed() | {s['trybe_id'] for s in approved()}; save(ids); print('seeded', len(ids))
elif a[0] == '--mark':
    ids = filed() | set(a[1:]); save(ids); print('filed total', len(ids))
elif a[0] == '--download':
    dest = a[1]; os.makedirs(dest, exist_ok=True); done = filed(); man = {}
    for s in approved():
        if s['trybe_id'] in done: continue
        d = api('/submissions/' + s['id']); url = d['asset']['url']
        ext = os.path.splitext(url.split('?')[0])[1] or '.mp4'
        safe = drive_name(s).replace('/', '__') + ext
        urllib.request.urlretrieve(url, os.path.join(dest, safe))
        man[safe] = {'drive_name': drive_name(s), 'trybe_id': s['trybe_id']}
        print('downloaded', safe)
    json.dump(man, open(os.path.join(dest, 'manifest.json'), 'w'), indent=1); print(len(man), 'ready in', dest)
