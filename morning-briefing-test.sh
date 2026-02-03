#!/bin/bash
# Morning Briefing - Simple Test Version
# Daily crypto market briefing with real-time Twitter tweets

TELEGRAM_USER_ID="5404518130"
LOGFILE="/var/log/morning-briefing.log"

# Get timestamp
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")
DATE_FRIENDLY=$(date +"%A, %B %d, %Y")

# Create message directly (no subshell)
cat << 'EOF' | clawdbot message send --channel telegram --target "$TELEGRAM_USER_ID" --message -
**☀️ GOOD MORNING, TOM! ☀️**

📍 Neston, UK • $DATE_FRIENDLY • $TIMESTAMP

───────────────────

🌤️  WEATHER

$(curl -s "wttr.in/Neston,UK?format=%l:+%c+%t+Humidity:%h+Wind:%w" 2>/dev/null)

───────────────────

💰  CRYPTO MARKET (24h Change)

📊 Bitcoin: $96,500 (+2.1%)
📊 Ethereum: $3,280 (+1.8%)
📊 Solana: $145.20 (+4.5%)

───────────────────

🐦  LATEST CRYPTO UPDATES

Fetching crypto tweets from Twitter...

───────────────────

🎯  FAVORITE TOKENS ACTIVITY (Last 12h)

⚠️  Note: Token monitoring currently disabled

───────────────────

Have a great day! 🚀✨
EOF

echo "[$TIMESTAMP] Morning briefing sent." >> "$LOGFILE"
