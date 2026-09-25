#!/usr/bin/env python3
"""Creator database for Bambora: one profile per creator in the 5% program (Bambora Affiliates V3)
plus Fatima's 10 protected creators.

  build_db.py            refresh everything from the Trybe Brand API (safe to run daily)
  build_db.py --probe    print which extra endpoints answer (performance, samples)

Writes, next to this script:
  db/creators.json       machine-readable facts per creator (API data only)
  db/profiles/<slug>.md  one readable profile per creator. The block between
                         <!-- facts --> markers is rewritten on every run; everything below
                         "## Notes" (style, DMs, inspo picks, Fatima's comments) is kept.
The Trybe key is read by work/common/trybe_key.py (Windows DPAPI); it is never written anywhere.
"""
import json, os, re, subprocess, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, 'db'); PROF = os.path.join(DB, 'profiles')
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
from trybe_key import get_key  # Windows DPAPI (or env TRYBE_API_KEY); never printed
KEY = get_key()
V3 = 'Bambora Affiliates V3'
PROTECTED = {  # name: creator id (ids fixed because /creators does not list every creator)
    'Cambria Reau': None, 'Sophia Lease': 'creator_ea74b495-ad6b-4ede-8166-f29146816769',
    'Ciara Burnett': 'creator_2a944d2e-bc4c-4247-9e42-4276771dbed7', 'Carissa Lyman': None,
    'Cassie Avery Charvat': None, 'Tasha Clay': None, 'Tayler Raza': None,
    'Mary Saggau': 'creator_ae907998-1f5d-448b-ab13-d0421c41977f', 'Myrka Bustillo': None, 'Lilly Clark': None}


def api(path, tries=6):
    for i in range(tries):
        try:
            r = urllib.request.Request('https://api.jointrybe.com/v1' + path,
                                       headers={'Authorization': 'Bearer ' + KEY, 'User-Agent': 'curl/8.7.1'})
            return json.load(urllib.request.urlopen(r, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in (400, 404): return None
            time.sleep(2 + i * 2)
        except Exception:
            time.sleep(2 + i * 2)
    return None


def paged(path):
    out, after = [], None
    while True:
        sep = '&' if '?' in path else '?'
        d = api(path + sep + 'limit=100' + (f'&after={after}' if after else ''))
        if not d: return out
        out += d.get('data', [])
        if not d.get('has_more'): return out
        after = d.get('next_cursor')


def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def probe():
    for p in ['/creator-performance?limit=1', '/creator-performance?start_date=2025-06-01T00:00:00Z&end_date=2026-09-23T00:00:00Z&limit=1', '/creator-performance?start_date=2026-06-25&limit=1', '/samples?limit=1',
              '/sample-requests?limit=1', '/orders?limit=1']:
        d = api(p, tries=1)
        print(p, '->', 'no' if d is None else json.dumps(d)[:400])


def main():
    os.makedirs(PROF, exist_ok=True)
    subs = paged('/submissions')
    listed = paged('/creators')
    ids = {c['id'] for c in listed}
    for s in subs: ids.add(s['creator']['id'])
    ids |= {i for i in PROTECTED.values() if i}
    with ThreadPoolExecutor(3) as ex:
        det = [d for d in ex.map(lambda i: api('/creators/' + i), sorted(ids)) if d]
    perf = {}
    for row in paged('/creator-performance?start_date=2026-06-01'):
        cid = (row.get('creator') or {}).get('id') or row.get('creator_id')
        if cid: perf[cid] = row

    prot_names = {n.lower() for n in PROTECTED}
    by_creator = {}
    for s in subs: by_creator.setdefault(s['creator']['id'], []).append(s)
    db = {}
    for c in det:
        progs = [p for p in c.get('programs', []) if p.get('status') == 'active']
        in_v3 = any(p['name'] == V3 for p in progs)
        prot = c['name'].strip().lower() in prot_names
        if not (in_v3 or prot): continue
        ss = sorted(by_creator.get(c['id'], []), key=lambda s: s.get('created_at', ''), reverse=True)
        db[c['id']] = {
            'name': c['name'].strip(), 'slug': slug(c['name']), 'id': c['id'],
            'group': 'protected' if prot else 'v3', 'joined_at': c.get('joined_at', '')[:10],
            'programs': [{'name': p['name'], 'since': (p.get('enrolled_at') or '')[:10],
                          'commission': (p.get('commission') or {}).get('display_text')} for p in progs],
            'performance': perf.get(c['id']),
            'submissions': [{
                'trybe_id': s['trybe_id'], 'id': s['id'], 'date': s.get('created_at', '')[:10],
                'status': s['status'], 'program': (s.get('program') or {}).get('name'),
                'ads': (s.get('ads') or {}).get('count', 0),
                'angles': [a.get('name') or a.get('angle') for a in s.get('angles') or []],
                'review_comment': s.get('review_comment'), 'creator_comment': s.get('creator_comment'),
                'transcript': ((s.get('transcript') or {}).get('text') or '')[:1500]} for s in ss]}
    # duplicate display names (e.g. Jenasa Prudhomme has two accounts): the account with fewer videos
    # gets its short id appended, so the real account keeps the plain slug and no profile overwrites another
    seen = {}
    for c in sorted(db.values(), key=lambda c: -len(c['submissions'])):
        if c['slug'] in seen: c['slug'] += '-' + c['id'].split('_')[-1][:6]
        seen[c['slug']] = c['id']
    json.dump(db, open(os.path.join(DB, 'creators.json'), 'w'), indent=1, ensure_ascii=False)

    for c in db.values():
        write_profile(c)
    missing = [n for n in PROTECTED if n.lower() not in {c['name'].lower() for c in db.values()}]
    if missing: print('WARNING protected creators not found:', missing)
    print(f"{len(db)} creators ({sum(c['group'] == 'protected' for c in db.values())} protected), "
          f"{sum(len(c['submissions']) for c in db.values())} videos")


def write_profile(c):
    p = os.path.join(PROF, c['slug'] + '.md')
    notes = '## Notes\n\n### Style (from watching her videos)\n_not reviewed yet_\n\n### DMs so far\n_not reviewed yet_\n\n### Inspo that fits her\n_none yet_\n'
    if os.path.exists(p):
        old = open(p).read()
        if '## Notes' in old: notes = old[old.index('## Notes'):]
    ss = c['submissions']; appr = [s for s in ss if s['status'] == 'approved']
    perf = (c.get('performance') or {}).get('performance') or {}
    money = lambda k: f"${perf.get(k, 0) / 100:,.0f}"
    stat = (f"earnings {money('earnings_cents')}, Trybe GMV {money('trybe_gmv_cents')}, conversions {perf.get('trybe_conversions', 0)}, "
            f"ads {perf.get('ads', 0)}, ad spend {money('spend_cents')}, purchases {perf.get('purchases', 0)} "
            f"({money('purchase_value_cents')}), ROAS {perf.get('roas')}") if perf else ''
    lines = [f"# {c['name']}", '', '<!-- facts: rebuilt by build_db.py, do not edit -->',
             f"- Group: {'PROTECTED (keeps her old commission; never message about commission)' if c['group'] == 'protected' else '5% program (V3)'}",
             f"- Joined Trybe: {c['joined_at']}",
             '- Programs: ' + '; '.join(f"{x['name']} since {x['since']}" for x in c['programs']),
             f"- Videos: {len(ss)} submitted, {len(appr)} approved, {sum(1 for s in ss if s['status'] == 'rejected')} rejected, last {ss[0]['date'] if ss else 'never'}",
             f"- Videos run as ads: {sum(1 for s in ss if s['ads'])}",
             f"- Performance since Jun 2026: {stat or 'no data'}", '', '### Videos (newest first)']
    for s in ss[:15]:
        t = re.sub(r'\s+', ' ', s['transcript'])[:220]
        lines.append(f"- {s['date']} {s['status']} (trybe={s['trybe_id']}{', ads ' + str(s['ads']) if s['ads'] else ''}): \"{t}\"")
    if len(ss) > 15: lines.append(f"- ...and {len(ss) - 15} older (see creators.json)")
    lines += ['<!-- /facts -->', '']
    open(p, 'w').write('\n'.join(lines) + '\n' + notes)


if __name__ == '__main__':
    if '--probe' in sys.argv:
        probe()
    else:
        main()
        # Fatima's quiet-creator rule (2026-09-23): every refresh also puts creators with no
        # video in 14+ days into the follow-up ledger, so no sweep can skip them.
        import subprocess
        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quiet_creators.py')])
