"""
SMART DESIGN GENERATOR for AdGenesis
Generates TRULY UNIQUE designs by analyzing and understanding the user's prompt
"""

import random
import hashlib
import re
import math
from typing import Dict, List, Any, Optional, Tuple

# =============================================================================
# COLOR PALETTES - Matched to moods/industries
# =============================================================================

PALETTES = {
    "warm": {
        "bg": ["#1A0F0A", "#3D2314", "#5C3D2E"],
        "accent": "#D4A574", "accent2": "#E8C4A0",
        "text": "#FFF8F0", "text_dark": "#1A0F0A",
    },
    "cool": {
        "bg": ["#0C4A6E", "#0369A1", "#0284C7"],
        "accent": "#38BDF8", "accent2": "#7DD3FC",
        "text": "#F0F9FF", "text_dark": "#0C4A6E",
    },
    "neon": {
        "bg": ["#0A0A1A", "#0F0F2D", "#1A1A3E"],
        "accent": "#00F5FF", "accent2": "#8B5CF6",
        "text": "#FFFFFF", "text_dark": "#0A0A1A",
    },
    "luxury": {
        "bg": ["#0D0D0D", "#1A1A1A", "#262626"],
        "accent": "#D4AF37", "accent2": "#FFD700",
        "text": "#FFFFFF", "text_dark": "#0D0D0D",
    },
    "vibrant": {
        "bg": ["#7C2D12", "#9A3412", "#C2410C"],
        "accent": "#FED7AA", "accent2": "#FB923C",
        "text": "#FFF7ED", "text_dark": "#431407",
    },
    "bold": {
        "bg": ["#0F0F0F", "#1A1A1A", "#262626"],
        "accent": "#EF4444", "accent2": "#F97316",
        "text": "#FFFFFF", "text_dark": "#0F0F0F",
    },
    "pink": {
        "bg": ["#4A1942", "#6B2158", "#831843"],
        "accent": "#F9A8D4", "accent2": "#F472B6",
        "text": "#FDF2F8", "text_dark": "#4A1942",
    },
    "gradient_pop": {
        "bg": ["#833AB4", "#FD1D1D", "#F77737"],
        "accent": "#FFFFFF", "accent2": "#FCAF45",
        "text": "#FFFFFF", "text_dark": "#262626",
    },
    "minimal": {
        "bg": ["#FAFAFA", "#F5F5F5", "#E5E5E5"],
        "accent": "#18181B", "accent2": "#3F3F46",
        "text": "#18181B", "text_dark": "#18181B",
    },
    "forest": {
        "bg": ["#052E16", "#14532D", "#166534"],
        "accent": "#86EFAC", "accent2": "#4ADE80",
        "text": "#F0FDF4", "text_dark": "#052E16",
    },
    "purple": {
        "bg": ["#1E1B4B", "#312E81", "#4338CA"],
        "accent": "#C4B5FD", "accent2": "#A78BFA",
        "text": "#EDE9FE", "text_dark": "#1E1B4B",
    },
    "teal": {
        "bg": ["#042F2E", "#134E4A", "#115E59"],
        "accent": "#5EEAD4", "accent2": "#2DD4BF",
        "text": "#F0FDFA", "text_dark": "#042F2E",
    },
}

# =============================================================================
# PROMPT ANALYZER - Extract meaningful info from user's prompt
# =============================================================================

def analyze_prompt(prompt: str) -> Dict[str, Any]:
    """
    Deeply analyze the user's prompt to extract all meaningful information
    """
    prompt_lower = prompt.lower()
    
    result = {
        "brand_name": None,
        "product": None,
        "industry": "general",
        "action": None,
        "offer": None,
        "platform_hint": None,
        "mood": "professional",
        "color_hint": None,
        "keywords": [],
        "is_sale": False,
        "is_launch": False,
        "is_event": False,
    }
    
    # Extract brand name - improved patterns
    brand_patterns = [
        # "named X" - one or two capitalized words
        r"named\s+['\"]?([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\b",
        # "called X" - one or two capitalized words  
        r"called\s+['\"]?([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\b",
        # "X's shop/cafe/store" - possessive
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'s\s+(?:shop|store|cafe|brand|company|business)",
        # "brand X" or "company X"
        r"(?:brand|company)\s+['\"]?([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\b",
        # "for X" at beginning - brand name
        r"^for\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\b",
    ]
    for pattern in brand_patterns:
        match = re.search(pattern, prompt)
        if match:
            name = match.group(1).strip().strip("'\"")
            # Remove common trailing words that aren't part of brand name
            stop_words = ['serving', 'launching', 'introducing', 'offering', 'selling', 'for', 'on', 'in', 'to', 'and', 'the', 'a', 'an', 'with', 'new', 'fresh', 'best']
            words = name.split()
            filtered = []
            for w in words:
                if w.lower() not in stop_words:
                    filtered.append(w)
                else:
                    break
            name = ' '.join(filtered)
            if len(name) >= 2 and len(name) <= 30:
                result["brand_name"] = name
                break
    
    # Detect industry from keywords
    industry_keywords = {
        "coffee": ["coffee", "cafe", "café", "espresso", "latte", "brew", "roast", "barista"],
        "food": ["food", "restaurant", "pizza", "burger", "eat", "menu", "chef", "cuisine", "delivery", "taste"],
        "fashion": ["fashion", "style", "clothing", "wear", "collection", "designer", "boutique", "outfit", "dress", "apparel"],
        "tech": ["tech", "software", "app", "digital", "ai", "startup", "saas", "cloud", "code", "developer", "innovation"],
        "fitness": ["fitness", "gym", "workout", "training", "exercise", "muscle", "protein", "sports", "yoga", "health"],
        "beauty": ["beauty", "skincare", "cosmetic", "makeup", "glow", "skin", "cream", "serum", "spa"],
        "travel": ["travel", "vacation", "trip", "destination", "hotel", "flight", "adventure", "explore", "tourism"],
        "real_estate": ["real estate", "property", "home", "house", "apartment", "rent", "buy", "sell"],
        "education": ["education", "course", "learn", "training", "class", "workshop", "tutorial"],
        "finance": ["finance", "bank", "invest", "money", "loan", "insurance", "crypto"],
        "entertainment": ["music", "concert", "movie", "show", "event", "party", "club", "dj"],
    }
    
    for industry, keywords in industry_keywords.items():
        for kw in keywords:
            if kw in prompt_lower:
                result["industry"] = industry
                result["keywords"].append(kw)
                break
        if result["industry"] != "general":
            break
    
    # Detect sale/discount
    sale_patterns = [
        r"(\d+)\s*%\s*(?:off|discount)",
        r"sale",
        r"discount",
        r"offer",
        r"deal",
        r"save",
        r"promo",
    ]
    for pattern in sale_patterns:
        if re.search(pattern, prompt_lower):
            result["is_sale"] = True
            # Try to extract percentage
            pct_match = re.search(r"(\d+)\s*%", prompt)
            if pct_match:
                result["offer"] = f"{pct_match.group(1)}% OFF"
            break
    
    # Detect launch/new
    if any(word in prompt_lower for word in ["launch", "new", "introducing", "announce", "release", "coming soon"]):
        result["is_launch"] = True
    
    # Detect event
    if any(word in prompt_lower for word in ["event", "party", "concert", "festival", "workshop", "webinar", "meetup"]):
        result["is_event"] = True
    
    # Detect mood/style
    mood_keywords = {
        "luxury": ["luxury", "premium", "exclusive", "elegant", "sophisticated", "high-end"],
        "playful": ["fun", "playful", "colorful", "vibrant", "exciting", "happy"],
        "urgent": ["urgent", "hurry", "limited", "now", "today", "flash", "quick"],
        "minimal": ["minimal", "simple", "clean", "modern", "sleek"],
        "bold": ["bold", "strong", "powerful", "intense", "dynamic"],
        "warm": ["warm", "cozy", "friendly", "welcoming", "homey"],
        "cool": ["cool", "fresh", "calm", "peaceful", "serene"],
    }
    
    for mood, keywords in mood_keywords.items():
        for kw in keywords:
            if kw in prompt_lower:
                result["mood"] = mood
                break
    
    # Detect color hints
    color_hints = {
        "warm": ["warm", "orange", "red", "brown", "golden", "autumn", "sunset"],
        "cool": ["cool", "blue", "ocean", "sea", "sky", "water", "ice"],
        "pink": ["pink", "rose", "feminine", "girly", "romantic"],
        "forest": ["green", "nature", "eco", "organic", "natural", "forest", "plant"],
        "purple": ["purple", "violet", "lavender", "royal"],
        "neon": ["neon", "cyber", "futuristic", "glow", "electric"],
        "luxury": ["gold", "golden", "luxury", "premium", "black", "dark"],
    }
    
    for color, keywords in color_hints.items():
        for kw in keywords:
            if kw in prompt_lower:
                result["color_hint"] = color
                break
    
    # Detect platform
    if "instagram" in prompt_lower or "insta" in prompt_lower:
        result["platform_hint"] = "instagram"
    elif "facebook" in prompt_lower or "fb" in prompt_lower:
        result["platform_hint"] = "facebook"
    elif "twitter" in prompt_lower or "x.com" in prompt_lower:
        result["platform_hint"] = "twitter"
    elif "linkedin" in prompt_lower:
        result["platform_hint"] = "linkedin"
    
    # Extract product if mentioned
    product_patterns = [
        r"(?:poster|ad|design|creative)\s+(?:for|about)\s+(?:my|our|a|an)?\s*([a-zA-Z\s]+?)(?:\s+(?:on|for|to)|$)",
    ]
    for pattern in product_patterns:
        match = re.search(pattern, prompt_lower)
        if match:
            product = match.group(1).strip()
            if len(product) > 2 and product not in ["my", "our", "the", "a", "an"]:
                result["product"] = product
                break
    
    return result


def generate_headline_from_prompt(analysis: Dict[str, Any], prompt: str) -> str:
    """Generate a contextual headline based on the analyzed prompt"""
    
    brand = analysis.get("brand_name")
    industry = analysis.get("industry", "general")
    is_sale = analysis.get("is_sale", False)
    is_launch = analysis.get("is_launch", False)
    offer = analysis.get("offer")
    
    # Sale-focused headlines
    if is_sale and offer:
        templates = [
            f"{offer}\nON EVERYTHING",
            f"MEGA SALE\n{offer}",
            f"SAVE\n{offer}",
            f"DON'T MISS\n{offer}",
        ]
        return random.choice(templates)
    
    if is_sale:
        templates = [
            "MASSIVE\nSALE",
            "BIG\nSAVINGS",
            "LIMITED\nTIME OFFER",
            "SPECIAL\nDEAL",
        ]
        return random.choice(templates)
    
    # Launch headlines
    if is_launch:
        if brand:
            templates = [
                f"INTRODUCING\n{brand.upper()}",
                f"MEET\n{brand.upper()}",
                f"NEW FROM\n{brand.upper()}",
                f"{brand.upper()}\nIS HERE",
            ]
        else:
            templates = [
                "NOW\nLAUNCHING",
                "SOMETHING\nNEW",
                "COMING\nSOON",
                "INTRODUCING",
            ]
        return random.choice(templates)
    
    # Brand-focused headlines
    if brand:
        industry_brand_templates = {
            "coffee": [f"WELCOME TO\n{brand.upper()}", f"{brand.upper()}\nCOFFEE", f"TASTE\n{brand.upper()}"],
            "food": [f"{brand.upper()}\nKITCHEN", f"EAT AT\n{brand.upper()}", f"{brand.upper()}\nSERVES"],
            "fashion": [f"{brand.upper()}\nSTYLE", f"WEAR\n{brand.upper()}", f"{brand.upper()}\nCOLLECTION"],
            "tech": [f"{brand.upper()}\nTECH", f"POWERED BY\n{brand.upper()}", f"{brand.upper()}\nINNOVATES"],
            "fitness": [f"TRAIN WITH\n{brand.upper()}", f"{brand.upper()}\nFITNESS", f"GET FIT AT\n{brand.upper()}"],
            "beauty": [f"{brand.upper()}\nBEAUTY", f"GLOW WITH\n{brand.upper()}", f"{brand.upper()}\nSKINCARE"],
            "travel": [f"EXPLORE WITH\n{brand.upper()}", f"{brand.upper()}\nTRAVEL", f"DISCOVER\n{brand.upper()}"],
        }
        
        if industry in industry_brand_templates:
            return random.choice(industry_brand_templates[industry])
        else:
            return f"DISCOVER\n{brand.upper()}"
    
    # Industry-specific headlines (no brand)
    industry_headlines = {
        "coffee": ["COFFEE\nPERFECTION", "BREW\nYOUR DAY", "FRESH\nROASTED", "CAFÉ\nVIBES"],
        "food": ["TASTE\nTHE BEST", "FRESH\nDAILY", "DELICIOUS\nAWAITS", "FOOD\nYOU'LL LOVE"],
        "fashion": ["STYLE\nREDEFINED", "NEW\nCOLLECTION", "WEAR\nCONFIDENCE", "FASHION\nFORWARD"],
        "tech": ["FUTURE\nIS NOW", "INNOVATE\nTODAY", "SMART\nSOLUTIONS", "TECH\nTHAT WORKS"],
        "fitness": ["GET\nSTRONGER", "TRANSFORM\nYOURSELF", "FITNESS\nGOALS", "TRAIN\nHARD"],
        "beauty": ["GLOW\nUP", "NATURAL\nBEAUTY", "SKIN\nPERFECT", "BEAUTY\nUNLOCKED"],
        "travel": ["EXPLORE\nMORE", "ADVENTURE\nCALLS", "TRAVEL\nDREAMS", "DISCOVER\nNEW"],
        "real_estate": ["FIND YOUR\nHOME", "DREAM\nPROPERTY", "LIVE\nBETTER"],
        "education": ["LEARN\nGROW", "SKILL UP", "KNOWLEDGE\nPOWER"],
        "entertainment": ["JOIN THE\nFUN", "LET'S\nPARTY", "EXPERIENCE\nMORE"],
    }
    
    if industry in industry_headlines:
        return random.choice(industry_headlines[industry])
    
    # Generic headlines
    return random.choice([
        "DISCOVER\nMORE", "QUALITY\nFIRST", "START\nTODAY", "MAKE IT\nHAPPEN"
    ])


def generate_subheadline_from_prompt(analysis: Dict[str, Any], headline: str) -> str:
    """Generate a contextual subheadline"""
    
    brand = analysis.get("brand_name")
    industry = analysis.get("industry", "general")
    is_sale = analysis.get("is_sale", False)
    
    if is_sale:
        return random.choice([
            "Limited time offer - Shop now!",
            "Don't miss out on these savings",
            "While supplies last",
            "Exclusive deals just for you",
        ])
    
    industry_subs = {
        "coffee": ["Crafted with passion", "Premium beans, perfect taste", "Your daily ritual, elevated"],
        "food": ["Made fresh with love", "Quality ingredients, amazing taste", "Where flavor meets quality"],
        "fashion": ["Style that speaks", "Curated for you", "Elevate your wardrobe"],
        "tech": ["Innovation at its best", "Built for the future", "Smart solutions for you"],
        "fitness": ["Your journey starts here", "Results you can see", "Push your limits"],
        "beauty": ["Reveal your glow", "Nature meets science", "Beauty from within"],
        "travel": ["Adventure awaits", "Create memories", "Explore the world"],
    }
    
    if industry in industry_subs:
        return random.choice(industry_subs[industry])
    
    if brand:
        return f"Experience the {brand} difference"
    
    return random.choice([
        "Quality you can trust",
        "Excellence in every detail",
        "Made for you",
        "Your satisfaction guaranteed",
    ])


def generate_cta_from_prompt(analysis: Dict[str, Any]) -> str:
    """Generate a contextual CTA"""
    
    is_sale = analysis.get("is_sale", False)
    industry = analysis.get("industry", "general")
    is_launch = analysis.get("is_launch", False)
    
    if is_sale:
        return random.choice(["Shop Sale", "Get Deal", "Save Now", "Claim Offer"])
    
    if is_launch:
        return random.choice(["Pre-Order", "Get Early Access", "Join Waitlist", "Learn More"])
    
    industry_ctas = {
        "coffee": ["Order Now", "Visit Us", "Find a Café", "Get Your Cup"],
        "food": ["Order Now", "View Menu", "Book Table", "Get Delivery"],
        "fashion": ["Shop Now", "View Collection", "Buy Now", "Explore"],
        "tech": ["Get Started", "Try Free", "Download", "Learn More"],
        "fitness": ["Join Now", "Start Free Trial", "Book Class", "Get Fit"],
        "beauty": ["Shop Now", "Try Now", "Get Yours", "Discover"],
        "travel": ["Book Now", "Explore Deals", "Plan Trip", "Get Quote"],
    }
    
    if industry in industry_ctas:
        return random.choice(industry_ctas[industry])
    
    return random.choice(["Get Started", "Learn More", "Shop Now", "Contact Us"])


def select_palette(analysis: Dict[str, Any]) -> Dict:
    """Select appropriate color palette based on analysis"""
    
    # If user specified a color hint, use it
    if analysis.get("color_hint") and analysis["color_hint"] in PALETTES:
        return PALETTES[analysis["color_hint"]]
    
    # Map moods to palettes
    mood_palettes = {
        "luxury": "luxury",
        "playful": "gradient_pop",
        "urgent": "bold",
        "minimal": "minimal",
        "bold": "bold",
        "warm": "warm",
        "cool": "cool",
    }
    
    mood = analysis.get("mood", "professional")
    if mood in mood_palettes:
        return PALETTES[mood_palettes[mood]]
    
    # Map industries to palettes
    industry_palettes = {
        "coffee": "warm",
        "food": "vibrant",
        "fashion": "luxury",
        "tech": "neon",
        "fitness": "bold",
        "beauty": "pink",
        "travel": "cool",
        "real_estate": "minimal",
        "education": "cool",
        "finance": "luxury",
        "entertainment": "gradient_pop",
    }
    
    industry = analysis.get("industry", "general")
    if industry in industry_palettes:
        return PALETTES[industry_palettes[industry]]
    
    # Random fallback
    return random.choice(list(PALETTES.values()))


# =============================================================================
# MAIN DESIGN GENERATOR
# =============================================================================

def generate_smart_design(prompt: str, platform: str = "instagram", 
                          format: str = "post") -> Dict[str, Any]:
    """
    Generate a TRULY UNIQUE design based on analyzing the user's prompt.
    This reads and understands the prompt to create relevant designs.
    """
    
    # Analyze the prompt deeply
    analysis = analyze_prompt(prompt)
    
    print(f"📊 Prompt Analysis: {analysis}")
    
    # Generate contextual content
    headline = generate_headline_from_prompt(analysis, prompt)
    subheadline = generate_subheadline_from_prompt(analysis, headline)
    cta_text = generate_cta_from_prompt(analysis)
    
    # Select appropriate palette
    palette = select_palette(analysis)
    
    # Canvas size
    FORMAT_SIZES = {
        "post": (1080, 1080), "square": (1080, 1080),
        "story": (1080, 1920), "reel": (1080, 1920),
        "landscape": (1200, 628), "portrait": (1080, 1350),
    }
    width, height = FORMAT_SIZES.get(format.lower(), (1080, 1080))
    
    # Build elements
    elements = []
    
    # Random seed for variety in layout
    seed = hash(prompt) % 10000
    random.seed(seed)
    
    # Layout variations
    layout_type = seed % 4  # 0=left, 1=center, 2=right, 3=bottom
    
    # 1. BACKGROUND DECORATIVE SHAPES
    # Large glow circles
    glow_x = random.randint(-20, 10) if layout_type != 2 else random.randint(60, 90)
    glow_y = random.randint(-20, 20)
    elements.append({
        "type": "shape", "shape_type": "circle",
        "position": {"x": glow_x, "y": glow_y},
        "size": {"width": 50, "height": 50},
        "fill_color": palette["accent"],
        "opacity": 0.1,
    })
    
    glow_x2 = random.randint(60, 90) if layout_type != 2 else random.randint(-10, 20)
    glow_y2 = random.randint(50, 80)
    elements.append({
        "type": "shape", "shape_type": "circle",
        "position": {"x": glow_x2, "y": glow_y2},
        "size": {"width": 40, "height": 40},
        "fill_color": palette["accent2"],
        "opacity": 0.12,
    })
    
    # 2. OVERLAY
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 0, "y": 0},
        "size": {"width": 100, "height": 100},
        "fill_color": "#000000",
        "opacity": 0.2 + random.random() * 0.1,
    })
    
    # 3. Decorative dots
    for i in range(4 + seed % 4):
        elements.append({
            "type": "shape", "shape_type": "circle",
            "position": {"x": 5 + (seed + i * 17) % 85, "y": 5 + (seed + i * 23) % 85},
            "size": {"width": 2 + i % 3, "height": 2 + i % 3},
            "fill_color": palette["accent"] if i % 2 == 0 else palette["accent2"],
            "opacity": 0.3 + (i % 3) * 0.1,
        })
    
    # 4. Corner accents
    if seed % 3 == 0:
        # L-shaped corners
        elements.extend([
            {"type": "shape", "shape_type": "rect", "position": {"x": 5, "y": 5}, "size": {"width": 12, "height": 0.4}, "fill_color": palette["accent"], "opacity": 0.7},
            {"type": "shape", "shape_type": "rect", "position": {"x": 5, "y": 5}, "size": {"width": 0.4, "height": 12}, "fill_color": palette["accent"], "opacity": 0.7},
            {"type": "shape", "shape_type": "rect", "position": {"x": 83, "y": 95}, "size": {"width": 12, "height": 0.4}, "fill_color": palette["accent"], "opacity": 0.7},
            {"type": "shape", "shape_type": "rect", "position": {"x": 95, "y": 83}, "size": {"width": 0.4, "height": 12}, "fill_color": palette["accent"], "opacity": 0.7},
        ])
    elif seed % 3 == 1:
        # Circle corners
        elements.extend([
            {"type": "shape", "shape_type": "circle", "position": {"x": 5, "y": 5}, "size": {"width": 8, "height": 8}, "fill_color": palette["accent"], "opacity": 0.3},
            {"type": "shape", "shape_type": "circle", "position": {"x": 87, "y": 87}, "size": {"width": 8, "height": 8}, "fill_color": palette["accent"], "opacity": 0.3},
        ])
    
    # 5. BADGE (if sale or launch)
    if analysis.get("is_sale") or analysis.get("is_launch"):
        badge_text = analysis.get("offer") or ("NEW" if analysis.get("is_launch") else "SALE")
        badge_x = 65 if layout_type in [0, 3] else 6
        elements.append({
            "type": "shape", "shape_type": "rect",
            "position": {"x": badge_x, "y": 6},
            "size": {"width": 28, "height": 5.5},
            "fill_color": palette["accent"],
            "corner_radius": 25,
        })
        elements.append({
            "type": "text",
            "position": {"x": badge_x, "y": 6.8},
            "size": {"width": 28, "height": 4},
            "content": badge_text,
            "font_size": 14,
            "font_weight": 700,
            "font_family": "Inter",
            "color": palette["text_dark"],
            "align": "center",
        })
    
    # 6. BRAND NAME (if detected)
    brand_name = analysis.get("brand_name")
    headline_y = 32
    if brand_name:
        headline_y = 38
        brand_x = 8 if layout_type in [0, 3] else (25 if layout_type == 1 else 40)
        elements.append({
            "type": "text",
            "position": {"x": brand_x, "y": 22},
            "size": {"width": 60, "height": 6},
            "content": brand_name.upper(),
            "font_size": 16,
            "font_weight": 600,
            "font_family": "Inter",
            "color": palette["accent"],
            "align": "left" if layout_type == 0 else ("center" if layout_type == 1 else "right"),
            "letter_spacing": 4,
        })
    
    # 7. MAIN HEADLINE
    headline_x = 8 if layout_type == 0 else (10 if layout_type == 1 else 30)
    headline_w = 60 if layout_type in [0, 2] else 80
    headline_align = "left" if layout_type == 0 else ("center" if layout_type == 1 else "right")
    
    if layout_type == 3:  # Bottom heavy
        headline_y = 50
    
    elements.append({
        "type": "text",
        "position": {"x": headline_x, "y": headline_y},
        "size": {"width": headline_w, "height": 25},
        "content": headline,
        "font_size": 68 + seed % 12,
        "font_weight": 900,
        "font_family": "Montserrat",
        "color": palette["text"],
        "align": headline_align,
        "line_height": 0.95,
        "letter_spacing": -1,
    })
    
    # 8. ACCENT LINE
    line_y = headline_y + 27
    line_x = headline_x if headline_align == "left" else (40 if headline_align == "center" else 60)
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": line_x, "y": line_y},
        "size": {"width": 18, "height": 0.8},
        "fill_color": palette["accent"],
    })
    
    # 9. SUBHEADLINE
    sub_y = line_y + 4
    elements.append({
        "type": "text",
        "position": {"x": headline_x, "y": sub_y},
        "size": {"width": headline_w, "height": 8},
        "content": subheadline,
        "font_size": 18 + seed % 4,
        "font_weight": 400,
        "font_family": "Inter",
        "color": palette["text"],
        "align": headline_align,
        "opacity": 0.9,
    })
    
    # 10. CTA BUTTON
    cta_y = sub_y + 15
    cta_x = headline_x if headline_align != "right" else 50
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": cta_x, "y": cta_y},
        "size": {"width": 35, "height": 9},
        "fill_color": palette["accent"],
        "corner_radius": 6 + seed % 4,
    })
    elements.append({
        "type": "text",
        "position": {"x": cta_x, "y": cta_y + 2},
        "size": {"width": 35, "height": 5},
        "content": cta_text.upper(),
        "font_size": 15,
        "font_weight": 700,
        "font_family": "Inter",
        "color": palette["text_dark"],
        "align": "center",
        "letter_spacing": 1,
    })
    
    # 11. Industry icon/emoji
    industry_icons = {
        "coffee": "☕", "food": "🍽️", "fashion": "✨", "tech": "💻",
        "fitness": "💪", "beauty": "✨", "travel": "✈️", "entertainment": "🎉",
        "real_estate": "🏠", "education": "📚", "finance": "💰",
    }
    icon = industry_icons.get(analysis.get("industry"), "⭐")
    icon_x = 70 if layout_type in [0, 3] else (75 if layout_type == 1 else 10)
    icon_y = 40 if layout_type != 3 else 20
    elements.append({
        "type": "text",
        "position": {"x": icon_x, "y": icon_y},
        "size": {"width": 15, "height": 15},
        "content": icon,
        "font_size": 56,
        "align": "center",
        "opacity": 0.85,
    })
    
    # Build blueprint
    gradient_angle = 120 + seed % 90
    
    blueprint = {
        "metadata": {
            "platform": platform,
            "format": format,
            "width": width,
            "height": height,
            "industry": analysis.get("industry", "general"),
            "brand": analysis.get("brand_name"),
            "is_sale": analysis.get("is_sale", False),
            "mood": analysis.get("mood", "professional"),
            "layout_type": ["left", "center", "right", "bottom"][layout_type],
            "elements_count": len(elements),
        },
        "background": {
            "type": "gradient",
            "colors": palette["bg"],
            "angle": gradient_angle,
            "color": palette["bg"][0],
        },
        "headline": headline,
        "subheadline": subheadline,
        "cta": cta_text,
        "brand_name": brand_name,
        "elements": elements,
        "color_palette": {
            "primary": palette["accent"],
            "secondary": palette["accent2"],
            "text": palette["text"],
        },
        "analysis": analysis,
    }
    
    return blueprint


def smart_blueprint_to_fabric(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """Convert blueprint to Fabric.js format"""
    
    width = blueprint["metadata"]["width"]
    height = blueprint["metadata"]["height"]
    fabric_objects = []
    
    # Background gradient
    bg = blueprint.get("background", {})
    colors = bg.get("colors", ["#1a1a2e", "#16213e", "#0f3460"])
    angle = bg.get("angle", 135)
    
    rad = math.radians(angle)
    cx, cy = width / 2, height / 2
    length = max(width, height) * 1.5
    x1 = cx - math.cos(rad) * length / 2
    y1 = cy - math.sin(rad) * length / 2
    x2 = cx + math.cos(rad) * length / 2
    y2 = cy + math.sin(rad) * length / 2
    
    color_stops = []
    for i, color in enumerate(colors):
        offset = i / (len(colors) - 1) if len(colors) > 1 else 0
        color_stops.append({"offset": offset, "color": color})
    
    fabric_objects.append({
        "type": "rect",
        "left": 0, "top": 0,
        "width": width, "height": height,
        "fill": {
            "type": "linear",
            "coords": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            "colorStops": color_stops,
        },
        "selectable": False, "evented": False,
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
                "left": left, "top": top,
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
            obj = {
                "id": f"shape_{idx}",
                "left": left, "top": top,
                "fill": element.get("fill_color", "#8B5CF6"),
                "opacity": element.get("opacity", 1),
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
            
            fabric_objects.append(obj)
    
    return {
        "version": "5.3.0",
        "objects": fabric_objects,
        "background": bg.get("color", colors[0]),
    }
