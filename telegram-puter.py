#!/usr/bin/env python3
"""
Telegram + Puter.js Image Generator
Generates images via Telegram using Puter.js
"""

import os
import sys
import time
import subprocess
import tempfile
import json

# Load config
config_path = os.path.join(os.path.dirname(__file__), '.zai-config')
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        for line in f:
            if line.startswith('ZAI_API_KEY='):
                # Not using Z.AI anymore, keeping for config structure
                pass

# HTML template with Puter.js integration
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://js.puter.com/v2/"></script>
</head>
<body>
    <script>
        const prompt = "{prompt}";
        const model = "{model}";

        puter.ai.txt2img(prompt, {{ model: model }})
            .then(imageElement => {{
                // Get base64 data
                const src = imageElement.src;
                console.log("IMAGE_READY:" + src);
                document.title = "DONE:" + src;
            }})
            .catch(err => {{
                console.log("ERROR:" + err.message);
                document.title = "ERROR:" + err.message;
            }});
    </script>
</body>
</html>
"""


def generate_with_browser(prompt, model="gemini-25-flash"):
    """
    Generate image using Puter.js via headless browser
    """
    # Create temp HTML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        html_content = HTML_TEMPLATE.format(
            prompt=prompt.replace('"', '\\"'),
            model=model
        )
        f.write(html_content)
        temp_file = f.name

    try:
        # Use Playwright (if available) or puppeteer-like approach
        # For simplicity, we'll use a curl-based approach if possible
        # Or provide instructions for manual use

        # Try direct API call (some Puter endpoints might work)
        import requests

        # Puter uses browser-based auth, so we'll provide the web interface method
        # Return temp file for manual use
        return temp_file

    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 telegram-puter.py <prompt> [--model <model>]")
        print("")
        print("Available models:")
        print("  gpt-image")
        print("  dalle-2")
        print("  dalle-3")
        print("  gemini-25-flash (Nano Banana)")
        print("  flux-1-schnell")
        print("  flux-1-pro")
        print("  stable-diffusion-3")
        print("  stable-diffusion-xl")
        sys.exit(1)

    prompt = sys.argv[1]
    model = "gemini-25-flash"

    for i, arg in enumerate(sys.argv):
        if arg == "--model" and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]

    print(f"🎨 Generating image...")
    print(f"📝 Prompt: {prompt}")
    print(f"🤖 Model: {model}")
    print("")

    # Generate
    temp_file = generate_with_browser(prompt, model)

    if temp_file:
        print(f"✅ HTML file created: {temp_file}")
        print("")
        print("💡 Open this file in your browser:")
        print(f"   file://{temp_file}")
        print("")
        print("🌐 Or use the web interface:")
        print("   /root/clawd/test-puter.sh")


if __name__ == '__main__':
    main()
