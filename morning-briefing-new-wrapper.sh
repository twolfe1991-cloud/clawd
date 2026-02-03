#!/bin/bash
# Wrapper script for morning briefing

LOGFILE="/var/log/morning-briefing.log"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")

echo "[$TIMESTAMP] Starting morning briefing..." >> "$LOGFILE"

# Run the Python script
python3 /root/clawd/morning-briefing-new.py >> "$LOGFILE" 2>&1

echo "[$TIMESTAMP] Morning briefing completed." >> "$LOGFILE"
