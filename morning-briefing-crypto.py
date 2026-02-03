#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

TELEGRAM_USER_ID = "5404518130"
LOGFILE = "/var/log/morning-briefing.log"

def get_crypto_price(symbol):
    try:
        result = subprocess.run(['curl', '-s', f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_change=true'], capture_output=True, text=True, timeout=10)
        data = json.loads(result.stdout)
        price = data.get(symbol, {}).get('usd', 'N/A')
        change = data.get(symbol, {}).get('usd_24h_change', 0.0)
        emoji = "📈" if change >= 0 else "📉"
        if price and price != "N/A":
            return f"${price:,.2f} ({emoji}{change:+.2f}%)"
        else:
            return f"{symbol}: N/A"
    except Exception as e:
        return f"{symbol}: N/A"

def get_crypto_tweets():
    try:
        result = subprocess.run(['bird', 'home', '--count', '50', '--json'], capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return []
        
        data = json.loads(result.stdout)
        if not isinstance(data, dict) or 'data' not in data:
            return []
            
        if isinstance(data, dict):
            tweets = data.get('data', [])
        elif isinstance(data, list):
            tweets = data
        
        crypto_keywords = ['bitcoin', 'ethereum', 'solana', 'crypto', 'btc', 'eth', 'defi', 'web3', 'blockchain', 'nft', 'token']
        crypto_tweets = []
        
        for tweet in tweets:
            if not isinstance(tweet, dict):
                continue
            
            text = tweet.get('text', '').lower()
            created_at = tweet.get('createdAt', '')
            
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00')) if created_at else None
            except:
                dt = None
            
            if dt and (datetime.utcnow() - dt).total_seconds() / 3600 < 12:
                if any(kw in text for kw in crypto_keywords):
                    crypto_tweets.append({
                        'created_at': created_at,
                        'username': tweet.get('author', {}).get('username', ''),
                        'text': text,
                        'id': tweet.get('id', '')
                    })
        
        top_5 = sorted(crypto_tweets, key=lambda x: x.get('text', '').lower().count('bitcoin') + x.get('text', '').lower().count('ethereum') + x.get('text', '').lower().count('solana'), reverse=True)[:5]
        
        return top_5

def main():
    msg = [
        "**☀️ GOOD MORNING, TOM! ☀️**",
        f"📍 Neston, UK • {datetime.now().strftime('%A, %B %d, %Y')} • {datetime.now().strftime('%H:%M UTC')}",
        "",
        "───────────────────",
        "",
        "🌤️  WEATHER"
    ]
    
    try:
        weather = subprocess.check_output(['curl', '-s', 'wttr.in/Neston,UK?format=%l:+%c+%t+Humidity:%h+Wind:%w'], timeout=10)
        weather = weather.stdout.strip()
        msg.append(weather if weather else "Weather data unavailable")
    except Exception:
        msg.append("Weather data unavailable")
    
    msg.append("")
    msg.append("───────────────────")
    msg.append("")
    msg.append("💰  CRYPTO MARKET (24h Change)")
    
    try:
        btc_price = get_crypto_price('bitcoin')
        eth_price = get_crypto_price('ethereum')
        sol_price = get_crypto_price('solana')
        
        if btc_price != "Bitcoin: N/A":
            msg.append(f"📊 {btc_price}")
        if eth_price != "Ethereum: N/A":
            msg.append(f"📊 {eth_price}")
        if sol_price != "Solana: N/A":
            msg.append(f"📊 {sol_price}")
    
    except Exception as e:
        msg.append("Error fetching crypto prices")
    
    msg.append("")
    msg.append("───────────────────")
    msg.append("")
    msg.append("🐦  TOP CRYPTO TWEETS (Last 12h)")
    
    crypto_tweets = get_crypto_tweets()
    
    if crypto_tweets:
        msg.append(f"📊 Found {len(crypto_tweets)} crypto-related tweets")
        
        for i, tweet in enumerate(crypto_tweets[:5]):
            created_at = tweet.get('created_at', '')
            username = tweet.get('author', {}).get('username', '')
            likes = tweet.get('likeCount', 0)
            text = tweet.get('text', '')[:80] + '...' if len(tweet.get('text', '')) > 80 else tweet.get('text', '')
            
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
        msg.append("No recent crypto tweets found")
    
    msg.append("───────────────────")
    msg.append("Have a great day! 🚀✨")
    
    message = "\n".join(msg)
    
    subprocess.run([
        'clawdbot', 'message', 'send',
        '--channel', 'telegram',
        '--target', TELEGRAM_USER_ID,
        '--message', message
    ])
    
    with open(LOGFILE, 'a') as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}] Morning briefing sent\n")
