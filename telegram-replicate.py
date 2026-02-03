#!/usr/bin/env python3
"""
Telegram + Replicate Image Generator
Generates images via Telegram using Replicate API
"""

import os
import sys
import requests
import argparse
import time

# You can get your API key from: https://replicate.com/account/api-tokens
REPLICATE_API_KEY = None

# Config file path
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '.replicate-config')


def load_config():
    """Load Replicate API key from config"""
    global REPLICATE_API_KEY

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            for line in f:
                if line.startswith('REPLICATE_API_KEY='):
                    REPLICATE_API_KEY = line.strip().split('=', 1)[1].strip('"')


def generate_image_replicate(prompt, model="black-forest-labs/flux-schnell"):
    """
    Generate image using Replicate API
    """
    if not REPLICATE_API_KEY:
        print("❌ Error: REPLICATE_API_KEY not set")
        print("")
        print("Please add your Replicate API key:")
        print(f"   echo 'REPLICATE_API_KEY=\"your-key\"' > {CONFIG_PATH}")
        return None

    headers = {
        'Authorization': f'Bearer {REPLICATE_API_KEY}',
        'Content-Type': 'application/json'
    }

    # For official models, use /models/{owner}/{name}/predictions endpoint
    # This doesn't require version parameter
    endpoint = f"https://api.replicate.com/v1/models/{model}/predictions"

    create_payload = {
        "input": {
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "num_outputs": 1
        }
    }

    print(f"🎨 Generating image with model: {model}")
    print(f"📝 Prompt: {prompt}")
    print("⏳ Creating prediction...")

    try:
        # Create prediction
        response = requests.post(
            endpoint,
            json=create_payload,
            headers=headers
        )

        if response.status_code != 201:
            print(f"❌ Error creating prediction: {response.status_code}")
            print(response.text)
            return None

        prediction = response.json()
        prediction_id = prediction['id']

        # Build get URL
        get_url = f"https://api.replicate.com/v1/models/{model}/predictions/{prediction_id}"

        print(f"✅ Prediction created: {prediction_id}")
        print("⏳ Processing...")

        # Poll for completion
        while True:
            status_response = requests.get(get_url, headers=headers)
            status_data = status_response.json()

            status = status_data['status']

            if status == 'succeeded':
                print("✅ Image generation complete!")

                # Handle different output formats
                output = status_data.get('output')

                if isinstance(output, str):
                    # Single URL string
                    output_url = output
                elif isinstance(output, list):
                    # Array of URLs
                    output_url = output[0] if output else None
                elif isinstance(output, dict):
                    # Dict with various fields
                    output_url = output.get('image') or output.get('url')
                else:
                    output_url = str(output)

                if output_url:
                    print(f"🔗 Image URL: {output_url}")
                    return output_url
                else:
                    print(f"❌ Unexpected output format: {type(output)}")
                    print(f"Output: {output}")
                    return None

            elif status == 'failed':
                print("❌ Generation failed")
                print(status_data)
                return None

            elif status in ['starting', 'processing', 'cancelling']:
                print(f"⏳ Status: {status}...", end='\r')
                time.sleep(2)
                continue

            else:
                print(f"❌ Unknown status: {status}")
                return None

    except KeyboardInterrupt:
        print("\n❌ Cancelled")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def download_image(url, output_path):
    """Download image from URL"""
    try:
        print(f"📥 Downloading to: {output_path}")
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Saved: {output_path}")
            return True
        else:
            print(f"❌ Download failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Download error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Generate images using Replicate API',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('prompt', help='Text prompt for image generation')
    parser.add_argument('--model', '-m', default='black-forest-labs/flux-schnell',
                      help='Model to use (default: black-forest-labs/flux-schnell)')
    parser.add_argument('--output', '-o', help='Output file path (e.g., output.png)')

    args = parser.parse_args()

    # Load config
    load_config()

    # Generate
    image_url = generate_image_replicate(args.prompt, args.model)

    if image_url and args.output:
        download_image(image_url, args.output)
    elif image_url:
        print("")
        print("💡 Add --output to save image to file")


if __name__ == '__main__':
    main()
