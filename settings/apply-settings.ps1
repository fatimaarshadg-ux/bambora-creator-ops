# Adds the Bambora routine's permission allowlist, trusted folders and the no-em-dash hooks to
# %USERPROFILE%\.claude\settings.json. Backs it up first. Only adds, never removes. Safe to rerun.
# The operator runs this herself (Claude is not allowed to change its own permissions):
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\settings\apply-settings.ps1"
# Why it matters: unattended scheduled runs freeze on the first permission prompt (memory
# scheduled-tasks-freeze-on-permissions). Rerun this whenever settings\allowlist.json changes.
$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) { Write-Host "Python is not installed yet. Run install.ps1 first."; exit 1 }
& py -3 (Join-Path $PSScriptRoot "apply_settings.py")
exit $LASTEXITCODE
