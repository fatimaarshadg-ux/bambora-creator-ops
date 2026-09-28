---
name: bambora-drive-approved-videos
description: Where approved Trybe videos get filed in Google Drive and the exact naming convention
metadata:
  type: reference
---

Approved Trybe submission videos go in the Drive folder **"Trybe"**: https://drive.google.com/drive/folders/1kleoyEuzTGxftUvYKwSK3aVUDTKkG53R (folder id `1kleoyEuzTGxftUvYKwSK3aVUDTKkG53R`, owned by fatima@bamboraco.com, empty as of 2026-09-23).

**Naming convention** (from her screenshot, 2026-09-23): `{CreatorFullNameNoSpaces}/fatima/trybe={trybe_id}`
- trybe_id = the 8-character short id, which is the last 8 characters of the `submission_<uuid>`.
- Examples: `BrittanyArchutowski/fatima/trybe=6c916aab`, `JenniferThomas/fatima/trybe=ecd22a7c`. Her examples mix a space before the first slash (Jennifer) with no space (Brittany); use no space unless she says otherwise.

**How to upload:** the Drive connector's create_file takes base64 content, which doesn't suit 30-60MB videos. Use the browser upload method in [[windows-drive-upload-technique]]. Download the fresh `asset.url` from the API first; it expires in about 20 minutes.


Her "Bambora_Trybe_DM_History" and "Tasks for Trybe Management" Google Docs are **not for Claude to use** (she said so on 2026-09-23). Leave them alone.

**Main Media is the media buyers' drive (Fatima, 2026-09-25):** only approved Trybe submissions go there (Main Media > Trybe). Inspo, example videos for creators, and anything else go in My Drive > Bambora Inspo (link-shared), never Main Media.

**Liam's sheet RETIRED (Fatima, 2026-09-27):** approved videos no longer go into Liam's ad-launcher sheet or his folder. Filing = upload to Main Media > Trybe (this folder), named as above, then `file_approved.py --mark`. Nothing else. Don't run liam_launch.py.
