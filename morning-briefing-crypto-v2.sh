#!/usr/bin/env python3
"""
Morning Briefing with Crypto Tweets - Robust Version
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Keywords for crypto
CRYPTO_KEYWORDS = ['bitcoin', 'ethereum', 'solana', 'crypto', 'btc', 'eth', 'defi', 'web3', 'blockchain', 'nft', 'token']

TELEGRAM_USER_ID="5404518130"
LOGFILE="/var/log/morning-briefing.log"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")
DATE_FRIENDLY=$(date +"%A, %B %d, %Y")

echo "[$(date -u)] Starting morning briefing..." >> "$LOGFILE"
MSGFILE=$(mktemp)

# Build message
{
    echo "**☀️ GOOD MORNING, TOM! ☀️**"
    echo ""
    echo "📍 Neston, UK • $DATE_FRIENDLY • $TIMESTAMP"
    echo ""
    echo "───────────────────"
    echo ""
    echo "🌤️  WEATHER"
    echo ""
    WEATHER=$(curl -s "wttr.in/Neston,UK?format=%l:+%c+%t+Humidity:%h+Wind:%w" 2>/dev/null)
    echo "${WEATHER:-Weather data unavailable}"
    echo ""
    echo "───────────────────"
    echo ""
    echo "💰  CRYPTO MARKET (24h Change)"
    echo ""
    
    # CoinGecko for major tokens
    def get_cg_price(sym):
        import subprocess
        try:
            result = subprocess.run([
                'curl', '-s', 
                f'https://api.coingecko.com/api/v3/simple/price?ids={sym}&vs_currencies=usd&include_24hr_change=true'
            ], capture_output=True, text=True, timeout=10
            ])
            data = json.loads(result.stdout)
            price = data.get(sym, {}).get('usd', 'N/A')
            change = data.get(sym, {}).get('usd_24h_change', 0.0)
            
            emoji = "📉" if change >= 0 else "📈"
            return f"${price:.2f} ({emoji}{change:+.2f}%%)"
        except Exception as e:
            return f"{sym}: N/A"
    
    # Major assets
    bitcoin_price = get_cg_price('bitcoin')
    eth_price = get_cg_price('ethereum')
    sol_price = get_cg_price('solana')
    
    if bitcoin_price != "bitcoin: N/A":
        echo "📊 Bitcoin: $bitcoin_price"
    if eth_price != "ethereum: N/A":
        echo "📊 Ethereum: $eth_price"
    if sol_price != "solana: N/A":
        echo "📊 Solana: $sol_price"
    
    echo ""
    echo "───────────────────"
    echo ""
    echo "🐦  TOP CRYPTO TWEETS (Last 12h)"
    echo ""
    
    # Try to fetch tweets from bird CLI
    try:
        # Run bird CLI to fetch following tweets
        result = subprocess.run([
            'bird', 'home', '--count', '100', '--json'
        ], capture_output=True, text=True, timeout=30)
        ])
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            tweets = data if isinstance(data, list) else []
            
            # Filter for crypto-related tweets (last 12 hours)
            twelve_hours_ago = datetime.utcnow() - timedelta(hours=12)
            crypto_tweets = []
            
            for tweet in tweets:
                text = tweet.get('text', '').lower()
                created_at = tweet.get('createdAt', '')
                author = tweet.get('author', {}).get('username', '')
                
                # Parse timestamp
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00'))
                except:
                    dt = None
                
                if dt and (dt > twelve_hours_ago or (dt.isoformat() == '')):
                    # Check if any crypto keyword
                    if any(keyword in text for keyword in CRYPTO_KEYWORDS):
                        crypto_tweets.append({
                            'created_at': created_at,
                            'username': author,
                            'text': text,
                            'id': tweet.get('id', '')
                        })
            
            # Get top 5 by likes
            crypto_tweets_sorted = sorted(crypto_tweets, key=lambda x: x.get('text', '').lower().count('bitcoin') + x.get('text', '').lower().count('ethereum') + x.get('text', '').lower().count('solana'), reverse=True)
            top_5 = crypto_tweets_sorted[:5]
            
            if crypto_tweets_sorted:
                top_5_count = len(top_5)
                print(f"📊 Found {top_5_count} crypto-related tweets")
                
                # Display top tweets
                for i, tweet in enumerate(top_5[:5], 1):
                    created_at = tweet.get('createdAt', '')
                    username = tweet.get('author', {}).get('username', '')
                    likes = tweet.get('likeCount', 0)
                    text = tweet.get('text', '')[:80] + '...' if len(tweet.get('text', '')) > 80 else tweet.get('text', '')
                    
                    # Format timestamp
                    try:
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00'))
                        time_str = dt.strftime('%H:%M') if dt else '??:??'
                    except:
                        time_str = created_at
                    
                    print(f"🐦 @{username} ({time_str})")
                    print(f"   💬 {likes}❤️")
                    print(f"   {text}")
                    print(f"   🔗 https://twitter.com/{username}/status/{tweet.get('id', '')}")
                    print()
            
                print("───────────────────")
            else:
                print("❌ Unable to fetch tweets from bird CLI")
        
    except Exception as e:
        print(f"❌ Error fetching tweets: {e}")
    
    echo "───────────────────"
    echo ""
    echo "Have a great day! 🚀✨"
} > "$MSGFILE"

MESSAGE=$(cat "$MSGFILE")

clawdbot message send --channel telegram --target "$TELEGRAM_USER_ID" --message "$MESSAGE" >> "$LOGFILE" 2>&1
rm -f "$MSGFILE"

echo "[$(date -u)] Morning briefing sent." >> "$LOGFILE"
