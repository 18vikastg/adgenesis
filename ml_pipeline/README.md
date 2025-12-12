# ADGENESIS ML Pipeline

## Overview
Custom fine-tuned model pipeline to replace OpenAI API for ad design generation.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ADGENESIS ML PIPELINE                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   Training   │──────│  Fine-tuned  │──────│ Inference │ │
│  │   Pipeline   │      │    Model     │      │  Service  │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│         │                      │                     │       │
│         ▼                      ▼                     ▼       │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │ Training Data│      │ Model Weights│      │   FastAPI │ │
│  │   (JSON)     │      │  (PyTorch)   │      │  Endpoint │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Base Model Options
- **GPT-2** (smallest, fastest) - Good for prototyping
- **Llama 2 7B** - Better quality, requires more resources
- **Mistral 7B** - Best balance of speed and quality
- **Phi-2** - Microsoft's efficient small model

### 2. Fine-tuning Strategy
- **Task**: Generate structured JSON design specifications from text prompts
- **Approach**: Instruction fine-tuning with LoRA/QLoRA
- **Dataset**: Platform-specific ad design examples with prompts

### 3. Deployment Options
- **Local**: Run on your own hardware
- **Cloud**: Deploy to AWS/Azure/GCP
- **Edge**: Quantized models for faster inference

## Quick Start

### Option A: Use Pre-trained GPT-2 (Fastest)
```bash
cd ml_pipeline
pip install -r requirements.txt
python train.py --model gpt2 --quick-start
python serve.py --model gpt2
```

### Option B: Fine-tune Llama 2
```bash
cd ml_pipeline
pip install -r requirements.txt
python prepare_data.py
python train.py --model llama2-7b --epochs 3
python serve.py --model llama2-7b
```

### Option C: Fine-tune Mistral (Recommended)
```bash
cd ml_pipeline
pip install -r requirements.txt
python prepare_data.py
python train.py --model mistral-7b --epochs 3 --use-lora
python serve.py --model mistral-7b
```

## Training Data Format

```json
{
  "prompt": "Create a modern tech startup ad for Meta square format",
  "platform": "meta",
  "format": "square",
  "response": {
    "background_color": "#1a1a2e",
    "elements": [
      {
        "type": "text",
        "text": "Launch Your Startup",
        "x": 100,
        "y": 200,
        "fontSize": 64,
        "color": "#ffffff",
        "fontFamily": "Montserrat"
      }
    ]
  }
}
```

## Integration with Backend

```python
# In backend/app/utils.py
from ml_pipeline.client import MLModelClient

ml_client = MLModelClient(base_url="http://localhost:8001")

async def generate_ai_design(prompt: str, platform: str, format: str) -> dict:
    design_spec = await ml_client.generate_design(prompt, platform, format)
    return design_spec
```

## Performance Comparison

| Model | Inference Time | Quality | Memory | Cost |
|-------|---------------|---------|--------|------|
| OpenAI GPT-3.5 | 2-5s | ⭐⭐⭐⭐⭐ | 0 GB | $0.002/req |
| GPT-2 Fine-tuned | 0.5s | ⭐⭐⭐ | 2 GB | $0 |
| Llama 2 7B | 1-2s | ⭐⭐⭐⭐ | 14 GB | $0 |
| Mistral 7B | 1-2s | ⭐⭐⭐⭐⭐ | 14 GB | $0 |

## Directory Structure

```
ml_pipeline/
├── README.md                    # This file
├── requirements.txt             # ML dependencies
├── config.py                    # Configuration
├── data/
│   ├── training_data.json      # Training examples
│   ├── validation_data.json    # Validation examples
│   └── templates/              # Design templates
├── models/
│   ├── base/                   # Downloaded base models
│   └── fine_tuned/             # Your trained models
├── scripts/
│   ├── prepare_data.py         # Data preparation
│   ├── train.py                # Training script
│   ├── evaluate.py             # Model evaluation
│   └── export.py               # Model export
├── src/
│   ├── model.py                # Model architecture
│   ├── trainer.py              # Training logic
│   ├── dataset.py              # Dataset classes
│   └── inference.py            # Inference engine
├── serve.py                     # FastAPI inference server
├── client.py                    # Python client
└── docker/
    ├── Dockerfile              # Container image
    └── docker-compose.yml      # Service orchestration
```

## Next Steps

1. **Collect Training Data**: Use existing designs as examples
2. **Choose Model**: Start with GPT-2 for quick testing
3. **Fine-tune**: Train on your specific ad design task
4. **Deploy**: Start inference server
5. **Integrate**: Update backend to use ML service
6. **Monitor**: Track quality and performance
7. **Iterate**: Add more training data and retrain

## Resources

- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [LoRA Fine-tuning](https://github.com/microsoft/LoRA)
- [Model Deployment Guide](https://fastapi.tiangolo.com/)
