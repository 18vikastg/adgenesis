# Quick Start Guide - Custom ML Pipeline

## 🎯 Overview
Replace OpenAI API with your own fine-tuned model for ad design generation.

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
cd ml_pipeline
pip install -r requirements.txt
```

### Step 2: Train a Quick Model (GPT-2)
```bash
# Quick training with GPT-2 (takes ~5-10 minutes)
python train.py --model gpt2 --quick-start

# Output: Model saved to models/fine_tuned/gpt2/
```

### Step 3: Start the ML Service
```bash
# Start inference server on port 8001
python serve.py --model gpt2

# You should see: ✅ Model loaded successfully
# Server running at: http://localhost:8001
```

### Step 4: Update Backend Configuration
```bash
cd ../backend

# Edit .env file and add:
MODEL_PROVIDER=custom
ML_SERVICE_URL=http://localhost:8001
```

### Step 5: Test It!
```bash
# Restart your backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Your app now uses your custom model instead of OpenAI! 🎉
```

## 📊 Model Comparison

### GPT-2 (Quick Start)
- ✅ **Fastest to train**: 5-10 minutes
- ✅ **Low memory**: 2 GB
- ✅ **Fast inference**: 0.5 seconds
- ⚠️ **Quality**: Good for testing
- 📦 **Size**: 500 MB

### Mistral 7B (Recommended)
- ✅ **Best quality**: Enterprise-grade
- ✅ **LoRA training**: 30-60 minutes
- ⚠️ **Memory**: 14 GB VRAM needed
- ⚠️ **Inference**: 1-2 seconds
- 📦 **Size**: 13 GB

### Training Commands

```bash
# GPT-2 (CPU-friendly, quick testing)
python train.py --model gpt2 --epochs 3

# GPT-2 Medium (better quality, still fast)
python train.py --model gpt2-medium --epochs 3

# Phi-2 (Microsoft's efficient model, good balance)
python train.py --model phi-2 --use-lora --epochs 3

# Mistral 7B (best quality, needs GPU)
python train.py --model mistral-7b --use-lora --epochs 3

# Llama 2 7B (needs HuggingFace token)
export HUGGINGFACE_TOKEN=your_token_here
python train.py --model llama2-7b --use-lora --epochs 3
```

## 🔧 Production Setup

### 1. Train with More Data
Add more examples to `data/training_data.json`:
```json
{
  "prompt": "Your design prompt",
  "platform": "meta",
  "format": "square",
  "response": {
    "background_color": "#ffffff",
    "elements": [...]
  }
}
```

### 2. Use Docker for Deployment
```bash
cd ml_pipeline/docker
docker-compose up -d
```

### 3. Scale with Multiple Workers
```bash
# Use gunicorn for production
gunicorn serve:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001 \
  --timeout 120
```

### 4. Monitor Performance
```bash
# Add experiment tracking
export WANDB_API_KEY=your_key
# Edit train.py: report_to="wandb"
```

## 🎓 Training Tips

### Add More Training Data
The more examples you have, the better your model:
- ✅ **Good**: 6 examples (current)
- ✅ **Better**: 50+ examples
- ✅ **Best**: 500+ examples

### Collect Real Data
Use your existing designs as training data:
```python
# Script to convert existing designs to training format
python scripts/export_training_data.py
```

### Fine-tune on Specific Platforms
Train separate models for each platform:
```bash
python train.py --model mistral-7b --platform meta
python train.py --model mistral-7b --platform google
```

## 💰 Cost Savings

### OpenAI Costs
- **GPT-3.5**: $0.002 per request
- **1000 requests/day**: $60/month
- **10,000 requests/day**: $600/month

### Custom Model Costs
- **Training**: One-time $5-20 (GPU hours)
- **Inference**: $0 (your own server)
- **1000 requests/day**: $0
- **10,000 requests/day**: $0

**Break-even**: After ~100 requests!

## 🐛 Troubleshooting

### "CUDA out of memory"
```bash
# Use smaller model
python train.py --model gpt2

# Or use 4-bit quantization
python train.py --model mistral-7b --use-lora
```

### "Model generates invalid JSON"
```bash
# Retrain with more epochs
python train.py --model gpt2 --epochs 5

# Or add more training examples
# Edit: data/training_data.json
```

### "Inference is slow"
```bash
# Use quantized model
python serve.py --model gpt2 --quantize

# Or use smaller model
python serve.py --model gpt2
```

## 📈 Next Steps

1. **Collect Data**: Export your existing designs as training data
2. **Train Better Model**: Use Mistral 7B for best quality
3. **A/B Test**: Compare OpenAI vs custom model quality
4. **Iterate**: Add more data and retrain regularly
5. **Deploy**: Use Docker for production deployment
6. **Monitor**: Track quality metrics and user feedback

## 🔄 Switch Back to OpenAI

If you need to switch back:
```bash
# Edit backend/.env
MODEL_PROVIDER=openai
OPENAI_API_KEY=your_key_here

# Restart backend
```

## 📚 Resources

- [Hugging Face Docs](https://huggingface.co/docs)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [Fine-tuning Guide](https://huggingface.co/docs/transformers/training)
- [Model Deployment](https://fastapi.tiangolo.com/)

## 💬 Need Help?

Check the logs:
```bash
# ML service logs
tail -f ml_pipeline/logs/serve.log

# Training logs
tail -f ml_pipeline/logs/train.log
```

Test the API directly:
```bash
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a tech ad",
    "platform": "meta",
    "format": "square"
  }'
```
