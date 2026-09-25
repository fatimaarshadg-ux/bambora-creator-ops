#!/usr/bin/env python3
"""Add the Bambora routine's permissions and the no-em-dash hooks to ~/.claude/settings.json.

Windows port of apply-allowlist-mac.sh + apply-no-dash-hooks-mac.sh. Backs up settings.json first,
only ADDS entries (never removes anything already there), and is safe to run more than once.
Run through apply-settings.ps1 (the operator runs it herself; Claude never changes its own permissions).
"""
import datetime as dt
import json
import os
import shutil
import sys

HOME = os.path.expanduser('~')
REPO = os.path.join(HOME, 'claude-setup')
P = os.path.join(HOME, '.claude', 'settings.json')

os.makedirs(os.path.dirname(P), exist_ok=True)
d = {}
if os.path.exists(P):
    shutil.copy2(P, P + '.bak-' + dt.datetime.now().strftime('%Y%m%d%H%M%S'))
    try:
        d = json.load(open(P, encoding='utf-8'))
    except Exception:
        sys.exit('settings.json is not valid JSON; fix or rename it, then run again (a backup was made).')

perm = d.setdefault('permissions', {})
allow = perm.setdefault('allow', [])
n = 0
for x in json.load(open(os.path.join(REPO, 'settings', 'allowlist.json'), encoding='utf-8')):
    if x not in allow:
        allow.append(x); n += 1

dirs = perm.setdefault('additionalDirectories', [])
m = 0
for x in json.load(open(os.path.join(REPO, 'settings', 'additional-dirs.json'), encoding='utf-8')):
    full = os.path.expanduser(x).replace('\\', '/')
    if full not in dirs:
        dirs.append(full); m += 1

hook = os.path.join(REPO, 'hooks', 'claude', 'no-dash-check.py').replace('\\', '/')
cmd = f'py -3 "{hook}"'
hooks = d.setdefault('hooks', {})


def add(ev, matcher):
    lst = hooks.setdefault(ev, [])
    if not any('no-dash-check.py' in json.dumps(x) for x in lst):
        e = {'hooks': [{'type': 'command', 'command': cmd}]}
        if matcher:
            e['matcher'] = matcher
        lst.append(e)


add('Stop', None)
add('PostToolUse', 'Write|Edit')
json.dump(d, open(P, 'w', encoding='utf-8'), indent=2)
print(f'permissions: added {n} (total {len(allow)}); trusted folders added {m}: {dirs}; no-dash hooks on')
