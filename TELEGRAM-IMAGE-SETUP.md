# Telegram Image Generation Setup

## ✅ Two Options Available

### Option 1: Puter.js (Free, Browser-Based)
**Files:**
- `/root/clawd/puter-image-generator.html` - Web interface
- `/root/clawd/test-puter.sh` - Quick launcher

**How to use:**
```bash
/root/clawd/test-puter.sh
```

Then open `http://localhost:8080/puter-image-generator.html` in your browser.

**Models available:**
- **gemini-25-flash** (Nano Banana - like Google's!)
- gpt-image, dalle-2, dalle-3
- flux-1-schnell, flux-1-pro
- stable-diffusion-3, stable-diffusion-xl

**Pros:**
- 100% free
- No API key required
- Unlimited generations

**Cons:**
- Requires browser access
- Not easily automated from Telegram


### Option 2: Replicate API (Pay-Per-Use, Programmatic)
**Files:**
- `/root/clawd/telegram-replicate.py` - CLI script
- `/root/clawd/.replicate-config` - Config file (create this)

**Setup required:**
1. Get free API key from https://replicate.com/account/api-tokens
2. Add to config:
   ```bash
   echo 'REPLICATE_API_KEY="your-key-here"' > /root/clawd/.replicate-config
   ```

**Usage:**
```bash
python3 /root/clawd/telegram-replicate.py "A cute cat in a spacesuit" --model black-forest-labs/flux-schnell
```

**Models available:**
- `stability-ai/stable-diffusion-3` - SD3
- `stability-ai/sdxl` - SDXL
- `black-forest-labs/flux-pro` - Flux Pro (high quality)
- `black-forest-labs/flux-schnell` - Flux Schnell (fast)

**Pros:**
- Easy to automate from Telegram
- High quality models
- Reliable API

**Cons:**
- Requires API key (free tier available)
- Pay-per-use (~$0.01-0.17 per image)


## 🚀 Recommendation

For **Telegram use**, go with **Replicate**:

1. It's designed for programmatic access
2. Free tier available for testing
3. Easy to integrate with Telegram bots
4. Wide range of high-quality models


## 📝 Quick Start with Replicate

```bash
# 1. Get API key from https://replicate.com/account/api-tokens

# 2. Add to config
echo 'REPLICATE_API_KEY="your-api-key"' > /root/clawd/.replicate-config

# 3. Test
python3 /root/clawd/telegram-replicate.py "A futuristic city with neon lights" -o /tmp/test.png
```


## 💬 Telegram Integration

To use from Telegram, you have a few options:

### Option A: Manual Commands
When you want an image, just message me:
```
Generate: [your prompt] using [model]
```

Example:
```
Generate: A cat in space using flux-schnell
```

### Option B: Bot Integration (Advanced)
I can create a Telegram bot that:
1. Listens for `/generate` commands
2. Calls Replicate API
3. Sends image back

Want me to set this up? Just say: "Create Telegram image bot"

---

*Updated: 2026-02-02*
