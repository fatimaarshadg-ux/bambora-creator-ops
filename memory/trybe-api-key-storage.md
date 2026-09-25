---
name: trybe-api-key-storage
description: "Where the Trybe Brand API key is stored on this Windows PC and how to load it for API calls"
metadata:
  type: reference
---

The Trybe Brand API key (bearer token, see [[trybe-brand-api]]) is stored at `%USERPROFILE%\.claude\secrets\trybe_api_key.dpapi`, encrypted with Windows DPAPI. Only this Windows account on this PC can decrypt it. The key value is never written to memory, chat, the repo, or the screen.

**How it got there:** install.ps1 opened a small masked box and the operator pasted the key Fatima gave her privately. To store or replace it again, the operator runs (it asks in the same masked box):
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\common\store-trybe-key.ps1" -Force
```
Never ask the operator to paste the key into chat.

**Loading it:**
- Python scripts (`build_db.py`, `file_approved.py`, `fetch_media.py`) call `work/common/trybe_key.py`, which reads the env var `TRYBE_API_KEY` first, then the DPAPI file.
- Quick check: `py -3 ~/claude-setup/work/common/trybe_key.py --check` prints "found (N characters)" and makes one test call.
- In Git Bash for a curl call, keep it inside a substitution so it never prints: `curl -s -H "Authorization: Bearer $(py -3 ~/claude-setup/work/common/trybe_key.py --print)" -A curl/8.7.1 https://api.jointrybe.com/v1/submissions?limit=1`
- In PowerShell:
```powershell
$s = Get-Content "$env:USERPROFILE\.claude\secrets\trybe_api_key.dpapi" | ConvertTo-SecureString
$key = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
```
- The Trybe MCP server (`~/Bombara/trybe-review/mcp-server/server.js`, tools `mcp__trybe__*`) reads the same file.

**If a call returns 401 or 403:** the key may have been rotated in the Trybe portal. Tell the operator; do not assume the storage broke. A new key is made in Trybe, Integrations, API, but **only after asking Fatima**, because making a new key can replace the old one and break her own setup.

**Why DPAPI:** chosen by Fatima (2026-09-20) over a plaintext `.env` for basic protection against casual file exposure, with no extra module to install. On Fatima's Mac the same key lives in the login Keychain (service `trybe-api-key`).
