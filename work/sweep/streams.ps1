# Per-stream tracker: PowerShell twin of streams.sh (same folder, same stamp files, same output).
# Built 2026-09-24 after Discovery went unreviewed all night while chat sweeps ran.
# Every stream records when it last ran:
#   powershell -NoProfile -ExecutionPolicy Bypass -File streams.ps1 done chat samples partnership submissions discovery ledger
# Show ages:                              ... streams.ps1 status
# Stale streams (older than N minutes):   ... streams.ps1 stale 60   (prints names, exit 1 if any)
# The .sh and .ps1 versions share the stamp files, so either can be used in Git Bash or PowerShell.
$dir = Join-Path $env:USERPROFILE "claude-setup\work\sweep\streams"
New-Item -ItemType Directory -Force $dir | Out-Null
$all = "chat", "samples", "partnership", "submissions", "discovery", "ledger"
function Now { [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() }
function Last($s) {
    $f = Join-Path $dir $s
    if (Test-Path $f) { try { return [int64](Get-Content $f -Raw).Trim() } catch { return 0 } }
    return 0
}
$cmd = $args[0]
$rest = @($args | Select-Object -Skip 1)
switch ($cmd) {
    "done" {
        foreach ($s in $rest) { Set-Content -LiteralPath (Join-Path $dir $s) -Value (Now) -Encoding ascii }
        Write-Output ("streams done: " + ($rest -join " ") + " (" + (Get-Date -Format "HH:mm") + ")")
    }
    "status" {
        $n = Now
        foreach ($s in $all) { Write-Output ("{0}: {1} min ago" -f $s, [math]::Floor(($n - (Last $s)) / 60)) }
    }
    "stale" {
        $max = 60
        if ($rest.Count -gt 0) { $max = [int]$rest[0] }
        $n = Now; $out = @()
        foreach ($s in $all) { if ([math]::Floor(($n - (Last $s)) / 60) -ge $max) { $out += $s } }
        if ($out.Count -gt 0) { Write-Output ("STALE: " + ($out -join " ")); exit 1 }
        Write-Output "all streams fresh"
    }
    default { Write-Output "usage: streams.ps1 done <streams...> | status | stale [minutes]" }
}
