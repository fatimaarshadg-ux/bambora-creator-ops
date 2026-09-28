#!/usr/bin/env python3
"""Volume commitments: what each creator agreed to film per week (Fatima, 2026-09-28).

Every creator who answered the volume question ("my top creators usually post 3 to 5 videos a week...
would that work for you?") is recorded here with their exact words, so every message and every inspo
can build on what they said. The data lives in commitments.json next to this script.

  commitments.py get <name>          what this creator agreed to (run before any message or inspo)
  commitments.py list [--verify]     everyone (or only entries whose quote still needs checking in the thread)
  commitments.py add <name> --agreed "3 to 5 a week" --quote "yes that works!" [--date 2026-09-28]
                 [--status yes|soft|conditional|below|no] [--asked "3 to 5"] [--source "..."] [--verified]
"""
import argparse, datetime, json, os, sys
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'commitments.json')

def load():
    return json.load(open(F, encoding='utf-8')) if os.path.exists(F) else {}

def save(d):
    json.dump(dict(sorted(d.items(), key=lambda kv: kv[0].lower())), open(F, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    open(F, 'a', encoding='utf-8').write('\n')

def find(d, name):
    n = name.strip().lower()
    hits = [k for k in d if k.lower() == n] or [k for k in d if n in k.lower()]
    return hits

def show(k, e):
    flag = '' if e.get('verified') else '  [quote to verify in the thread]'
    print(f"{k}: {e.get('status','?').upper()} to {e.get('agreed','?')} (asked {e.get('asked','?')}, {e.get('date','?')}){flag}")
    if e.get('quote'): print(f'    "{e["quote"]}"')
    if e.get('source'): print(f"    source: {e['source']}")

def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    g = sp.add_parser('get'); g.add_argument('name', nargs='+')
    l = sp.add_parser('list'); l.add_argument('--verify', action='store_true')
    a = sp.add_parser('add'); a.add_argument('name', nargs='+')
    a.add_argument('--agreed', required=True); a.add_argument('--quote', default='')
    a.add_argument('--date', default=datetime.date.today().isoformat())
    a.add_argument('--status', default='yes', choices=['yes', 'soft', 'conditional', 'below', 'no'])
    a.add_argument('--asked', default='3 to 5 a week'); a.add_argument('--source', default='Discovery thread')
    a.add_argument('--verified', action='store_true')
    x = ap.parse_args(); d = load()
    if x.cmd == 'get':
        hits = find(d, ' '.join(x.name))
        if not hits: print(f"no commitment recorded for {' '.join(x.name)} (check the thread; if they answered the volume question, add it)"); return
        for k in hits: show(k, d[k])
    elif x.cmd == 'list':
        for k, e in d.items():
            if not x.verify or not e.get('verified'): show(k, e)
        print(f"{len(d)} creators recorded")
    elif x.cmd == 'add':
        k = ' '.join(x.name).strip()
        old = find(d, k); k = old[0] if len(old) == 1 and old[0].lower() == k.lower() else k
        d[k] = {'agreed': x.agreed, 'status': x.status, 'quote': x.quote, 'date': x.date, 'asked': x.asked,
                'source': x.source, 'verified': bool(x.verified)}
        save(d); show(k, d[k])

if __name__ == '__main__':
    main()
