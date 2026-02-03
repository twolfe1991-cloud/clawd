#!/usr/bin/env python3
"""
Telegram + Puter.js Image Generator (Headless Browser)
Generates images via Telegram using Puter.js through Playwright
"""

import os
import sys
import asyncio
import base64
from playwright.async_api import async_playwright

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
                // Get base64 data from image
                const src = imageElement.src;

                // Send to Python via console log
                console.log("IMAGE_GENERATED:" + src);

                // Also set as page title for easy detection
                document.title = "SUCCESS:" + src;
            }})
            .catch(err => {{
                console.log("ERROR:" + err.message);
                document.title = "ERROR:" + err.message;
            }});
    </script>
</body>
</html>
"""


async def generate_image(prompt, model="gemini-25-flash", timeout=60000):
    """
    Generate image using Puter.js via headless browser
    Returns the base64 image data
    """
    print(f"🎨 Generating image with model: {model}")
    print(f"📝 Prompt: {prompt}")
    print("")

    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Listen for console messages
        image_data = None
        error_msg = None

        def handle_console(msg):
            nonlocal image_data, error_msg
            if msg.type == 'log':
                text = msg.text
                if text.startswith('IMAGE_GENERATED:'):
                    image_data = text.split(':', 1)[1].strip()
                    print("✅ Image generated via browser!")
                elif text.startswith('ERROR:'):
                    error_msg = text.split(':', 1)[1].strip()
                    print(f"❌ Browser error: {error_msg}")

        page.on('console', handle_console)

        # Create temp HTML content
        html_content = HTML_TEMPLATE.format(
            prompt=prompt.replace('"', '\\"'),
            model=model
        )

        # Set content and wait for result
        await page.set_content(html_content)

        try:
            # Wait for title change (our success signal)
            await page.wait_for_function(
                lambda: document.title.startswith('SUCCESS:') or document.title.startswith('ERROR:'),
                timeout=timeout
            )

            title = await page.title()

            if title.startswith('SUCCESS:'):
                image_data = title.split(':', 1)[1].strip()
                print(f"🖼️ Image data received ({len(image_data)} chars)")
                return image_data
            else:
                error_msg = title.split(':', 1)[1].strip()
                print(f"❌ Generation failed: {error_msg}")
                return None

        except Exception as e:
            print(f"❌ Timeout or error: {e}")
            return None
        finally:
            await browser.close()

    return None


def save_image(base64_data, output_path):
    """Save base64 image to file"""
    try:
        # Parse data URL format: data:image/png;base64,xxx
        if base64_data.startswith('data:image'):
            header, encoded = base64_data.split(',', 1)
            image_bytes = base64.b64decode(encoded)

            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

            with open(output_path, 'wb') as f:
                f.write(image_bytes)
            print(f"💾 Saved to: {output_path}")
            return True
    except Exception as e:
        print(f"❌ Failed to save: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 telegram-puter-headless.py <prompt> [--model <model>] [--output <file>]")
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
        print("")
        print("Example:")
        print("  python3 telegram-puter-headless.py 'A cat in space' --model gemini-25-flash")
        sys.exit(1)

    prompt = sys.argv[1]
    model = "gemini-25-flash"
    output = f"/tmp/puter_image_{int(time.time())}.png"

    for i, arg in enumerate(sys.argv):
        if arg == "--model" and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
        elif arg == "--output" and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]

    # Generate
    image_data = asyncio.run(generate_image(prompt, model))

    if image_data:
        if save_image(image_data, output):
            print("")
            print("✅ Done! Ready to send via Telegram")
        else:
            print("")
            print("❌ Failed to save image")
    else:
        print("")
        print("❌ Failed to generate image")


if __name__ == '__main__':
    main()
