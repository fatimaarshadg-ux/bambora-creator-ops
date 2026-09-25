# Registers a Windows scheduled task that runs the monitor every Monday at 09:00 and posts to Slack.
# Run once:  powershell -NoProfile -ExecutionPolicy Bypass -File .\schedule-weekly.ps1
# Remove:    Unregister-ScheduledTask -TaskName "Bambora Ads Library monitor" -Confirm:$false
# The task runs under your account, so it can decrypt the DPAPI secrets. The PC must be on (or wake) at that time.
param([string]$Day = "Monday", [string]$Time = "09:00")

$python = (Get-Command python).Source
$script = Join-Path $PSScriptRoot "monitor.py"
$log = Join-Path $PSScriptRoot "state\last_run.log"   # written by monitor.py itself

$action = New-ScheduledTaskAction -Execute $python -Argument "`"$script`"" -WorkingDirectory $PSScriptRoot
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Day -At $Time
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -ExecutionTimeLimit (New-TimeSpan -Hours 2)

Register-ScheduledTask -TaskName "Bambora Ads Library monitor" -Action $action -Trigger $trigger `
    -Settings $settings -Description "Scans the Meta Ads Library for Bambora brand terms, copied copy and copied creatives; posts new hits to Slack." -Force | Out-Null

Write-Host "Scheduled: every $Day at $Time. Log: $log"
Write-Host "Test it now with: Start-ScheduledTask -TaskName 'Bambora Ads Library monitor'"
