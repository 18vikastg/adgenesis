"""
PREMIUM GRAPHIC DESIGN GENERATOR for AdGenesis
Creates agency-quality, visually stunning poster designs with rich graphics
"""

import random
from typing import Dict, List, Any, Optional
import re
import math

# =============================================================================
# PREMIUM COLOR PALETTES - Rich & Vibrant
# =============================================================================

PREMIUM_PALETTES = {
    "coffee_premium": {
        "name": "Premium Coffee",
        "bg_gradient": ["#1A0F0A", "#3D2314", "#5C3D2E"],
        "accent1": "#D4A574",
        "accent2": "#E8C4A0", 
        "accent3": "#F5DEB3",
        "highlight": "#FFD700",
        "text_light": "#FFF8F0",
        "text_dark": "#1A0F0A",
        "glow": "#D4A574",
        "shapes": ["#8B5E34", "#A67B5B", "#C49A6C"],
    },
    "tech_neon": {
        "name": "Tech Neon",
        "bg_gradient": ["#0A0A1A", "#0F0F2D", "#1A1A3E"],
        "accent1": "#00F5FF",
        "accent2": "#8B5CF6",
        "accent3": "#FF10F0",
        "highlight": "#39FF14",
        "text_light": "#FFFFFF",
        "text_dark": "#0A0A1A",
        "glow": "#00F5FF",
        "shapes": ["#6366F1", "#8B5CF6", "#A78BFA"],
    },
    "fashion_luxury": {
        "name": "Luxury Fashion",
        "bg_gradient": ["#0D0D0D", "#1A1A1A", "#262626"],
        "accent1": "#D4AF37",
        "accent2": "#FFD700",
        "accent3": "#F5E6A3",
        "highlight": "#FFFFFF",
        "text_light": "#FFFFFF",
        "text_dark": "#0D0D0D",
        "glow": "#D4AF37",
        "shapes": ["#8B7355", "#A08C5B", "#B5A167"],
    },
    "food_vibrant": {
        "name": "Vibrant Food",
        "bg_gradient": ["#7C2D12", "#9A3412", "#C2410C"],
        "accent1": "#FED7AA",
        "accent2": "#FDBA74",
        "accent3": "#FB923C",
        "highlight": "#FBBF24",
        "text_light": "#FFF7ED",
        "text_dark": "#431407",
        "glow": "#FB923C",
        "shapes": ["#EA580C", "#F97316", "#FB923C"],
    },
    "fitness_power": {
        "name": "Power Fitness",
        "bg_gradient": ["#0F0F0F", "#1A1A1A", "#262626"],
        "accent1": "#EF4444",
        "accent2": "#F97316",
        "accent3": "#FACC15",
        "highlight": "#22C55E",
        "text_light": "#FFFFFF",
        "text_dark": "#0F0F0F",
        "glow": "#EF4444",
        "shapes": ["#DC2626", "#EF4444", "#F87171"],
    },
    "beauty_glow": {
        "name": "Beauty Glow",
        "bg_gradient": ["#4A1942", "#6B2158", "#831843"],
        "accent1": "#F9A8D4",
        "accent2": "#F472B6",
        "accent3": "#EC4899",
        "highlight": "#FDF4FF",
        "text_light": "#FDF2F8",
        "text_dark": "#4A1942",
        "glow": "#F472B6",
        "shapes": ["#BE185D", "#DB2777", "#EC4899"],
    },
    "travel_sunset": {
        "name": "Sunset Travel",
        "bg_gradient": ["#0C4A6E", "#0369A1", "#0284C7"],
        "accent1": "#38BDF8",
        "accent2": "#7DD3FC",
        "accent3": "#BAE6FD",
        "highlight": "#FDE047",
        "text_light": "#F0F9FF",
        "text_dark": "#0C4A6E",
        "glow": "#38BDF8",
        "shapes": ["#0EA5E9", "#38BDF8", "#7DD3FC"],
    },
    "instagram_gradient": {
        "name": "Instagram Style",
        "bg_gradient": ["#833AB4", "#FD1D1D", "#F77737"],
        "accent1": "#FFFFFF",
        "accent2": "#FCAF45",
        "accent3": "#FFE5B4",
        "highlight": "#FFFFFF",
        "text_light": "#FFFFFF",
        "text_dark": "#262626",
        "glow": "#FCAF45",
        "shapes": ["#E1306C", "#F77737", "#FCAF45"],
    },
    "minimal_elegant": {
        "name": "Minimal Elegant",
        "bg_gradient": ["#FAFAFA", "#F5F5F5", "#E5E5E5"],
        "accent1": "#18181B",
        "accent2": "#3F3F46",
        "accent3": "#71717A",
        "highlight": "#EF4444",
        "text_light": "#FAFAFA",
        "text_dark": "#18181B",
        "glow": "#3F3F46",
        "shapes": ["#27272A", "#3F3F46", "#52525B"],
    },
}

# =============================================================================
# INDUSTRY-SPECIFIC CONTENT
# =============================================================================

INDUSTRY_CONTENT = {
    "coffee": {
        "headlines": [
            "BREW\nPERFECTION",
            "COFFEE\nCULTURE",
            "WAKE UP\nIN STYLE",
            "ARTISAN\nBREWS",
            "TASTE THE\nDIFFERENCE"
        ],
        "subheadlines": [
            "Premium Artisan Coffee",
            "Freshly Roasted Daily",
            "Handcrafted Excellence",
            "Where Coffee is Art"
        ],
        "ctas": ["Order Now", "Visit Us Today", "Try Our Blend", "Get 20% Off"],
        "badges": ["☕ PREMIUM", "★ ARTISAN", "✦ FRESH ROAST"],
        "icons": ["☕", "✦", "★", "●"],
        "palette": "coffee_premium"
    },
    "tech": {
        "headlines": [
            "FUTURE\nIS HERE",
            "NEXT GEN\nTECH",
            "INNOVATE\nTODAY",
            "SMART\nSOLUTIONS",
            "POWER UP"
        ],
        "subheadlines": [
            "Revolutionary Technology",
            "Built for Tomorrow",
            "Experience Innovation",
            "The Smart Choice"
        ],
        "ctas": ["Get Started", "Learn More", "Try Free", "Pre-Order"],
        "badges": ["⚡ NEW", "🚀 FAST", "✦ AI POWERED"],
        "icons": ["⚡", "◆", "▲", "●"],
        "palette": "tech_neon"
    },
    "fashion": {
        "headlines": [
            "DEFINE\nLUXURY",
            "NEW\nCOLLECTION",
            "TIMELESS\nSTYLE",
            "ELEVATE\nYOUR LOOK",
            "PURE\nELEGANCE"
        ],
        "subheadlines": [
            "Exclusive Designer Collection",
            "Luxury Redefined",
            "Where Fashion Meets Art",
            "Curated for Excellence"
        ],
        "ctas": ["Shop Now", "Explore", "View Collection", "Get 30% Off"],
        "badges": ["✦ EXCLUSIVE", "★ LIMITED", "◆ PREMIUM"],
        "icons": ["◆", "✦", "★", "●"],
        "palette": "fashion_luxury"
    },
    "food": {
        "headlines": [
            "TASTE\nPERFECTION",
            "FRESH &\nDELICIOUS",
            "SAVOR\nTHE MOMENT",
            "FLAVOR\nEXPLOSION",
            "CHEF'S\nSPECIAL"
        ],
        "subheadlines": [
            "Fresh Ingredients Daily",
            "Crafted by Master Chefs",
            "Unforgettable Taste",
            "Quality You Can Taste"
        ],
        "ctas": ["Order Now", "View Menu", "Book Table", "Get Delivery"],
        "badges": ["🔥 HOT", "★ FRESH", "✦ SPECIAL"],
        "icons": ["●", "✦", "★", "◆"],
        "palette": "food_vibrant"
    },
    "fitness": {
        "headlines": [
            "UNLEASH\nPOWER",
            "STRONGER\nDAILY",
            "NO LIMITS",
            "TRANSFORM\nNOW",
            "PEAK\nPERFORMANCE"
        ],
        "subheadlines": [
            "Train Like a Champion",
            "Results Guaranteed",
            "Push Your Limits",
            "Your Fitness Journey"
        ],
        "ctas": ["Join Now", "Start Free", "Get Fit", "Sign Up"],
        "badges": ["💪 PRO", "⚡ POWER", "★ #1 RATED"],
        "icons": ["▲", "◆", "●", "★"],
        "palette": "fitness_power"
    },
    "beauty": {
        "headlines": [
            "GLOW\nDIFFERENT",
            "RADIANT\nBEAUTY",
            "PURE\nGLOW",
            "SKIN\nPERFECTION",
            "REVEAL\nYOU"
        ],
        "subheadlines": [
            "Clinically Proven Results",
            "Nature Meets Science",
            "Luxury Skincare",
            "Your Natural Glow"
        ],
        "ctas": ["Shop Now", "Try Free", "Get Yours", "Save 25%"],
        "badges": ["✦ NATURAL", "★ BESTSELLER", "◆ ORGANIC"],
        "icons": ["✦", "◆", "●", "★"],
        "palette": "beauty_glow"
    },
    "travel": {
        "headlines": [
            "EXPLORE\nMORE",
            "ADVENTURE\nAWAITS",
            "DISCOVER\nPARADISE",
            "DREAM\nDESTINATIONS",
            "ESCAPE\nNOW"
        ],
        "subheadlines": [
            "Unforgettable Experiences",
            "Your Perfect Getaway",
            "Create Lasting Memories",
            "Where Dreams Come True"
        ],
        "ctas": ["Book Now", "Explore Deals", "Plan Trip", "Save 40%"],
        "badges": ["✈ DEALS", "★ TOP RATED", "◆ EXCLUSIVE"],
        "icons": ["✦", "◆", "▲", "●"],
        "palette": "travel_sunset"
    },
    "default": {
        "headlines": [
            "DISCOVER\nNEW",
            "EXPERIENCE\nMORE",
            "THE BEST\nCHOICE",
            "QUALITY\nFIRST",
            "START\nTODAY"
        ],
        "subheadlines": [
            "Experience Excellence",
            "Quality You Deserve",
            "Built for You",
            "Your Success, Our Priority"
        ],
        "ctas": ["Get Started", "Learn More", "Shop Now", "Try Free"],
        "badges": ["★ PREMIUM", "✦ TRUSTED", "◆ QUALITY"],
        "icons": ["●", "◆", "✦", "★"],
        "palette": "minimal_elegant"
    }
}

# =============================================================================
# GRAPHIC DESIGN GENERATOR
# =============================================================================

def detect_industry(prompt: str) -> str:
    """Detect industry from prompt"""
    prompt_lower = prompt.lower()
    
    keywords = {
        "coffee": ["coffee", "cafe", "espresso", "latte", "brew", "roast", "barista", "cappuccino"],
        "tech": ["tech", "software", "app", "digital", "ai", "smart", "startup", "saas", "cloud"],
        "fashion": ["fashion", "style", "clothing", "wear", "collection", "luxury", "designer", "boutique"],
        "food": ["food", "restaurant", "delivery", "menu", "taste", "chef", "cuisine", "eat", "delicious"],
        "fitness": ["fitness", "gym", "workout", "training", "health", "exercise", "muscle", "protein", "sports"],
        "beauty": ["beauty", "skincare", "cosmetic", "makeup", "glow", "skin", "cream", "serum", "spa"],
        "travel": ["travel", "vacation", "trip", "destination", "hotel", "flight", "adventure", "explore", "tourism"],
    }
    
    for industry, kw_list in keywords.items():
        for kw in kw_list:
            if kw in prompt_lower:
                return industry
    return "default"

def extract_brand_name(prompt: str) -> Optional[str]:
    """Extract brand name from prompt"""
    patterns = [
        r"(?:named|called|for)\s+([A-Z][a-zA-Z']+(?:\s+[A-Z][a-zA-Z']+)?)",
        r"([A-Z][a-zA-Z']+(?:'s)?)\s+(?:coffee|shop|store|brand)",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def generate_decorative_shapes(palette: Dict, width: int, height: int) -> List[Dict]:
    """Generate decorative graphic elements"""
    shapes = []
    shape_colors = palette["shapes"]
    
    # Large background circles (blur effect simulation)
    shapes.append({
        "type": "shape", "shape_type": "circle",
        "position": {"x": -15, "y": -15},
        "size": {"width": 50, "height": 50},
        "fill_color": palette["glow"],
        "opacity": 0.08,
        "blur": 60,
    })
    shapes.append({
        "type": "shape", "shape_type": "circle",
        "position": {"x": 75, "y": 70},
        "size": {"width": 45, "height": 45},
        "fill_color": palette["accent2"],
        "opacity": 0.1,
        "blur": 50,
    })
    
    # Geometric accent shapes
    shapes.append({
        "type": "shape", "shape_type": "circle",
        "position": {"x": 85, "y": 5},
        "size": {"width": 20, "height": 20},
        "fill_color": palette["accent1"],
        "opacity": 0.25,
    })
    shapes.append({
        "type": "shape", "shape_type": "circle",
        "position": {"x": 5, "y": 80},
        "size": {"width": 15, "height": 15},
        "fill_color": palette["accent2"],
        "opacity": 0.2,
    })
    
    # Small decorative dots
    dot_positions = [(10, 15), (90, 85), (80, 20), (15, 75), (50, 8), (45, 92)]
    for i, (x, y) in enumerate(dot_positions):
        shapes.append({
            "type": "shape", "shape_type": "circle",
            "position": {"x": x, "y": y},
            "size": {"width": 2 + (i % 3), "height": 2 + (i % 3)},
            "fill_color": palette["accent1"] if i % 2 == 0 else palette["highlight"],
            "opacity": 0.4 + (i % 3) * 0.1,
        })
    
    # Accent lines
    shapes.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 8, "y": 25},
        "size": {"width": 0.5, "height": 15},
        "fill_color": palette["accent1"],
        "opacity": 0.6,
    })
    shapes.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 20, "y": 88},
        "size": {"width": 25, "height": 0.4},
        "fill_color": palette["accent1"],
        "opacity": 0.5,
    })
    
    # Corner frame elements
    shapes.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 5, "y": 5},
        "size": {"width": 15, "height": 0.3},
        "fill_color": palette["accent1"],
        "opacity": 0.7,
    })
    shapes.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 5, "y": 5},
        "size": {"width": 0.3, "height": 15},
        "fill_color": palette["accent1"],
        "opacity": 0.7,
    })
    shapes.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 80, "y": 95},
        "size": {"width": 15, "height": 0.3},
        "fill_color": palette["accent1"],
        "opacity": 0.7,
    })
    shapes.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 95, "y": 80},
        "size": {"width": 0.3, "height": 15},
        "fill_color": palette["accent1"],
        "opacity": 0.7,
    })
    
    return shapes

def generate_premium_design(prompt: str, platform: str = "instagram", 
                            format: str = "post") -> Dict[str, Any]:
    """
    Generate a PREMIUM, visually stunning graphic design.
    This creates agency-quality posters with rich visual elements.
    """
    
    # Detect industry
    industry = detect_industry(prompt)
    content = INDUSTRY_CONTENT.get(industry, INDUSTRY_CONTENT["default"])
    
    # Get palette
    palette_name = content.get("palette", "minimal_elegant")
    palette = PREMIUM_PALETTES.get(palette_name, PREMIUM_PALETTES["minimal_elegant"])
    
    # Canvas size
    FORMAT_SIZES = {
        "post": (1080, 1080), "square": (1080, 1080),
        "story": (1080, 1920), "reel": (1080, 1920),
        "landscape": (1200, 628), "portrait": (1080, 1350),
    }
    width, height = FORMAT_SIZES.get(format.lower(), (1080, 1080))
    
    # Extract brand
    brand_name = extract_brand_name(prompt)
    
    # Select content
    headline = random.choice(content["headlines"])
    subheadline = random.choice(content["subheadlines"])
    cta_text = random.choice(content["ctas"])
    badge_text = random.choice(content["badges"])
    icon = random.choice(content["icons"])
    
    # Build elements
    elements = []
    
    # 1. DECORATIVE BACKGROUND SHAPES
    elements.extend(generate_decorative_shapes(palette, width, height))
    
    # 2. OVERLAY for depth
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 0, "y": 0},
        "size": {"width": 100, "height": 100},
        "fill_color": "#000000",
        "opacity": 0.25,
    })
    
    # 3. TOP BADGE
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 8, "y": 8},
        "size": {"width": 28, "height": 5},
        "fill_color": palette["accent1"],
        "corner_radius": 25,
        "opacity": 0.9,
    })
    elements.append({
        "type": "text",
        "position": {"x": 8, "y": 8.5},
        "size": {"width": 28, "height": 4},
        "content": badge_text,
        "font_size": 13,
        "font_weight": 700,
        "font_family": "Inter",
        "color": palette["text_dark"],
        "align": "center",
        "letter_spacing": 1,
    })
    
    # 4. BRAND NAME (if detected)
    if brand_name:
        elements.append({
            "type": "text",
            "position": {"x": 8, "y": 17},
            "size": {"width": 50, "height": 4},
            "content": brand_name.upper(),
            "font_size": 14,
            "font_weight": 600,
            "font_family": "Inter",
            "color": palette["accent1"],
            "align": "left",
            "letter_spacing": 4,
        })
    
    # 5. DECORATIVE ICON
    elements.append({
        "type": "text",
        "position": {"x": 8, "y": 28},
        "size": {"width": 10, "height": 10},
        "content": icon,
        "font_size": 36,
        "color": palette["accent1"],
        "align": "left",
        "opacity": 0.8,
    })
    
    # 6. MAIN HEADLINE (Large & Bold)
    elements.append({
        "type": "text",
        "position": {"x": 8, "y": 35},
        "size": {"width": 84, "height": 28},
        "content": headline,
        "font_size": 72,
        "font_weight": 900,
        "font_family": "Montserrat",
        "color": palette["text_light"],
        "align": "left",
        "line_height": 0.95,
        "letter_spacing": -1,
    })
    
    # 7. ACCENT LINE under headline
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 8, "y": 65},
        "size": {"width": 20, "height": 0.8},
        "fill_color": palette["accent1"],
        "opacity": 1,
    })
    
    # 8. SUBHEADLINE
    elements.append({
        "type": "text",
        "position": {"x": 8, "y": 68},
        "size": {"width": 60, "height": 6},
        "content": subheadline,
        "font_size": 20,
        "font_weight": 400,
        "font_family": "Inter",
        "color": palette["text_light"],
        "align": "left",
        "opacity": 0.9,
    })
    
    # 9. FEATURE ICONS ROW
    features = ["✓ Premium Quality", "✓ Fast Delivery", "✓ Best Price"]
    for i, feature in enumerate(features):
        elements.append({
            "type": "text",
            "position": {"x": 8 + (i * 30), "y": 77},
            "size": {"width": 28, "height": 4},
            "content": feature,
            "font_size": 12,
            "font_weight": 500,
            "font_family": "Inter",
            "color": palette["accent1"],
            "align": "left",
            "opacity": 0.85,
        })
    
    # 10. CTA BUTTON
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 8, "y": 85},
        "size": {"width": 35, "height": 8},
        "fill_color": palette["accent1"],
        "corner_radius": 8,
    })
    elements.append({
        "type": "text",
        "position": {"x": 8, "y": 86.5},
        "size": {"width": 35, "height": 5},
        "content": cta_text.upper(),
        "font_size": 16,
        "font_weight": 700,
        "font_family": "Inter",
        "color": palette["text_dark"],
        "align": "center",
        "letter_spacing": 2,
    })
    
    # 11. SECONDARY CTA
    elements.append({
        "type": "text",
        "position": {"x": 48, "y": 87},
        "size": {"width": 30, "height": 5},
        "content": "Learn More →",
        "font_size": 14,
        "font_weight": 500,
        "font_family": "Inter",
        "color": palette["text_light"],
        "align": "left",
        "opacity": 0.8,
    })
    
    # 12. LARGE DECORATIVE ELEMENT (Right side)
    elements.append({
        "type": "shape", "shape_type": "circle",
        "position": {"x": 60, "y": 25},
        "size": {"width": 50, "height": 50},
        "fill_color": palette["accent1"],
        "opacity": 0.15,
    })
    elements.append({
        "type": "shape", "shape_type": "circle",
        "position": {"x": 65, "y": 30},
        "size": {"width": 40, "height": 40},
        "fill_color": palette["accent2"],
        "opacity": 0.12,
    })
    
    # 13. ICON/EMOJI CENTER (Product placeholder)
    industry_icons = {
        "coffee": "☕",
        "tech": "💻",
        "fashion": "👗",
        "food": "🍽️",
        "fitness": "💪",
        "beauty": "✨",
        "travel": "✈️",
        "default": "⭐"
    }
    elements.append({
        "type": "text",
        "position": {"x": 70, "y": 40},
        "size": {"width": 20, "height": 20},
        "content": industry_icons.get(industry, "⭐"),
        "font_size": 72,
        "align": "center",
        "opacity": 0.9,
    })
    
    # Build blueprint
    blueprint = {
        "metadata": {
            "platform": platform,
            "format": format,
            "width": width,
            "height": height,
            "industry": industry,
            "design_quality": "premium",
            "elements_count": len(elements),
        },
        "background": {
            "type": "gradient",
            "colors": palette["bg_gradient"],
            "angle": 135 + random.randint(-20, 20),
            "color": palette["bg_gradient"][0],
        },
        "headline": headline,
        "subheadline": subheadline,
        "cta": cta_text,
        "brand_name": brand_name,
        "elements": elements,
        "color_palette": {
            "primary": palette["accent1"],
            "secondary": palette["accent2"],
            "accent": palette["highlight"],
            "text": palette["text_light"],
            "glow": palette["glow"],
        }
    }
    
    return blueprint


def premium_blueprint_to_fabric(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """Convert premium blueprint to Fabric.js format"""
    
    width = blueprint["metadata"]["width"]
    height = blueprint["metadata"]["height"]
    fabric_objects = []
    
    # Background gradient
    bg = blueprint.get("background", {})
    colors = bg.get("colors", ["#1a1a2e", "#16213e"])
    angle = bg.get("angle", 135)
    
    # Calculate gradient coordinates
    rad = math.radians(angle)
    cx, cy = width / 2, height / 2
    length = max(width, height) * 1.5
    x1 = cx - math.cos(rad) * length / 2
    y1 = cy - math.sin(rad) * length / 2
    x2 = cx + math.cos(rad) * length / 2
    y2 = cy + math.sin(rad) * length / 2
    
    # Create color stops for multi-color gradient
    color_stops = []
    for i, color in enumerate(colors):
        offset = i / (len(colors) - 1) if len(colors) > 1 else 0
        color_stops.append({"offset": offset, "color": color})
    
    fabric_objects.append({
        "type": "rect",
        "left": 0,
        "top": 0,
        "width": width,
        "height": height,
        "fill": {
            "type": "linear",
            "coords": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            "colorStops": color_stops,
        },
        "selectable": False,
        "evented": False,
    })
    
    # Convert elements
    for idx, element in enumerate(blueprint.get("elements", [])):
        pos = element.get("position", {"x": 0, "y": 0})
        size = element.get("size", {"width": 10, "height": 10})
        
        left = (pos["x"] / 100) * width
        top = (pos["y"] / 100) * height
        el_width = (size["width"] / 100) * width
        el_height = (size["height"] / 100) * height
        
        if element["type"] == "text":
            fabric_objects.append({
                "type": "textbox",
                "id": f"text_{idx}",
                "left": left,
                "top": top,
                "width": el_width,
                "text": element.get("content", ""),
                "fontSize": element.get("font_size", 24),
                "fontFamily": element.get("font_family", "Inter"),
                "fontWeight": element.get("font_weight", 400),
                "fill": element.get("color", "#ffffff"),
                "textAlign": element.get("align", "left"),
                "lineHeight": element.get("line_height", 1.2),
                "charSpacing": element.get("letter_spacing", 0) * 10,
                "opacity": element.get("opacity", 1),
            })
        
        elif element["type"] == "shape":
            shape_type = element.get("shape_type", "rect")
            opacity = element.get("opacity", 1)
            
            obj = {
                "id": f"shape_{idx}",
                "left": left,
                "top": top,
                "fill": element.get("fill_color", "#8B5CF6"),
                "opacity": opacity,
            }
            
            if shape_type == "circle":
                obj["type"] = "circle"
                obj["radius"] = min(el_width, el_height) / 2
            else:
                obj["type"] = "rect"
                obj["width"] = el_width
                obj["height"] = el_height
                obj["rx"] = element.get("corner_radius", 0)
                obj["ry"] = element.get("corner_radius", 0)
            
            if element.get("stroke_color"):
                obj["stroke"] = element["stroke_color"]
                obj["strokeWidth"] = element.get("stroke_width", 1)
            
            fabric_objects.append(obj)
    
    return {
        "version": "5.3.0",
        "objects": fabric_objects,
        "background": bg.get("color", colors[0]),
    }
