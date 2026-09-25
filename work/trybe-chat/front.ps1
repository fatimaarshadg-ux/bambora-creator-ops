# Bring Chrome to the front and switch to the Trybe tab you are working in (Windows port of front.sh).
# Chrome ignores clicks and keypresses in background tabs, so run this before every browser send.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\trybe-chat\front.ps1" [marker] [-Title text]
#
# How it finds the tab: Windows can only see the title of each Chrome window's ACTIVE tab, not the URLs
# (the Mac's AppleScript could read every URL). So:
#   1. It brings the Chrome window whose title contains -Title (default "Trybe") to the front.
#   2. If the active tab's title does not contain -Title, it presses Ctrl+Tab (up to 25 times) until one does.
#   3. The marker argument (cl=3, cl=1, tab=samples ...) is printed back so Claude can confirm with
#      javascript_tool that location.href contains it; if not, Claude switches tabs with the extension
#      (tabs_context_mcp, then navigate in the right tab) and runs this again.
# Exit code 0 = Chrome is in front with a matching title, 1 = no Chrome window found.
param([string]$Marker = "cl=3", [string]$Title = "Trybe")

Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class FrontWin {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
    [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
    [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte scan, uint flags, UIntPtr extra);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
'@

function Get-ChromeWindows {
    Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle }
}

function Bring($h) {
    if ([FrontWin]::IsIconic($h)) { [FrontWin]::ShowWindow($h, 9) | Out-Null }   # 9 = restore
    # Windows refuses SetForegroundWindow from a background process unless a key event just happened;
    # tapping Alt satisfies that rule.
    [FrontWin]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero); [FrontWin]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero)
    [FrontWin]::SetForegroundWindow($h) | Out-Null
    Start-Sleep -Milliseconds 300
}

$wins = @(Get-ChromeWindows)
if ($wins.Count -eq 0) { Write-Output "No Chrome window found. Open Chrome (signed in) with the Trybe tab first."; exit 1 }
$pick = $wins | Where-Object { $_.MainWindowTitle -like "*$Title*" } | Select-Object -First 1
if (-not $pick) { $pick = $wins | Select-Object -First 1 }
Bring $pick.MainWindowHandle

$wsh = New-Object -ComObject WScript.Shell
for ($i = 0; $i -lt 25; $i++) {
    $t = (Get-Process -Id $pick.Id).MainWindowTitle
    if ($t -like "*$Title*") { break }
    $wsh.SendKeys("^{TAB}")
    Start-Sleep -Milliseconds 250
}
$t = (Get-Process -Id $pick.Id).MainWindowTitle
Write-Output "Chrome in front: '$t'. Confirm location.href contains '$Marker' before any click or send."
