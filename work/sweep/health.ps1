# One-glance health check of every background piece the routine needs. Safe to run any time; changes nothing.
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\sweep\health.ps1"
# Prints OK or PROBLEM per line, with what to do. Claude runs it at the start of each shift and whenever
# something seems stuck; the operator can run it too.
$repo = Join-Path $env:USERPROFILE "claude-setup"
$sweep = Join-Path $repo "work\sweep"
function Line($ok, $name, $detail, $fix) {
    if ($ok) { Write-Host ("OK       {0,-22} {1}" -f $name, $detail) -ForegroundColor Green }
    else { Write-Host ("PROBLEM  {0,-22} {1}  -> {2}" -f $name, $detail, $fix) -ForegroundColor Yellow }
}

# keep-awake
$ka = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $sweep "keep-awake.ps1") status
Line ($LASTEXITCODE -eq 0) "keep-awake" "$ka" "run work\sweep\keep-awake.ps1 start (or start.ps1)"

# helper server
$srv = $false
try { $r = Invoke-WebRequest -Uri "http://127.0.0.1:8765/chat-helpers.js" -UseBasicParsing -TimeoutSec 4; $srv = ($r.StatusCode -eq 200) } catch { }
Line $srv "helper server :8765" $(if ($srv) { "serving chat-helpers.js" } else { "not answering" }) "run work\sweep\start.ps1 (it starts cors_srv.py)"

# last sweep + streams
$stamp = Join-Path $sweep "last_sweep"
$age = -1
if (Test-Path $stamp) { $age = [math]::Floor(([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() - [int64](Get-Content $stamp -Raw).Trim()) / 60) }
Line (($age -ge 0) -and ($age -lt 45)) "last full sweep" $(if ($age -ge 0) { "$age min ago" } else { "never" }) "tell Claude: run the full sweep now (routines/full-run.md)"
$st = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $sweep "streams.ps1") stale 60
Line ($LASTEXITCODE -eq 0) "six streams" "$st" "tell Claude to run the stale streams now"

# watchdog (a bash or powershell process running watchdog.sh / watchdog.ps1)
$wd = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'watchdog\.(sh|ps1)' })
Line ($wd.Count -gt 0) "watchdog" $(if ($wd.Count) { "running ($($wd.Count))" } else { "not running" }) "tell Claude: start the watchdog in the background (bash ~/claude-setup/work/sweep/watchdog.sh 30 60)"

# Chrome with Trybe
$chrome = @(Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 })
Line ($chrome.Count -gt 0) "Chrome" $(if ($chrome.Count) { "open: '" + $chrome[0].MainWindowTitle + "'" } else { "not open" }) "open Chrome (Bambora profile) with the Trybe tabs"

# Claude app
$cl = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match '^(claude|Claude)$' })
Line ($cl.Count -gt 0) "Claude app" $(if ($cl.Count) { "running" } else { "not running" }) "open the Claude app, Code tab, Bombara folder, then: start the routines"

# Trybe key
$kf = Join-Path $env:USERPROFILE ".claude\secrets\trybe_api_key.dpapi"
Line (Test-Path $kf) "Trybe API key" $(if (Test-Path $kf) { "stored (DPAPI)" } else { "missing" }) "run work\common\store-trybe-key.ps1 (key from Fatima)"

# repo state
$dirty = @(git -C $repo status --porcelain 2>$null).Count
$ahead = (git -C $repo rev-list --count "@{u}..HEAD" 2>$null)
Line ($ahead -eq "0" -or -not $ahead) "GitHub sync" "$dirty changed file(s), $ahead commit(s) not pushed" "tell Claude: run sync.ps1"

# power: is the PC set to sleep when plugged in?
$ac = (powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE 2>$null | Select-String "Current AC Power Setting Index" | ForEach-Object { ($_ -split ":")[1].Trim() })
if ($ac) {
    $mins = [Convert]::ToInt32($ac, 16) / 60
    Line ($mins -eq 0) "sleep when plugged in" $(if ($mins -eq 0) { "never" } else { "after $mins min" }) "Settings > System > Power > Screen and sleep > When plugged in, put my device to sleep after: Never (keep-awake also covers this while it runs)"
}
