# Stores the Trybe Brand API key encrypted with Windows DPAPI, in
#   %USERPROFILE%\.claude\secrets\trybe_api_key.dpapi
# Only your Windows account on this PC can decrypt it. The key never goes into chat, shell history,
# or the repo. A small window asks for it (the text is hidden; Ctrl+V to paste).
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\common\store-trybe-key.ps1"
#
# Get the key from Fatima privately. Do NOT create a new key in Trybe without asking her first:
# a new key can replace the old one and break her own setup.
#
#   -Force  replace a key that is already stored
#   -Test   for the automated Windows test only (.github/workflows/windows-test.yml): no window opens and a
#           fixed DUMMY string (not a Trybe key) is stored through the same DPAPI code, so the scripts that
#           read the key can be tested. Never use it on the operator's PC: it would replace nothing useful
#           with a key that cannot log in.
param([switch]$Force, [switch]$Test)

# The dummy value the test stores and then reads back (it is public on purpose; it is not a key).
$TestKey = "bambora-ci-dummy-key-not-a-real-trybe-key"

function Save-Key($plain) {
    $len = $plain.Length
    if ($len -lt 10 -or $plain -match '[\x00-\x1F\s]') {
        Write-Host "That does not look like a Trybe key (length $len). Nothing saved. Run it again and paste with Ctrl+V."
        exit 1
    }
    $secure = ConvertTo-SecureString $plain -AsPlainText -Force
    $secure | ConvertFrom-SecureString | Set-Content -LiteralPath $path -Encoding ascii
    return $len
}

$dir = Join-Path $env:USERPROFILE ".claude\secrets"
New-Item -ItemType Directory -Force $dir | Out-Null
$path = Join-Path $dir "trybe_api_key.dpapi"

if ((Test-Path $path) -and -not $Force) {
    Write-Host "A Trybe key is already stored at $path"
    Write-Host "To replace it, run this again with -Force."
    exit 0
}

if ($Test) {
    $len = Save-Key $TestKey
    Write-Host "TEST MODE: stored the dummy test key ($len characters) at $path with DPAPI. It cannot log in to Trybe."
    exit 0
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$form = New-Object System.Windows.Forms.Form
$form.Text = "Trybe API key"
$form.Size = New-Object System.Drawing.Size(560, 180)
$form.StartPosition = "CenterScreen"
$form.TopMost = $true
$label = New-Object System.Windows.Forms.Label
$label.Text = "Paste the Trybe API key Fatima gave you (Ctrl+V), then click OK. It stays hidden."
$label.AutoSize = $true
$label.Location = New-Object System.Drawing.Point(12, 15)
$box = New-Object System.Windows.Forms.TextBox
$box.UseSystemPasswordChar = $true
$box.Width = 520
$box.Location = New-Object System.Drawing.Point(12, 45)
$ok = New-Object System.Windows.Forms.Button
$ok.Text = "OK"
$ok.Location = New-Object System.Drawing.Point(452, 90)
$ok.DialogResult = [System.Windows.Forms.DialogResult]::OK
$cancel = New-Object System.Windows.Forms.Button
$cancel.Text = "Skip for now"
$cancel.Width = 100
$cancel.Location = New-Object System.Drawing.Point(340, 90)
$cancel.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
$form.AcceptButton = $ok
$form.CancelButton = $cancel
$form.Controls.AddRange(@($label, $box, $ok, $cancel))
$form.Add_Shown({ $box.Focus() })

if ($form.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
    Write-Host "Skipped. No key saved. Run this script again when you have the key."
    exit 2
}
$len = Save-Key $box.Text.Trim()
$box.Text = ""
Write-Host "Saved the Trybe key ($len characters) at $path. Only your Windows account on this PC can read it."
