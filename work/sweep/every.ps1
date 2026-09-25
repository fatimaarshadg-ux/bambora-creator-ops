# Timed extra checks that don't run every sweep: PowerShell twin of every.sh (same stamp files).
#   ... every.ps1 due metaaccess 300   -> prints DUE (exit 0) if 300+ min since last run, else "not due" (exit 1)
#   ... every.ps1 done metaaccess      -> record that it ran now
$dir = Join-Path $env:USERPROFILE "claude-setup\work\sweep\every"
New-Item -ItemType Directory -Force $dir | Out-Null
$cmd = $args[0]; $name = $args[1]
$now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
switch ($cmd) {
    "due" {
        $max = 300; if ($args.Count -ge 3) { $max = [int]$args[2] }
        $f = Join-Path $dir $name; $last = 0
        if (Test-Path $f) { try { $last = [int64](Get-Content $f -Raw).Trim() } catch { $last = 0 } }
        $age = [math]::Floor(($now - $last) / 60)
        if ($age -ge $max) { Write-Output "DUE: $name ($age min since last)"; exit 0 }
        Write-Output "not due: $name ($age min)"; exit 1
    }
    "done" {
        Set-Content -LiteralPath (Join-Path $dir $name) -Value $now -Encoding ascii
        Write-Output ("$name done " + (Get-Date -Format "HH:mm"))
    }
    default { Write-Output "usage: every.ps1 due <name> [minutes] | done <name>" }
}
