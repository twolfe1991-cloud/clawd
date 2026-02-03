#!/usr/bin/env python3
"""
x402 Layer API Wrapper
Simple direct API calls to x402-layer endpoints
"""

import os
import sys
import json
import hashlib
import argparse
import requests

# x402 Layer endpoints
X402_BASE = "https://api.x402layer.cc/skill/v1"

# Simple in-memory auth (for demo - in production, use proper auth)
AUTH_HEADER = {}


def get_headers(api_key=None):
    """Get headers with optional API key"""
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['x-api-key'] = api_key
    elif 'X402_API_KEY' in os.environ:
        headers['x-api-key'] = os.environ['X402_API_KEY']
    return headers


def generate_image(prompt, model="default", save_path=None):
    """Generate image using x402 Layer"""
    print(f"🎨 Generating image with x402 Layer...")
    print(f"📝 Prompt: {prompt}")
    print(f"🤖 Model: {model}")
    print("")

    try:
        # Create generation request
        payload = {
            "model": model if model != "default" else None,
            "input": {"prompt": prompt},
            "return_binary": False
        }

        response = requests.post(
            f"{X402_BASE}/generate/image",
            json=payload,
            headers=get_headers(),
            timeout=120
        )

        if response.status_code != 200:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None

        result = response.json()

        if not result.get('success'):
            print(f"❌ API returned error: {result}")
            return None

        # Get image data
        data = result.get('data', {})
        image_base64 = data.get('image')

        if not image_base64:
            print(f"❌ No image in response")
            print(f"Full response: {json.dumps(result, indent=2)}")
            return None

        print("✅ Image generated successfully!")
        print(f"🖼️ Image size: {len(image_base64)} bytes")

        # Decode base64
        if image_base64.startswith('data:image/'):
            header, encoded = image_base64.split(',', 1)
            import base64
            image_bytes = base64.b64decode(encoded)

            # Save to file
            if save_path:
                os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(image_bytes)
                print(f"💾 Saved to: {save_path}")

            return image_bytes

        print("❌ Unsupported image format")
        return None

    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Generate images using x402 Layer API',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('prompt', help='Text prompt for image generation')
    parser.add_argument('--model', '-m', default='default',
                      help='Model to use (default: default)')
    parser.add_argument('--output', '-o', help='Output file path (e.g., output.png)')
    parser.add_argument('--api-key', '-k', help='x402 Layer API key (optional)')

    args = parser.parse_args()

    # Generate image
    image_bytes = generate_image(
        args.prompt,
        args.model,
        args.output
    )

    if not image_bytes and not args.output:
        print("")
        print("💡 Tip: Use --output to save image to file")


if __name__ == '__main__':
    main()
