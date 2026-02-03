#!/usr/bin/env python3
"""
Morning Briefing Script
Features:
- Detailed weather report
- Today's calendar events (personal + family)
- Major crypto prices and 24h changes
- Other token prices (base tokens, etc.)
- Latest Twitter updates
"""

import subprocess
import json
from datetime import datetime, timedelta, date, timezone
import os

TELEGRAM_USER_ID = "5404518130"
LOGFILE = "/var/log/morning-briefing.log"

def get_detailed_weather(location="Neston,UK"):
    """Get detailed weather information from wttr.in"""
    try:
        # Get current conditions
        result = subprocess.run([
            'curl', '-s', f'wttr.in/{location}?format=%c+%t+%C'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode != 0 or not result.stdout:
            return "Weather data unavailable"

        current_data = result.stdout.strip()
        parts = current_data.split()
        icon = parts[0] if len(parts) > 0 else "🌤️"
        temp = parts[1] if len(parts) > 1 else "N/A"
        condition = ' '.join(parts[2:]) if len(parts) > 2 else "Unknown"

        # Get wind, humidity, pressure
        extra_result = subprocess.run([
            'curl', '-s', f'wttr.in/{location}?format=%w+%h+%P'
        ], capture_output=True, text=True, timeout=10)

        extra_data = ""
        if extra_result.returncode == 0 and extra_result.stdout:
            extra_data = extra_result.stdout.strip()

        # Get forecast
        forecast_result = subprocess.run([
            'curl', '-s', f'wttr.in/{location}?format=j1'
        ], capture_output=True, text=True, timeout=10)

        max_temp = min_temp = sunrise = sunset = "N/A"
        if forecast_result.returncode == 0 and forecast_result.stdout:
            try:
                data = json.loads(forecast_result.stdout)
                today = data.get('weather', [{}])[0]
                max_temp = today.get('maxtempC', 'N/A')
                min_temp = today.get('mintempC', 'N/A')
                sunrise = today.get('astronomy', [{}])[0].get('sunrise', 'N/A')
                sunset = today.get('astronomy', [{}])[0].get('sunset', 'N/A')
            except:
                pass

        # Build weather report
        weather_lines = [
            f"🌤️  CURRENT WEATHER",
            f"",
            f"  {icon}  {temp}  {condition}",
            f"  {extra_data}" if extra_data else "",
            f"  📊  High: {max_temp}°C  Low: {min_temp}°C",
            f"  🌅  {sunrise}  🌇  {sunset}"
        ]

        # Remove empty lines
        weather_lines = [line for line in weather_lines if line]

        return "\n".join(weather_lines)

    except Exception as e:
        return f"🌤️  WEATHER DATA UNAVAILABLE\n\n{str(e)}"

def get_calendar_events():
    """Get today's calendar events from Gog"""
    events_text = []

    try:
        # Try to get today's events
        today_start = date.today().strftime('%Y-%m-%dT00:00:00')
        today_end = date.today().strftime('%Y-%m-%dT23:59:59')

        # Get personal calendar events
        result = subprocess.run([
            'gog', 'calendar', 'events', 'primary',
            '--from', today_start,
            '--to', today_end
        ], capture_output=True, text=True, timeout=15)

        if result.returncode == 0 and result.stdout:
            events_text.append("📅 Today's Schedule (Personal):")
            events_text.append(result.stdout.strip())
        else:
            events_text.append("📅 Today's Schedule (Personal): No events")
    except Exception as e:
        events_text.append(f"📅 Today's Schedule (Personal): Unable to fetch - {str(e)}")

    try:
        # Try family calendar if configured
        result = subprocess.run([
            'gog', 'calendar', 'events', 'family',
            '--from', today_start,
            '--to', today_end
        ], capture_output=True, text=True, timeout=15)

        if result.returncode == 0 and result.stdout:
            events_text.append("")
            events_text.append("📅 Today's Schedule (Family):")
            events_text.append(result.stdout.strip())
    except Exception as e:
        # Family calendar might not exist, that's okay
        pass

    return "\n".join(events_text) if events_text else "📅 No calendar data available"

def get_crypto_price_coingecko(coin_id):
    """Get crypto price from CoinGecko API"""
    try:
        result = subprocess.run([
            'curl', '-s',
            f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode != 0 or not result.stdout.strip():
            return None

        data = json.loads(result.stdout)
        if coin_id not in data:
            return None

        price = data[coin_id].get('usd')
        change = data[coin_id].get('usd_24hr_change')

        if price is None:
            return None

        # Handle missing change data
        if change is None:
            return f"${price:,.2f}"

        emoji = "📈" if change >= 0 else "📉"
        return f"${price:,.2f} ({emoji}{change:+.2f}%)"
    except Exception as e:
        return None

def get_crypto_price_dexscreener(contract_address):
    """Get crypto price from DexScreener (for Base and Ethereum tokens)"""
    try:
        result = subprocess.run([
            'curl', '-s',
            f'https://api.dexscreener.com/latest/dex/tokens/{contract_address}'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode != 0 or not result.stdout.strip():
            return None

        data = json.loads(result.stdout)
        pairs = data.get('pairs', [])

        if not pairs:
            return None

        # Get first pair with liquidity
        pair = next((p for p in pairs if p.get('liquidity', {}).get('usd', 0) > 0), pairs[0])

        price = float(pair.get('priceUsd', 0))
        price_change = pair.get('priceChange', {}).get('h24', 0)

        if price <= 0:
            return None

        emoji = "📈" if price_change >= 0 else "📉"
        price_format = f"${price:,.8f}" if price < 0.001 else f"${price:,.4f}"
        return f"{price_format} ({emoji}{price_change:+.2f}%)"
    except Exception as e:
        return None

def get_crypto_price_contract(network, contract_address):
    """Get crypto price from contract address - try DexScreener first"""
    # Try DexScreener first for both Base and Ethereum
    price_info = get_crypto_price_dexscreener(contract_address)
    if price_info:
        return price_info

    # Fallback to CoinGecko
    try:
        result = subprocess.run([
            'curl', '-s',
            f'https://api.coingecko.com/api/v3/simple/token_price/{network}?contract_addresses={contract_address}&vs_currencies=usd&include_24hr_change=true'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode != 0 or not result.stdout.strip():
            return None

        data = json.loads(result.stdout)
        if contract_address.lower() not in data:
            return None

        token_data = data[contract_address.lower()]
        price = token_data.get('usd')
        change = token_data.get('usd_24hr_change')

        if price is None:
            return None

        # Handle missing change data
        if change is None:
            return f"${price:,.4f}"

        emoji = "📈" if change >= 0 else "📉"
        return f"${price:,.4f} ({emoji}{change:+.2f}%)"
    except Exception as e:
        return None

def get_major_crypto_prices_dexscreener(search_term):
    """Get major crypto price from DexScreener search"""
    try:
        result = subprocess.run([
            'curl', '-s',
            f'https://api.dexscreener.com/latest/dex/search?q={search_term}&limit=1'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode != 0 or not result.stdout.strip():
            return None

        data = json.loads(result.stdout)
        pairs = data.get('pairs', [])

        if not pairs:
            return None

        # Get first pair with high volume and liquidity
        pair = pairs[0]

        price = float(pair.get('priceUsd', 0))
        price_change = pair.get('priceChange', {}).get('h24', 0)

        if price <= 0:
            return None

        emoji = "📈" if price_change >= 0 else "📉"
        return f"${price:,.2f} ({emoji}{price_change:+.2f}%)"
    except Exception as e:
        return None

def get_major_crypto_prices():
    """Get major crypto prices using DexScreener, with CoinGecko fallback"""
    tokens = [
        ('bitcoin', 'BTC'),
        ('ethereum', 'ETH'),
        ('solana', 'SOL'),
        ('ripple', 'XRP'),
        ('dogecoin', 'DOGE'),
        ('sui', 'SUI'),
        ('hype', 'HYPE'),
        ('pax-gold', 'PAXG')
    ]

    lines = ["💰 MAJOR CRYPTO PRICES (24h Change)"]

    for search_term, symbol in tokens:
        # Try DexScreener first
        price_info = get_major_crypto_prices_dexscreener(search_term)
        
        # Fallback to CoinGecko for tokens not found on DexScreener
        if not price_info:
            # Map search term to CoinGecko ID for specific tokens
            coin_id = search_term  # Most are the same
            price_info = get_crypto_price_coingecko(coin_id)
        
        if price_info:
            lines.append(f"📊 {symbol}: {price_info}")
        else:
            lines.append(f"📊 {symbol}: N/A")

    return "\n".join(lines)

def get_other_token_prices():
    """Get other token prices (Base tokens, etc.)"""
    # Contract addresses for the tokens
    tokens = [
        ('MOG', 'ethereum', '0xaaee1a9723aadb7afa2810263653a34ba2c21c7a'),
        ('REI', 'base', '0x6b2504a03ca4d43d0d73776f6ad46dab2f2a4cfd'),
        ('VIRTUAL', 'base', '0x0b3e328455c4059eeb9e3f84b5543f74e24e7e1b'),
        ('KEYCAT', 'base', '0x9a26f5433671751c3276a065f57e5a02d2817973'),
        ('KTA', 'base', '0xc0634090f2fe6c6d75e61be2b949464abb498973'),
        ('TIBBIR', 'base', '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00')
    ]

    lines = ["💎 OTHER TOKEN PRICES (24h Change)"]

    for symbol, network, contract in tokens:
        price_info = get_crypto_price_contract(network, contract)
        if price_info:
            lines.append(f"📊 {symbol}: {price_info}")
        else:
            lines.append(f"📊 {symbol}: N/A")

    return "\n".join(lines)

def get_twitter_updates():
    """Get latest Twitter updates"""
    try:
        result = subprocess.run([
            'bird', 'home', '--count', '20', '--json'
        ], capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return ["🐦 Unable to fetch Twitter updates"]

        data = json.loads(result.stdout)

        # Handle different response formats
        if isinstance(data, dict):
            tweets = data.get('data', [])
        elif isinstance(data, list):
            tweets = data
        else:
            return ["🐦 No Twitter data available"]

        if not tweets:
            return ["🐦 No recent tweets"]

        lines = ["🐦 LATEST TWITTER UPDATES (Last 24h)"]

        current_time = datetime.now(timezone.utc)
        recent_tweets = []

        for tweet in tweets[:10]:  # Get last 10 tweets
            if not isinstance(tweet, dict):
                continue

            created_at = tweet.get('createdAt', '')
            tweet_id = tweet.get('id', '')
            username = tweet.get('author', {}).get('username', 'Unknown')
            text = tweet.get('text', '')
            likes = tweet.get('likeCount', 0)

            # Parse timestamp
            try:
                # Twitter format: "Tue Feb 03 14:46:22 +0000 2026"
                dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                # Ensure timezone is set
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                
                hours_ago = (current_time - dt).total_seconds() / 3600

                # Only include tweets from last 24 hours
                if hours_ago > 24:
                    continue

                time_str = f"{int(hours_ago)}h ago" if hours_ago >= 1 else f"{int(hours_ago * 60)}m ago"
            except:
                time_str = "? ago"

            # Truncate long tweets
            display_text = text[:150] + '...' if len(text) > 150 else text

            # Create tweet URL
            tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"

            lines.append(f"@{username} • {time_str}")
            lines.append(f"   {display_text}")
            lines.append(f"   🔗 {tweet_url}")
            lines.append("")

        if len(lines) == 1:  # Only header
            lines.append("No recent tweets (last 24h)")

        return lines

    except Exception as e:
        return [f"🐦 Error fetching Twitter: {str(e)}"]

def main():
    """Main function to build and send morning briefing"""
    # Build message sections
    sections = [
        f"**☀️ GOOD MORNING, TOM! ☀️**",
        "",
        "──────────────────",
        f"📍 Neston, UK",
        f"📅 {datetime.now().strftime('%A, %B %d, %Y')}",
        f"⏰ {datetime.now().strftime('%H:%M UTC')}",
        "",
        "──────────────────",
        "",
    ]

    # Weather
    sections.append(get_detailed_weather())
    sections.append("")
    sections.append("")

    # Calendar
    sections.append("──────────────────")
    sections.append("")
    sections.append(get_calendar_events())
    sections.append("")

    # Major Crypto
    sections.append("──────────────────")
    sections.append("")
    sections.append(get_major_crypto_prices())
    sections.append("")

    # Other Tokens
    sections.append("──────────────────")
    sections.append("")
    sections.append(get_other_token_prices())
    sections.append("")

    # Twitter
    sections.append("──────────────────")
    sections.append("")
    sections.extend(get_twitter_updates())
    sections.append("")

    # Footer
    sections.extend([
        "──────────────────",
        "",
        "Have a great day! 🚀✨"
    ])

    message = "\n".join(sections)

    # Send message
    result = subprocess.run([
        'clawdbot', 'message', 'send',
        '--channel', 'telegram',
        '--target', TELEGRAM_USER_ID,
        '--message', message
    ], capture_output=True, text=True)

    # Log
    with open(LOGFILE, 'a') as f:
        log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        f.write(f"[{log_time}] Morning briefing sent\n")
        if result.returncode != 0:
            f.write(f"[{log_time}] Error: {result.stderr}\n")

    print(f"Morning briefing sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

if __name__ == "__main__":
    main()
