# Keep the PC awake during the work shift (the Windows version of the Mac's `caffeinate -dimsu`).
#
# Why: the routine runs inside Claude Code on this PC. If Windows sleeps, Claude, Chrome and the timers
# all stop, and every sweep in that time is simply missed (creators wait, follow-ups slip).
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\sweep\keep-awake.ps1" start
#   ... keep-awake.ps1 status     is it running?
#   ... keep-awake.ps1 stop       let the PC sleep normally again (end of shift)
#
# How: a hidden PowerShell window asks Windows every 50 seconds to keep the system AND the display on
# (SetThreadExecutionState with ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED). Its process id
# is saved in keepawake.pid so it is never started twice. It stops when you run "stop", sign out or
# restart. It does NOT stop a laptop from sleeping when the LID is closed: set "When I close the lid:
# Do nothing (plugged in)" once (docs/09-background-machinery.md), or keep the lid open.
# Alternative if you prefer an app: Microsoft PowerToys, "Awake" (winget install Microsoft.PowerToys).
param([ValidateSet("start", "stop", "status")][string]$Action = "start")
$pidFile = Join-Path $env:USERPROFILE "claude-setup\work\sweep\keepawake.pid"

function Current {
    if (Test-Path $pidFile) {
        $id = (Get-Content $pidFile -Raw).Trim()
        if ($id) { return Get-Process -Id $id -ErrorAction SilentlyContinue }
    }
    return $null
}

switch ($Action) {
    "status" {
        $p = Current
        if ($p) { Write-Output "keep-awake: RUNNING (pid $($p.Id), since $($p.StartTime))"; exit 0 }
        Write-Output "keep-awake: NOT running (start it: keep-awake.ps1 start)"; exit 1
    }
    "stop" {
        $p = Current
        if ($p) { Stop-Process -Id $p.Id -Force; Write-Output "keep-awake: stopped" } else { Write-Output "keep-awake: was not running" }
        Remove-Item $pidFile -ErrorAction SilentlyContinue
    }
    "start" {
        $p = Current
        if ($p) { Write-Output "keep-awake: already running (pid $($p.Id))"; exit 0 }
        $code = @'
Add-Type -Namespace KA -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint f);'
while ($true) { [KA.Power]::SetThreadExecutionState([uint32]"0x80000003") | Out-Null; Start-Sleep -Seconds 50 }
'@
        $enc = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($code))
        $np = Start-Process powershell -ArgumentList "-NoProfile", "-WindowStyle", "Hidden", "-EncodedCommand", $enc -WindowStyle Hidden -PassThru
        Set-Content -LiteralPath $pidFile -Value $np.Id -Encoding ascii
        Write-Output "keep-awake: started (pid $($np.Id))"
    }
}
