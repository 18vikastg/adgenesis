"""
Fine-tuning Script for AdGenesis Design Model
Trains a model to generate structured JSON design blueprints from prompts

This script supports training smaller models like:
- GPT-2 (for testing)
- Phi-2/Phi-3 (2.7B params - good balance)
- Mistral-7B (if you have GPU)
- TinyLlama (1.1B - very fast)
"""

import os
import json
import torch
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from datasets import Dataset, load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType,
)
import warnings
warnings.filterwarnings("ignore")

# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class ModelConfig:
    """Configuration for model training"""
    
    # Model selection - choose based on your hardware
    # Options: "gpt2", "gpt2-medium", "microsoft/phi-2", "TinyLlama/TinyLlama-1.1B-Chat-v1.0", "mistralai/Mistral-7B-v0.1"
    model_name: str = "gpt2-medium"  # Start with GPT-2 medium for testing
    
    # Training data
    data_path: str = "data/design_training_data_formatted.json"
    
    # Output
    output_dir: str = "models/fine_tuned/design_model"
    
    # Training parameters
    num_epochs: int = 3
    batch_size: int = 4
    learning_rate: float = 2e-4
    max_length: int = 1024  # GPT-2 max is 1024
    gradient_accumulation_steps: int = 4
    warmup_steps: int = 100
    
    # LoRA parameters (for efficient training)
    use_lora: bool = True
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    
    # Quantization (for large models on limited VRAM)
    use_4bit: bool = False  # Enable for 7B+ models
    use_8bit: bool = False
    
    # Hardware
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    fp16: bool = torch.cuda.is_available()

# =============================================================================
# DATA PREPARATION
# =============================================================================

def load_training_data(data_path: str) -> Dataset:
    """Load and prepare training data"""
    
    print(f"Loading training data from {data_path}")
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Convert to dataset format
    texts = []
    for sample in data:
        # Format: instruction + output
        text = f"{sample['instruction']}\n\n{sample['output']}"
        texts.append({"text": text})
    
    dataset = Dataset.from_list(texts)
    print(f"Loaded {len(dataset)} training samples")
    
    return dataset

def tokenize_dataset(dataset: Dataset, tokenizer, max_length: int):
    """Tokenize the dataset"""
    
    def tokenize_function(examples):
        result = tokenizer(
            examples["text"],
            truncation=True,
            max_length=max_length,
            padding="max_length",
        )
        result["labels"] = result["input_ids"].copy()
        return result
    
    tokenized = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names,
        desc="Tokenizing"
    )
    
    return tokenized

# =============================================================================
# MODEL SETUP
# =============================================================================

def setup_model_and_tokenizer(config: ModelConfig):
    """Setup model and tokenizer with optional quantization and LoRA"""
    
    print(f"Loading model: {config.model_name}")
    print(f"Device: {config.device}")
    
    # Quantization config for large models
    bnb_config = None
    if config.use_4bit:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
    elif config.use_8bit:
        bnb_config = BitsAndBytesConfig(load_in_8bit=True)
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        config.model_name,
        trust_remote_code=True,
    )
    
    # Set pad token if not exists
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    # Load model
    model_kwargs = {
        "trust_remote_code": True,
        "torch_dtype": torch.float16 if config.fp16 else torch.float32,
    }
    
    if bnb_config:
        model_kwargs["quantization_config"] = bnb_config
        model_kwargs["device_map"] = "auto"
    else:
        model_kwargs["device_map"] = config.device
    
    model = AutoModelForCausalLM.from_pretrained(
        config.model_name,
        **model_kwargs
    )
    
    # Prepare for k-bit training if quantized
    if config.use_4bit or config.use_8bit:
        model = prepare_model_for_kbit_training(model)
    
    # Apply LoRA
    if config.use_lora:
        print("Applying LoRA...")
        
        # Find target modules based on model architecture
        target_modules = ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
        
        # For GPT-2 style models
        if "gpt2" in config.model_name.lower():
            target_modules = ["c_attn", "c_proj", "c_fc"]
        
        lora_config = LoraConfig(
            r=config.lora_r,
            lora_alpha=config.lora_alpha,
            target_modules=target_modules,
            lora_dropout=config.lora_dropout,
            bias="none",
            task_type=TaskType.CAUSAL_LM,
        )
        
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
    
    return model, tokenizer

# =============================================================================
# TRAINING
# =============================================================================

def train_model(config: ModelConfig):
    """Main training function"""
    
    print("="*60)
    print("AdGenesis Design Model Fine-tuning")
    print("="*60)
    
    # Load data
    dataset = load_training_data(config.data_path)
    
    # Split into train/eval
    dataset = dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = dataset["train"]
    eval_dataset = dataset["test"]
    
    print(f"Train samples: {len(train_dataset)}")
    print(f"Eval samples: {len(eval_dataset)}")
    
    # Setup model
    model, tokenizer = setup_model_and_tokenizer(config)
    
    # Tokenize
    train_dataset = tokenize_dataset(train_dataset, tokenizer, config.max_length)
    eval_dataset = tokenize_dataset(eval_dataset, tokenizer, config.max_length)
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # Causal LM, not masked LM
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        overwrite_output_dir=True,
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        warmup_steps=config.warmup_steps,
        logging_steps=50,
        eval_strategy="steps",
        eval_steps=500,
        save_strategy="steps",
        save_steps=500,
        save_total_limit=3,
        load_best_model_at_end=True,
        fp16=config.fp16,
        report_to="none",  # Disable wandb etc.
        push_to_hub=False,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )
    
    # Train
    print("\nStarting training...")
    trainer.train()
    
    # Save final model
    print(f"\nSaving model to {config.output_dir}")
    trainer.save_model()
    tokenizer.save_pretrained(config.output_dir)
    
    # Save training config
    config_path = Path(config.output_dir) / "training_config.json"
    with open(config_path, 'w') as f:
        json.dump({
            "model_name": config.model_name,
            "num_epochs": config.num_epochs,
            "batch_size": config.batch_size,
            "learning_rate": config.learning_rate,
            "max_length": config.max_length,
            "use_lora": config.use_lora,
            "lora_r": config.lora_r,
            "lora_alpha": config.lora_alpha,
        }, f, indent=2)
    
    print("\nTraining complete!")
    return model, tokenizer

# =============================================================================
# INFERENCE
# =============================================================================

def load_trained_model(model_path: str, config: Optional[ModelConfig] = None):
    """Load a trained model for inference"""
    
    if config is None:
        config = ModelConfig()
    
    print(f"Loading trained model from {model_path}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # Load base model + LoRA weights
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if config.fp16 else torch.float32,
        device_map=config.device,
    )
    
    return model, tokenizer

def generate_design(
    model, 
    tokenizer, 
    prompt: str,
    max_new_tokens: int = 1500,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> dict:
    """Generate a design blueprint from a prompt"""
    
    # Format the prompt
    full_prompt = f"""You are an AI ad design assistant. Given a prompt describing an ad, generate a complete design blueprint in JSON format.

The blueprint should include:
- metadata (platform, format, dimensions)
- headline and subheadline text
- CTA button text
- background configuration
- color palette
- positioned design elements (text, shapes, buttons)

Prompt: {prompt}

Generate the design blueprint JSON:"""
    
    # Tokenize
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    
    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    
    # Decode
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract JSON from response
    try:
        # Find JSON in the output
        json_start = generated_text.find('{')
        json_end = generated_text.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = generated_text[json_start:json_end]
            blueprint = json.loads(json_str)
            return blueprint
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return {"error": "Failed to generate valid JSON", "raw_output": generated_text}
    
    return {"error": "No JSON found in output", "raw_output": generated_text}

# =============================================================================
# QUICK START TRAINING (for testing)
# =============================================================================

def quick_train():
    """Quick training with minimal settings for testing"""
    
    config = ModelConfig(
        model_name="gpt2",  # Small model for quick testing
        num_epochs=1,
        batch_size=2,
        max_length=1024,
        gradient_accumulation_steps=2,
        use_lora=True,
        lora_r=8,
        output_dir="models/fine_tuned/design_model_quick",
    )
    
    return train_model(config)

def full_train():
    """Full training with better model"""
    
    config = ModelConfig(
        model_name="gpt2-medium",  # Better quality
        num_epochs=3,
        batch_size=4,
        max_length=2048,
        gradient_accumulation_steps=4,
        use_lora=True,
        lora_r=16,
        output_dir="models/fine_tuned/design_model",
    )
    
    return train_model(config)

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train AdGenesis Design Model")
    parser.add_argument("--quick", action="store_true", help="Quick training for testing")
    parser.add_argument("--model", type=str, default="gpt2-medium", help="Base model to use")
    parser.add_argument("--epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    
    args = parser.parse_args()
    
    if args.quick:
        print("Running quick training (for testing)...")
        model, tokenizer = quick_train()
    else:
        config = ModelConfig(
            model_name=args.model,
            num_epochs=args.epochs,
            batch_size=args.batch_size,
        )
        model, tokenizer = train_model(config)
    
    # Test generation
    print("\n" + "="*60)
    print("Testing generation...")
    print("="*60)
    
    test_prompt = "Create a bold Instagram post ad for a fitness app. Campaign type: product launch. Target audience: young professionals."
    
    blueprint = generate_design(model, tokenizer, test_prompt)
    print(f"\nGenerated blueprint:\n{json.dumps(blueprint, indent=2)[:1500]}...")
