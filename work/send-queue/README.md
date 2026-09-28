# Send queue

Creator messages, accepts, approvals and rejections only go out from 12 PM US Eastern (Fatima's rule, 2026-09-27). Before that, each sweep writes what it would send into `<date>.md` here. At 12 PM ET the next sweep sends the whole queue, then normal sending carries on.

Check it with (it also says whether the window is open):

    powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\work\common\us-time.ps1"
