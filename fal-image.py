#!/usr/bin/env python3
"""
Telegram + Fal.ai Image Generator
Generates images via Telegram using Fal.ai API (free credits available)
"""

import os
import sys
import requests
import argparse
import time

# Config file path
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '.fal-config')
FAL_API_KEY = None


def load_config():
    """Load Fal.ai API key from config"""
    global FAL_API_KEY

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            for line in f:
                if line.startswith('FAL_API_KEY='):
                    FAL_API_KEY = line.strip().split('=', 1)[1].strip('"')


def generate_image_fal(prompt, model="fal-ai/flux/dev"):
    """
    Generate image using Fal.ai API
    """
    if not FAL_API_KEY:
        print("❌ Error: FAL_API_KEY not set")
        print("")
        print("To get free credits:")
        print("1. Go to https://fal.ai/")
        print("2. Sign up (free)")
        print("3. Get API key from https://fal.ai/dashboard")
        print("")
        print("Then add to config:")
        print(f"   echo 'FAL_API_KEY=\"your-key\"' > {CONFIG_PATH}")
        return None

    headers = {
        'Authorization': f'Key {FAL_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Fal.ai API endpoint for text-to-image
    # Different models use different endpoints
    endpoint = f"https://queue.fal.run/{model}"

    payload = {
        "prompt": prompt,
        "image_size": "square_hd"  # or landscape_4_3, portrait_4_3, etc.
    }

    print(f"🎨 Generating image with model: {model}")
    print(f"📝 Prompt: {prompt}")
    print("⏳ Submitting to queue...")

    try:
        # Submit to queue
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return None

        result = response.json()
        request_id = result['request_id']
        print(f"✅ Request submitted: {request_id}")
        print("⏳ Waiting for result...")

        # Poll for result
        poll_url = f"https://queue.fal.run/{model}/requests/{request_id}/status"

        # Fal.ai provides a status endpoint we can poll
        for i in range(60):  # Wait up to 2 minutes
            status_response = requests.get(poll_url, headers=headers)

            if status_response.status_code == 200:
                status_data = status_response.json()

                if status_data.get('status') == 'COMPLETED':
                    print("✅ Image generation complete!")
                    output = status_data.get('logs', [])[0] if status_data.get('logs') else None

                    if output and 'images' in output:
                        image_url = output['images'][0]['url']
                        print(f"🔗 Image URL: {image_url}")
                        return image_url
                    elif output and 'file' in output:
                        image_url = output['file']['url']
                        print(f"🔗 Image URL: {image_url}")
                        return image_url
                    else:
                        print(f"Output: {output}")

                elif status_data.get('status') == 'FAILED':
                    print("❌ Generation failed")
                    print(status_data)
                    return None
                elif status_data.get('status') == 'IN_PROGRESS':
                    print(f"⏳ Processing... ({i+1}/60)", end='\r')

                elif status_data.get('status') == 'IN_QUEUE':
                    print(f"📍 Queued... ({i+1}/60)", end='\r')

            time.sleep(2)

        print("❌ Timeout - generation took too long")
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
        description='Generate images using Fal.ai API (free credits available)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available models:
  fal-ai/flux/dev              Flux Dev (fast)
  fal-ai/flux-pro              Flux Pro (high quality)
  fal-ai/nano-banana-pro       Nano Banana Pro (like Google's!)
  fal-ai/stable-diffusion-3     Stable Diffusion 3
  fal-ai/stable-diffusion-xl      Stable Diffusion XL
  fal-ai/fast-sdxl              Fast SDXL

Example:
  python3 fal-image.py "A cat in space" --model fal-ai/flux-dev
  python3 fal-image.py "Sunset" --model fal-ai/nano-banana-pro -o output.png
        """
    )

    parser.add_argument('prompt', help='Text prompt for image generation')
    parser.add_argument('--model', '-m', default='fal-ai/flux-dev',
                      help='Model to use (default: fal-ai/flux-dev)')
    parser.add_argument('--output', '-o', help='Output file path (e.g., output.png)')

    args = parser.parse_args()

    # Load config
    load_config()

    # Generate
    image_url = generate_image_fal(args.prompt, args.model)

    if image_url and args.output:
        download_image(image_url, args.output)
    elif image_url:
        print("")
        print("💡 Add --output to save image to file")


if __name__ == '__main__':
    main()
