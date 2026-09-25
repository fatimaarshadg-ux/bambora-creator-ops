# Zip the whole claude-setup repo (history included) for the nightly Drive backup (Windows port of
# make_backup_zip.sh). Fatima's rule, 2026-09-23: "everything should be backed up on Drive so it's not
# reliant on my device". Output: %USERPROFILE%\claude-backup-staging\claude-setup-YYYY-MM-DD.zip, alone
# in that folder. Secrets never live in the repo, so the zip holds none.
# Upload it with: drive-upload.ps1 -Source "$env:USERPROFILE\claude-backup-staging" -Target Backup
$stage = Join-Path $env:USERPROFILE "claude-backup-staging"
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Force $stage | Out-Null
$zip = Join-Path $stage ("claude-setup-" + (Get-Date -Format "yyyy-MM-dd") + ".zip")
# tar.exe (built into Windows 10 1803+ and 11) writes a real zip with -a and includes the hidden .git folder.
# Compress-Archive is only the fallback: it skips hidden items, so that zip would have no git history.
$tar = Join-Path $env:SystemRoot "System32\tar.exe"
if (Test-Path $tar) {
    & $tar -a -c -f $zip -C $env:USERPROFILE claude-setup
} else {
    Compress-Archive -Path (Join-Path $env:USERPROFILE "claude-setup") -DestinationPath $zip -CompressionLevel Optimal
}
Get-ChildItem $stage | Format-Table Name, Length -AutoSize
