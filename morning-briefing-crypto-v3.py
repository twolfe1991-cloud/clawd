#!/usr/bin/env python3
"""
Morning Briefing with Crypto Tweets - Direct Python execution
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta

# Keywords for crypto
CRYPTO_KEYWORDS = ['bitcoin', 'ethereum', 'solana', 'crypto', 'btc', 'eth', 'defi', 'web3', 'blockchain', 'nft', 'token']

TELEGRAM_USER_ID="5404518130"
LOGFILE="/var/log/morning-briefing.log"
TIMESTAMP=$(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
DATE_FRIENDLY=TIMESTAMP.strftime('%A, %B %d, %Y')

def main():
    msg = []
    
    # Header
    msg.append("**☀️ GOOD MORNING, TOM! ☀️**")
    msg.append(f"📍 Neston, UK • {DATE_FRIENDLY}")
    msg.append("")
    msg.append("───────────────────")
    msg.append("")
    msg.append("🌤️ WEATHER")
    msg.append("")
    
    # Weather
    try:
        weather = subprocess.check_output(['curl', '-s', 'wttr.in/Neston,UK?format=%l:+%c+%t+Humidity:%h+Wind:%w'], timeout=10)
        msg.append(f"{weather}")
    except Exception:
        msg.append("Weather data unavailable")
    
    msg.append("")
    msg.append("───────────────────")
    msg.append("")
    msg.append("💰 CRYPTO MARKET (24h Change)")
    msg.append("")
    
    # Major assets prices
    try:
        btc_result = subprocess.check_output(['curl', '-s', 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true'], timeout=10)
        eth_result = subprocess.check_output(['curl', '-s', 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_24hr_change=true'], timeout=10)
        sol_result = subprocess.check_output(['curl', '-s', 'https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_24hr_change=true'], timeout=10)
        
        btc_data = json.loads(btc_result.stdout)
        eth_data = json.loads(eth_result.stdout)
        sol_data = json.loads(sol_result.stdout)
        
        btc_price = btc_data.get('bitcoin', {}).get('usd', 'N/A')
        btc_change = btc_data.get('bitcoin', {}).get('usd_24h_change', 0.0)
        
        eth_price = eth_data.get('ethereum', {}).get('usd', 'N/A')
        eth_change = eth_data.get('ethereum', {}).get('usd_24h_change', 0.0)
        
        sol_price = sol_data.get('solana', {}).get('usd', 'N/A')
        sol_change = sol_data.get('solana', {}).get('usd_24h_change', 0.0)
        
        def format_price(price, change):
            if price and price != 'N/A':
                emoji = "📈" if float(change) > 0 else "📉"
                return f"${price:,.2f} ({change:+.2f}%) {emoji}"
            else:
                return "N/A"
        
        msg.append(f"📊 Bitcoin: {format_price(btc_price, btc_change)}")
        msg.append(f"📊 Ethereum: {format_price(eth_price, eth_change)}")
        msg.append(f"📊 Solana: {format_price(sol_price, sol_change)}")
    
    except Exception as e:
        msg.append(f"Error fetching crypto prices: {e}")
    
    msg.append("")
    msg.append("───────────────────")
    msg.append("")
    msg.append("🐦  TOP CRYPTO TWEETS (Last 12h)")
    msg.append("")
    
    # Crypto tweets from Twitter (using bird CLI)
    try:
        # Use bird CLI to fetch tweets
        bird_result = subprocess.run([
            'bird', 'home', '--count', '50', '--json'
        ], capture_output=True, text=True, timeout=30)
        
        if bird_result.returncode == 0:
            tweets_data = json.loads(bird_result.stdout)
            
            # Filter crypto-related tweets
            if isinstance(tweets_data, list):
                tweets_list = tweets_data
            elif isinstance(tweets_data, dict):
                tweets_list = [tweets_data]
            
            crypto_tweets = []
            twelve_hours_ago = datetime.now() - timedelta(hours=12)
            
            for tweet in tweets_list:
                text = tweet.get('text', '').lower()
                created_at = tweet.get('createdAt', '')
                
                # Parse timestamp
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00')) if created_at else None
                except:
                    dt = None
                
                if dt and dt > twelve_hours_ago:
                    # Check if any crypto keyword
                    if any(keyword in text for keyword in CRYPTO_KEYWORDS):
                        crypto_tweets.append({
                            'created_at': created_at,
                            'username': tweet.get('author', {}).get('username', ''),
                            'id': tweet.get('id', ''),
                            'text': text
                        })
            
            # Get top 5 by likes
            crypto_tweets_sorted = sorted(crypto_tweets, key=lambda x: x.get('text', '').lower().count('bitcoin') + x.get('text', '').lower().count('ethereum') + x.get('text', '').lower().count('solana'), reverse=True)
            top_5 = crypto_tweets_sorted[:5]
            
            if crypto_tweets_sorted:
                msg.append(f"📊 Found {len(top_5)} crypto-related tweets")
                
                # Display top 5
                for i, tweet in enumerate(top_5, 1):
                    created_at = tweet.get('createdAt', '')
                    username = tweet.get('author', {}).get('username', '')
                    likes = tweet.get('likeCount', 0)
                    text = tweet.get('text', '')[:60] + '...' if len(tweet.get('text', '')) > 60 else tweet.get('text', '')
                    
                    # Format timestamp
                    try:
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00')) if created_at else None
                        time_str = dt.strftime('%H:%M') if dt else '??:??'
                    except:
                        time_str = created_at
                    
                    msg.append(f"🐦 @{username} ({time_str})")
                    msg.append(f"   💬 {likes}❤️")
                    msg.append(f"   {text}")
                    msg.append(f"   🔗 https://twitter.com/{username}/status/{tweet.get('id', '')}")
                    msg.append("")
        
        else:
            msg.append("❌ Unable to fetch crypto tweets")
    
    msg.append("")
    msg.append("───────────────────")
    msg.append("")
    msg.append("Have a great day! 🚀✨")
    
    # Send via Telegram
    message = "\n".join(msg)
    
    subprocess.run([
        'clawdbot', 'message', 'send',
        '--channel', 'telegram',
        '--target', TELEGRAM_USER_ID,
        '--message', message
    ])
    
    # Log
    with open(LOGFILE, 'a') as f:
        f.write(f"[{TIMESTAMP}] Morning briefing sent\n")

if __name__ == '__main__':
    main()
