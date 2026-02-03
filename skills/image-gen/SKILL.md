---
name: image-gen
description: Generate images using Google AI Studio's Gemini 2.5 Flash Image API for free.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"env":["GOOGLE_API_KEY"]}}}
---

# Google AI Studio Image Generation

Generate high-quality images for free using Google's Gemini 2.5 Flash Image API via Google AI Studio.

## Quick Start

### 1. Get Your API Key

1. Go to **https://aistudio.google.com/**
2. Sign in with your Google account
3. Click **"Get API Key"** (top right)
4. Create a new project
5. Copy your API key

### 2. Set API Key

```bash
# Set environment variable
export GOOGLE_API_KEY='your-key-here'

# Or save to file
echo 'your-key-here' > /root/clawd/.google_api_key
```

### 3. Generate Images

**Simple command line:**
```bash
python3 /root/clawd/skills/image-gen/generate.py "your prompt here"
```

**From Telegram:**
Just send me: `generate an image of [description]`

## API Details

**Free tier limits:**
- 1,500 images per day
- 60 requests per minute
- Gemini 2.5 Flash model (fastest, excellent quality)

**Supported models:**
- `gemini-2.0-flash-exp` (Flash - fastest)
- `gemini-2.5-flash-exp` (Flash - new, better quality)

## Output

Images are saved to `/root/clawd/images/` with timestamps:
- `image_YYYYMMDD_HHMMSS.png`
- Also creates `latest_image.png` for easy access

## Examples

```bash
# Generate a lion at sunset
python3 /root/clawd/skills/image-gen/generate.py "A majestic lion standing on a rocky cliff at sunset, digital art style, vibrant colors"

# Generate crypto chart visualization
python3 /root/clawd/skills/image-gen/generate.py "A futuristic cryptocurrency dashboard with glowing neon accents and data visualizations"

# Create portrait
python3 /root/clawd/skills/image-gen/generate.py "A professional LinkedIn headshot photo, studio lighting, neutral background"
```

## Notes

- Google AI Studio is **completely free** with the daily limits
- Images are returned as base64 encoded PNG data
- Model produces high-quality, vibrant images
- Perfect for digital art, illustrations, mockups, and more

## API Key Security

Your API key is stored at `/root/clawd/.google_api_key` and is protected with file permissions. Never share it publicly.

## Free Alternatives

If you hit daily limits (1,500 images/day), consider:
- **Together AI** - Free FLUX.1 Schnell for 3 months (excellent quality)
- **Replicate** - Multiple FLUX models available (~$0.003/image)
