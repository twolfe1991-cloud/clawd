---
name: x402-layer
version: 1.0.0
description: |
  This skill should be used when the user asks to "create x402 endpoint",
  "deploy monetized API", "pay for API with USDC", "check x402 credits",
  "consume API credits", "list endpoint on marketplace", "buy API credits",
  "topup endpoint", "browse x402 marketplace", or manage x402 Singularity
  Layer operations on Base or Solana networks.
homepage: https://studio.x402layer.cc/docs/agentic-access/openclaw-skill
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://studio.x402layer.cc
    os:
      - linux
      - darwin
    requires:
      bins:
        - python3
      env:
        - WALLET_ADDRESS
        - PRIVATE_KEY
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
---


# x402 Singularity Layer

x402 is a **Web3 payment layer** enabling AI agents to:
- 💰 **Pay** for API access using USDC
- 🚀 **Deploy** monetized endpoints
- 🔍 **Discover** services via marketplace
- 📊 **Manage** endpoints and credits

**Networks:** Base (EVM) • Solana  
**Currency:** USDC  
**Protocol:** HTTP 402 Payment Required

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r {baseDir}/requirements.txt
```

### 2. Set Up Wallet
```bash
# For Base (EVM)
export PRIVATE_KEY="0x..."
export WALLET_ADDRESS="0x..."

# For Solana (optional)
export SOLANA_SECRET_KEY="[1,2,3,...]"  # JSON array
```

---

## Scripts Overview

### 🛒 CONSUMER MODE (Buying Services)

| Script | Purpose |
|--------|---------|
| `pay_base.py` | Pay for endpoint on Base network |
| `pay_solana.py` | Pay for endpoint on Solana network |
| `consume_credits.py` | Use pre-purchased credits (fast) |
| `consume_product.py` | Purchase digital products (files) |
| `check_credits.py` | Check your credit balance |
| `recharge_credits.py` | Buy credit packs for an endpoint |
| `discover_marketplace.py` | Browse available services |

### 🏭 PROVIDER MODE (Selling Services)

| Script | Purpose |
|--------|---------|
| `create_endpoint.py` | Deploy new monetized endpoint ($5) |
| `manage_endpoint.py` | View/update your endpoints |
| `topup_endpoint.py` | Add credits to YOUR endpoint |
| `list_on_marketplace.py` | Publish endpoint publicly |

---

## Consumer Flows

### A. Pay-Per-Request (Recommended)

```bash
# Pay with Base (EVM) - 100% reliable
python {baseDir}/scripts/pay_base.py https://api.x402layer.cc/e/weather-data

# Pay with Solana - includes retry logic
python {baseDir}/scripts/pay_solana.py https://api.x402layer.cc/e/weather-data
```

### B. Credit-Based (Fastest)

```bash
# Check balance first
python {baseDir}/scripts/check_credits.py weather-data

# Buy a credit pack
python {baseDir}/scripts/recharge_credits.py weather-data pack_100

# Consume using credits (zero blockchain latency!)
python {baseDir}/scripts/consume_credits.py https://api.x402layer.cc/e/weather-data
```

### C. Digital Products

```bash
# Purchase and download a digital product
python {baseDir}/scripts/consume_product.py pussio --download
```

---

## Provider Flows

### A. Create Monetized Endpoint

```bash
python {baseDir}/scripts/create_endpoint.py my-api "My Service" https://api.example.com 0.01
```

### B. Monitor & Manage

```bash
# List your endpoints
python {baseDir}/scripts/manage_endpoint.py list

# Get stats
python {baseDir}/scripts/manage_endpoint.py info my-api
```

### C. Top Up Your Endpoint

```bash
# Add credits so your service can call other services  
python {baseDir}/scripts/topup_endpoint.py my-api 10
```

---

## Resources

- **ClawHub:** https://clawhub.ai/ivaavimusic/x402-layer
- **Documentation:** https://studio.x402layer.cc/docs/agentic-access/openclaw-skill
- **Marketplace:** https://studio.x402layer.cc/marketplace
- **GitHub:** https://github.com/ivaavimusic/x402-Layer-Clawhub-Skill
