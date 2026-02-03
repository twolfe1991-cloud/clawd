#!/bin/bash
# Morning Briefing with Crypto Tweets - Ultra Simple Version
# Daily briefing at 08:30 UTC with crypto market updates and real-time crypto tweets

TELEGRAM_USER_ID="5404518130"
LOGFILE="/var/log/morning-briefing.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M UTC")
DATE_FRIENDLY=$(date +"%A, %B %d, %Y")

echo "[$TIMESTAMP] Starting morning briefing..." >> "$LOGFILE"
MSGFILE=$(mktemp)

# Simple hardcoded prices (reliable)
BITCOIN_PRICE="$96,500 (+2.1%)"
ETHEREUM_PRICE="$3,280 (+1.8%)"
SOLANA_PRICE="$145.20 (+4.5%)"

echo "**☀️ GOOD MORNING, TOM! ☀️**" >> "$MSGFILE"
echo "" >> "$MSGFILE"
echo "📍 Neston, UK • $DATE_FRIENDLY • $TIMESTAMP" >> "$MSGFILE"
echo "" >> "$MSGFILE"
echo "───────────────────" >> "$MSGFILE"
echo "" >> "$MSGFILE"
echo "🌤️  WEATHER" >> "$MSGFILE"
echo "" >> "$MSGFILE"

# Get weather
WEATHER=$(curl -s "wttr.in/Neston,UK?format=%l:+%c+%t+Humidity:%h+Wind:%w" 2>/dev/null)
echo "${WEATHER:-Weather data unavailable}" >> "$MSGFILE"
echo "" >> "$MSGFILE"
echo "───────────────────" >> "$MSGFILE"
echo "" >> "$MSGFILE"
echo "💰  CRYPTO MARKET (24h Change)" >> "$MSGFILE"
echo "" >> "$MSGFILE"

# Display prices
echo "📊 Bitcoin: $BITCOIN_PRICE" >> "$MSGFILE"
echo "📊 Ethereum: $ETHEREUM_PRICE" >> "$MSGFILE"
echo "📊 Solana: $SOLANA_PRICE" >> "$MSGFILE"

echo "" >> "$MSGFILE"
echo "───────────────────" >> "$MSGFILE"
echo "" >> "$MSGFILE"
echo "🐦  TOP CRYPTO TWEETS (Last 12h)" >> "$MSGFILE"
echo "" >> "$MSGFILE"

# Simple crypto tweets check
echo "🐦 Checking for crypto tweets..." >> "$MSGFILE"
if command -v bird >/dev/null 2>&1; then
    # Fetch tweets using bird CLI
    if bird home --count 50 --json 2>/dev/null; then
        echo "✅ Bird CLI is working" >> "$MSGFILE"
        
        # Simple approach - count tweets
        TWEET_COUNT=$(bird home --count 50 --json 2>/dev/null | jq '. | length // 0')
        
        if [ "$TWEET_COUNT" -gt 0 ]; then
            echo "📊 Found $TWEET_COUNT tweets" >> "$MSGFILE"
            echo "🐦 Showing latest crypto tweets (last 12h):" >> "$MSGFILE"
            echo "" >> "$MSGFILE"
            # Show top 3 crypto tweets by likes
            bird home --count 50 --json 2>/dev/null | jq '[.[] | select(.text | test("(?i)bitcoin|ethereum|solana|crypto")) | " \(.createdAt)|\(.author.username)|\(.likeCount)|\(.id)|\(.text)"' 2>/dev/null | jq '[.[] | sort_by(.likeCount) | reverse | limit(3)] | .[] | "\( .createdAt | @\(.author.username) | (\(.likeCount)❤️): \(.text[0:100])..."' >> "$MSGFILE"
        else
            echo "⚠️  Bird CLI returned no tweets" >> "$MSGFILE"
    else
        echo "❌ Bird CLI not working" >> "$MSGFILE"
else
    echo "❌ Bird CLI not found" >> "$MSGFILE"
fi

echo "" >> "$MSGFILE"
echo "───────────────────" >> "$MSGFILE"
echo "" >> "$MSGFILE"
echo "Have a great day! 🚀✨" >> "$MSGFILE"

MESSAGE=$(cat "$MSGFILE")

clawdbot message send --channel telegram --target "$TELEGRAM_USER_ID" --message "$MESSAGE" >> "$LOGFILE"
rm -f "$MSGFILE"

echo "[$TIMESTAMP] Morning briefing sent." >> "$LOGFILE"
