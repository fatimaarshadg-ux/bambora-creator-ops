#!/bin/bash
# Windows handover: the Mac version used osascript. This wrapper runs the PowerShell port (front.ps1).
# Usage: bash front.sh [marker]   (marker defaults to cl=3)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/trybe-chat/front.ps1" "${1:-cl=3}"
