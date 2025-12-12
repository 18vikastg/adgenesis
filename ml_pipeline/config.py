"""
Configuration for ML Pipeline
"""
import os
from pathlib import Path
from typing import Literal

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
BASE_MODELS_DIR = MODELS_DIR / "base"
FINE_TUNED_DIR = MODELS_DIR / "fine_tuned"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
BASE_MODELS_DIR.mkdir(exist_ok=True)
FINE_TUNED_DIR.mkdir(exist_ok=True)

# Model configurations
MODEL_CONFIGS = {
    "gpt2": {
        "model_name": "gpt2",
        "context_length": 1024,
        "batch_size": 8,
        "learning_rate": 5e-5,
        "memory_gb": 2,
    },
    "gpt2-medium": {
        "model_name": "gpt2-medium",
        "context_length": 1024,
        "batch_size": 4,
        "learning_rate": 3e-5,
        "memory_gb": 4,
    },
    "mistral-7b": {
        "model_name": "mistralai/Mistral-7B-v0.1",
        "context_length": 4096,
        "batch_size": 2,
        "learning_rate": 2e-4,
        "memory_gb": 14,
        "use_lora": True,
    },
    "llama2-7b": {
        "model_name": "meta-llama/Llama-2-7b-hf",
        "context_length": 4096,
        "batch_size": 2,
        "learning_rate": 2e-4,
        "memory_gb": 14,
        "use_lora": True,
        "requires_auth": True,  # Requires HuggingFace token
    },
    "phi-2": {
        "model_name": "microsoft/phi-2",
        "context_length": 2048,
        "batch_size": 4,
        "learning_rate": 2e-4,
        "memory_gb": 6,
        "use_lora": True,
    },
}

# Training configuration
TRAINING_CONFIG = {
    "num_epochs": 3,
    "warmup_steps": 100,
    "logging_steps": 10,
    "save_steps": 500,
    "eval_steps": 250,
    "max_grad_norm": 1.0,
    "weight_decay": 0.01,
    "gradient_accumulation_steps": 4,
}

# LoRA configuration (for efficient fine-tuning)
LORA_CONFIG = {
    "r": 16,  # LoRA rank
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],  # For Llama/Mistral
    "bias": "none",
    "task_type": "CAUSAL_LM",
}

# Quantization (for reduced memory)
QUANTIZATION_CONFIG = {
    "load_in_4bit": True,
    "bnb_4bit_compute_dtype": "float16",
    "bnb_4bit_quant_type": "nf4",
    "bnb_4bit_use_double_quant": True,
}

# Inference configuration
INFERENCE_CONFIG = {
    "max_new_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "repetition_penalty": 1.1,
    "do_sample": True,
}

# Platform specifications (from main app)
PLATFORM_SPECS = {
    "meta": {
        "square": {"width": 1080, "height": 1080, "min_text_ratio": 0.2},
        "landscape": {"width": 1200, "height": 628, "min_text_ratio": 0.2},
        "portrait": {"width": 1080, "height": 1350, "min_text_ratio": 0.2},
        "story": {"width": 1080, "height": 1920, "min_text_ratio": 0.2},
    },
    "google": {
        "square": {"width": 1200, "height": 1200, "max_file_size": 150000},
        "landscape": {"width": 1200, "height": 628, "max_file_size": 150000},
    },
    "linkedin": {
        "square": {"width": 1200, "height": 1200},
        "landscape": {"width": 1200, "height": 627},
    },
}

# Server configuration
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8001,
    "workers": 1,  # Single worker for GPU
    "timeout": 120,
}

# Environment variables
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
DEVICE = os.getenv("DEVICE", "cuda" if os.path.exists("/proc/driver/nvidia") else "cpu")
