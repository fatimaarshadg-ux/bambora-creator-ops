# One-shot startup for a Bambora work session (Windows port of start.sh).
# Claude runs this when the operator says "start the routines". It starts the shell side:
# keep-awake, the helper server, a repo pull, the ledger, and the stream ages.
# The Claude side (timers, watchdog, first full run) is in routines/START.md.
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\sweep\start.ps1"
$repo = Join-Path $env:USERPROFILE "claude-setup"
$chat = Join-Path $repo "work\trybe-chat"
$state = Join-Path $repo "work\sweep"

# 1. Keep the PC awake (the Mac used caffeinate -dimsu). See keep-awake.ps1 for how and why.
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $state "keep-awake.ps1") start

# 2. Helper server on 127.0.0.1:8765 so Chrome can load chat-helpers.js, roster-scan.js, sample-status.js
function PortOpen {
    try { $c = New-Object Net.Sockets.TcpClient; $c.Connect("127.0.0.1", 8765); $c.Close(); return $true } catch { return $false }
}
if (-not (PortOpen)) {
    Start-Process py -ArgumentList "-3", "cors_srv.py" -WorkingDirectory $chat -WindowStyle Hidden | Out-Null
    Start-Sleep -Seconds 2
}
try {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/chat-helpers.js" -UseBasicParsing -TimeoutSec 5
    Write-Output "helper server: $($r.StatusCode)"
} catch { Write-Output "helper server: NOT RUNNING (run: py -3 cors_srv.py in $chat)" }

# 3. Pull the latest repo (the operator may have pushed from another machine, or Fatima may have)
$old = $ErrorActionPreference; $ErrorActionPreference = "Continue"
# --rebase --autostash: a plain pull fails when this PC has its own unpushed commits or an edited ledger.
git -C $repo pull -q --rebase --autostash 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Output "repo up to date" } else { Write-Output "repo pull FAILED (probably the same file changed here and on GitHub; Claude: run git -C ~/claude-setup status and sort out the conflict before sweeping)" }
# Who pushed last, and when: a push from Fatima's side in the last hour means she may be on shift (one machine at a time).
$last = git -C $repo log -1 --format="%an, %ar: %s" 2>$null
if ($last) { Write-Output "last change on GitHub: $last" }
$ErrorActionPreference = $old

# 4. What is owed today, and how fresh each stream is
& py -3 (Join-Path $repo "work\creator-db\followups.py") due | Select-Object -Last 40
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $state "streams.ps1") status
