# End of session: copy what Claude learned on this PC (skills, memory, CLAUDE.md, task prompts) back into
# this repo, refuse anything that looks like a secret, then commit and push.
# Port of Fatima's sync-from-windows.ps1 for the handover repo.
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\sync.ps1" -Message "what changed"
param([string]$Message = "Sync from the Windows PC")

$ErrorActionPreference = "Continue"
$repo = $PSScriptRoot

# 1. PC -> repo (adds and updates only; never deletes; MEMORY.md gets new lines appended)
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo "work\backup\sync_check.ps1")

# 2. Refuse to push anything that looks like a real credential. Pointers to where the key lives are fine.
$files = git -C $repo ls-files --cached --others --exclude-standard |
    Where-Object { $_ -notmatch '\.(ps1|sh)$' -and $_ -notmatch '^tools/' } |
    ForEach-Object { Join-Path $repo $_ } |
    Where-Object { Test-Path $_ -PathType Leaf }
$hits = $files | Select-String -Pattern 'Bearer\s+[A-Za-z0-9_\-\.]{20,}', '(sk|pk|key|tok|tk)_[A-Za-z0-9]{20,}', 'eyJ[A-Za-z0-9_\-]{20,}\.', '01000000d08c9ddf0115d1118c7a00c04fc297eb' -ErrorAction SilentlyContinue
if ($hits) {
    $hits | ForEach-Object { Write-Host "$($_.Path):$($_.LineNumber)" }
    Write-Host "Possible secret found in the files above. Nothing was committed." -ForegroundColor Red
    exit 1
}

# 3. Commit and push (the pre-commit hook blocks em dashes in added lines)
git -C $repo config core.hooksPath hooks
git -C $repo add -A
git -C $repo diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Write-Host "Nothing changed. Already up to date."; exit 0 }
git -C $repo commit -m $Message
if ($LASTEXITCODE -ne 0) { Write-Host "Commit failed (see above; an em dash in a new line is the usual reason)." -ForegroundColor Yellow; exit 1 }
git -C $repo push
if ($LASTEXITCODE -ne 0) { Write-Host "Push FAILED. The commit is saved on this PC; run 'gh auth login' (or check the internet) and run sync.ps1 again." -ForegroundColor Yellow; exit 1 }
Write-Host "Pushed: $Message"
