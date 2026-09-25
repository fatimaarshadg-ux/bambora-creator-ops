# Sweep watchdog: PowerShell twin of watchdog.sh (same logic, same stamp files).
# Run it in the background from the live Claude session. It exits, which wakes Claude, as soon as
# the last sweep is MAX minutes old OR any stream (chat, samples, partnership, submissions,
# discovery, ledger) hasn't run for STREAM_MAX minutes. Claude then runs routines/full-run.md,
# marks each stream with streams done, runs mark, and starts this watchdog again.
#   powershell -NoProfile -ExecutionPolicy Bypass -File watchdog.ps1 30 60
$max = 30; $streamMax = 60
if ($args.Count -ge 1) { $max = [int]$args[0] }
if ($args.Count -ge 2) { $streamMax = [int]$args[1] }
$here = Join-Path $env:USERPROFILE "claude-setup\work\sweep"
$stamp = Join-Path $here "last_sweep"
while ($true) {
    $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $last = 0
    if (Test-Path $stamp) { try { $last = [int64](Get-Content $stamp -Raw).Trim() } catch { $last = 0 } }
    $age = [math]::Floor(($now - $last) / 60)
    if ($age -ge $max) {
        Write-Output "SWEEP DUE: last sweep $age min ago. Run routines/full-run.md (ALL streams) now, then restart the watchdog."
        exit 0
    }
    $st = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $here "streams.ps1") stale $streamMax
    if ($LASTEXITCODE -ne 0) {
        Write-Output "$st (not run for $streamMax+ min). Run those streams now per routines/full-run.md, then restart the watchdog."
        exit 0
    }
    Start-Sleep -Seconds 60
}
