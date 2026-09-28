# Prints the current US Eastern time and whether creator messages may go out yet.
# Fatima's send window (2026-09-27): nothing to creators before 12 PM US Eastern.
$et = [TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, 'Eastern Standard Time')
$open = $et.Hour -ge 12
Write-Output ("US Eastern: {0:yyyy-MM-dd HH:mm}  send window: {1}" -f $et, $(if ($open) { "OPEN (send the queue, then send normally)" } else { "CLOSED until 12:00 ET (queue in work/send-queue/<date>.md)" }))
