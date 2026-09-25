#!/bin/bash
# Windows handover: the Mac version used caffeinate, lsof and /usr/bin/python3, which Git Bash does not have.
# This wrapper runs the PowerShell port (start.ps1) so old references to start.sh still work.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/sweep/start.ps1"
