"""
Professional High-Quality Design Generator for AdGenesis
Creates stunning, advertising-agency quality poster designs
"""

import random
from typing import Dict, List, Any, Optional
import re

# =============================================================================
# PROFESSIONAL COLOR PALETTES - Premium Quality
# =============================================================================

PROFESSIONAL_PALETTES = {
    "coffee_warm": {
        "name": "Coffee Shop Warmth",
        "background": {"type": "gradient", "colors": ["#2D1B0E", "#4A2C17"], "angle": 135},
        "primary": "#D4A574",
        "secondary": "#8B5E34",
        "accent": "#F5E6D3",
        "text_light": "#FFF8F0",
        "text_dark": "#1A0F0A",
        "highlight": "#E8C4A0",
        "badge_bg": "#C17F4E"
    },
    "modern_tech": {
        "name": "Tech Startup",
        "background": {"type": "gradient", "colors": ["#0F0F1A", "#1A1A2E"], "angle": 180},
        "primary": "#6366F1",
        "secondary": "#8B5CF6",
        "accent": "#22D3EE",
        "text_light": "#FFFFFF",
        "text_dark": "#0F0F1A",
        "highlight": "#A78BFA",
        "badge_bg": "#3730A3"
    },
    "fashion_luxury": {
        "name": "Luxury Fashion",
        "background": {"type": "gradient", "colors": ["#0D0D0D", "#1A1A1A"], "angle": 180},
        "primary": "#D4AF37",
        "secondary": "#FFD700",
        "accent": "#FFFFFF",
        "text_light": "#FFFFFF",
        "text_dark": "#0D0D0D",
        "highlight": "#F5E6A3",
        "badge_bg": "#8B7355"
    },
    "health_fresh": {
        "name": "Health & Wellness",
        "background": {"type": "gradient", "colors": ["#0D3320", "#1A5C38"], "angle": 135},
        "primary": "#4ADE80",
        "secondary": "#22C55E",
        "accent": "#FEF08A",
        "text_light": "#FFFFFF",
        "text_dark": "#0D3320",
        "highlight": "#86EFAC",
        "badge_bg": "#166534"
    },
    "food_vibrant": {
        "name": "Food & Restaurant",
        "background": {"type": "gradient", "colors": ["#7C2D12", "#C2410C"], "angle": 45},
        "primary": "#FED7AA",
        "secondary": "#FDBA74",
        "accent": "#FBBF24",
        "text_light": "#FFF7ED",
        "text_dark": "#431407",
        "highlight": "#FB923C",
        "badge_bg": "#9A3412"
    },
    "fitness_energy": {
        "name": "Fitness & Energy",
        "background": {"type": "gradient", "colors": ["#18181B", "#27272A"], "angle": 180},
        "primary": "#EF4444",
        "secondary": "#F97316",
        "accent": "#FACC15",
        "text_light": "#FFFFFF",
        "text_dark": "#18181B",
        "highlight": "#FB7185",
        "badge_bg": "#DC2626"
    },
    "beauty_elegant": {
        "name": "Beauty & Cosmetics",
        "background": {"type": "gradient", "colors": ["#4A1942", "#831843"], "angle": 135},
        "primary": "#F9A8D4",
        "secondary": "#F472B6",
        "accent": "#FDFCDC",
        "text_light": "#FDF2F8",
        "text_dark": "#4A1942",
        "highlight": "#FBCFE8",
        "badge_bg": "#BE185D"
    },
    "travel_adventure": {
        "name": "Travel & Adventure",
        "background": {"type": "gradient", "colors": ["#0C4A6E", "#0369A1"], "angle": 135},
        "primary": "#38BDF8",
        "secondary": "#0EA5E9",
        "accent": "#FDE047",
        "text_light": "#F0F9FF",
        "text_dark": "#0C4A6E",
        "highlight": "#7DD3FC",
        "badge_bg": "#0284C7"
    },
    "premium_dark": {
        "name": "Premium Dark",
        "background": {"type": "gradient", "colors": ["#09090B", "#18181B"], "angle": 180},
        "primary": "#FAFAFA",
        "secondary": "#A1A1AA",
        "accent": "#8B5CF6",
        "text_light": "#FAFAFA",
        "text_dark": "#09090B",
        "highlight": "#E4E4E7",
        "badge_bg": "#3F3F46"
    },
    "instagram_vibrant": {
        "name": "Instagram Style",
        "background": {"type": "gradient", "colors": ["#833AB4", "#FD1D1D", "#F77737"], "angle": 45},
        "primary": "#FFFFFF",
        "secondary": "#F0F0F0",
        "accent": "#FCAF45",
        "text_light": "#FFFFFF",
        "text_dark": "#262626",
        "highlight": "#FFE5B4",
        "badge_bg": "#C13584"
    }
}

# =============================================================================
# PROFESSIONAL LAYOUTS - Agency Quality
# =============================================================================

PROFESSIONAL_LAYOUTS = {
    "hero_impact": {
        "name": "Hero Impact",
        "elements": [
            # Background overlay
            {"type": "overlay", "x": 0, "y": 0, "w": 100, "h": 100, "opacity": 0.4},
            # Top badge
            {"type": "badge", "x": 10, "y": 8, "w": 30, "h": 6, "content": "badge"},
            # Main headline
            {"type": "headline", "x": 8, "y": 28, "w": 84, "h": 24, "font_size": 72, "font_weight": 800},
            # Subheadline
            {"type": "subheadline", "x": 8, "y": 55, "w": 70, "h": 10, "font_size": 24, "font_weight": 400},
            # Divider line
            {"type": "divider", "x": 8, "y": 68, "w": 20, "h": 0.5},
            # Body text
            {"type": "body", "x": 8, "y": 72, "w": 60, "h": 8, "font_size": 16},
            # CTA Button
            {"type": "cta", "x": 8, "y": 85, "w": 35, "h": 8, "font_size": 18},
            # Decorative circles
            {"type": "decoration_circle", "x": 80, "y": 5, "w": 25, "h": 25, "opacity": 0.15},
            {"type": "decoration_circle", "x": -5, "y": 75, "w": 20, "h": 20, "opacity": 0.1},
        ]
    },
    "centered_premium": {
        "name": "Centered Premium",
        "elements": [
            {"type": "overlay", "x": 0, "y": 0, "w": 100, "h": 100, "opacity": 0.35},
            # Logo placeholder
            {"type": "logo_area", "x": 40, "y": 10, "w": 20, "h": 10},
            # Main headline centered
            {"type": "headline", "x": 10, "y": 32, "w": 80, "h": 22, "font_size": 64, "font_weight": 800, "align": "center"},
            # Accent line
            {"type": "accent_line", "x": 40, "y": 56, "w": 20, "h": 0.5},
            # Subheadline
            {"type": "subheadline", "x": 15, "y": 60, "w": 70, "h": 10, "font_size": 22, "align": "center"},
            # Feature badges row
            {"type": "feature_badge", "x": 15, "y": 74, "w": 20, "h": 5, "content": "feature1"},
            {"type": "feature_badge", "x": 40, "y": 74, "w": 20, "h": 5, "content": "feature2"},
            {"type": "feature_badge", "x": 65, "y": 74, "w": 20, "h": 5, "content": "feature3"},
            # CTA
            {"type": "cta", "x": 30, "y": 85, "w": 40, "h": 8, "font_size": 18, "align": "center"},
            # Corner decorations
            {"type": "corner_accent", "x": 0, "y": 0, "w": 15, "h": 15},
            {"type": "corner_accent", "x": 85, "y": 85, "w": 15, "h": 15, "flip": True},
        ]
    },
    "split_bold": {
        "name": "Split Bold",
        "elements": [
            # Left panel background
            {"type": "panel", "x": 0, "y": 0, "w": 55, "h": 100, "opacity": 0.95},
            # Right image area
            {"type": "image_placeholder", "x": 55, "y": 0, "w": 45, "h": 100},
            # Badge top left
            {"type": "badge", "x": 8, "y": 10, "w": 25, "h": 5, "content": "badge"},
            # Main headline
            {"type": "headline", "x": 8, "y": 25, "w": 44, "h": 28, "font_size": 56, "font_weight": 900},
            # Subheadline
            {"type": "subheadline", "x": 8, "y": 56, "w": 40, "h": 10, "font_size": 20},
            # Bullet points
            {"type": "bullet", "x": 8, "y": 70, "w": 40, "h": 4, "content": "bullet1"},
            {"type": "bullet", "x": 8, "y": 76, "w": 40, "h": 4, "content": "bullet2"},
            # CTA
            {"type": "cta", "x": 8, "y": 86, "w": 30, "h": 7, "font_size": 16},
        ]
    },
    "instagram_story": {
        "name": "Instagram Story",
        "elements": [
            {"type": "overlay", "x": 0, "y": 0, "w": 100, "h": 100, "opacity": 0.45},
            # Top branding
            {"type": "brand_text", "x": 10, "y": 5, "w": 30, "h": 4, "font_size": 14},
            # Central headline
            {"type": "headline", "x": 8, "y": 35, "w": 84, "h": 18, "font_size": 48, "font_weight": 800, "align": "center"},
            # Offer text
            {"type": "offer", "x": 20, "y": 55, "w": 60, "h": 12, "font_size": 36, "font_weight": 900, "align": "center"},
            # Subtext
            {"type": "subheadline", "x": 15, "y": 70, "w": 70, "h": 6, "font_size": 18, "align": "center"},
            # Swipe up CTA
            {"type": "swipe_cta", "x": 35, "y": 88, "w": 30, "h": 8},
            # Decorative elements
            {"type": "sparkle", "x": 10, "y": 30, "w": 8, "h": 8},
            {"type": "sparkle", "x": 82, "y": 48, "w": 6, "h": 6},
        ]
    },
    "product_showcase": {
        "name": "Product Showcase",
        "elements": [
            # Background
            {"type": "overlay", "x": 0, "y": 0, "w": 100, "h": 100, "opacity": 0.3},
            # Product image area (center)
            {"type": "product_area", "x": 25, "y": 20, "w": 50, "h": 40},
            # Brand name top
            {"type": "brand_text", "x": 30, "y": 6, "w": 40, "h": 5, "font_size": 16, "align": "center"},
            # Product name
            {"type": "headline", "x": 10, "y": 62, "w": 80, "h": 10, "font_size": 42, "font_weight": 700, "align": "center"},
            # Price/Offer
            {"type": "price", "x": 30, "y": 74, "w": 40, "h": 8, "font_size": 32, "align": "center"},
            # CTA
            {"type": "cta", "x": 25, "y": 86, "w": 50, "h": 8, "font_size": 18, "align": "center"},
            # Trust badges
            {"type": "trust_badge", "x": 10, "y": 90, "w": 15, "h": 4},
            {"type": "trust_badge", "x": 75, "y": 90, "w": 15, "h": 4},
        ]
    },
    "minimal_elegant": {
        "name": "Minimal Elegant",
        "elements": [
            # Subtle border
            {"type": "border_frame", "x": 4, "y": 4, "w": 92, "h": 92, "stroke": 1},
            # Headline
            {"type": "headline", "x": 12, "y": 38, "w": 76, "h": 16, "font_size": 52, "font_weight": 600, "align": "center"},
            # Thin divider
            {"type": "divider", "x": 35, "y": 56, "w": 30, "h": 0.3},
            # Subheadline
            {"type": "subheadline", "x": 20, "y": 60, "w": 60, "h": 8, "font_size": 18, "align": "center"},
            # CTA
            {"type": "cta_minimal", "x": 32, "y": 75, "w": 36, "h": 6, "font_size": 14, "align": "center"},
            # Corner accents
            {"type": "corner_line", "x": 4, "y": 4, "w": 12, "h": 0.3},
            {"type": "corner_line_v", "x": 4, "y": 4, "w": 0.3, "h": 12},
            {"type": "corner_line", "x": 84, "y": 92, "w": 12, "h": 0.3},
            {"type": "corner_line_v", "x": 92, "y": 80, "w": 0.3, "h": 12},
        ]
    }
}

# =============================================================================
# CONTENT GENERATION
# =============================================================================

INDUSTRY_CONTENT = {
    "coffee": {
        "headlines": [
            "BREW YOUR\nPERFECT DAY",
            "COFFEE\nTHAT MOVES YOU",
            "TASTE THE\nDIFFERENCE",
            "AWAKEN\nYOUR SENSES",
            "CRAFTED WITH\nPASSION"
        ],
        "subheadlines": [
            "Premium Artisan Coffee • Freshly Roasted Daily",
            "Where Every Cup Tells a Story",
            "Handcrafted Excellence in Every Sip",
            "Your Daily Ritual, Elevated"
        ],
        "ctas": ["Order Now", "Visit Us", "Explore Menu", "Get 20% Off"],
        "badges": ["☕ PREMIUM", "🌟 AWARD WINNING", "🌱 ORGANIC"],
        "features": ["100% Arabica", "Fair Trade", "Fresh Roasted"],
        "palette": "coffee_warm"
    },
    "tech": {
        "headlines": [
            "THE FUTURE\nIS NOW",
            "INNOVATION\nREDEFINED",
            "NEXT-GEN\nTECHNOLOGY",
            "POWER YOUR\nPOTENTIAL",
            "SMART.\nSIMPLE.\nSECURE."
        ],
        "subheadlines": [
            "Experience Tomorrow's Technology Today",
            "Built for the Modern World",
            "Revolutionizing How You Work",
            "The Intelligent Choice"
        ],
        "ctas": ["Learn More", "Get Started", "Try Free", "Pre-Order"],
        "badges": ["🚀 NEW", "⚡ FAST", "🔒 SECURE"],
        "features": ["AI-Powered", "Cloud Sync", "24/7 Support"],
        "palette": "modern_tech"
    },
    "fashion": {
        "headlines": [
            "DEFINE YOUR\nSTYLE",
            "LUXURY\nREIMAGINED",
            "TIMELESS\nELEGANCE",
            "THE NEW\nCOLLECTION",
            "ELEVATE\nYOUR LOOK"
        ],
        "subheadlines": [
            "Exclusive Designs for the Distinguished",
            "Where Fashion Meets Art",
            "Curated for the Modern Individual",
            "Effortless Style, Unmatched Quality"
        ],
        "ctas": ["Shop Now", "Explore", "View Collection", "Get 30% Off"],
        "badges": ["✨ NEW ARRIVAL", "👗 EXCLUSIVE", "💎 PREMIUM"],
        "features": ["Limited Edition", "Free Shipping", "Easy Returns"],
        "palette": "fashion_luxury"
    },
    "food": {
        "headlines": [
            "TASTE THE\nDIFFERENCE",
            "FLAVOR\nPERFECTED",
            "FRESH &\nDELICIOUS",
            "SAVOR\nEVERY BITE",
            "MADE WITH\nLOVE"
        ],
        "subheadlines": [
            "Fresh Ingredients, Unforgettable Taste",
            "From Our Kitchen to Your Table",
            "Crafted by Master Chefs",
            "Quality You Can Taste"
        ],
        "ctas": ["Order Now", "View Menu", "Get Delivery", "Book Table"],
        "badges": ["🍽️ CHEF'S SPECIAL", "⭐ 5-STAR", "🔥 HOT & FRESH"],
        "features": ["Farm Fresh", "No Preservatives", "Fast Delivery"],
        "palette": "food_vibrant"
    },
    "fitness": {
        "headlines": [
            "TRANSFORM\nYOUR BODY",
            "UNLEASH YOUR\nPOTENTIAL",
            "STRONGER\nEVERY DAY",
            "NO LIMITS.\nNO EXCUSES.",
            "YOUR FITNESS\nJOURNEY"
        ],
        "subheadlines": [
            "Train Like a Champion",
            "Results That Speak for Themselves",
            "Push Beyond Your Limits",
            "Where Champions Are Made"
        ],
        "ctas": ["Join Now", "Start Free Trial", "Get Fit", "Book Session"],
        "badges": ["💪 PRO", "🏆 #1 RATED", "⚡ HIGH ENERGY"],
        "features": ["Expert Trainers", "24/7 Access", "Premium Equipment"],
        "palette": "fitness_energy"
    },
    "beauty": {
        "headlines": [
            "REVEAL YOUR\nRADIANCE",
            "BEAUTY\nREDEFINED",
            "GLOW FROM\nWITHIN",
            "TIMELESS\nBEAUTY",
            "YOUR SKIN\nDESERVES BETTER"
        ],
        "subheadlines": [
            "Clinically Proven Results",
            "Nature Meets Science",
            "Luxury Skincare for Everyone",
            "Discover Your Natural Beauty"
        ],
        "ctas": ["Shop Now", "Try It Free", "Get Your Glow", "Save 25%"],
        "badges": ["🌿 NATURAL", "✨ BESTSELLER", "💖 DERMATOLOGIST APPROVED"],
        "features": ["Vegan", "Cruelty-Free", "Paraben-Free"],
        "palette": "beauty_elegant"
    },
    "travel": {
        "headlines": [
            "ADVENTURE\nAWAITS",
            "EXPLORE THE\nWORLD",
            "YOUR JOURNEY\nBEGINS",
            "DISCOVER\nPARADISE",
            "ESCAPE\nTHE ORDINARY"
        ],
        "subheadlines": [
            "Unforgettable Experiences Await",
            "Create Memories That Last Forever",
            "Where Dreams Become Destinations",
            "Your Perfect Getaway Starts Here"
        ],
        "ctas": ["Book Now", "Explore Deals", "Plan Trip", "Get 40% Off"],
        "badges": ["✈️ BEST DEALS", "🌴 EXCLUSIVE", "⭐ TOP RATED"],
        "features": ["Best Price Guarantee", "Free Cancellation", "24/7 Support"],
        "palette": "travel_adventure"
    },
    "default": {
        "headlines": [
            "DISCOVER\nSOMETHING NEW",
            "ELEVATE YOUR\nEXPERIENCE",
            "THE SMART\nCHOICE",
            "QUALITY YOU\nCAN TRUST",
            "START YOUR\nJOURNEY"
        ],
        "subheadlines": [
            "Experience Excellence",
            "Built for You",
            "Quality Meets Innovation",
            "Your Satisfaction, Our Priority"
        ],
        "ctas": ["Learn More", "Get Started", "Shop Now", "Discover"],
        "badges": ["⭐ PREMIUM", "🏆 TOP RATED", "✓ TRUSTED"],
        "features": ["Quality", "Value", "Service"],
        "palette": "premium_dark"
    }
}

# =============================================================================
# PROFESSIONAL DESIGN GENERATOR
# =============================================================================

def detect_industry(prompt: str) -> str:
    """Detect industry from prompt"""
    prompt_lower = prompt.lower()
    
    industry_keywords = {
        "coffee": ["coffee", "cafe", "espresso", "latte", "brew", "roast", "barista"],
        "tech": ["tech", "software", "app", "digital", "ai", "smart", "innovation", "startup"],
        "fashion": ["fashion", "style", "clothing", "wear", "collection", "luxury", "designer"],
        "food": ["food", "restaurant", "delivery", "menu", "taste", "chef", "cuisine", "eat"],
        "fitness": ["fitness", "gym", "workout", "training", "health", "exercise", "muscle", "protein"],
        "beauty": ["beauty", "skincare", "cosmetic", "makeup", "glow", "skin", "cream", "serum"],
        "travel": ["travel", "vacation", "trip", "destination", "hotel", "flight", "adventure", "explore"],
    }
    
    for industry, keywords in industry_keywords.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                return industry
    
    return "default"

def extract_brand_name(prompt: str) -> Optional[str]:
    """Extract brand name from prompt"""
    patterns = [
        r"(?:for|called|named|brand)\s+(?:my\s+)?([A-Z][a-zA-Z']+(?:\s+[A-Z][a-zA-Z']+)?)",
        r"([A-Z][a-zA-Z']+(?:'s)?)\s+(?:coffee|shop|store|brand|restaurant)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def generate_professional_design(prompt: str, platform: str = "instagram", 
                                  format: str = "post", 
                                  industry_override: str = None) -> Dict[str, Any]:
    """
    Generate a professional, high-quality design blueprint.
    This creates advertising-agency quality posters.
    """
    
    # Detect industry from prompt
    industry = industry_override or detect_industry(prompt)
    content = INDUSTRY_CONTENT.get(industry, INDUSTRY_CONTENT["default"])
    
    # Get color palette
    palette_name = content.get("palette", "premium_dark")
    palette = PROFESSIONAL_PALETTES.get(palette_name, PROFESSIONAL_PALETTES["premium_dark"])
    
    # Select layout based on format
    if "story" in format.lower() or "reel" in format.lower():
        layout = PROFESSIONAL_LAYOUTS["instagram_story"]
    elif "product" in prompt.lower() or "showcase" in prompt.lower():
        layout = PROFESSIONAL_LAYOUTS["product_showcase"]
    elif random.random() > 0.5:
        layout = random.choice([
            PROFESSIONAL_LAYOUTS["hero_impact"],
            PROFESSIONAL_LAYOUTS["centered_premium"],
            PROFESSIONAL_LAYOUTS["split_bold"]
        ])
    else:
        layout = PROFESSIONAL_LAYOUTS["minimal_elegant"]
    
    # Determine canvas size
    FORMAT_SIZES = {
        "post": (1080, 1080),
        "square": (1080, 1080),
        "story": (1080, 1920),
        "reel": (1080, 1920),
        "landscape": (1200, 628),
        "portrait": (1080, 1350),
        "wide": (1920, 1080),
    }
    
    width, height = FORMAT_SIZES.get(format.lower(), (1080, 1080))
    
    # Extract brand name if present
    brand_name = extract_brand_name(prompt)
    
    # Select content
    headline = random.choice(content["headlines"])
    subheadline = random.choice(content["subheadlines"])
    cta_text = random.choice(content["ctas"])
    badge_text = random.choice(content["badges"])
    features = content["features"]
    
    # Build elements list
    elements = []
    
    for element in layout["elements"]:
        el_type = element["type"]
        base_element = {
            "id": f"{el_type}_{len(elements)}",
            "position": {"x": element["x"], "y": element["y"]},
            "size": {"width": element["w"], "height": element["h"]},
        }
        
        if el_type == "overlay":
            elements.append({
                **base_element,
                "type": "shape",
                "shape_type": "rect",
                "fill_color": "#000000",
                "opacity": element.get("opacity", 0.4),
            })
        
        elif el_type == "headline":
            elements.append({
                **base_element,
                "type": "text",
                "content": headline,
                "font_size": element.get("font_size", 64),
                "font_weight": element.get("font_weight", 800),
                "font_family": "Montserrat",
                "color": palette["text_light"],
                "align": element.get("align", "left"),
                "line_height": 1.1,
                "letter_spacing": 2,
            })
        
        elif el_type == "subheadline":
            elements.append({
                **base_element,
                "type": "text",
                "content": subheadline,
                "font_size": element.get("font_size", 22),
                "font_weight": element.get("font_weight", 400),
                "font_family": "Inter",
                "color": palette["text_light"],
                "align": element.get("align", "left"),
                "opacity": 0.9,
            })
        
        elif el_type == "body":
            elements.append({
                **base_element,
                "type": "text",
                "content": "Premium quality you can trust. Join thousands of satisfied customers.",
                "font_size": element.get("font_size", 16),
                "font_weight": 400,
                "font_family": "Inter",
                "color": palette["text_light"],
                "align": element.get("align", "left"),
                "opacity": 0.8,
            })
        
        elif el_type == "cta" or el_type == "cta_minimal":
            # CTA Background
            elements.append({
                "id": f"cta_bg_{len(elements)}",
                "type": "shape",
                "shape_type": "rect",
                "position": {"x": element["x"], "y": element["y"]},
                "size": {"width": element["w"], "height": element["h"]},
                "fill_color": palette["primary"] if el_type == "cta" else "transparent",
                "stroke_color": palette["primary"] if el_type == "cta_minimal" else None,
                "stroke_width": 2 if el_type == "cta_minimal" else 0,
                "corner_radius": 8,
            })
            # CTA Text
            elements.append({
                **base_element,
                "type": "text",
                "content": cta_text,
                "font_size": element.get("font_size", 18),
                "font_weight": 600,
                "font_family": "Inter",
                "color": palette["text_light"] if el_type == "cta" else palette["primary"],
                "align": "center",
            })
        
        elif el_type == "badge":
            # Badge background
            elements.append({
                "id": f"badge_bg_{len(elements)}",
                "type": "shape",
                "shape_type": "rect",
                "position": {"x": element["x"], "y": element["y"]},
                "size": {"width": element["w"], "height": element["h"]},
                "fill_color": palette["badge_bg"],
                "corner_radius": 20,
                "opacity": 0.9,
            })
            # Badge text
            elements.append({
                **base_element,
                "type": "text",
                "content": badge_text,
                "font_size": 12,
                "font_weight": 700,
                "font_family": "Inter",
                "color": palette["text_light"],
                "align": "center",
                "letter_spacing": 1,
            })
        
        elif el_type == "divider" or el_type == "accent_line":
            elements.append({
                **base_element,
                "type": "shape",
                "shape_type": "rect",
                "fill_color": palette["primary"],
                "opacity": 0.8,
            })
        
        elif el_type.startswith("decoration_circle"):
            elements.append({
                **base_element,
                "type": "shape",
                "shape_type": "circle",
                "fill_color": palette["accent"],
                "opacity": element.get("opacity", 0.15),
            })
        
        elif el_type == "feature_badge":
            idx = int(element.get("content", "feature1")[-1]) - 1
            feature_text = features[idx] if idx < len(features) else "Quality"
            
            elements.append({
                **base_element,
                "type": "text",
                "content": f"✓ {feature_text}",
                "font_size": 14,
                "font_weight": 500,
                "font_family": "Inter",
                "color": palette["text_light"],
                "align": "center",
                "opacity": 0.85,
            })
        
        elif el_type == "brand_text":
            elements.append({
                **base_element,
                "type": "text",
                "content": brand_name.upper() if brand_name else industry.upper(),
                "font_size": element.get("font_size", 14),
                "font_weight": 600,
                "font_family": "Inter",
                "color": palette["text_light"],
                "align": element.get("align", "left"),
                "letter_spacing": 3,
                "opacity": 0.9,
            })
        
        elif el_type == "offer":
            # Extract any percentage or offer from prompt
            offer_match = re.search(r'(\d+%?\s*(?:off|discount)?)', prompt, re.IGNORECASE)
            offer_text = offer_match.group(1).upper() if offer_match else "SPECIAL OFFER"
            
            elements.append({
                **base_element,
                "type": "text",
                "content": offer_text,
                "font_size": element.get("font_size", 36),
                "font_weight": 900,
                "font_family": "Montserrat",
                "color": palette["accent"],
                "align": "center",
            })
        
        elif el_type == "swipe_cta":
            elements.append({
                **base_element,
                "type": "text",
                "content": "↑ SWIPE UP",
                "font_size": 14,
                "font_weight": 600,
                "font_family": "Inter",
                "color": palette["text_light"],
                "align": "center",
                "letter_spacing": 2,
            })
        
        elif el_type == "sparkle":
            elements.append({
                **base_element,
                "type": "text",
                "content": "✨",
                "font_size": 24,
                "align": "center",
            })
        
        elif el_type == "border_frame":
            elements.append({
                **base_element,
                "type": "shape",
                "shape_type": "rect",
                "fill_color": "transparent",
                "stroke_color": palette["primary"],
                "stroke_width": element.get("stroke", 1),
                "opacity": 0.3,
            })
        
        elif el_type.startswith("corner"):
            elements.append({
                **base_element,
                "type": "shape",
                "shape_type": "rect",
                "fill_color": palette["primary"],
                "opacity": 0.5,
            })
        
        elif el_type == "panel":
            elements.append({
                **base_element,
                "type": "shape",
                "shape_type": "rect",
                "fill_color": palette["background"]["colors"][0] if isinstance(palette["background"], dict) else "#000000",
                "opacity": element.get("opacity", 0.95),
            })
        
        elif el_type == "image_placeholder" or el_type == "product_area":
            # Add a stylized placeholder
            elements.append({
                **base_element,
                "type": "shape",
                "shape_type": "rect",
                "fill_color": palette["secondary"],
                "opacity": 0.3,
                "corner_radius": 12 if el_type == "product_area" else 0,
            })
            # Add icon
            elements.append({
                "id": f"placeholder_icon_{len(elements)}",
                "type": "text",
                "position": {"x": element["x"] + element["w"]/2 - 5, "y": element["y"] + element["h"]/2 - 5},
                "size": {"width": 10, "height": 10},
                "content": "📷" if el_type == "image_placeholder" else "🛍️",
                "font_size": 48,
                "align": "center",
                "opacity": 0.5,
            })
        
        elif el_type == "price":
            elements.append({
                **base_element,
                "type": "text",
                "content": "$29.99",
                "font_size": element.get("font_size", 32),
                "font_weight": 700,
                "font_family": "Montserrat",
                "color": palette["accent"],
                "align": "center",
            })
        
        elif el_type == "trust_badge":
            elements.append({
                **base_element,
                "type": "text",
                "content": "⭐ 4.9",
                "font_size": 12,
                "font_weight": 500,
                "font_family": "Inter",
                "color": palette["text_light"],
                "align": "center",
                "opacity": 0.7,
            })
        
        elif el_type == "bullet":
            idx = int(element.get("content", "bullet1")[-1]) - 1
            bullet_texts = [
                f"✓ {features[0] if len(features) > 0 else 'Premium Quality'}",
                f"✓ {features[1] if len(features) > 1 else 'Fast Delivery'}",
            ]
            elements.append({
                **base_element,
                "type": "text",
                "content": bullet_texts[idx] if idx < len(bullet_texts) else "✓ Quality",
                "font_size": 14,
                "font_weight": 400,
                "font_family": "Inter",
                "color": palette["text_light"],
                "align": "left",
                "opacity": 0.85,
            })
        
        elif el_type == "logo_area":
            elements.append({
                **base_element,
                "type": "text",
                "content": brand_name[:2].upper() if brand_name else "AD",
                "font_size": 28,
                "font_weight": 800,
                "font_family": "Montserrat",
                "color": palette["primary"],
                "align": "center",
            })
    
    # Build final blueprint
    blueprint = {
        "metadata": {
            "platform": platform,
            "format": format,
            "width": width,
            "height": height,
            "industry": industry,
            "layout": layout["name"],
        },
        "background": {
            "type": palette["background"]["type"],
            "colors": palette["background"]["colors"],
            "angle": palette["background"].get("angle", 180),
            "color": palette["background"]["colors"][0],  # Fallback solid color
        },
        "headline": headline,
        "subheadline": subheadline,
        "cta": cta_text,
        "brand_name": brand_name,
        "elements": elements,
        "color_palette": {
            "primary": palette["primary"],
            "secondary": palette["secondary"],
            "accent": palette["accent"],
            "text": palette["text_light"],
        }
    }
    
    return blueprint


def professional_blueprint_to_fabric(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert professional blueprint to Fabric.js format with high quality rendering.
    """
    width = blueprint["metadata"]["width"]
    height = blueprint["metadata"]["height"]
    
    fabric_objects = []
    
    # Background handling
    bg = blueprint.get("background", {})
    bg_type = bg.get("type", "solid")
    
    if bg_type == "gradient" and len(bg.get("colors", [])) >= 2:
        # Create gradient background
        angle = bg.get("angle", 180)
        colors = bg["colors"]
        
        # Calculate gradient coordinates based on angle
        import math
        rad = math.radians(angle)
        x1 = width/2 - math.cos(rad) * width
        y1 = height/2 - math.sin(rad) * height
        x2 = width/2 + math.cos(rad) * width
        y2 = height/2 + math.sin(rad) * height
        
        fabric_objects.append({
            "type": "rect",
            "left": 0,
            "top": 0,
            "width": width,
            "height": height,
            "fill": {
                "type": "linear",
                "coords": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "colorStops": [
                    {"offset": 0, "color": colors[0]},
                    {"offset": 1, "color": colors[-1]},
                ]
            },
            "selectable": False,
            "evented": False,
        })
    else:
        fabric_objects.append({
            "type": "rect",
            "left": 0,
            "top": 0,
            "width": width,
            "height": height,
            "fill": bg.get("color", bg.get("colors", ["#1a1a2e"])[0]),
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
            text_content = element.get("content", "")
            
            fabric_obj = {
                "type": "textbox",
                "id": element.get("id", f"text_{len(fabric_objects)}"),
                "left": left,
                "top": top,
                "width": el_width,
                "text": text_content,
                "fontSize": element.get("font_size", 48),
                "fontFamily": element.get("font_family", "Inter"),
                "fontWeight": element.get("font_weight", 400),
                "fill": element.get("color", "#ffffff"),
                "textAlign": element.get("align", "left"),
                "lineHeight": element.get("line_height", 1.2),
                "charSpacing": element.get("letter_spacing", 0) * 10,
                "opacity": element.get("opacity", 1),
            }
            
            fabric_objects.append(fabric_obj)
        
        elif element["type"] == "shape":
            shape_type = element.get("shape_type", "rect")
            
            fabric_obj = {
                "id": element.get("id", f"shape_{len(fabric_objects)}"),
                "left": left,
                "top": top,
                "fill": element.get("fill_color", "#8B5CF6"),
                "opacity": element.get("opacity", 1),
            }
            
            if shape_type == "circle":
                fabric_obj["type"] = "circle"
                fabric_obj["radius"] = min(el_width, el_height) / 2
            else:
                fabric_obj["type"] = "rect"
                fabric_obj["width"] = el_width
                fabric_obj["height"] = el_height
                fabric_obj["rx"] = element.get("corner_radius", 0)
                fabric_obj["ry"] = element.get("corner_radius", 0)
            
            # Handle stroke
            if element.get("stroke_color"):
                fabric_obj["stroke"] = element["stroke_color"]
                fabric_obj["strokeWidth"] = element.get("stroke_width", 1)
            
            fabric_objects.append(fabric_obj)
    
    return {
        "version": "5.3.0",
        "objects": fabric_objects,
        "background": bg.get("color", bg.get("colors", ["#1a1a2e"])[0]),
    }
