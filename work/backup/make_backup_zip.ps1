# Zip the whole claude-setup repo (history included) for the nightly Drive backup (Windows port of
# make_backup_zip.sh). Fatima's rule, 2026-09-23: "everything should be backed up on Drive so it's not
# reliant on my device". Output: %USERPROFILE%\claude-backup-staging\claude-setup-YYYY-MM-DD.zip, alone
# in that folder. Secrets never live in the repo, so the zip holds none.
# Upload it with: drive-upload.ps1 -Source "$env:USERPROFILE\claude-backup-staging" -Target Backup
$stage = Join-Path $env:USERPROFILE "claude-backup-staging"
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Force $stage | Out-Null
$zip = Join-Path $stage ("claude-setup-" + (Get-Date -Format "yyyy-MM-dd") + ".zip")
Compress-Archive -Path (Join-Path $env:USERPROFILE "claude-setup") -DestinationPath $zip -CompressionLevel Optimal
Get-ChildItem $stage | Format-Table Name, Length -AutoSize
