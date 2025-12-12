"""
Training script for fine-tuning models on ad design generation
"""
import argparse
import json
import torch
from pathlib import Path
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
import config


def load_training_data():
    """Load and prepare training data"""
    with open(config.DATA_DIR / "training_data.json", "r") as f:
        data = json.load(f)
    
    # Format data for training
    formatted_data = []
    for example in data:
        # Create instruction-response format
        instruction = f"""Generate a JSON design specification for an advertisement.
Platform: {example['platform']}
Format: {example['format']}
Prompt: {example['prompt']}

Return a valid JSON with background_color and elements array."""
        
        response = json.dumps(example['response'], indent=2)
        
        # Combine into training format
        text = f"### Instruction:\n{instruction}\n\n### Response:\n{response}"
        formatted_data.append({"text": text})
    
    return Dataset.from_list(formatted_data)


def tokenize_function(examples, tokenizer, max_length=1024):
    """Tokenize the training examples"""
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )


def train_model(
    model_name: str = "gpt2",
    output_dir: str = None,
    use_lora: bool = False,
    epochs: int = 3,
    quick_start: bool = False,
):
    """
    Fine-tune a language model on ad design generation
    
    Args:
        model_name: Name of base model (gpt2, mistral-7b, llama2-7b, phi-2)
        output_dir: Where to save the fine-tuned model
        use_lora: Use LoRA for efficient fine-tuning
        epochs: Number of training epochs
        quick_start: Use smaller settings for quick testing
    """
    print(f"🚀 Starting training with {model_name}")
    
    # Get model configuration
    if model_name not in config.MODEL_CONFIGS:
        raise ValueError(f"Unknown model: {model_name}. Choose from {list(config.MODEL_CONFIGS.keys())}")
    
    model_config = config.MODEL_CONFIGS[model_name]
    base_model_name = model_config["model_name"]
    
    # Set output directory
    if output_dir is None:
        output_dir = config.FINE_TUNED_DIR / model_name
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 Loading tokenizer and model: {base_model_name}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model
    if use_lora or model_config.get("use_lora", False):
        print("🔧 Loading model with 4-bit quantization for LoRA")
        model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            load_in_4bit=True,
            device_map="auto",
            torch_dtype=torch.float16,
        )
        model = prepare_model_for_kbit_training(model)
        
        # Configure LoRA
        lora_config = LoraConfig(**config.LORA_CONFIG)
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
    else:
        print("📥 Loading full model")
        model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
        )
    
    # Load and prepare dataset
    print("📊 Loading training data")
    dataset = load_training_data()
    
    # Tokenize
    print("🔤 Tokenizing dataset")
    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer, model_config["context_length"]),
        batched=True,
        remove_columns=dataset.column_names,
    )
    
    # Split into train/eval
    split_dataset = tokenized_dataset.train_test_split(test_size=0.1)
    train_dataset = split_dataset["train"]
    eval_dataset = split_dataset["test"]
    
    print(f"📈 Training samples: {len(train_dataset)}, Eval samples: {len(eval_dataset)}")
    
    # Training arguments
    batch_size = 2 if quick_start else model_config["batch_size"]
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=1 if quick_start else epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        gradient_accumulation_steps=config.TRAINING_CONFIG["gradient_accumulation_steps"],
        learning_rate=model_config["learning_rate"],
        warmup_steps=config.TRAINING_CONFIG["warmup_steps"] if not quick_start else 10,
        logging_steps=config.TRAINING_CONFIG["logging_steps"],
        eval_steps=config.TRAINING_CONFIG["eval_steps"] if not quick_start else 50,
        save_steps=config.TRAINING_CONFIG["save_steps"] if not quick_start else 100,
        save_total_limit=2,
        fp16=torch.cuda.is_available(),
        eval_strategy="steps",  # Updated from evaluation_strategy
        load_best_model_at_end=True,
        push_to_hub=False,
        report_to="none",  # Change to "wandb" if you want experiment tracking
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )
    
    # Train!
    print("🏋️ Starting training...")
    trainer.train()
    
    # Save final model
    print(f"💾 Saving model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save config info
    with open(output_dir / "training_info.json", "w") as f:
        json.dump({
            "base_model": base_model_name,
            "model_name": model_name,
            "use_lora": use_lora or model_config.get("use_lora", False),
            "epochs": epochs,
            "training_samples": len(train_dataset),
        }, f, indent=2)
    
    print("✅ Training complete!")
    print(f"📁 Model saved to: {output_dir}")
    
    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train ad design generation model")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt2",
        choices=list(config.MODEL_CONFIGS.keys()),
        help="Base model to fine-tune",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory for fine-tuned model",
    )
    parser.add_argument(
        "--use-lora",
        action="store_true",
        help="Use LoRA for efficient fine-tuning",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Number of training epochs",
    )
    parser.add_argument(
        "--quick-start",
        action="store_true",
        help="Use minimal settings for quick testing",
    )
    
    args = parser.parse_args()
    
    train_model(
        model_name=args.model,
        output_dir=args.output_dir,
        use_lora=args.use_lora,
        epochs=args.epochs,
        quick_start=args.quick_start,
    )
