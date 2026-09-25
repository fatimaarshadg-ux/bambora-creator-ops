# Stores a secret encrypted with Windows DPAPI in ~\.claude\secrets\<Name>.dpapi (same approach as the Trybe key).
# A small popup asks for the value (masked, Ctrl+V works). The value never lands in chat or shell history.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\store-secret.ps1 -Name apify_api_token
#       token from https://console.apify.com/settings/integrations
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\store-secret.ps1 -Name slack_webhook
#       incoming webhook URL from https://api.slack.com/apps (Incoming Webhooks, channel #copycat-alerts)
param([Parameter(Mandatory = $true)][string]$Name)

$dir = Join-Path $env:USERPROFILE ".claude\secrets"
New-Item -ItemType Directory -Force $dir | Out-Null
$path = Join-Path $dir "$Name.dpapi"

Add-Type -AssemblyName System.Windows.Forms
$form = New-Object System.Windows.Forms.Form
$form.Text = "Store $Name"
$form.Size = New-Object System.Drawing.Size(520, 170)
$form.StartPosition = "CenterScreen"
$form.TopMost = $true
$label = New-Object System.Windows.Forms.Label
$label.Text = "Paste the value for $Name (Ctrl+V), then click OK. It is hidden as you paste."
$label.AutoSize = $true
$label.Location = New-Object System.Drawing.Point(12, 15)
$box = New-Object System.Windows.Forms.TextBox
$box.UseSystemPasswordChar = $true
$box.Width = 480
$box.Location = New-Object System.Drawing.Point(12, 45)
$ok = New-Object System.Windows.Forms.Button
$ok.Text = "OK"
$ok.Location = New-Object System.Drawing.Point(412, 85)
$ok.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $ok
$form.Controls.AddRange(@($label, $box, $ok))
$form.Add_Shown({ $box.Focus() })

if ($form.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { Write-Host "Cancelled. Nothing saved."; exit 1 }
$plain = $box.Text.Trim()
$len = $plain.Length
if ($len -lt 10 -or $plain -match '[\x00-\x1F]') {
    Write-Host "That does not look like a real value (length $len). Nothing saved. Run it again and paste with Ctrl+V into the box."
    exit 1
}
$secure = ConvertTo-SecureString $plain -AsPlainText -Force
$plain = $null
$secure | ConvertFrom-SecureString | Set-Content $path -Encoding ascii
Write-Host "Saved $Name ($len characters). Only your Windows account on this PC can decrypt it."
