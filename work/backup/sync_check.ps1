# Nightly (Windows port of sync_check.sh): make sure everything on this PC that Claude relies on is in
# the claude-setup repo. Copies (never deletes) skills, memory files and scheduled-task prompts that are
# missing or different on the PC, then prints what changed. MEMORY.md is never overwritten: new index
# lines are appended. The memory folder is found from the working folder name (see install.ps1).
#   powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\backup\sync_check.ps1"
$repo = Join-Path $env:USERPROFILE "claude-setup"
$claude = Join-Path $env:USERPROFILE ".claude"
$slugFile = Join-Path $repo ".project-slug"
if (-not (Test-Path $slugFile)) { Write-Output "Missing $slugFile (install.ps1 writes it). Run install.ps1 once."; exit 1 }
$slug = (Get-Content $slugFile -Raw).Trim()
$mem = Join-Path $claude "projects\$slug\memory"

function Same($a, $b) {
    if (-not (Test-Path $b)) { return $false }
    return ((Get-FileHash $a).Hash -eq (Get-FileHash $b).Hash)
}
# The installed copies have the real project folder name where the repo has <PROJECT>; compare
# with that swapped back so an unchanged file is not reported as changed.
function Restore($text) { return $text.Replace($slug, "<PROJECT>") }
$utf8 = New-Object Text.UTF8Encoding $false

foreach ($s in Get-ChildItem (Join-Path $claude "skills") -Directory) {
    foreach ($f in Get-ChildItem $s.FullName -Recurse -File | Where-Object { $_.FullName -notmatch '\\(\.git|__pycache__|\.venv)\\' }) {
        $rel = $f.FullName.Substring($s.FullName.Length).TrimStart('\')
        $dst = Join-Path $repo "skills\$($s.Name)\$rel"
        if ($f.Extension -eq ".md") {
            $t = Restore ([IO.File]::ReadAllText($f.FullName))
            if (-not (Test-Path $dst) -or [IO.File]::ReadAllText($dst) -ne $t) {
                New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
                [IO.File]::WriteAllText($dst, $t, $utf8); Write-Output "skill synced: $($s.Name)\$rel"
            }
        } elseif (-not (Same $f.FullName $dst)) {
            New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
            Copy-Item $f.FullName $dst -Force; Write-Output "skill synced: $($s.Name)\$rel"
        }
    }
}

if (Test-Path $mem) {
    foreach ($f in Get-ChildItem $mem -Filter *.md -File) {
        if ($f.Name -eq "MEMORY.md") { continue }
        $dst = Join-Path $repo "memory\$($f.Name)"
        $t = Restore ([IO.File]::ReadAllText($f.FullName))
        if (-not (Test-Path $dst) -or [IO.File]::ReadAllText($dst) -ne $t) { [IO.File]::WriteAllText($dst, $t, $utf8); Write-Output "memory synced: $($f.Name)" }
    }
    $repoIndex = Join-Path $repo "memory\MEMORY.md"
    $have = [IO.File]::ReadAllLines($repoIndex)
    foreach ($line in [IO.File]::ReadAllLines((Join-Path $mem "MEMORY.md"))) {
        $l = Restore $line
        if ($l.Trim() -and ($have -notcontains $l)) { [IO.File]::AppendAllText($repoIndex, $l + "`n", $utf8); Write-Output ("index line added: " + $l.Substring(0, [Math]::Min(60, $l.Length))) }
    }
}

$tasks = Join-Path $claude "scheduled-tasks"
if (Test-Path $tasks) {
    foreach ($t in Get-ChildItem $tasks -Directory) {
        $src = Join-Path $t.FullName "SKILL.md"
        if (-not (Test-Path $src)) { continue }
        $dst = Join-Path $repo "scheduled-tasks\$($t.Name)\SKILL.md"
        $txt = Restore ([IO.File]::ReadAllText($src))
        if (-not (Test-Path $dst) -or [IO.File]::ReadAllText($dst) -ne $txt) {
            New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
            [IO.File]::WriteAllText($dst, $txt, $utf8); Write-Output "task prompt synced: $($t.Name)"
        }
    }
}

$cm = Join-Path $claude "CLAUDE.md"
$cmRepo = Join-Path $repo "claude\CLAUDE.md"
if (Test-Path $cm) {
    $txt = Restore ([IO.File]::ReadAllText($cm))
    if ([IO.File]::ReadAllText($cmRepo) -ne $txt) { [IO.File]::WriteAllText($cmRepo, $txt, $utf8); Write-Output "CLAUDE.md synced" }
}
Write-Output "sync check done"
