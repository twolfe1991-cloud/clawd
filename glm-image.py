#!/usr/bin/env python3
"""
GLM-Image Generator using Z.AI API
Supports text-to-image and image-to-image generation
"""

import os
import sys
import argparse
import requests
import base64

# Load config
config_path = os.path.join(os.path.dirname(__file__), '.zai-config')
if not os.path.exists(config_path):
    print(f"Error: Config file not found at {config_path}")
    sys.exit(1)

with open(config_path, 'r') as f:
    for line in f:
        if line.startswith('ZAI_API_KEY='):
            API_KEY = line.strip().split('=', 1)[1].strip('"')
        elif line.startswith('ZAI_BASE_URL='):
            BASE_URL = line.strip().split('=', 1)[1].strip('"')

ENDPOINT = f"{BASE_URL}/images/generations"
EDIT_ENDPOINT = f"{BASE_URL}/images/edits"


def generate_image(prompt, size="1280x1280", n=1):
    """Generate image from text prompt"""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": "glm-image",
        "prompt": prompt,
        "size": size,
        "n": n
    }

    response = requests.post(ENDPOINT, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    result = response.json()
    if 'data' in result and len(result['data']) > 0:
        return result['data'][0]['url']
    return None


def edit_image(image_path, prompt, size="1280x1280"):
    """Edit existing image with text prompt"""
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        return None

    # Read and encode image
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": "glm-image",
        "image": image_data,
        "prompt": prompt,
        "size": size
    }

    response = requests.post(EDIT_ENDPOINT, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    result = response.json()
    if 'data' in result and len(result['data']) > 0:
        return result['data'][0]['url']
    return None


def main():
    parser = argparse.ArgumentParser(description='GLM-Image Generator')
    subparsers = parser.add_subparsers(dest='command', help='Command')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate image from text')
    gen_parser.add_argument('prompt', help='Text prompt for image generation')
    gen_parser.add_argument('--size', default='1280x1280', help='Image size (e.g., 1280x1280)')
    gen_parser.add_argument('--output', '-o', help='Save image to file')

    # Edit command
    edit_parser = subparsers.add_parser('edit', help='Edit existing image')
    edit_parser.add_argument('image', help='Path to image to edit')
    edit_parser.add_argument('prompt', help='Edit prompt')
    edit_parser.add_argument('--size', default='1280x1280', help='Output image size')

    args = parser.parse_args()

    if args.command == 'generate':
        print(f"Generating image: {args.prompt}")
        url = generate_image(args.prompt, args.size)

        if url:
            print(f"✅ Image generated successfully!")
            print(f"🔗 URL: {url}")

            if args.output:
                # Download and save
                img_resp = requests.get(url)
                if img_resp.status_code == 200:
                    with open(args.output, 'wb') as f:
                        f.write(img_resp.content)
                    print(f"💾 Saved to: {args.output}")
        else:
            print("❌ Failed to generate image")

    elif args.command == 'edit':
        print(f"Editing image: {args.image}")
        url = edit_image(args.image, args.prompt, args.size)

        if url:
            print(f"✅ Image edited successfully!")
            print(f"🔗 URL: {url}")
        else:
            print("❌ Failed to edit image")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
