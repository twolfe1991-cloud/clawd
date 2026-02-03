#!/usr/bin/env python3
"""
Puter.js Image Generator - CLI Wrapper
Uses Puter.js for free AI image generation without API keys
"""

import os
import sys
import argparse
import requests
import json
import time
import base64

# Puter.js API endpoint
PUTER_API_URL = "https://api.puter.com/v2/ai/txt2img"


def generate_image(prompt, model="gpt-image", save_path=None):
    """
    Generate image using Puter.js

    Available models:
    - gpt-image
    - dalle-2
    - dalle-3
    - gemini-25-flash (Nano Banana)
    - flux-1-schnell
    - flux-1-kontext
    - flux-1-pro
    - stable-diffusion-3
    - stable-diffusion-xl
    """
    print(f"🎨 Generating image with model: {model}")
    print(f"📝 Prompt: {prompt}")
    print("")

    # Prepare payload
    payload = {
        "prompt": prompt,
        "model": model
    }

    try:
        # Make request
        response = requests.post(
            PUTER_API_URL,
            json=payload,
            headers={
                "Content-Type": "application/json"
            },
            timeout=60
        )

        if response.status_code != 200:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None

        result = response.json()

        # Check for image data
        if 'image' in result:
            image_data = result['image']

            # Handle different response formats
            if image_data.startswith('data:image'):
                # Base64 encoded image
                header, encoded = image_data.split(',', 1)
                image_bytes = base64.b64decode(encoded)
                file_ext = 'png'
            elif image_data.startswith('http'):
                # URL
                print(f"🔗 Image URL: {image_data}")

                # Download
                img_response = requests.get(image_data)
                if img_response.status_code == 200:
                    image_bytes = img_response.content
                    file_ext = 'png'  # Default
                else:
                    print(f"❌ Failed to download image from URL")
                    return None
            else:
                print("❌ Unknown response format")
                return None

            # Save to file if path provided
            if save_path and image_bytes:
                # Ensure directory exists
                os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(image_bytes)
                print(f"✅ Saved to: {save_path}")

            return image_data

        else:
            print("❌ No image in response")
            print(f"Response: {json.dumps(result, indent=2)}")
            return None

    except requests.exceptions.Timeout:
        print("❌ Request timed out. Try again.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Generate images using Puter.js (free, no API key required)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available models:
  gpt-image              GPT Image model
  dalle-2                DALL-E 2
  dalle-3                DALL-E 3
  gemini-25-flash         Gemini 2.5 Flash (Nano Banana)
  flux-1-schnell          Flux.1 Schnell (fast)
  flux-1-kontext          Flux.1 Kontext
  flux-1-pro              Flux 1.1 Pro (high quality)
  stable-diffusion-3       Stable Diffusion 3
  stable-diffusion-xl       Stable Diffusion XL

Examples:
  python3 puter-image.py "A cat in space"
  python3 puter-image.py "Sunset over mountains" --model flux-1-schnell
  python3 puter-image.py "A cyberpunk city" --model gemini-25-flash -o output.png
        """
    )

    parser.add_argument('prompt', help='Text prompt for image generation')
    parser.add_argument('--model', '-m', default='gpt-image',
                      help='Model to use (default: gpt-image)')
    parser.add_argument('--output', '-o', help='Output file path (e.g., output.png)')

    args = parser.parse_args()

    # Validate model
    valid_models = [
        'gpt-image', 'dalle-2', 'dalle-3', 'gemini-25-flash',
        'flux-1-schnell', 'flux-1-kontext', 'flux-1-pro',
        'stable-diffusion-3', 'stable-diffusion-xl'
    ]

    if args.model not in valid_models:
        print(f"❌ Invalid model: {args.model}")
        print(f"Valid models: {', '.join(valid_models)}")
        sys.exit(1)

    # Generate image
    result = generate_image(args.prompt, args.model, args.output)

    if not args.output:
        print("")
        print("💡 Tip: Use --output to save image to file")


if __name__ == '__main__':
    main()
