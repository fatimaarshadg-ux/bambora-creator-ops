# Send REAL keystrokes to the front window (Windows port of the Mac's "osascript ... key code" trick).
# Chrome only opens a file chooser on a trusted gesture, and clicks from the browser extension do not
# count. Real key presses from the OS do. Used by the browser fallback for Drive uploads and for the
# Trybe "New brief" upload (memory windows-drive-upload-technique).
#
#   ... sendkeys.ps1 -Keys "{DOWN}{DOWN}{ENTER}"          Drive: New menu, down to "File upload", open it
#   ... sendkeys.ps1 -Text "C:\Users\me\Downloads\x" -Keys "{ENTER}"   type into the Windows file dialog
#
# -Keys uses .NET SendKeys codes: {ENTER} {DOWN} {TAB} {ESC} ^a (Ctrl+A) +{TAB} (Shift+Tab).
# By default it first brings Chrome forward (front.ps1). Use -NoFront when the file dialog is already open.
# Safety: never use this to type into a message composer; it is for menus and file dialogs only.
param([string]$Text = "", [string]$Keys = "", [switch]$NoFront, [int]$DelayMs = 400)
if (-not $NoFront) {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $env:USERPROFILE "claude-setup\work\trybe-chat\front.ps1") "none" | Out-Null
}
$wsh = New-Object -ComObject WScript.Shell
Start-Sleep -Milliseconds $DelayMs
if ($Text) {
    # SendKeys treats + ^ % ~ ( ) { } [ ] as special; escape them so paths type literally
    $safe = ($Text -replace '([\+\^%~\(\)\{\}\[\]])', '{$1}')
    $wsh.SendKeys($safe)
    Start-Sleep -Milliseconds $DelayMs
}
if ($Keys) { $wsh.SendKeys($Keys); Start-Sleep -Milliseconds $DelayMs }
Write-Output "sent"
