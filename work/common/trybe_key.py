#!/usr/bin/env python3
"""Load the Trybe Brand API key without ever writing it anywhere.

Where the key lives (checked in this order):
  1. the environment variable TRYBE_API_KEY (handy for a one-off test; never put it in a file)
  2. Windows DPAPI: %USERPROFILE%\\.claude\\secrets\\trybe_api_key.dpapi
     (written by install.ps1 or work/common/store-trybe-key.ps1; only this Windows account
     on this PC can decrypt it)
  3. macOS login Keychain, service trybe-api-key (Fatima's Mac)

Usage from other scripts:
    sys.path.insert(0, <path to work/common>); from trybe_key import get_key; KEY = get_key()
From the command line:
    py -3 trybe_key.py --check    prints "Trybe key: found (N characters)" and tests one API call
    py -3 trybe_key.py --print    prints the key itself; only use inside $(...), never on screen
"""
import os
import platform
import subprocess
import sys

DPAPI_FILE = os.path.join(os.path.expanduser('~'), '.claude', 'secrets', 'trybe_api_key.dpapi')


def _dpapi_decrypt(blob):
    import ctypes
    from ctypes import wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', wintypes.DWORD), ('pbData', ctypes.POINTER(ctypes.c_char))]

    buf = ctypes.create_string_buffer(blob, len(blob))
    inp = DATA_BLOB(len(blob), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
    out = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(inp), None, None, None, None, 0, ctypes.byref(out)):
        raise OSError('CryptUnprotectData failed')
    try:
        return ctypes.string_at(out.pbData, out.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(out.pbData)


def _from_dpapi():
    if not os.path.exists(DPAPI_FILE):
        return ''
    text = open(DPAPI_FILE, encoding='ascii', errors='ignore').read().strip()
    # ConvertFrom-SecureString writes the DPAPI blob as hex; the secret inside is UTF-16LE.
    try:
        return _dpapi_decrypt(bytes.fromhex(text)).decode('utf-16-le').strip()
    except Exception:
        pass
    ps = ('$s = Get-Content -LiteralPath "%s" | ConvertTo-SecureString; '
          '$b = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s); '
          '[System.Runtime.InteropServices.Marshal]::PtrToStringAuto($b)') % DPAPI_FILE
    r = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True)
    return r.stdout.strip()


def _from_keychain():
    r = subprocess.run(['security', 'find-generic-password', '-s', 'trybe-api-key', '-w'],
                       capture_output=True, text=True)
    return r.stdout.strip()


def get_key(required=True):
    key = os.environ.get('TRYBE_API_KEY', '').strip()
    if not key and platform.system() == 'Windows':
        key = _from_dpapi()
    if not key and platform.system() == 'Darwin':
        key = _from_keychain()
    if not key and required:
        sys.exit('Trybe API key not found. On Windows run: powershell -NoProfile -ExecutionPolicy Bypass '
                 '-File "%USERPROFILE%\\claude-setup\\work\\common\\store-trybe-key.ps1" (it asks for the key '
                 'in a masked box). Ask Fatima for the key; never paste it into chat.')
    return key


if __name__ == '__main__':
    if '--print' in sys.argv:
        sys.stdout.write(get_key())
    else:
        k = get_key(required=False)
        if not k:
            print('Trybe key: NOT FOUND')
            sys.exit(1)
        print(f'Trybe key: found ({len(k)} characters)')
        if '--check' in sys.argv:
            import urllib.request, urllib.error, json
            req = urllib.request.Request('https://api.jointrybe.com/v1/submissions?limit=1',
                                         headers={'Authorization': 'Bearer ' + k, 'User-Agent': 'curl/8.7.1'})
            try:
                json.load(urllib.request.urlopen(req, timeout=30))
                print('Trybe API: OK (the key works)')
            except urllib.error.HTTPError as e:
                print(f'Trybe API: HTTP {e.code}' + (' (key rejected: ask Fatima whether it was replaced)' if e.code in (401, 403) else ''))
                sys.exit(1)
            except Exception as e:
                print(f'Trybe API: could not verify ({str(e)[:80]})')
                sys.exit(1)
