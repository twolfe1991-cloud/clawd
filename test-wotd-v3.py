#!/usr/bin/env python3
import subprocess
import json
import re
import sys

# Get the email
cmd = ["gog", "gmail", "get", "19c23bf3dfee1db2", "--json"]
env = {"GOG_ACCOUNT": "twolfe1991@gmail.com"}
env.update({k:v for k,v in __import__('os').environ.items() if k != 'GOG_ACCOUNT'})
result = subprocess.run(cmd, capture_output=True, text=True, env=env)

if result.returncode != 0:
    print(f"Error: {result.stderr}", file=sys.stderr)
    sys.exit(1)

email = json.loads(result.stdout)
body = email.get('body', '')

# Find pronunciation bracket first
pronunciation_match = re.search(r'^\s*\[([^\]]+)\]\s*$', body, re.MULTILINE)
pronunciation = pronunciation_match.group(1) if pronunciation_match else None

# Find the word - the line immediately before the pronunciation bracket
word = None
if pronunciation_match:
    # Get all lines and find the one before pronunciation
    lines = body.split('\n')
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
part_speech_match = re.search(r'(noun|verb|adjective|adverb)\s*:\s*([^\n]+)', body, re.IGNORECASE)
part_speech = part_speech_match.group(1) if part_speech_match else None
definition = part_speech_match.group(2).strip() if part_speech_match else None

# Extract explanation section
explanation_match = re.search(r'Explanation\s*\n\s*(.+?)(?:\n\n|\nExample:)', body, re.DOTALL | re.IGNORECASE)
explanation = explanation_match.group(1).strip() if explanation_match else None

# Extract example
example_match = re.search(r'Example:\s*(.+?)(?:\n\n|See Full Definition)', body, re.IGNORECASE)
example = example_match.group(1).strip() if example_match else None

# Format message
lines = [
    f"📚 **Word of the Day** (Today)",
    "",
    f"**{word}**",
]

if pronunciation:
    lines.append(f"_{pronunciation}_")

if part_speech and definition:
    lines.append("")
    lines.append(f"**{part_speech.title()}:** {definition}")

if explanation:
    lines.append("")
    lines.append(f"💡 {explanation}")

if example:
    lines.append("")
    lines.append(f"📝 *Example:* {example}")

message = "\n".join(lines)
print(message)
