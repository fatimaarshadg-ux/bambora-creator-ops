# Record that a sweep just finished (the watchdog reads this). PowerShell twin of mark.sh.
$stamp = Join-Path $env:USERPROFILE "claude-setup\work\sweep\last_sweep"
Set-Content -LiteralPath $stamp -Value ([DateTimeOffset]::UtcNow.ToUnixTimeSeconds()) -Encoding ascii
Write-Output ("sweep marked " + (Get-Date -Format "HH:mm"))
