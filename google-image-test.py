#!/usr/bin/env python3
"""
Google AI Studio Image Generation Test Script
Uses Gemini 2.5 Flash Image API for free image generation
"""

import subprocess
import json
import os

def generate_image(prompt, api_key):
    """Generate an image using Google Gemini 2.5 Flash Image API"""
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
    
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt}
            ]
        }]
    }
    
    try:
        result = subprocess.run([
            'curl', '-X', 'POST',
            url,
            '-H', f'x-goog-api-key: {api_key}',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(payload),
            '-s'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        
        # Parse response
        response = json.loads(result.stdout)
        
        # Check for image data
        if 'candidates' in response:
            for candidate in response['candidates']:
                if 'content' in candidate:
                    for part in candidate['content']['parts']:
                        if 'inlineData' in part:
                            return part['inlineData']['data']
        
        return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    """Main function"""
    # Get API key from environment or prompt
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set!")
        print("\nHow to set up:")
        print("1. Go to https://aistudio.google.com/")
        print("2. Sign in with your Google account")
        print("3. Click 'Get API Key'")
        print("4. Copy your API key")
        print("5. Run: export GOOGLE_API_KEY='your-key-here'")
        return
    
    # Simple test prompt
    prompt = "A majestic lion standing on a rocky cliff at sunset, digital art style, vibrant colors"
    
    print(f"🎨 Generating image: '{prompt}'")
    print(f"⏳ This may take 10-30 seconds...")
    
    # Generate image
    image_data = generate_image(prompt, api_key)
    
    if image_data:
        # Save to file
        filename = f"generated_image_{json.dumps(prompt)[:20].replace(' ', '_')}.png"
        
        import base64
        image_bytes = base64.b64decode(image_data)
        
        with open(filename, 'wb') as f:
            f.write(image_bytes)
        
        print(f"✅ Image saved to: {filename}")
        print(f"📊 Size: {len(image_bytes):,} bytes")
    else:
        print("❌ Failed to generate image")

if __name__ == "__main__":
    main()
