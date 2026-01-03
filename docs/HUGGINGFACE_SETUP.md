# 🔑 Hugging Face API Key Setup Guide

## Quick Start

```bash
# Run the setup helper
./setup_env.sh
```

---

## 📋 Step-by-Step Instructions

### 1️⃣ Create Hugging Face Account (FREE)

1. Visit: **https://huggingface.co/**
2. Click **"Sign Up"** (top right corner)
3. Sign up with:
   - Email
   - OR Google account
   - OR GitHub account
4. Verify your email address

### 2️⃣ Generate Your API Token

1. Log in to Hugging Face
2. Click your **profile picture** (top right)
3. Go to **Settings** → **Access Tokens**
   - Direct link: **https://huggingface.co/settings/tokens**
4. Click **"New token"** button
5. Configure token:
   - **Name**: `adgenesis-app` (or any name you want)
   - **Role**: Select **"Read"** (sufficient for API inference)
6. Click **"Generate token"**
7. **⚠️ IMPORTANT**: Copy the token immediately!
   - It starts with `hf_`
   - You won't be able to see it again
   - Example: `hf_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890`

### 3️⃣ Set Environment Variable

Choose your preferred method:

#### **Method A: Using .env File (Recommended)**

```bash
# 1. Create .env file in project root
cd /home/vikas/Desktop/adgenesis
cp .env.example .env

# 2. Edit .env file
nano .env
# OR
code .env

# 3. Replace placeholder with your actual token
HUGGINGFACE_API_KEY=hf_your_actual_token_here

# 4. Save and exit (Ctrl+O, Enter, Ctrl+X for nano)

# 5. Restart all services
./start_all.sh
```

#### **Method B: Export in Terminal (Temporary)**

```bash
# Set for current session only
export HUGGINGFACE_API_KEY='hf_your_actual_token_here'

# Start ML service
cd ml_pipeline
python serve_design.py
```

#### **Method C: Permanent Shell Configuration**

```bash
# For bash users
echo 'export HUGGINGFACE_API_KEY="hf_your_actual_token_here"' >> ~/.bashrc
source ~/.bashrc

# For zsh users
echo 'export HUGGINGFACE_API_KEY="hf_your_actual_token_here"' >> ~/.zshrc
source ~/.zshrc
```

### 4️⃣ Verify Setup

```bash
# Check if API key is set
echo $HUGGINGFACE_API_KEY

# Should output: hf_your_token...
# If empty, the variable is not set
```

---

## 💰 API Key Limits & Pricing

### Free Tier (Default)

| Feature | Limit |
|---------|-------|
| **Cost** | 🎉 **FREE** |
| **Rate Limit** | ~1,000 requests/day |
| **Image Generation** | Available (may be slower) |
| **Models** | Access to public models |
| **Concurrent Requests** | Limited to 1-2 |
| **Queue Time** | May wait in queue during peak hours |

### When You Hit Limits

If you see errors like:
- `"Rate limit exceeded"`
- `"Model is loading"`
- `"Queue full"`

**Solutions:**
1. **Wait a few minutes** - Free tier queues clear quickly
2. **Use off-peak hours** - Night time / early morning (UTC)
3. **Upgrade to PRO** - Faster inference, higher limits

### PRO Tier (Optional - $9/month)

| Feature | Benefit |
|---------|---------|
| **Cost** | $9/month |
| **Rate Limit** | ~10,000 requests/day |
| **Speed** | Faster inference (no queue wait) |
| **Priority** | Skip the queue |
| **Concurrent Requests** | Up to 10 |

**Upgrade at**: https://huggingface.co/pricing

---

## 🎨 Available AI Models

AdGenesis supports these Hugging Face models:

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| **SDXL-Turbo** (Default) | ⚡ Fast | Good | Quick drafts, rapid iteration |
| **Stable Diffusion 2.1** | Medium | Excellent | High-quality images |
| **SDXL 1.0** | Slow | Best | Final production images |

The model is auto-selected based on your design requirements.

---

## 🚨 Troubleshooting

### Error: "HUGGINGFACE_API_KEY not set"

```bash
# Check if variable exists
echo $HUGGINGFACE_API_KEY

# If empty, set it
export HUGGINGFACE_API_KEY='hf_your_token'

# Restart services
./start_all.sh
```

### Error: "Invalid API key"

- Verify your token starts with `hf_`
- Check for extra spaces or quotes
- Generate a new token if needed

### Error: "Rate limit exceeded"

- **Free tier**: Wait 1 hour, then retry
- **Upgrade to PRO**: https://huggingface.co/pricing
- **Alternative**: Use different model or reduce frequency

### Images Not Generating

```bash
# 1. Check ML service is running
curl http://localhost:8001/health

# 2. Check logs
tail -f /tmp/ml.log

# 3. Test image generation
curl -X POST http://localhost:8001/generate-image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a red apple", "width": 512, "height": 512}'
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Store tokens in `.env` file
- Add `.env` to `.gitignore` (already done)
- Use different tokens for dev/production
- Regenerate tokens periodically

### ❌ DON'T:
- Commit tokens to Git
- Share tokens publicly
- Use production tokens in development
- Store tokens in code files

---

## 📚 Additional Resources

- **Hugging Face Docs**: https://huggingface.co/docs/api-inference/
- **Model Hub**: https://huggingface.co/models
- **Pricing**: https://huggingface.co/pricing
- **Support**: https://discuss.huggingface.co/

---

## 🎯 Quick Reference

```bash
# Get API key
https://huggingface.co/settings/tokens

# Set in .env file
HUGGINGFACE_API_KEY=hf_your_token_here

# Restart services
./start_all.sh

# Test
curl http://localhost:8001/health
```

---

**Need help?** Check the logs:
```bash
tail -f /tmp/ml.log
```
