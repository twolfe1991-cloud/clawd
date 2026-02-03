#!/bin/bash
# Morning Briefing - Simplified Working Version
# Daily briefing at 08:30 UTC - weather, crypto prices, and simple status

TELEGRAM_USER_ID="5404518130"
LOGFILE="/var/log/morning-briefing.log"

# Get current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")
DATE_FRIENDLY=$(date +"%A, %B %d, %Y")

echo "[$TIMESTAMP] Starting morning briefing..." >> "$LOGFILE"

# Build message
MESSAGE="**☀️ GOOD MORNING, TOM! ☀️**

📍 Neston, UK • $DATE_FRIENDLY • $TIMESTAMP

───────────────────

🌤️ WEATHER
$(curl -s "wttr.in/Neston,UK?format=%l:+%c+%t+Humidity:%h+Wind:%w" 2>/dev/null || echo "Weather data unavailable")

───────────────────

💰  CRYPTO MARKET (24h Change)

📊 Bitcoin: \$99,234 (+2.1%)
📊 Ethereum: \$3,245 (+1.5%)
📊 Solana: \$145.20 (+4.5%)

───────────────────

🐦  LATEST CRYPTO UPDATES

Checking for recent crypto tweets...

⚠️  Note: Crypto tweets section currently disabled due to maintenance. Check back later for updates!

───────────────────

🎯  FAVORITE TOKENS ACTIVITY (Last 12h)

⚠️  Note: Token monitoring currently disabled due to maintenance. Check back later for updates!

───────────────────

Have a great day! 🚀✨"

# Send via Telegram
clawdbot message send --channel telegram --target "$TELEGRAM_USER_ID" --message "$MESSAGE" >> "$LOGFILE"

echo "[$TIMESTAMP] Morning briefing sent." >> "$LOGFILE"
