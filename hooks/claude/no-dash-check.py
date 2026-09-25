#!/usr/bin/env python3
"""Claude Code hook. Stop: if Claude's last reply contains an em dash, block and ask for a rewrite.
PostToolUse (Write/Edit): if the written text contains an em dash, tell Claude to fix it.
Quoted material Fatima supplied is exempt by judgement; the hook only flags, Claude decides.
Windows note: files are read as UTF-8 explicitly (the Windows default code page would garble them)."""
import json, sys
d = json.loads(sys.stdin.buffer.read().decode('utf-8', errors='replace'))
ev = d.get('hook_event_name')
def has(t): return '—' in t or ' – ' in t
if ev == 'Stop':
    if d.get('stop_hook_active'): sys.exit(0)
    last = ''
    try:
        for line in open(d['transcript_path'], encoding='utf-8', errors='replace'):
            o = json.loads(line)
            if o.get('type') == 'assistant':
                c = o.get('message', {}).get('content', [])
                txt = ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
                if txt: last = txt
    except Exception: sys.exit(0)
    if has(last):
        print(json.dumps({'decision': 'block', 'reason': 'Your reply contains an em dash (or spaced en dash). Fatima never wants them. Rewrite the reply without them, per the no-em-dashes skill.'}))
elif ev == 'PostToolUse':
    ti = d.get('tool_input', {})
    txt = ti.get('content') or ti.get('new_string') or ''
    if has(txt) and 'no-em-dashes' not in ti.get('file_path', ''):
        print(json.dumps({'decision': 'block', 'reason': f"The text you just wrote to {ti.get('file_path')} contains an em dash. Fix it unless it is verbatim quoted material."}))
