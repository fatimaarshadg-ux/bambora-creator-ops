# Bambora creator-ops handover: ONE installer for a Windows PC that has nothing on it yet.
#
# Run it from PowerShell (the "-ExecutionPolicy Bypass" applies to this one run only):
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\install.ps1"
#
# What it does, in order (each step says PASS, SKIP or what went wrong):
#   1. Puts this repo at %USERPROFILE%\claude-setup (every note and script expects it there)
#   2. Installs the programs with winget: Git, Python, Chrome, Node.js, ffmpeg, yt-dlp,
#      Google Drive for desktop, GitHub CLI, and the Claude desktop app (skips anything already there)
#   3. Installs the Python packages the scripts use (Pillow, numpy, faster-whisper, yt-dlp)
#   4. Makes Python print emoji and names correctly (PYTHONUTF8) and adds a python3 shim for Git Bash
#   5. Creates the working folder %USERPROFILE%\Bombara (brief, checklist, Trybe data, Trybe MCP server)
#   6. Installs the media watcher (lets Claude watch videos and hear audio)
#   7. Copies the skills, the memory and the global instructions (CLAUDE.md) into %USERPROFILE%\.claude
#   8. Stores the Trybe API key with Windows DPAPI (a masked box asks for it; nothing is written in plain text)
#   9. Optionally adds the routine's permission allowlist and the no-em-dash hooks to Claude's settings
#  10. Self-test: PASS or FAIL for every piece
#
# Safe to run again: it skips what is done, never deletes your work, and backs up anything it replaces.
#   -Refresh   also overwrite skills and memory files that differ on this PC (backups are kept)
#   -NoWinget  skip program installs (if you installed everything by hand from the README links)
param([switch]$Refresh, [switch]$NoWinget)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
$utf8 = New-Object Text.UTF8Encoding $false
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$results = New-Object System.Collections.ArrayList

function Step($n, $text) { Write-Host ""; Write-Host "[$n/10] $text" -ForegroundColor Cyan }
function Say($text) { Write-Host "       $text" }
function Warn($text) { Write-Host "       $text" -ForegroundColor Yellow }
function Refresh-Path {
    $m = [Environment]::GetEnvironmentVariable("Path", "Machine")
    $u = [Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = "$m;$u"
}
function Has($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
# Run a program quietly and return its exit code (PowerShell 5.1 turns stderr into errors otherwise).
function Run {
    $exe = $args[0]; $rest = @($args | Select-Object -Skip 1)
    try { & $exe @rest 2>&1 | Out-Null; return $LASTEXITCODE } catch { return 1 }
}
function Check($name, $ok, $hint) {
    [void]$results.Add([pscustomobject]@{ Item = $name; Result = $(if ($ok) { "PASS" } else { "FAIL" }); Fix = $(if ($ok) { "" } else { $hint }) })
}
function Write-Utf8($path, $text) {
    New-Item -ItemType Directory -Force (Split-Path $path) | Out-Null
    [IO.File]::WriteAllText($path, $text, $utf8)
}

Write-Host "== Bambora creator ops: Windows install ==" -ForegroundColor Green
Write-Host "This takes 15 to 40 minutes the first time (mostly downloads). You can use the PC meanwhile."
Write-Host "Nothing here needs your passwords. The only thing you paste is the Trybe API key, into a hidden box."

# ---------------------------------------------------------------- 1. repo location
Step 1 "Putting this repo at %USERPROFILE%\claude-setup"
$here = (Resolve-Path $PSScriptRoot).Path.TrimEnd('\')
$repo = Join-Path $env:USERPROFILE "claude-setup"
if ($here -ne $repo) {
    if (Test-Path (Join-Path $repo "install.ps1")) {
        Warn "There is already a copy at $repo. Using that one (it is where all the notes point)."
        Warn "If you meant to update it, run: git -C `"$repo`" pull"
    } else {
        New-Item -ItemType Directory -Force $repo | Out-Null
        robocopy $here $repo /E /NFL /NDL /NJH /NJS /NP /XD node_modules | Out-Null
        Say "copied from $here"
    }
} else { Say "already there" }
Set-Location $repo

# ---------------------------------------------------------------- 2. programs
Step 2 "Installing programs (winget)"
$apps = @(
    @{ Id = "Git.Git";              Test = { Has git };     Name = "Git (includes Git Bash, which Claude Code needs)" },
    @{ Id = "Python.Python.3.12";   Test = { Has py };      Name = "Python 3.12" },
    @{ Id = "Google.Chrome";        Test = { (Test-Path "$env:ProgramFiles\Google\Chrome\Application\chrome.exe") -or (Test-Path "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe") -or (Test-Path "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe") }; Name = "Google Chrome" },
    @{ Id = "OpenJS.NodeJS.LTS";    Test = { Has node };    Name = "Node.js (runs the Trybe MCP server)" },
    @{ Id = "Gyan.FFmpeg";          Test = { Has ffmpeg };  Name = "ffmpeg (video frames)" },
    @{ Id = "yt-dlp.yt-dlp";        Test = { Has yt-dlp };  Name = "yt-dlp (TikTok, Instagram and YouTube videos)" },
    @{ Id = "Google.GoogleDrive";   Test = { (Test-Path "$env:ProgramFiles\Google\Drive File Stream") };  Name = "Google Drive for desktop (uploads to Drive)" },
    @{ Id = "GitHub.cli";           Test = { Has gh };      Name = "GitHub CLI (push and pull the repo)" },
    @{ Id = "Anthropic.Claude";     Test = { (Test-Path "$env:LOCALAPPDATA\AnthropicClaude") -or (Test-Path "$env:LOCALAPPDATA\Programs\Claude") -or (Has claude) }; Name = "Claude desktop app (Claude Code lives in its Code tab)" }
)
if ($NoWinget) {
    Say "skipped (-NoWinget)"
} elseif (-not (Has winget)) {
    Warn "winget is not on this PC (it comes with the Microsoft 'App Installer'). Install the programs by hand from the README links, then rerun with -NoWinget."
} else {
    $missing = @($apps | Where-Object { -not (& $_.Test) })
    if ($missing.Count -eq 0) { Say "everything is already installed" }
    else {
        Say "Will install:"
        $missing | ForEach-Object { Say "  - $($_.Name)" }
        Say "(winget accepts each program's standard license for you; Windows may ask 'allow changes?' for some. Click Yes.)"
        foreach ($a in $missing) {
            Say "installing $($a.Name) ..."
            $code = Run winget install -e --id $a.Id --silent --accept-package-agreements --accept-source-agreements
            Refresh-Path
            if (& $a.Test) { Say "  ok" } else { Warn "  winget returned $code. If it is still missing at the end, install it from the README link." }
        }
    }
}
Refresh-Path

# ---------------------------------------------------------------- 3. python packages
Step 3 "Python packages for the scripts"
if (Has py) {
    Run py -3 -m pip install --user --upgrade --disable-pip-version-check pip | Out-Null
    $code = Run py -3 -m pip install --user --upgrade --disable-pip-version-check pillow numpy faster-whisper yt-dlp
    if ($code -eq 0) { Say "Pillow, numpy, faster-whisper, yt-dlp installed" } else { Warn "pip returned $code (check the internet connection and rerun)" }
} else { Warn "Python is not installed yet, so this was skipped. Rerun install.ps1 after installing Python." }

# ---------------------------------------------------------------- 4. utf-8 + shims
Step 4 "Text encoding and a python3 shim for Git Bash"
[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User"); $env:PYTHONUTF8 = "1"
[Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User"); $env:PYTHONIOENCODING = "utf-8"
$bin = Join-Path $env:USERPROFILE "bin"
New-Item -ItemType Directory -Force $bin | Out-Null
Write-Utf8 (Join-Path $bin "python3") "#!/bin/sh`nexec py -3 `"`$@`"`n"
$bashrc = Join-Path $env:USERPROFILE ".bashrc"
$line = 'export PATH="$HOME/bin:$PATH"; export PYTHONUTF8=1; export PYTHONIOENCODING=utf-8  # bambora-ops'
$have = ""; if (Test-Path $bashrc) { $have = [IO.File]::ReadAllText($bashrc) }
if ($have -notmatch "bambora-ops") { [IO.File]::AppendAllText($bashrc, "`n$line`n", $utf8) }
$profileFile = Join-Path $env:USERPROFILE ".bash_profile"
if (-not (Test-Path $profileFile)) { Write-Utf8 $profileFile "test -f ~/.bashrc && . ~/.bashrc`n" }
Say "PYTHONUTF8=1 set for your user; ~/bin/python3 runs py -3 in Git Bash"

# ---------------------------------------------------------------- 5. working folder
Step 5 "Working folder %USERPROFILE%\Bombara"
$work = Join-Path $env:USERPROFILE "Bombara"
New-Item -ItemType Directory -Force $work | Out-Null
robocopy (Join-Path $repo "work\bombara-folder") $work /E /XO /NFL /NDL /NJH /NJS /NP /XD node_modules | Out-Null
Say "copied the brief, checklist, Trybe data and the Trybe MCP server (newer files on this PC are kept)"
$mcp = Join-Path $work "trybe-review\mcp-server"
if ((Has npm) -and (Test-Path (Join-Path $mcp "package.json"))) {
    Push-Location $mcp; $code = Run npm install --silent --no-audit --no-fund; Pop-Location
    if ($code -eq 0) { Say "Trybe MCP server packages installed" } else { Warn "npm install returned $code" }
}
if ((Has npm) -and (Test-Path (Join-Path $work "package.json"))) {
    Push-Location $work; Run npm install --silent --no-audit --no-fund | Out-Null; Pop-Location
}
# Claude Code names each project's memory folder after its path: every character that is not a
# letter or digit becomes "-". C:\Users\Sara\Bombara -> C--Users-Sara-Bombara
$slug = [regex]::Replace($work, '[^a-zA-Z0-9]', '-')
Write-Utf8 (Join-Path $repo ".project-slug") "$slug`n"
Say "Claude's memory folder for it: .claude\projects\$slug\memory"

# ---------------------------------------------------------------- 6. media watcher
Step 6 "Media watcher (lets Claude watch videos). 3 to 15 minutes, about 900 MB, once."
$mwInstaller = Join-Path $repo "tools\claude-media-watcher\install.ps1"
$mwPy = Join-Path $env:USERPROFILE "claude-media-watcher\.venv\Scripts\python.exe"
if ((Test-Path $mwPy) -and -not $Refresh) { Say "already installed (rerun with -Refresh to update)" }
else {
    & powershell -NoProfile -ExecutionPolicy Bypass -File $mwInstaller
    if ($LASTEXITCODE -ne 0) { Warn "The media watcher installer stopped. Rerun install.ps1; it continues where it left off." }
}
# ffmpeg and yt-dlp fallback: if winget could not install them, use the media watcher's copies
$mwBin = Join-Path $env:USERPROFILE "claude-media-watcher\bin"
if ((Test-Path $mwBin) -and (-not (Has ffmpeg) -or -not (Has yt-dlp))) {
    $u = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($u -notlike "*claude-media-watcher\bin*") { [Environment]::SetEnvironmentVariable("Path", "$u;$mwBin", "User") }
    Refresh-Path
    Say "added $mwBin to your PATH (ffmpeg, ffprobe, yt-dlp)"
}

# ---------------------------------------------------------------- 7. skills, memory, CLAUDE.md
Step 7 "Skills, memory and Claude's global instructions"
$claude = Join-Path $env:USERPROFILE ".claude"
$skillsDir = Join-Path $claude "skills"
$memDir = Join-Path $claude "projects\$slug\memory"
New-Item -ItemType Directory -Force $skillsDir, $memDir | Out-Null

function Install-Text($src, $dst) {
    # copies one file, replacing the <PROJECT> placeholder with this PC's project folder name
    $isText = $src -match '\.(md|txt|py|json|js|ps1|sh)$'
    if ($isText) { $new = [IO.File]::ReadAllText($src).Replace("<PROJECT>", $slug) }
    if (Test-Path $dst) {
        $same = $false
        if ($isText) { $same = ([IO.File]::ReadAllText($dst) -eq $new) } else { $same = ((Get-FileHash $src).Hash -eq (Get-FileHash $dst).Hash) }
        if ($same) { return "same" }
        if (-not $Refresh) { return "kept" }
        Copy-Item $dst "$dst.bak-$stamp" -Force
    }
    New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
    if ($isText) { [IO.File]::WriteAllText($dst, $new, $utf8) } else { Copy-Item $src $dst -Force }
    return "written"
}
$kept = 0; $written = 0
foreach ($f in Get-ChildItem (Join-Path $repo "skills") -Recurse -File) {
    $rel = $f.FullName.Substring((Join-Path $repo "skills").Length).TrimStart('\')
    $dst = Join-Path $skillsDir $rel
    # the media watcher's own installer just wrote its generic skill; always put the Bambora one back
    if ($rel -like "media-watcher\*" -and (Test-Path $dst)) { Remove-Item $dst -Force }
    $r = Install-Text $f.FullName $dst
    if ($r -eq "kept") { $kept++ } elseif ($r -eq "written") { $written++ }
}
foreach ($f in Get-ChildItem (Join-Path $repo "memory") -Filter *.md -File) {
    if ($f.Name -eq "MEMORY.md") { continue }
    $r = Install-Text $f.FullName (Join-Path $memDir $f.Name)
    if ($r -eq "kept") { $kept++ } elseif ($r -eq "written") { $written++ }
}
# The memory index: add missing lines, never overwrite
$idx = Join-Path $memDir "MEMORY.md"
$haveLines = @(); if (Test-Path $idx) { $haveLines = [IO.File]::ReadAllLines($idx) }
$add = @()
foreach ($l in [IO.File]::ReadAllLines((Join-Path $repo "memory\MEMORY.md"))) {
    $l2 = $l.Replace("<PROJECT>", $slug)
    if ($l2.Trim() -and ($haveLines -notcontains $l2)) { $add += $l2 }
}
if ($add.Count -gt 0) { [IO.File]::AppendAllText($idx, (($add -join "`n") + "`n"), $utf8) }
Say "$written file(s) written, $kept kept because this PC's copy is different (rerun with -Refresh to replace them; backups are kept)"

# Scheduled task prompts (the tasks themselves are created in the Claude app, see docs\07-scheduled-tasks.md)
foreach ($t in Get-ChildItem (Join-Path $repo "scheduled-tasks") -Directory) {
    Install-Text (Join-Path $t.FullName "SKILL.md") (Join-Path $claude "scheduled-tasks\$($t.Name)\SKILL.md") | Out-Null
}

# CLAUDE.md: ours goes between markers; anything that was there before is kept below it and backed up
$cm = Join-Path $claude "CLAUDE.md"
$ours = [IO.File]::ReadAllText((Join-Path $repo "claude\CLAUDE.md")).Replace("<PROJECT>", $slug)
$block = "<!-- bambora-ops:start (installed by claude-setup\install.ps1; edit claude-setup\claude\CLAUDE.md instead) -->`n" + $ours.TrimEnd() + "`n<!-- bambora-ops:end -->`n"
if (Test-Path $cm) {
    $old = [IO.File]::ReadAllText($cm)
    Copy-Item $cm "$cm.bak-$stamp" -Force
    $m = [regex]::Match($old, '(?s)<!-- bambora-ops:start.*?<!-- bambora-ops:end -->\r?\n?')
    if ($m.Success) {
        $new = $old.Substring(0, $m.Index) + $block + $old.Substring($m.Index + $m.Length)
    } else {
        $new = $block + "`n# Earlier instructions on this PC (kept by install.ps1)`n`n" + $old
    }
    [IO.File]::WriteAllText($cm, $new, $utf8)
    Say "CLAUDE.md updated (backup: CLAUDE.md.bak-$stamp)"
} else {
    [IO.File]::WriteAllText($cm, $block, $utf8)
    Say "CLAUDE.md written"
}

# Git for this repo: the no-em-dash commit guard, and a name for commits
if (Has git) {
    Run git -C $repo config core.hooksPath hooks | Out-Null
    $gname = (& git -C $repo config user.name) 2>$null
    if (-not $gname) {
        $n = Read-Host "Your first name, for the repo's history (press Enter for 'Bambora operator')"
        if (-not $n) { $n = "Bambora operator" }
        Run git -C $repo config user.name $n | Out-Null
        Run git -C $repo config user.email "operator@users.noreply.github.com" | Out-Null
    }
}

# ---------------------------------------------------------------- 8. Trybe key
Step 8 "Trybe API key (stored with Windows DPAPI)"
$keyFile = Join-Path $claude "secrets\trybe_api_key.dpapi"
if (Test-Path $keyFile) { Say "already stored" }
else {
    Say "A small window will open. Paste the Trybe key Fatima gave you (Ctrl+V) and click OK."
    Say "No key yet? Click 'Skip for now' and run work\common\store-trybe-key.ps1 later."
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo "work\common\store-trybe-key.ps1")
}

# ---------------------------------------------------------------- 9. permissions
Step 9 "Claude permissions for the routine (optional, recommended)"
Say "This lets the unattended routine run its own scripts without stopping for a yes every time."
Say "It only ADDS entries to %USERPROFILE%\.claude\settings.json and backs the file up first."
$ans = Read-Host "Add them now? (Y/n)"
if ($ans -eq "" -or $ans -match '^[Yy]') {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo "settings\apply-settings.ps1")
} else { Say "skipped. Run settings\apply-settings.ps1 any time." }

# ---------------------------------------------------------------- 10. self-test
Step 10 "Self-test"
Refresh-Path
$gitBash = (Test-Path "$env:ProgramFiles\Git\bin\bash.exe") -or (Test-Path "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe")
Check "Git + Git Bash" ((Has git) -and $gitBash) "winget install Git.Git (or https://git-scm.com/download/win)"
Check "Python (py -3)" ((Has py) -and ((Run py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)") -eq 0)) "winget install Python.Python.3.12 (or https://www.python.org/downloads/windows/)"
Check "Python packages (Pillow, numpy, faster-whisper)" ((Has py) -and ((Run py -3 -c "import PIL, numpy, faster_whisper") -eq 0)) "py -3 -m pip install --user pillow numpy faster-whisper"
Check "ffmpeg + ffprobe" ((Has ffmpeg) -and (Has ffprobe)) "winget install Gyan.FFmpeg, then open a new PowerShell"
Check "yt-dlp" (Has yt-dlp) "winget install yt-dlp.yt-dlp"
Check "Node.js (Trybe MCP server)" ((Has node) -and (Test-Path (Join-Path $mcp "node_modules"))) "winget install OpenJS.NodeJS.LTS, then rerun install.ps1"
Check "Google Chrome" (& $apps[2].Test) "https://www.google.com/chrome/"
Check "Google Drive for desktop" (& $apps[6].Test) "winget install Google.GoogleDrive (or https://www.google.com/drive/download/)"
Check "Claude desktop app / Claude Code" (& $apps[8].Test) "https://claude.ai/download"
Check "Working folder ~/Bombara" (Test-Path (Join-Path $work "bambora-content-checklist.html")) "rerun install.ps1"
$nSkills = @(Get-ChildItem $skillsDir -Directory -ErrorAction SilentlyContinue).Count
Check "Skills installed ($nSkills)" ((Test-Path (Join-Path $skillsDir "creator-ops-daily\SKILL.md")) -and (Test-Path (Join-Path $skillsDir "fatima-creator-voice\lessons.md"))) "rerun install.ps1"
$nMem = @(Get-ChildItem $memDir -Filter *.md -ErrorAction SilentlyContinue).Count
Check "Memory installed ($nMem files)" ((Test-Path (Join-Path $memDir "core-rules.md")) -and (Test-Path $idx)) "rerun install.ps1"
Check "CLAUDE.md" ((Test-Path $cm) -and ([IO.File]::ReadAllText($cm) -match "bambora-ops:start")) "rerun install.ps1"
Check "Media watcher" ((Test-Path $mwPy) -and (Test-Path (Join-Path $env:USERPROFILE "claude-media-watcher\watch.cmd"))) "rerun install.ps1 (it continues where it stopped)"
$ledgerOk = $false
if (Has py) { $ledgerOk = ((Run py -3 (Join-Path $repo "work\creator-db\followups.py") due) -eq 0) }
Check "Follow-up ledger (followups.py due)" $ledgerOk "py -3 %USERPROFILE%\claude-setup\work\creator-db\followups.py due"
$lintOk = $false
if (Has py) { $lintOk = ((Run py -3 (Join-Path $repo "work\trybe-chat\lint_message.py") "awesome!! thank you") -eq 0) }
Check "Message linter (lint_message.py)" $lintOk "py -3 %USERPROFILE%\claude-setup\work\trybe-chat\lint_message.py test"
Check "Stream tracker (streams.ps1)" ((Run powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo "work\sweep\streams.ps1") status) -eq 0) "see work\sweep\streams.ps1"
$keyOk = $false
if ((Has py) -and (Test-Path $keyFile)) { $keyOk = ((Run py -3 (Join-Path $repo "work\common\trybe_key.py") --check) -eq 0) }
Check "Trybe API key stored and working" $keyOk "powershell -NoProfile -ExecutionPolicy Bypass -File %USERPROFILE%\claude-setup\work\common\store-trybe-key.ps1 -Force (ask Fatima for the key)"
Check "PYTHONUTF8 set" ([Environment]::GetEnvironmentVariable("PYTHONUTF8", "User") -eq "1") "rerun install.ps1"

Write-Host ""
$results | Format-Table -AutoSize | Out-String -Width 200 | Write-Host
$fails = @($results | Where-Object { $_.Result -eq "FAIL" }).Count
if ($fails -eq 0) {
    Write-Host "ALL PASS. Next: open the Claude app, Code tab, choose the folder $work, and paste FIRST-PROMPT.md." -ForegroundColor Green
} else {
    Write-Host "$fails item(s) FAILED. Fix each with the hint in the Fix column, then run install.ps1 again (it skips what is done)." -ForegroundColor Yellow
    Write-Host "After installing a program, open a NEW PowerShell window before rerunning, so Windows sees it."
}
