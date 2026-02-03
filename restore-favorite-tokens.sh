#!/bin/bash
# Morning Briefing - Restore Favorite Token Monitoring
# Restores the version with favorite token tracking

TELEGRAM_USER_ID="5404518130"
LOGFILE="/var/log/morning-briefing.log"

# Copy the working version with token monitoring
cp /root/clawd/morning-briefing-final.sh /root/clawd/morning-briefing.sh

echo "✅ Restored morning briefing script with favorite token monitoring"
echo "📍 Script: /root/clawd/morning-briefing.sh"
echo "🔄 Ready to test - this version includes crypto tweets + favorite tokens"

# Run it now for test
bash /root/clawd/morning-briefing.sh 2>&1 | tail -50
