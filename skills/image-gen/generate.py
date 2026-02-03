#!/usr/bin/env python3
"""
Google AI Studio Image Generator
Generate images using Gemini 2.5 Flash Image API
"""

import os
import requests
import json
import base64
from datetime import datetime
from pathlib import Path

# Configuration
API_KEY_FILE = "/root/clawd/.google_api_key"
OUTPUT_DIR = "/root/clawd/images"
OUTPUT_FILE = "/root/clawd/images/latest_image.png"

# API endpoint (corrected)
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"

def get_api_key():
    """Get API key from file or environment"""
    # Check environment variable first
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    # Fall back to file
    if not api_key:
        try:
            with open(API_KEY_FILE, 'r') as f:
                api_key = f.read().strip()
        except:
            pass
    
    return api_key

def generate_image(prompt, api_key):
    """Generate an image using Google AI Studio API"""
    
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            return {
                'success': False,
                'error': f"API Error ({response.status_code}): {error_msg}"
            }
        
        data = response.json()
        
        # Check for image data
        if 'candidates' in data:
            for candidate in data['candidates']:
                if 'content' in candidate:
                    for part in candidate['content']['parts']:
                        if 'inlineData' in part:
                            # Decode base64 and save image
                            image_bytes = base64.b64decode(part['inlineData']['data'])
                            
                            # Create output directory
                            Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
                            
                            # Save with timestamp
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"image_{timestamp}.png"
                            filepath = Path(OUTPUT_DIR) / filename
                            
                            with open(filepath, 'wb') as f:
                                f.write(image_bytes)
                            
                            # Also save as latest
                            import shutil
                            shutil.copy(filepath, OUTPUT_FILE)
                            
                            return {
                                'success': True,
                                'filename': filename,
                                'filepath': str(filepath),
                                'size': len(image_bytes),
                                'message': f"✅ Image saved to {filename} ({len(image_bytes)} bytes)"
                            }
        
        return {
            'success': False,
            'error': 'No image data in response'
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timed out (60s)'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Exception: {str(e)}"
        }

def main():
    """Main function - generate image from prompt argument"""
    import sys
    
    # Get API key
    api_key = get_api_key()
    
    if not api_key:
        print("❌ No API key found!")
        print("\nHow to set up:")
        print("1. Go to https://aistudio.google.com/")
        print("2. Sign in with your Google account")
        print("3. Click 'Get API Key'")
        print("4. Save the key to: /root/clawd/.google_api_key")
        print("5. Run: python3 /root/clawd/skills/image-gen/generate.py 'your prompt here'")
        return
    
    # Get prompt from argument or use default
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "A beautiful sunset over mountains with warm colors"
    
    print(f"🎨 Generating image: '{prompt}'")
    print(f"⏳ Please wait...")
    
    # Generate image
    result = generate_image(prompt, api_key)
    
    if result['success']:
        print(result['message'])
        print(f"📁 Latest: {OUTPUT_FILE}")
    else:
        print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    main()
