---
name: windows-drive-upload-technique
description: How to upload local files (approved videos, inspo packs, backups) to Google Drive on this Windows PC; replaces the Mac's AppleScript trick
metadata:
  type: reference
---

Uploading local files to Google Drive from this PC.

**Things that do NOT work (same as on the Mac):**
- Drive's web page has no `input[type=file]`, so the Chrome extension's `file_upload` has no target.
- Synthetic drag and drop fails (Chrome returns null from `webkitGetAsEntry()` for built DataTransfer items).
- The Drive connector's `create_file` needs base64 in the tool call, so any video blows the context window. Fine for small text files only.

**Main method: Google Drive for desktop (no browser at all).**
1. Installed by install.ps1 (`winget install Google.GoogleDrive`). The operator signs in once with the Bambora Google account. Drive then appears in File Explorer as a drive letter (usually `G:`) with `My Drive` and `Shared drives`.
2. Copy the files in: `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/trybe-drive-filing/drive-upload.ps1" -Source <folder> -Target Trybe` (or `-Target Inspo -Subfolder "Week of YYYY-MM-DD"`, or `-Target Backup`). It finds the folder, remembers it in `drive-folders.json`, and copies everything except `manifest.json`. If it cannot find a folder, run it with `-Find` and pass `-TargetPath`.
3. Wait for the upload (the Drive tray icon stops spinning; big videos take a few minutes).
4. Verify with the Drive connector: `search_files` with `parentId = '<folder id>'`. Trybe folder `1kleoyEuzTGxftUvYKwSK3aVUDTKkG53R`, Bambora Inspo `1HleYAep0n7C5gFGt3RhRsgy0dmiQEb8Y`, Repo snapshots `1FHhB0_QemdOFsdAMr2j7tLBDRYaBF5Yx`.
5. Rename each file with `update_file` to its manifest `drive_name` (for example `CreatorName/fatima/trybe=1234abcd`). Windows file names cannot contain "/", so files are copied as `CreatorName__fatima__trybe=1234abcd.mp4` and renamed in Drive.
6. Only after the rename is verified: `file_approved.py --mark <ids>`, then delete the local download folder.

**Fallback: the browser, with real keystrokes.** Chrome only opens a file chooser on a *trusted* gesture, and extension clicks do not count. Real keystrokes from Windows do:
1. With the Chrome extension, click Drive's **New** button (menus open fine that way).
2. `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/trybe-drive-filing/sendkeys.ps1" -Keys "{DOWN}{DOWN}{ENTER}"` (Down to "New folder", Down to "File upload", Enter).
3. In the Windows file dialog, the File name box has focus. Type the folder path and Enter to go there, then type the file names in quotes and Enter: `sendkeys.ps1 -NoFront -Text "C:\Users\<name>\Downloads\trybe-filing-2026-09-28" -Keys "{ENTER}"`, then `sendkeys.ps1 -NoFront -Text '"a.mp4" "b.mp4"' -Keys "{ENTER}"`. (Or Shift+Tab into the file list, Ctrl+A, Enter.)
4. Verify and rename with the Drive connector as above.
Before any keystroke, make sure Chrome is the front window (front.ps1), because the operator may be typing somewhere else. Never send keystrokes into a chat composer.

**Where things go (Fatima, 2026-09-25):** only approved Trybe submissions go to Main Media > Trybe (the media buyers' drive). Inspo, example videos and anything else go to My Drive > Bambora Inspo (link-shared), never Main Media. See [[bambora-drive-approved-videos]].

History: on the Mac this was New, then AppleScript key codes (Down, Down, Return), Cmd+Shift+G to the folder, Cmd+A, Return; it handled 15 videos (123 MB) in one go.
