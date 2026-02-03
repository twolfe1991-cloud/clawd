#!/bin/bash
# Morning Briefing - Final Version
# Calls Python script directly for clean execution

TELEGRAM_USER_ID="5404518130"
LOGFILE="/var/log/morning-briefing.log"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")
DATE_FRIENDLY=$(date +"%A, %B %d, %Y")

echo "[$(date -u)] Starting morning briefing..." >> "$LOGFILE"

# Call Python script directly
python3 /root/clawd/morning-briefing-crypto.py >> "$LOGFILE" 2>&1

echo "[$(date -u)] Morning briefing sent." >> "$LOGFILE"
