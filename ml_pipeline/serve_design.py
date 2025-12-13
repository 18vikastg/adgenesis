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
    Generate a complete design blueprint.
    Uses model if available, otherwise falls back to rule-based generation.
    """
    
    # Get format dimensions
    format_key = request.format.lower()
    if format_key == "square":
        width, height = 1080, 1080
    elif format_key == "story":
        width, height = 1080, 1920
    elif format_key == "landscape":
        width, height = 1200, 628
    elif format_key == "portrait":
        width, height = 1080, 1350
    elif format_key == "wide":
        width, height = 1920, 1080
    else:
        width, height = 1080, 1080
    
    # Select palette based on tone
    tone = request.tone or "professional"
    palettes = COLOR_PALETTES.get(tone, COLOR_PALETTES["professional"])
    palette = random.choice(palettes)
    
    # Override with brand colors if provided
    if request.brand_colors and len(request.brand_colors) >= 2:
        palette["primary"] = request.brand_colors[0]
        palette["secondary"] = request.brand_colors[1]
        if len(request.brand_colors) >= 3:
            palette["accent"] = request.brand_colors[2]
    
    # Select layout
    layout_name = random.choice(list(LAYOUTS.keys()))
    layout = LAYOUTS[layout_name]
    
    # Generate content
    headline = generate_headline(request.prompt)
    subheadline = generate_subheadline(request.prompt)
    cta = random.choice(CTA_OPTIONS)
    
    # Font selection
    font = request.brand_fonts[0] if request.brand_fonts else "Inter"
    
    # Font size based on format
    headline_size = 72 if format_key == "square" else (56 if format_key == "story" else 48)
    subheadline_size = 24 if format_key == "square" else 20
    
    # Build elements
    elements = []
    
    # Headline
    hl = layout["headline"]
    elements.append({
        "type": "text",
        "id": "headline_1",
        "content": headline,
        "style": "headline",
        "position": {"x": hl["x"], "y": hl["y"]},
        "size": {"width": hl["w"], "height": hl["h"]},
        "font_family": font,
        "font_size": headline_size,
        "font_weight": 700,
        "color": palette["text_primary"],
        "align": "center" if layout_name == "centered" else "left",
        "line_height": 1.1,
        "letter_spacing": -1
    })
    
    # Subheadline
    sh = layout["subheadline"]
    elements.append({
        "type": "text",
        "id": "subheadline_1",
        "content": subheadline,
        "style": "subheadline",
        "position": {"x": sh["x"], "y": sh["y"]},
        "size": {"width": sh["w"], "height": sh["h"]},
        "font_family": font,
        "font_size": subheadline_size,
        "font_weight": 400,
        "color": palette["text_secondary"],
        "align": "center" if layout_name == "centered" else "left",
        "line_height": 1.4,
        "letter_spacing": 0
    })
    
    # CTA Button
    cta_pos = layout["cta"]
    elements.append({
        "type": "cta_button",
        "id": "cta_1",
        "text": cta,
        "position": {"x": cta_pos["x"], "y": cta_pos["y"]},
        "size": {"width": cta_pos["w"], "height": cta_pos["h"]},
        "background_color": palette["primary"],
        "text_color": "#FFFFFF",
        "font_size": 18,
        "font_weight": 600,
        "corner_radius": random.choice([8, 12, 24, 100]),
        "padding": 16
    })
    
    # Add accent shapes
    accent_shapes = [
        {"type": "circle", "x": 80, "y": 10, "w": 15, "h": 15, "opacity": 0.2},
        {"type": "circle", "x": 5, "y": 75, "w": 20, "h": 20, "opacity": 0.15},
    ]
    
    for i, shape in enumerate(accent_shapes):
        elements.append({
            "type": "shape",
            "id": f"accent_{i}",
            "shape_type": shape["type"],
            "position": {"x": shape["x"], "y": shape["y"]},
            "size": {"width": shape["w"], "height": shape["h"]},
            "fill_color": palette["primary"],
            "stroke_color": None,
            "stroke_width": 0,
            "opacity": shape["opacity"],
            "corner_radius": 0
        })
    
    # Build blueprint
    blueprint = {
        "metadata": {
            "platform": request.platform,
            "format": request.format,
            "width": width,
            "height": height,
            "industry": request.industry,
            "campaign_type": "general",
            "target_audience": "general"
        },
        "headline": headline,
        "subheadline": subheadline,
        "body_text": None,
        "cta_text": cta,
        "background": {
            "type": "background",
            "color": palette["background"],
            "gradient": None,
            "image_placeholder": None
        },
        "color_palette": palette,
        "elements": elements,
        "design_notes": f"Generated {tone} design with {layout_name} layout."
    }
    
    return blueprint

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
    """Load the fine-tuned design model"""
    global model, tokenizer, model_loaded
    
    model_path = Path(model_path)
    
    if not model_path.exists():
        print(f"⚠️ Model path {model_path} not found. Using rule-based generation.")
        return False
    
    try:
        print(f"🔄 Loading model from {model_path}")
        
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
        model_loaded = False
        return False

def generate_with_model(request: DesignRequest) -> Optional[Dict[str, Any]]:
    """Generate design using the trained model"""
    if not model_loaded or model is None:
        return None
    
    prompt_text = f"""You are an AI ad design assistant. Generate a complete design blueprint in JSON format.

Platform: {request.platform}
Format: {request.format}
Industry: {request.industry or 'general'}
Tone: {request.tone or 'professional'}

Prompt: {request.prompt}

Generate the design blueprint JSON:"""
    
    try:
        inputs = tokenizer(prompt_text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )
        
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract JSON
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = text[json_start:json_end]
            return json.loads(json_str)
    
    except Exception as e:
        print(f"Model generation failed: {e}")
    
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

@app.post("/generate", response_model=DesignResponse)
async def generate_design(request: DesignRequest):
    """
    Generate a design blueprint from a prompt.
    Returns both the blueprint and Fabric.js-ready JSON.
    """
    try:
        # Try model first if available
        blueprint = None
        if model_loaded:
            blueprint = generate_with_model(request)
        
        # Fallback to rule-based generation
        if blueprint is None:
            blueprint = generate_design_blueprint(request)
        
        # Convert to Fabric.js format
        fabric_json = blueprint_to_fabric(blueprint)
        
        return DesignResponse(
            success=True,
            blueprint=blueprint,
            fabric_json=fabric_json,
            message="Design generated successfully"
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
