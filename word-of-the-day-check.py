#!/usr/bin/env python3
"""
Dictionary.com Word of the Day Checker
Checks Gmail for Dictionary.com Word of the Day emails and sends formatted summary to Telegram
"""

import subprocess
import json
import re
import os
from datetime import datetime, timedelta

# Configuration
TELEGRAM_USER_ID = "5404518130"
GMAIL_ACCOUNT = "twolfe1991@gmail.com"
STATE_FILE = "/root/clawd/.word_of_the_day_state.json"

def run_gog_search(query, max_results=1):
    """Run gog gmail search and return JSON results"""
    cmd = [
        "gog", "gmail", "search", query, "--max", str(max_results), "--json"
    ]
    env = os.environ.copy()
    env["GOG_ACCOUNT"] = GMAIL_ACCOUNT
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)

def run_gog_get(message_id):
    """Run gog gmail get and return email content"""
    cmd = ["gog", "gmail", "get", message_id, "--json"]
    env = os.environ.copy()
    env["GOG_ACCOUNT"] = GMAIL_ACCOUNT
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)

def extract_word_info(email_body):
    """Extract word, pronunciation, definition, explanation, and example from email"""
    # Find pronunciation bracket first (must be on its own line)
    pronunciation_match = re.search(r'^\s*\[([^\]]+)\]\s*$', email_body, re.MULTILINE)
    pronunciation = pronunciation_match.group(1) if pronunciation_match else None

    # Find the word - line immediately before the pronunciation bracket
    word = None
    if pronunciation_match:
        # Get all lines and find the one before pronunciation
        lines = email_body.split('\n')
        for i in range(len(lines) - 1):
            line = lines[i]
            next_line = lines[i + 1]
            # Check if next line is the pronunciation bracket
            if next_line.strip() == f'[{pronunciation}]':
                # Extract word from current line
                word_match = re.match(r'^([a-z]+)', line.strip(), re.IGNORECASE)
                if word_match:
                    word = word_match.group(1)
                    break

    # Extract part of speech and definition
    part_speech_match = re.search(r'(noun|verb|adjective|adverb)\s*:\s*([^\n]+)', email_body, re.IGNORECASE)
    part_speech = part_speech_match.group(1) if part_speech_match else None
    definition = part_speech_match.group(2).strip() if part_speech_match else None

    # Extract explanation section
    explanation_match = re.search(r'Explanation\s*\n\s*(.+?)(?:\n\n|\nExample:)', email_body, re.DOTALL | re.IGNORECASE)
    explanation = explanation_match.group(1).strip() if explanation_match else None

    # Extract example
    example_match = re.search(r'Example:\s*(.+?)(?:\n\n|See Full Definition)', email_body, re.IGNORECASE)
    example = example_match.group(1).strip() if example_match else None

    return {
        "word": word,
        "pronunciation": pronunciation,
        "part_speech": part_speech,
        "definition": definition,
        "explanation": explanation,
        "example": example
    }

def format_telegram_message(word_info, email_date):
    """Format the word information for Telegram"""
    lines = [
        f"📚 **Word of the Day** ({email_date})",
        "",
        f"**{word_info['word']}**",
    ]

    if word_info['pronunciation']:
        lines.append(f"_{word_info['pronunciation']}_")

    if word_info['part_speech'] and word_info['definition']:
        lines.append("")
        lines.append(f"**{word_info['part_speech'].title()}:** {word_info['definition']}")

    if word_info['explanation']:
        lines.append("")
        lines.append(f"💡 {word_info['explanation']}")

    if word_info['example']:
        lines.append("")
        lines.append(f"📝 *Example:* {word_info['example']}")

    return "\n".join(lines)

def send_telegram_message(message):
    """Send message to Telegram"""
    cmd = [
        "clawdbot", "message", "send",
        "--channel", "telegram",
        "--to", TELEGRAM_USER_ID,
        "--message", message
    ]
    subprocess.run(cmd, check=True)

def load_state():
    """Load last processed state"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_processed_ids": []}

def save_state(state):
    """Save processed state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def check_new_emails():
    """Check for new Dictionary.com Word of the Day emails"""
    # Search for recent Dictionary.com emails
    query = 'from:dictionary.com "Word of the Day"'
    results = run_gog_search(query, max_results=5)

    if not results or not results.get('threads'):
        return []

    state = load_state()
    processed_ids = set(state.get('last_processed_ids', []))
    new_words = []

    for thread in results['threads']:
        message_id = thread['id']

        if message_id in processed_ids:
            continue

        # Get email content
        email = run_gog_get(message_id)
        if not email:
            continue

        # Extract word information
        word_info = extract_word_info(email.get('body', ''))

        if word_info['word']:
            # Format date from email headers
            email_date = email.get('headers', {}).get('date', 'Unknown date')

            # Format message
            message = format_telegram_message(word_info, email_date)

            new_words.append({
                "message_id": message_id,
                "word_info": word_info,
                "message": message
            })

    return new_words

def main():
    """Main function"""
    new_words = check_new_words()

    if not new_words:
        print("No new Word of the Day emails found")
        return

    state = load_state()
    processed_ids = set(state.get('last_processed_ids', []))

    for item in new_words:
        # Send to Telegram
        send_telegram_message(item['message'])
        print(f"Sent Word of the Day: {item['word_info']['word']}")

        # Mark as processed
        processed_ids.add(item['message_id'])

    # Update state (keep only last 100)
    state['last_processed_ids'] = list(processed_ids)[-100:]
    state['last_check'] = datetime.now().isoformat()
    save_state(state)

if __name__ == "__main__":
    main()
