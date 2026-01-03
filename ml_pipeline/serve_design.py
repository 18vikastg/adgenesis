"""
AdGenesis ML Service - Design Blueprint Generation
Serves the fine-tuned model that generates structured JSON design blueprints
"""

import json
import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from peft import PeftModel
from pathlib import Path
from typing import Optional, List, Dict, Any
import random

# Import design schema and templates
from design_schema import (
    DesignBlueprint, 
    blueprint_to_fabric_json,
    FORMAT_SPECS,
    PLATFORM_GUIDELINES,
    EXAMPLE_BLUEPRINT,
)

# Import modern design system
from modern_design_system import (
    MODERN_COLOR_SCHEMES,
    MODERN_LAYOUTS,
    MODERN_FONTS,
    MODERN_HEADLINES,
    MODERN_SUBHEADLINES,
    MODERN_CTAS,
    detect_category,
    generate_modern_decorations
)
from modern_blueprint_generator import generate_modern_design_blueprint

# Import retail design system
from retail_design_system import (
    RetailDesignGenerator,
    Platform,
    DesignTone,
    RETAIL_COLOR_PALETTES,
    PLATFORM_SPECS,
    ComplianceEngine,
    create_protein_bar_creative
)

# =============================================================================
# APP SETUP
# =============================================================================

app = FastAPI(
    title="AdGenesis Design Service",
    version="3.0.0",
    description="AI-powered ad design blueprint generation"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
model = None
tokenizer = None
model_loaded = False

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class DesignRequest(BaseModel):
    """Request to generate a design blueprint"""
    prompt: str = Field(..., description="User's ad description")
    platform: str = Field(default="meta", description="meta, google, linkedin, twitter, tiktok")
    format: str = Field(default="square", description="square, story, landscape, portrait, wide")
    industry: Optional[str] = Field(default=None, description="e-commerce, saas, fitness, etc.")
    tone: Optional[str] = Field(default="professional", description="professional, playful, urgent, etc.")
    brand_colors: Optional[List[str]] = Field(default=None, description="Brand color hex codes")
    brand_fonts: Optional[List[str]] = Field(default=None, description="Brand font names")

class DesignResponse(BaseModel):
    """Generated design blueprint"""
    success: bool
    blueprint: Dict[str, Any]
    fabric_json: Dict[str, Any]
    message: Optional[str] = None

class TemplateListResponse(BaseModel):
    """List of available templates"""
    templates: List[Dict[str, Any]]

class ComplianceCheckRequest(BaseModel):
    """Request to check design compliance"""
    blueprint: Dict[str, Any]
    platform: str

class ComplianceCheckResponse(BaseModel):
    """Compliance check result"""
    compliant: bool
    issues: List[str]
    suggestions: List[str]


class RetailCreativeRequest(BaseModel):
    """Request for retail-focused creative generation"""
    brand_name: str = Field(..., description="Brand name")
    brand_colors: Dict[str, str] = Field(
        default={"primary": "#1E1E2F", "accent": "#F5B700", "secondary": "#FFFFFF"},
        description="Brand color palette with primary, accent, secondary"
    )
    headline: str = Field(..., description="Main headline text")
    subheadline: Optional[str] = Field(default=None, description="Secondary headline")
    cta: str = Field(default="Shop Now", description="Call to action text")
    offer: Optional[str] = Field(default=None, description="Offer text e.g. '20% OFF'")
    trust_signals: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="Trust badges e.g. [{'icon': '🌱', 'text': 'Plant-Based'}]"
    )
    products: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Product information with images"
    )
    platform: str = Field(default="instagram_feed", description="Target platform")
    tone: str = Field(default="bold_fmcg", description="Design tone")
    logo_url: Optional[str] = Field(default=None, description="Logo image URL")


class RetailCreativeResponse(BaseModel):
    """Response with generated retail creative"""
    success: bool
    design: Dict[str, Any]
    variants: Optional[List[Dict[str, Any]]] = None
    all_formats: Optional[Dict[str, Dict[str, Any]]] = None
    compliance: Dict[str, Any]
    message: Optional[str] = None

# =============================================================================
# DESIGN GENERATION (Fallback/Rule-based)
# =============================================================================

# Color palettes organized by tone
COLOR_PALETTES = {
    "professional": [
        {"primary": "#2563EB", "secondary": "#1E40AF", "background": "#0F172A", "text_primary": "#F8FAFC", "text_secondary": "#94A3B8", "accent": "#3B82F6"},
        {"primary": "#0D9488", "secondary": "#115E59", "background": "#042F2E", "text_primary": "#F0FDFA", "text_secondary": "#5EEAD4", "accent": "#14B8A6"},
        {"primary": "#6366F1", "secondary": "#4F46E5", "background": "#0F0F23", "text_primary": "#E0E7FF", "text_secondary": "#A5B4FC", "accent": "#818CF8"},
    ],
    "playful": [
        {"primary": "#EC4899", "secondary": "#F472B6", "background": "#1F1235", "text_primary": "#FEFCE8", "text_secondary": "#FDE68A", "accent": "#FBBF24"},
        {"primary": "#8B5CF6", "secondary": "#A78BFA", "background": "#1E1B4B", "text_primary": "#FFFFFF", "text_secondary": "#C4B5FD", "accent": "#F472B6"},
    ],
    "urgent": [
        {"primary": "#DC2626", "secondary": "#EF4444", "background": "#18181B", "text_primary": "#FFFFFF", "text_secondary": "#FCA5A5", "accent": "#FBBF24"},
        {"primary": "#EA580C", "secondary": "#F97316", "background": "#1C1917", "text_primary": "#FFFBEB", "text_secondary": "#FDBA74", "accent": "#FACC15"},
    ],
    "luxurious": [
        {"primary": "#D4AF37", "secondary": "#B8860B", "background": "#0C0A09", "text_primary": "#FAFAF9", "text_secondary": "#A8A29E", "accent": "#F5D77A"},
        {"primary": "#9333EA", "secondary": "#7C3AED", "background": "#0F0520", "text_primary": "#FAF5FF", "text_secondary": "#C4B5FD", "accent": "#D4AF37"},
    ],
    "minimalist": [
        {"primary": "#18181B", "secondary": "#3F3F46", "background": "#FAFAFA", "text_primary": "#09090B", "text_secondary": "#71717A", "accent": "#18181B"},
        {"primary": "#FFFFFF", "secondary": "#E4E4E7", "background": "#09090B", "text_primary": "#FAFAFA", "text_secondary": "#A1A1AA", "accent": "#FAFAFA"},
    ],
    "bold": [
        {"primary": "#7C3AED", "secondary": "#8B5CF6", "background": "#030712", "text_primary": "#FFFFFF", "text_secondary": "#9CA3AF", "accent": "#06B6D4"},
        {"primary": "#059669", "secondary": "#10B981", "background": "#022C22", "text_primary": "#ECFDF5", "text_secondary": "#6EE7B7", "accent": "#FBBF24"},
    ],
    "friendly": [
        {"primary": "#F59E0B", "secondary": "#FBBF24", "background": "#1F2937", "text_primary": "#FFFFFF", "text_secondary": "#D1D5DB", "accent": "#34D399"},
        {"primary": "#06B6D4", "secondary": "#22D3EE", "background": "#0F172A", "text_primary": "#F0F9FF", "text_secondary": "#7DD3FC", "accent": "#F472B6"},
    ],
}

# Layout templates
LAYOUTS = {
    "centered": {
        "headline": {"x": 10, "y": 30, "w": 80, "h": 15},
        "subheadline": {"x": 15, "y": 50, "w": 70, "h": 10},
        "cta": {"x": 30, "y": 70, "w": 40, "h": 8},
    },
    "left_aligned": {
        "headline": {"x": 8, "y": 25, "w": 55, "h": 18},
        "subheadline": {"x": 8, "y": 48, "w": 50, "h": 10},
        "cta": {"x": 8, "y": 68, "w": 35, "h": 8},
    },
    "hero_top": {
        "headline": {"x": 5, "y": 15, "w": 90, "h": 20},
        "subheadline": {"x": 10, "y": 42, "w": 80, "h": 10},
        "cta": {"x": 25, "y": 72, "w": 50, "h": 10},
    },
    "bottom_focus": {
        "headline": {"x": 8, "y": 55, "w": 84, "h": 12},
        "subheadline": {"x": 12, "y": 70, "w": 76, "h": 8},
        "cta": {"x": 30, "y": 85, "w": 40, "h": 7},
    },
}

# Headlines and CTAs
HEADLINE_TEMPLATES = [
    "{action} Your {noun}",
    "Discover {noun}",
    "Transform Your {noun}",
    "The {adjective} Way to {action}",
    "{adjective} {noun} Awaits",
    "Unlock {noun} Today",
    "Experience {adjective} {noun}",
    "{action} Like Never Before",
]

CTA_OPTIONS = [
    "Shop Now", "Get Started", "Learn More", "Sign Up Free",
    "Try Free", "Download Now", "Explore", "Join Now",
    "Claim Offer", "Book Now", "Start Free Trial", "See More"
]

def extract_keywords(prompt: str) -> Dict[str, str]:
    """Extract keywords from prompt for headline generation"""
    words = prompt.lower().split()
    
    # Default values
    result = {
        "action": random.choice(["Discover", "Transform", "Unlock", "Experience"]),
        "noun": random.choice(["Success", "Growth", "Results", "Potential"]),
        "adjective": random.choice(["Amazing", "Revolutionary", "Powerful", "Smart"]),
    }
    
    # Industry-specific keywords
    industry_keywords = {
        "fitness": {"action": "Achieve", "noun": "Fitness Goals", "adjective": "Peak"},
        "ecommerce": {"action": "Shop", "noun": "Deals", "adjective": "Exclusive"},
        "saas": {"action": "Streamline", "noun": "Workflow", "adjective": "Smart"},
        "food": {"action": "Taste", "noun": "Flavors", "adjective": "Delicious"},
        "fashion": {"action": "Elevate", "noun": "Style", "adjective": "Trendy"},
        "tech": {"action": "Experience", "noun": "Innovation", "adjective": "Cutting-Edge"},
        "finance": {"action": "Grow", "noun": "Wealth", "adjective": "Secure"},
        "travel": {"action": "Explore", "noun": "Destinations", "adjective": "Dream"},
    }
    
    for industry, keywords in industry_keywords.items():
        if industry in prompt.lower():
            result.update(keywords)
            break
    
    return result

def generate_headline(prompt: str) -> str:
    """Generate a headline from prompt"""
    keywords = extract_keywords(prompt)
    template = random.choice(HEADLINE_TEMPLATES)
    
    headline = template.format(**keywords)
    return headline

def generate_subheadline(prompt: str) -> str:
    """Generate a subheadline"""
    templates = [
        "Your journey starts here",
        "Built for people like you",
        "Join thousands of satisfied customers",
        "Limited time offer",
        "No commitment required",
        "See the difference today",
    ]
    return random.choice(templates)

def generate_design_blueprint(request: DesignRequest) -> Dict[str, Any]:
    """
    Generate a complete MODERN design blueprint.
    Creates professional advertising-quality posters.
    """
    return generate_modern_design_blueprint(
        request, 
        MODERN_COLOR_SCHEMES, 
        MODERN_LAYOUTS,
        MODERN_HEADLINES, 
        MODERN_SUBHEADLINES, 
        MODERN_CTAS,
        MODERN_FONTS, 
        detect_category
    )

def blueprint_to_fabric(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """Convert blueprint to Fabric.js JSON format"""
    
    width = blueprint["metadata"]["width"]
    height = blueprint["metadata"]["height"]
    
    fabric_objects = []
    
    # Background
    bg_color = blueprint.get("background", {}).get("color", "#1a1a2e")
    fabric_objects.append({
        "type": "rect",
        "left": 0,
        "top": 0,
        "width": width,
        "height": height,
        "fill": bg_color,
        "selectable": False,
        "evented": False,
    })
    
    # Convert elements
    for element in blueprint.get("elements", []):
        pos = element.get("position", {"x": 0, "y": 0})
        size = element.get("size", {"width": 50, "height": 10})
        
        left = (pos["x"] / 100) * width
        top = (pos["y"] / 100) * height
        el_width = (size["width"] / 100) * width
        el_height = (size["height"] / 100) * height
        
        if element["type"] == "text":
            fabric_objects.append({
                "type": "textbox",
                "id": element.get("id", "text"),
                "left": left,
                "top": top,
                "width": el_width,
                "text": element.get("content", ""),
                "fontSize": element.get("font_size", 48),
                "fontFamily": element.get("font_family", "Inter"),
                "fontWeight": element.get("font_weight", 400),
                "fill": element.get("color", "#ffffff"),
                "textAlign": element.get("align", "center"),
                "lineHeight": element.get("line_height", 1.2),
                "charSpacing": element.get("letter_spacing", 0) * 10,
            })
        
        elif element["type"] == "shape":
            shape_obj = {
                "id": element.get("id", "shape"),
                "left": left,
                "top": top,
                "width": el_width,
                "height": el_height,
                "fill": element.get("fill_color", "#8B5CF6"),
                "opacity": element.get("opacity", 1),
            }
            
            if element.get("shape_type") == "circle":
                shape_obj["type"] = "circle"
                shape_obj["radius"] = min(el_width, el_height) / 2
            else:
                shape_obj["type"] = "rect"
                shape_obj["rx"] = element.get("corner_radius", 0)
                shape_obj["ry"] = element.get("corner_radius", 0)
            
            fabric_objects.append(shape_obj)
        
        elif element["type"] == "cta_button":
            # Button background
            fabric_objects.append({
                "type": "rect",
                "id": f"{element.get('id', 'cta')}_bg",
                "left": left,
                "top": top,
                "width": el_width,
                "height": el_height,
                "fill": element.get("background_color", "#8B5CF6"),
                "rx": element.get("corner_radius", 8),
                "ry": element.get("corner_radius", 8),
            })
            
            # Button text
            fabric_objects.append({
                "type": "textbox",
                "id": f"{element.get('id', 'cta')}_text",
                "left": left,
                "top": top + (el_height - element.get("font_size", 16)) / 2,
                "width": el_width,
                "text": element.get("text", "Click"),
                "fontSize": element.get("font_size", 16),
                "fontWeight": element.get("font_weight", 600),
                "fill": element.get("text_color", "#ffffff"),
                "textAlign": "center",
            })
    
    return {
        "version": "5.3.0",
        "objects": fabric_objects,
        "background": bg_color,
    }

# =============================================================================
# MODEL LOADING
# =============================================================================

def load_model(model_path: str):
    """Load the fine-tuned design model (supports both full models and LoRA adapters)"""
    global model, tokenizer, model_loaded
    
    model_path = Path(model_path)
    
    if not model_path.exists():
        print(f"⚠️ Model path {model_path} not found. Using rule-based generation.")
        return False
    
    try:
        print(f"🔄 Loading model from {model_path}")
        
        # Check if this is a LoRA adapter
        adapter_config_path = model_path / "adapter_config.json"
        is_lora_adapter = adapter_config_path.exists()
        
        if is_lora_adapter:
            print("📎 Detected LoRA adapter, loading with PEFT...")
            import json
            with open(adapter_config_path) as f:
                adapter_config = json.load(f)
            
            base_model_name = adapter_config.get("base_model_name_or_path", "gpt2-medium")
            print(f"   Base model: {base_model_name}")
            
            # Load tokenizer from adapter path
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            # Load base model
            print(f"   Loading base model {base_model_name}...")
            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
            )
            
            # Load LoRA adapter
            print(f"   Loading LoRA adapter...")
            model = PeftModel.from_pretrained(base_model, model_path)
            model = model.merge_and_unload()  # Merge for faster inference
            print("   ✅ LoRA adapter merged with base model")
        else:
            # Regular model loading
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
            )
        
        model.eval()
        model_loaded = True
        print("✅ Model loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        import traceback
        traceback.print_exc()
        model_loaded = False
        return False

def fix_json_string(json_str: str) -> str:
    """Fix common JSON issues from model output"""
    import re
    
    # Remove control characters
    json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_str)
    
    # Fix trailing commas before } or ]
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    # Fix missing quotes around keys (if word followed by colon without quotes)
    json_str = re.sub(r'(\{|,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)
    
    # Fix single quotes to double quotes
    json_str = json_str.replace("'", '"')
    
    # Fix escaped newlines in strings
    json_str = json_str.replace('\\n', ' ')
    
    return json_str

def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Extract valid JSON from model output using multiple strategies"""
    import re
    
    # Debug: print first 500 chars of output to understand structure
    print(f"📄 Raw model output preview: {text[:500]}...")
    
    # Strategy 1: Find balanced braces
    json_start = text.find('{')
    if json_start == -1:
        print("❌ No opening brace found in output")
        return None
    
    depth = 0
    best_json = None
    for i, char in enumerate(text[json_start:], json_start):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                json_str = text[json_start:i+1]
                print(f"📋 Found potential JSON ({len(json_str)} chars)")
                try:
                    # Try direct parsing
                    result = json.loads(json_str)
                    print("✅ Direct JSON parse succeeded!")
                    return result
                except json.JSONDecodeError as e:
                    print(f"⚠️ Direct parse failed: {e}")
                    # Try with fixes
                    fixed = fix_json_string(json_str)
                    try:
                        result = json.loads(fixed)
                        print("✅ Fixed JSON parse succeeded!")
                        return result
                    except json.JSONDecodeError as e2:
                        print(f"⚠️ Fixed parse also failed: {e2}")
                        # Store the best attempt
                        if best_json is None:
                            best_json = json_str
                # Continue looking for another valid JSON
    
    # Strategy 2: Try to build a minimal valid design from partial output
    if best_json:
        print(f"🔧 Attempting to salvage partial JSON...")
        # Try to extract key-value pairs manually
        try:
            # Extract headline if present
            headline_match = re.search(r'"headline"\s*:\s*"([^"]*)"', text)
            background_match = re.search(r'"background"\s*:\s*"([^"]*)"', text)
            
            if headline_match:
                salvaged = {
                    "headline": headline_match.group(1),
                    "background": background_match.group(1) if background_match else "#1a1a2e",
                    "elements": []
                }
                print(f"✅ Salvaged basic design from partial output")
                return salvaged
        except Exception as e:
            print(f"❌ Salvage failed: {e}")
    
    # Strategy 3: Try regex patterns for known structures
    patterns = [
        r'\{[^{}]*"elements"\s*:\s*\[[^\]]*\][^{}]*\}',
        r'\{[^{}]*"objects"\s*:\s*\[[^\]]*\][^{}]*\}',
        r'\{[^{}]*"headline"\s*:[^{}]*\}',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                result = json.loads(fix_json_string(match))
                print(f"✅ Pattern match succeeded!")
                return result
            except:
                continue
    
    print("❌ All extraction strategies failed")
    return None


def generate_with_model(request: DesignRequest) -> Optional[Dict[str, Any]]:
    """Generate design using the trained model"""
    if not model_loaded or model is None:
        print("⚠️ Model not loaded, skipping model generation")
        return None
    
    prompt_text = f"""You are an AI ad design assistant. Generate a complete design blueprint in JSON format.

Platform: {request.platform}
Format: {request.format}
Industry: {request.industry or 'general'}
Tone: {request.tone or 'professional'}

Prompt: {request.prompt}

Generate the design blueprint JSON:"""
    
    try:
        print(f"🧠 Attempting model generation for: {request.prompt[:50]}...")
        inputs = tokenizer(prompt_text, return_tensors="pt", truncation=True, max_length=256)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=500,  # Slightly increased for better JSON completion
                temperature=0.6,     # Lowered for more coherent output
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                use_cache=True,
            )
        
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"📝 Model raw output length: {len(text)} chars")
        
        # Use improved JSON extraction
        result = extract_json_from_text(text)
        
        if result:
            print(f"✅ Model generated valid design JSON!")
            return result
        
        print(f"⚠️ Could not extract valid JSON from model output")
        return None
    
    except Exception as e:
        print(f"❌ Model generation failed: {e}")
        import traceback
        traceback.print_exc()
    
    return None

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    return {
        "service": "AdGenesis Design Service",
        "version": "3.0.0",
        "model_loaded": model_loaded,
        "endpoints": [
            "/generate - Generate design blueprint",
            "/templates - Get template gallery",
            "/compliance - Check design compliance",
            "/health - Health check"
        ]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model_loaded,
        "gpu_available": torch.cuda.is_available()
    }


@app.get("/model-info")
async def model_info():
    """Get information about the loaded model"""
    if model_loaded and model is not None:
        return {
            "model_loaded": True,
            "model_type": "fine_tuned_lora" if hasattr(model, 'peft_config') else "full_model",
            "base_model": "gpt2-medium",
            "device": str(model.device) if hasattr(model, 'device') else "cpu",
            "inference_ready": True,
            "message": "Trained model is loaded and ready for inference"
        }
    else:
        return {
            "model_loaded": False,
            "model_type": None,
            "inference_ready": False,
            "message": "No model loaded. Using rule-based generation as fallback."
        }

@app.post("/generate", response_model=DesignResponse)
async def generate_design(request: DesignRequest):
    """
    Generate a design blueprint from a prompt.
    Returns both the blueprint and Fabric.js-ready JSON.
    """
    try:
        # Try model first if available
        blueprint = None
        generation_method = "rule_based"
        
        if model_loaded:
            blueprint = generate_with_model(request)
            if blueprint is not None:
                generation_method = "trained_model"
        
        # Fallback to rule-based generation
        if blueprint is None:
            print(f"\n🎨 Generating MODERN design for: {request.prompt}")
            blueprint = generate_design_blueprint(request)
            generation_method = "rule_based"
        
        # Convert to Fabric.js format
        fabric_json = blueprint_to_fabric(blueprint)
        
        # Add generation metadata
        blueprint["_generation_info"] = {
            "method": generation_method,
            "model_loaded": model_loaded,
            "timestamp": str(Path(".")),  # Will be replaced with actual timestamp
        }
        
        # Log which method was used
        if generation_method == "trained_model":
            print(f"✅ Design generated using TRAINED MODEL")
        else:
            print(f"📋 Design generated using RULE-BASED SYSTEM (fallback)")
        
        return DesignResponse(
            success=True,
            blueprint=blueprint,
            fabric_json=fabric_json,
            message=f"Design generated successfully using {generation_method}"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates", response_model=TemplateListResponse)
async def get_templates():
    """Get list of available design templates"""
    
    templates = [
        {
            "id": "modern_product",
            "name": "Modern Product Launch",
            "category": "e-commerce",
            "thumbnail": "/templates/modern_product.png",
            "formats": ["square", "story", "landscape"]
        },
        {
            "id": "tech_promo",
            "name": "Tech Startup Promo",
            "category": "saas",
            "thumbnail": "/templates/tech_promo.png",
            "formats": ["square", "landscape"]
        },
        {
            "id": "flash_sale",
            "name": "Flash Sale",
            "category": "retail",
            "thumbnail": "/templates/flash_sale.png",
            "formats": ["square", "story"]
        },
        {
            "id": "fitness_motivation",
            "name": "Fitness Motivation",
            "category": "fitness",
            "thumbnail": "/templates/fitness.png",
            "formats": ["square", "story", "portrait"]
        },
        {
            "id": "minimalist_brand",
            "name": "Minimalist Brand",
            "category": "brand_awareness",
            "thumbnail": "/templates/minimalist.png",
            "formats": ["square", "landscape", "wide"]
        },
    ]
    
    return TemplateListResponse(templates=templates)

@app.post("/compliance", response_model=ComplianceCheckResponse)
async def check_compliance(request: ComplianceCheckRequest):
    """Check if a design complies with platform guidelines"""
    
    platform = request.platform.lower()
    blueprint = request.blueprint
    
    issues = []
    suggestions = []
    
    # Get platform guidelines
    guidelines = PLATFORM_GUIDELINES.get(platform, {})
    
    # Check text ratio (simplified)
    text_elements = [e for e in blueprint.get("elements", []) if e.get("type") == "text"]
    total_text_area = sum(
        (e.get("size", {}).get("width", 0) * e.get("size", {}).get("height", 0))
        for e in text_elements
    )
    
    max_ratio = guidelines.get("text_ratio_limit", 0.25)
    if total_text_area > (100 * 100 * max_ratio):  # Simplified calculation
        issues.append(f"Text may exceed {platform}'s recommended limit")
        suggestions.append("Consider reducing text size or removing some text elements")
    
    # Check for forbidden words
    forbidden = guidelines.get("forbidden_words", [])
    all_text = " ".join([
        e.get("content", "") for e in text_elements
    ]).lower()
    
    for word in forbidden:
        if word.lower() in all_text:
            issues.append(f"Contains potentially restricted word: '{word}'")
            suggestions.append(f"Consider replacing '{word}' with alternative phrasing")
    
    # Check color contrast (simplified)
    # In a real implementation, you'd calculate WCAG contrast ratios
    
    return ComplianceCheckResponse(
        compliant=len(issues) == 0,
        issues=issues,
        suggestions=suggestions if issues else ["Design looks compliant!"]
    )

@app.post("/refine")
async def refine_design(
    blueprint: Dict[str, Any],
    instruction: str,
):
    """Refine an existing design based on user feedback"""
    
    # This would use the model to modify the design
    # For now, return the same design with a note
    
    return {
        "success": True,
        "blueprint": blueprint,
        "message": f"Refinement noted: {instruction}. Model refinement coming soon."
    }


# =============================================================================
# RETAIL DESIGN ENDPOINTS
# =============================================================================

@app.post("/retail/generate", response_model=RetailCreativeResponse)
async def generate_retail_creative(request: RetailCreativeRequest):
    """
    Generate agency-grade retail creative for D2C, FMCG, and e-commerce.
    Returns design with variants and multi-platform formats.
    """
    try:
        generator = RetailDesignGenerator()
        
        # Map string platform to enum
        platform_map = {
            "instagram_feed": Platform.INSTAGRAM_FEED,
            "instagram_story": Platform.INSTAGRAM_STORY,
            "facebook_feed": Platform.FACEBOOK_FEED,
            "facebook_story": Platform.FACEBOOK_STORY,
            "amazon_main": Platform.AMAZON_MAIN,
            "amazon_lifestyle": Platform.AMAZON_LIFESTYLE,
            "flipkart_banner": Platform.FLIPKART_BANNER,
            "google_display": Platform.GOOGLE_DISPLAY,
        }
        
        tone_map = {
            "bold_fmcg": DesignTone.BOLD_FMCG,
            "premium_modern": DesignTone.PREMIUM_MODERN,
            "luxury_dark": DesignTone.LUXURY_DARK,
            "clean_retail": DesignTone.CLEAN_RETAIL,
            "vibrant_playful": DesignTone.VIBRANT_PLAYFUL,
            "tech_modern": DesignTone.TECH_MODERN,
            "trust_corporate": DesignTone.TRUST_CORPORATE,
        }
        
        platform = platform_map.get(request.platform, Platform.INSTAGRAM_FEED)
        tone = tone_map.get(request.tone, DesignTone.BOLD_FMCG)
        
        brand_config = {
            "brand_name": request.brand_name,
            "brand_colors": request.brand_colors,
            "logo_url": request.logo_url or ""
        }
        
        content = {
            "headline": request.headline,
            "subheadline": request.subheadline or "",
            "cta": request.cta,
            "offer": request.offer,
            "trust_signals": request.trust_signals or [],
            "products": request.products or [],
            "logo_url": request.logo_url or ""
        }
        
        # Generate primary design
        design = generator.generate_creative(
            brand_config=brand_config,
            content=content,
            platform=platform,
            tone=tone
        )
        
        # Generate variants
        variants = generator.generate_variants(design)
        
        # Generate all formats
        all_formats = generator.generate_all_formats(
            design,
            [Platform.INSTAGRAM_FEED, Platform.INSTAGRAM_STORY, 
             Platform.FACEBOOK_FEED, Platform.AMAZON_LIFESTYLE]
        )
        
        # Convert enum keys to strings for JSON serialization
        all_formats_serializable = {
            str(k.value) if hasattr(k, 'value') else str(k): v 
            for k, v in all_formats.items()
        }
        
        return RetailCreativeResponse(
            success=True,
            design=design,
            variants=variants,
            all_formats=all_formats_serializable,
            compliance=design.get("compliance", {}),
            message="Retail creative generated successfully"
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/retail/palettes")
async def get_retail_palettes():
    """Get available retail color palettes"""
    return {
        "palettes": {
            name: {
                "name": palette["name"],
                "description": palette["description"],
                "preview": {
                    "primary": palette["primary"],
                    "accent": palette["accent"],
                    "background": palette["background"]["css"] if isinstance(palette["background"], dict) else palette["background"]
                }
            }
            for name, palette in RETAIL_COLOR_PALETTES.items()
        }
    }


@app.get("/retail/platforms")
async def get_retail_platforms():
    """Get supported platforms and their specifications"""
    return {
        "platforms": {
            platform.value: {
                "name": spec["name"],
                "dimensions": spec["dimensions"],
                "aspect_ratios": spec["aspect_ratios"],
                "max_file_size_kb": spec["max_file_size_kb"],
            }
            for platform, spec in PLATFORM_SPECS.items()
        }
    }


@app.get("/retail/demo")
async def get_retail_demo():
    """Get demo protein bar creative (as shown in the design brief)"""
    try:
        result = create_protein_bar_creative()
        return {
            "success": True,
            "demo_creative": result,
            "message": "Demo creative for Plant-Based Protein Bar campaign"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/retail/compliance-check")
async def check_retail_compliance(
    design: Dict[str, Any],
    platform: str
):
    """Run AI compliance check on a retail design"""
    try:
        platform_map = {
            "instagram_feed": Platform.INSTAGRAM_FEED,
            "instagram_story": Platform.INSTAGRAM_STORY,
            "facebook_feed": Platform.FACEBOOK_FEED,
            "amazon_main": Platform.AMAZON_MAIN,
            "amazon_lifestyle": Platform.AMAZON_LIFESTYLE,
            "flipkart_banner": Platform.FLIPKART_BANNER,
        }
        
        platform_enum = platform_map.get(platform, Platform.INSTAGRAM_FEED)
        
        compliance_engine = ComplianceEngine()
        result = compliance_engine.check_design(design, platform_enum)
        
        return {
            "success": True,
            "compliance": result,
            "is_compliant": result["summary"]["is_compliant"],
            "message": "Compliance check completed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/retail/auto-fix")
async def auto_fix_retail_design(
    design: Dict[str, Any],
    platform: str
):
    """Apply AI auto-fixes to resolve compliance issues"""
    try:
        platform_map = {
            "instagram_feed": Platform.INSTAGRAM_FEED,
            "instagram_story": Platform.INSTAGRAM_STORY,
            "facebook_feed": Platform.FACEBOOK_FEED,
            "amazon_main": Platform.AMAZON_MAIN,
        }
        
        platform_enum = platform_map.get(platform, Platform.INSTAGRAM_FEED)
        
        compliance_engine = ComplianceEngine()
        result = compliance_engine.auto_fix_all(design, platform_enum)
        
        return {
            "success": True,
            "fixed_design": result["design"],
            "fixes_applied": result["fixes_applied"],
            "remaining_issues": result["remaining_issues"],
            "message": f"Applied {len(result['fixes_applied'])} auto-fixes"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# DESIGN STORAGE ENDPOINTS
# =============================================================================

import os
from datetime import datetime
import base64

# Storage directory for generated designs
DESIGNS_DIR = Path("generated_designs")
DESIGNS_DIR.mkdir(exist_ok=True)


@app.post("/save-design")
async def save_design(
    design_id: str,
    design_data: Dict[str, Any],
    image_data: Optional[str] = None  # Base64 encoded image
):
    """Save a generated design to storage"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save design JSON
        design_path = DESIGNS_DIR / f"{design_id}_{timestamp}.json"
        with open(design_path, "w") as f:
            json.dump(design_data, f, indent=2, default=str)
        
        image_path = None
        
        # Save image if provided
        if image_data:
            # Remove data URL prefix if present
            if image_data.startswith("data:image"):
                image_data = image_data.split(",")[1]
            
            image_bytes = base64.b64decode(image_data)
            image_path = DESIGNS_DIR / f"{design_id}_{timestamp}.png"
            with open(image_path, "wb") as f:
                f.write(image_bytes)
        
        return {
            "success": True,
            "design_id": design_id,
            "design_path": str(design_path),
            "image_path": str(image_path) if image_path else None,
            "timestamp": timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/saved-designs")
async def list_saved_designs():
    """List all saved designs"""
    try:
        designs = []
        for file in DESIGNS_DIR.glob("*.json"):
            with open(file, "r") as f:
                design = json.load(f)
                designs.append({
                    "filename": file.name,
                    "design_id": file.stem.split("_")[0],
                    "created": file.stat().st_mtime,
                    "has_image": (file.with_suffix(".png")).exists()
                })
        
        return {
            "success": True,
            "count": len(designs),
            "designs": sorted(designs, key=lambda x: x["created"], reverse=True)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generation-status")
async def generation_status():
    """Get current status of design generation capabilities"""
    return {
        "service": "AdGenesis ML Design Service",
        "version": "3.0.0",
        "capabilities": {
            "trained_model": {
                "available": model_loaded,
                "model_type": "GPT-2 Medium with LoRA fine-tuning",
                "status": "active" if model_loaded else "not_loaded"
            },
            "rule_based": {
                "available": True,
                "status": "active (fallback)"
            },
            "retail_system": {
                "available": True,
                "palettes": len(RETAIL_COLOR_PALETTES),
                "platforms": len(PLATFORM_SPECS)
            }
        },
        "generation_priority": [
            "1. Trained ML Model (if loaded and generates valid output)",
            "2. Rule-Based Modern Design System (fallback)"
        ],
        "storage": {
            "directory": str(DESIGNS_DIR),
            "saved_designs": len(list(DESIGNS_DIR.glob("*.json")))
        }
    }

# =============================================================================
# STARTUP
# =============================================================================

@app.on_event("startup")
async def startup():
    """Load model on startup"""
    # Try to load the design model
    model_paths = [
        "models/fine_tuned/design_model",
        "models/fine_tuned/gpt2",
    ]
    
    for path in model_paths:
        if Path(path).exists():
            if load_model(path):
                break
    
    if not model_loaded:
        print("⚠️ No model loaded. Using rule-based generation.")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="models/fine_tuned/design_model")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--host", type=str, default="0.0.0.0")
    args = parser.parse_args()
    
    # Load model
    load_model(args.model_path)
    
    # Run server
    uvicorn.run(app, host=args.host, port=args.port)
