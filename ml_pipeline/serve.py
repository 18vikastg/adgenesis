"""
FastAPI server for model inference
"""
import json
import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from peft import PeftModel
import config
from pathlib import Path
import argparse


app = FastAPI(title="ADGENESIS ML Model Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global model and tokenizer
model = None
tokenizer = None
generation_config = None


class DesignRequest(BaseModel):
    prompt: str
    platform: str
    format: str


class DesignResponse(BaseModel):
    background_color: str
    elements: list
    layout: dict = {}


def generate_fallback_design(prompt: str, platform: str, format: str, specs: dict) -> dict:
    """Generate a professional-looking design when ML model fails"""
    import hashlib
    import re
    
    # Extract keywords from prompt
    words = re.findall(r'\w+', prompt.lower())
    keywords = [w for w in words if len(w) > 3][:3]
    
    # Color schemes based on keywords
    color_schemes = {
        "tech": {"bg": "#1a1a2e", "primary": "#3b82f6", "text": "#ffffff", "accent": "#60a5fa"},
        "fashion": {"bg": "#ff6b9d", "primary": "#ffe66d", "text": "#ffffff", "accent": "#ff1744"},
        "sale": {"bg": "#dc2626", "primary": "#fbbf24", "text": "#ffffff", "accent": "#000000"},
        "food": {"bg": "#fef3c7", "primary": "#ef4444", "text": "#78350f", "accent": "#92400e"},
        "business": {"bg": "#0a66c2", "primary": "#ffffff", "text": "#ffffff", "accent": "#94a3b8"},
        "default": {"bg": "#ffffff", "primary": "#3b82f6", "text": "#000000", "accent": "#6b7280"},
    }
    
    # Select color scheme
    scheme = color_schemes["default"]
    for keyword in keywords:
        if keyword in color_schemes:
            scheme = color_schemes[keyword]
            break
    
    # Create headline (first 40 chars or first sentence)
    headline = prompt[:40] if len(prompt) <= 40 else prompt.split('.')[0][:40]
    
    # Build design elements
    elements = []
    width = specs.get("width", 1080)
    height = specs.get("height", 1080)
    
    # Add main headline
    elements.append({
        "type": "text",
        "text": headline.upper() if "sale" in keywords else headline.title(),
        "x": width * 0.1,
        "y": height * 0.25,
        "fontSize": 64 if width > 800 else 48,
        "color": scheme["text"],
        "fontFamily": "Arial Black" if "sale" in keywords else "Arial",
        "fontWeight": "bold"
    })
    
    # Add subtext
    subtext = f"Powered by AI • {platform.title()}"
    elements.append({
        "type": "text",
        "text": subtext,
        "x": width * 0.1,
        "y": height * 0.45,
        "fontSize": 24,
        "color": scheme["accent"],
        "fontFamily": "Arial"
    })
    
    # Add CTA button
    elements.append({
        "type": "rectangle",
        "x": width * 0.1,
        "y": height * 0.65,
        "width": 300,
        "height": 70,
        "color": scheme["primary"],
        "borderRadius": 8
    })
    
    elements.append({
        "type": "text",
        "text": "Learn More" if "business" in keywords else "Shop Now",
        "x": width * 0.1 + 80,
        "y": height * 0.65 + 22,
        "fontSize": 24,
        "color": scheme["bg"] if scheme["bg"] != "#ffffff" else "#000000",
        "fontFamily": "Arial",
        "fontWeight": "600"
    })
    
    return {
        "background_color": scheme["bg"],
        "elements": elements,
        "layout": {"type": "fallback", "prompt": prompt}
    }


def load_model(model_path: str, use_lora: bool = False):
    """Load the fine-tuned model"""
    global model, tokenizer, generation_config
    
    print(f"🔄 Loading model from {model_path}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model
    if use_lora:
        print("📦 Loading LoRA model")
        # Load base model first
        training_info_path = Path(model_path) / "training_info.json"
        if training_info_path.exists():
            with open(training_info_path) as f:
                info = json.load(f)
                base_model_name = info["base_model"]
        else:
            raise ValueError("Cannot determine base model for LoRA. training_info.json not found.")
        
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        model = PeftModel.from_pretrained(base_model, model_path)
        model = model.merge_and_unload()  # Merge LoRA weights
    else:
        print("📦 Loading full model")
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
        )
    
    model.eval()
    
    # Generation config
    generation_config = GenerationConfig(
        max_new_tokens=config.INFERENCE_CONFIG["max_new_tokens"],
        temperature=config.INFERENCE_CONFIG["temperature"],
        top_p=config.INFERENCE_CONFIG["top_p"],
        top_k=config.INFERENCE_CONFIG["top_k"],
        repetition_penalty=config.INFERENCE_CONFIG["repetition_penalty"],
        do_sample=config.INFERENCE_CONFIG["do_sample"],
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    
    print("✅ Model loaded successfully")


def generate_design_spec(prompt: str, platform: str, format: str) -> dict:
    """Generate design specification using the model"""
    if model is None or tokenizer is None:
        raise RuntimeError("Model not loaded. Call load_model() first.")
    
    # Get platform specs
    specs = config.PLATFORM_SPECS.get(platform, {}).get(format, {"width": 1080, "height": 1080})
    
    # Create instruction - SIMPLIFIED for better GPT-2 results
    instruction = f"""Design a {platform} ad in {format} format.
Prompt: {prompt}
Size: {specs['width']}x{specs['height']}

JSON output:"""
    
    # Format as training format
    input_text = f"{instruction}\n"
    
    # Tokenize
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    # Generate with stricter parameters for better JSON
    generation_config_local = GenerationConfig(
        max_new_tokens=256,  # Shorter for better control
        temperature=0.3,      # Lower for more deterministic
        top_p=0.9,
        top_k=40,
        repetition_penalty=1.2,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    
    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            generation_config=generation_config_local,
        )
    
    # Decode
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract JSON from response
    try:
        # Look for JSON patterns
        json_start = generated_text.find("{")
        json_end = generated_text.rfind("}") + 1
        
        if json_start != -1 and json_end > json_start:
            json_text = generated_text[json_start:json_end]
            design_spec = json.loads(json_text)
            
            # Ensure required fields
            if "background_color" not in design_spec:
                design_spec["background_color"] = "#ffffff"
            if "elements" not in design_spec:
                design_spec["elements"] = []
            
            return design_spec
    
    except (json.JSONDecodeError, ValueError) as e:
        print(f"❌ Failed to parse JSON: {e}")
        print(f"Generated text: {generated_text[:500]}")
    
    # FALLBACK: Generate a proper design programmatically
    print("📝 Using fallback design generation")
    return generate_fallback_design(prompt, platform, format, specs)


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "healthy",
        "service": "ADGENESIS ML Model",
        "model_loaded": model is not None,
    }


@app.post("/generate", response_model=DesignResponse)
async def generate_design(request: DesignRequest):
    """
    Generate ad design specification
    
    Args:
        request: DesignRequest with prompt, platform, format
    
    Returns:
        DesignResponse with background_color, elements, layout
    """
    try:
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        design_spec = generate_design_spec(
            prompt=request.prompt,
            platform=request.platform,
            format=request.format,
        )
        
        return DesignResponse(**design_spec)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.get("/models")
async def list_models():
    """List available models"""
    models = []
    for model_dir in config.FINE_TUNED_DIR.iterdir():
        if model_dir.is_dir():
            info_file = model_dir / "training_info.json"
            if info_file.exists():
                with open(info_file) as f:
                    info = json.load(f)
                models.append({
                    "name": model_dir.name,
                    "path": str(model_dir),
                    **info,
                })
    return {"models": models}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start ML model inference server")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt2",
        help="Model name or path to load",
    )
    parser.add_argument(
        "--use-lora",
        action="store_true",
        help="Model uses LoRA",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=config.SERVER_CONFIG["host"],
        help="Server host",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=config.SERVER_CONFIG["port"],
        help="Server port",
    )
    
    args = parser.parse_args()
    
    # Load model
    model_path = Path(args.model)
    if not model_path.exists():
        # Try finding in fine_tuned directory
        model_path = config.FINE_TUNED_DIR / args.model
        if not model_path.exists():
            raise ValueError(f"Model not found: {args.model}")
    
    load_model(str(model_path), use_lora=args.use_lora)
    
    # Start server
    import uvicorn
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        workers=config.SERVER_CONFIG["workers"],
        timeout_keep_alive=config.SERVER_CONFIG["timeout"],
    )
