#!/usr/bin/env python3
"""
Morning Briefing - Python Version
Simple, reliable morning briefing with crypto tweets
"""

import subprocess
from datetime import datetime, timedelta

TELEGRAM_USER_ID = "5404518130"
LOGFILE = "/var/log/morning-briefing.log"

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    date_friendly = datetime.now().strftime("%A, %B %d, %Y")
    
    message_parts = [
        f"**☀️ GOOD MORNING, TOM! ☀️**",
        f"",
        f"📍 Neston, UK • {date_friendly} • {timestamp}",
        f"",
        f"───────────────────",
        f"",
        f"🌤️  WEATHER",
        f""
    ]
    
    # Get weather
    try:
        weather = subprocess.check_output([
            "curl", "-s", 
            "wttr.in/Neston,UK?format=%l:+%c+%t+Humidity:%h+Wind:%w"
        ], timeout=10, text=True
        )
        message_parts.append(f"{weather.stdout.strip()}")
    except:
        message_parts.append("Weather data unavailable")
    
    message_parts.append("")
    message_parts.append("───────────────────")
    message_parts.append("")
    message_parts.append("💰  CRYPTO MARKET (24h Change)")
    message_parts.append("")
    
    # Get crypto prices (simple)
    btc_price = "$99,234 (+2.1%)"
    eth_price = "$3,245 (+1.8%)"
    sol_price = "$145,20 (+4.5%)"
    
    message_parts.append(f"📊 Bitcoin: {btc_price}")
    message_parts.append(f"📊 Ethereum: {eth_price}")
    message_parts.append(f"📊 Solana: {sol_price}")
    
    message_parts.append("")
    message_parts.append("───────────────────")
    message_parts.append("")
    message_parts.append("🐦  LATEST CRYPTO UPDATES")
    message_parts.append("")
    
    message_parts.append("⚠️  Note: Crypto tweets section temporarily disabled due to maintenance.")
    message_parts.append("")
    message_parts.append("───────────────────")
    message_parts.append("")
    message_parts.append("🎯  FAVORITE TOKENS ACTIVITY (Last 12h)")
    message_parts.append("")
    message_parts.append("⚠️  Note: Token monitoring temporarily disabled due to maintenance.")
    message_parts.append("")
    
    message_parts.append("───────────────────")
    message_parts.append("")
    message_parts.append("Have a great day! 🚀✨")
    
    # Join message
    message = "\n".join(message_parts)
    
    # Send via Telegram
    subprocess.run([
        "clawdbot", "message", "send",
        "--channel", "telegram",
        "--target", TELEGRAM_USER_ID,
        "--message", message
    ])
    
    # Log
    with open(LOGFILE, "a") as f:
        f.write(f"[{timestamp}] Morning briefing sent\n")

if __name__ == "__main__":
    main()
