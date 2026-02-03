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
pronunciation_match = re.search(r'\[([^\]]+)\]', body)
pronunciation = pronunciation_match.group(1) if pronunciation_match else None

# Find the word - look for pattern: word [url] on one line, then [pronunciation] on next line
word = None
if pronunciation_match:
    # Get text area around pronunciation
    start = max(0, pronunciation_match.start() - 500)
    end = min(len(body), pronunciation_match.end() + 100)
    context = body[start:end]

    # Pattern: word followed by URL on one line, then [pronunciation] on next
    lines = context.split('\n')
    for i in range(len(lines) - 1):
        # Check if next line has the pronunciation bracket
        if '[' in lines[i+1] and ']' in lines[i+1]:
            # Extract word from current line
            word_match = re.match(r'^([a-z]+)', lines[i].strip(), re.IGNORECASE)
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
