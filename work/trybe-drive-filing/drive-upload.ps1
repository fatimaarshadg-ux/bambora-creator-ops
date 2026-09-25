# Put files into a Google Drive folder on Windows (replaces the Mac's AppleScript upload trick).
#
# Main method: Google Drive for desktop. Once it is installed and signed in (with the Bambora
# Google account), Drive shows up in File Explorer as a drive letter (usually G:) with
# "My Drive" and "Shared drives" inside. Copying a file there uploads it. No browser, no clicks.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\trybe-drive-filing\drive-upload.ps1" -Source <local folder> -Target Trybe
#   ... -Target Inspo -Subfolder "Week of 2026-09-28"
#   ... -TargetPath "G:\Shared drives\Main Media\Trybe"         (any folder, if the guess is wrong)
#   ... -Find                                                   (just list the Drive folders it can see)
#
# Targets it knows (first match wins; set -TargetPath to override, and save the right path in
# drive-folders.json next to this script so it is remembered):
#   Trybe : approved Trybe videos (Drive folder id 1kleoyEuzTGxftUvYKwSK3aVUDTKkG53R, the media buyers' Main Media > Trybe)
#   Inspo : "Bambora Inspo" (id 1HleYAep0n7C5gFGt3RhRsgy0dmiQEb8Y), one subfolder per week
#   Backup: "Claude Backup / Repo snapshots" (id 1FHhB0_QemdOFsdAMr2j7tLBDRYaBF5Yx)
#
# After copying, the files upload in the background. Then Claude checks them with the Google Drive
# connector (search_files with parentId = the folder id) and renames each one to its manifest
# drive_name (for example CreatorName/fatima/trybe=1234abcd) with update_file, because Windows file
# names cannot contain "/". Only after the rename is verified: file_approved.py --mark <ids>.
param(
    [string]$Source,
    [ValidateSet("Trybe", "Inspo", "Backup")][string]$Target = "",
    [string]$Subfolder = "",
    [string]$TargetPath = "",
    [switch]$Find
)
$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$cfgFile = Join-Path $here "drive-folders.json"
$cfg = @{}
if (Test-Path $cfgFile) {
    $json = Get-Content $cfgFile -Raw | ConvertFrom-Json
    foreach ($p in $json.PSObject.Properties) { $cfg[$p.Name] = $p.Value }
}

# Find Google Drive for desktop roots (any drive letter with "My Drive" or "Shared drives")
$roots = @()
foreach ($d in Get-PSDrive -PSProvider FileSystem) {
    foreach ($n in "My Drive", "Shared drives") {
        $p = Join-Path $d.Root $n
        if (Test-Path $p) { $roots += $p }
    }
}
if ($roots.Count -eq 0) {
    Write-Output "Google Drive for desktop was not found. Install it (winget install Google.GoogleDrive), sign in with the Bambora Google account, then run this again. Browser fallback: memory windows-drive-upload-technique."
    exit 1
}
if ($Find) {
    foreach ($r in $roots) { Write-Output "== $r"; Get-ChildItem $r -Directory -ErrorAction SilentlyContinue | ForEach-Object { Write-Output "   $($_.FullName)" } }
    exit 0
}

if (-not $TargetPath) {
    if ($Target -and $cfg.ContainsKey($Target) -and (Test-Path $cfg[$Target])) {
        $TargetPath = $cfg[$Target]
    } else {
        $guesses = switch ($Target) {
            "Trybe"  { "Shared drives\Main Media\Trybe", "My Drive\Main Media\Trybe", "My Drive\Trybe" }
            "Inspo"  { "My Drive\Bambora Inspo" }
            "Backup" { "My Drive\Claude Backup\Repo snapshots" }
            default  { @() }
        }
        foreach ($d in Get-PSDrive -PSProvider FileSystem) {
            foreach ($g in $guesses) {
                $p = Join-Path $d.Root $g
                if (-not $TargetPath -and (Test-Path $p)) { $TargetPath = $p }
            }
        }
    }
}
if (-not $TargetPath -or -not (Test-Path $TargetPath)) {
    Write-Output "Could not find the '$Target' folder in Google Drive for desktop. Run with -Find to list folders, then rerun with -TargetPath ""<path>"" (and add it to $cfgFile as {""$Target"": ""<path>""})."
    exit 1
}
if ($Target -and -not $cfg.ContainsKey($Target)) {
    $cfg[$Target] = $TargetPath
    ($cfg | ConvertTo-Json) | Set-Content $cfgFile -Encoding UTF8
}
if ($Subfolder) {
    $TargetPath = Join-Path $TargetPath $Subfolder
    New-Item -ItemType Directory -Force $TargetPath | Out-Null
}
if (-not $Source -or -not (Test-Path $Source)) { Write-Output "Give -Source <folder with the files>."; exit 1 }

$n = 0
foreach ($f in Get-ChildItem $Source -File) {
    if ($f.Name -eq "manifest.json") { continue }
    Copy-Item -LiteralPath $f.FullName -Destination (Join-Path $TargetPath $f.Name) -Force
    Write-Output "copied $($f.Name)"
    $n++
}
Write-Output "$n file(s) copied to $TargetPath. Google Drive uploads them in the background (watch the Drive icon in the taskbar tray)."
Write-Output "Next: verify with the Drive connector (search_files, parentId = the folder id), rename to each manifest drive_name with update_file, then --mark the ids."
