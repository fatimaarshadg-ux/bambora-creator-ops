# Record that a sweep just finished (the watchdog reads this). PowerShell twin of mark.sh.
$stamp = Join-Path $env:USERPROFILE "claude-setup\work\sweep\last_sweep"
# LF only (no CRLF): watchdog.sh reads this with $(cat) and bash arithmetic fails on a trailing \r
[IO.File]::WriteAllText($stamp, "$([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())`n")
Write-Output ("sweep marked " + (Get-Date -Format "HH:mm"))
