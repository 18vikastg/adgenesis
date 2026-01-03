"""
PREMIUM GRAPHIC DESIGN GENERATOR for AdGenesis
Creates UNIQUE, agency-quality designs with HIGH VARIETY for each prompt
"""

import random
import hashlib
from typing import Dict, List, Any, Optional
import re
import math

# =============================================================================
# DIVERSE COLOR PALETTES - Each prompt gets different colors
# =============================================================================

ALL_PALETTES = [
    {
        "id": "coffee_warm",
        "name": "Warm Coffee",
        "bg_gradient": ["#1A0F0A", "#3D2314", "#5C3D2E"],
        "accent1": "#D4A574", "accent2": "#E8C4A0", "accent3": "#F5DEB3",
        "highlight": "#FFD700", "text_light": "#FFF8F0", "text_dark": "#1A0F0A",
        "glow": "#D4A574", "shapes": ["#8B5E34", "#A67B5B", "#C49A6C"],
    },
    {
        "id": "neon_cyber",
        "name": "Cyber Neon",
        "bg_gradient": ["#0A0A1A", "#0F0F2D", "#1A1A3E"],
        "accent1": "#00F5FF", "accent2": "#8B5CF6", "accent3": "#FF10F0",
        "highlight": "#39FF14", "text_light": "#FFFFFF", "text_dark": "#0A0A1A",
        "glow": "#00F5FF", "shapes": ["#6366F1", "#8B5CF6", "#A78BFA"],
    },
    {
        "id": "luxury_gold",
        "name": "Luxury Gold",
        "bg_gradient": ["#0D0D0D", "#1A1A1A", "#262626"],
        "accent1": "#D4AF37", "accent2": "#FFD700", "accent3": "#F5E6A3",
        "highlight": "#FFFFFF", "text_light": "#FFFFFF", "text_dark": "#0D0D0D",
        "glow": "#D4AF37", "shapes": ["#8B7355", "#A08C5B", "#B5A167"],
    },
    {
        "id": "sunset_orange",
        "name": "Sunset Vibes",
        "bg_gradient": ["#7C2D12", "#9A3412", "#C2410C"],
        "accent1": "#FED7AA", "accent2": "#FDBA74", "accent3": "#FB923C",
        "highlight": "#FBBF24", "text_light": "#FFF7ED", "text_dark": "#431407",
        "glow": "#FB923C", "shapes": ["#EA580C", "#F97316", "#FB923C"],
    },
    {
        "id": "power_red",
        "name": "Power Red",
        "bg_gradient": ["#0F0F0F", "#1A1A1A", "#262626"],
        "accent1": "#EF4444", "accent2": "#F97316", "accent3": "#FACC15",
        "highlight": "#22C55E", "text_light": "#FFFFFF", "text_dark": "#0F0F0F",
        "glow": "#EF4444", "shapes": ["#DC2626", "#EF4444", "#F87171"],
    },
    {
        "id": "pink_glow",
        "name": "Pink Glow",
        "bg_gradient": ["#4A1942", "#6B2158", "#831843"],
        "accent1": "#F9A8D4", "accent2": "#F472B6", "accent3": "#EC4899",
        "highlight": "#FDF4FF", "text_light": "#FDF2F8", "text_dark": "#4A1942",
        "glow": "#F472B6", "shapes": ["#BE185D", "#DB2777", "#EC4899"],
    },
    {
        "id": "ocean_blue",
        "name": "Ocean Blue",
        "bg_gradient": ["#0C4A6E", "#0369A1", "#0284C7"],
        "accent1": "#38BDF8", "accent2": "#7DD3FC", "accent3": "#BAE6FD",
        "highlight": "#FDE047", "text_light": "#F0F9FF", "text_dark": "#0C4A6E",
        "glow": "#38BDF8", "shapes": ["#0EA5E9", "#38BDF8", "#7DD3FC"],
    },
    {
        "id": "instagram_pop",
        "name": "Instagram Pop",
        "bg_gradient": ["#833AB4", "#FD1D1D", "#F77737"],
        "accent1": "#FFFFFF", "accent2": "#FCAF45", "accent3": "#FFE5B4",
        "highlight": "#FFFFFF", "text_light": "#FFFFFF", "text_dark": "#262626",
        "glow": "#FCAF45", "shapes": ["#E1306C", "#F77737", "#FCAF45"],
    },
    {
        "id": "minimal_light",
        "name": "Minimal Light",
        "bg_gradient": ["#FAFAFA", "#F5F5F5", "#E5E5E5"],
        "accent1": "#18181B", "accent2": "#3F3F46", "accent3": "#71717A",
        "highlight": "#EF4444", "text_light": "#FAFAFA", "text_dark": "#18181B",
        "glow": "#3F3F46", "shapes": ["#27272A", "#3F3F46", "#52525B"],
    },
    {
        "id": "forest_green",
        "name": "Forest Green",
        "bg_gradient": ["#052E16", "#14532D", "#166534"],
        "accent1": "#86EFAC", "accent2": "#4ADE80", "accent3": "#22C55E",
        "highlight": "#FDE047", "text_light": "#F0FDF4", "text_dark": "#052E16",
        "glow": "#4ADE80", "shapes": ["#16A34A", "#22C55E", "#4ADE80"],
    },
    {
        "id": "purple_dream",
        "name": "Purple Dream",
        "bg_gradient": ["#1E1B4B", "#312E81", "#4338CA"],
        "accent1": "#C4B5FD", "accent2": "#A78BFA", "accent3": "#8B5CF6",
        "highlight": "#F472B6", "text_light": "#EDE9FE", "text_dark": "#1E1B4B",
        "glow": "#A78BFA", "shapes": ["#6366F1", "#7C3AED", "#8B5CF6"],
    },
    {
        "id": "teal_fresh",
        "name": "Fresh Teal",
        "bg_gradient": ["#042F2E", "#134E4A", "#115E59"],
        "accent1": "#5EEAD4", "accent2": "#2DD4BF", "accent3": "#14B8A6",
        "highlight": "#FBBF24", "text_light": "#F0FDFA", "text_dark": "#042F2E",
        "glow": "#2DD4BF", "shapes": ["#0D9488", "#14B8A6", "#2DD4BF"],
    },
    {
        "id": "rose_elegant",
        "name": "Rose Elegant",
        "bg_gradient": ["#1C1917", "#292524", "#44403C"],
        "accent1": "#FDA4AF", "accent2": "#FB7185", "accent3": "#F43F5E",
        "highlight": "#FEF3C7", "text_light": "#FFF1F2", "text_dark": "#1C1917",
        "glow": "#FB7185", "shapes": ["#E11D48", "#F43F5E", "#FB7185"],
    },
    {
        "id": "amber_warm",
        "name": "Amber Warmth",
        "bg_gradient": ["#451A03", "#78350F", "#92400E"],
        "accent1": "#FCD34D", "accent2": "#FBBF24", "accent3": "#F59E0B",
        "highlight": "#FFFFFF", "text_light": "#FFFBEB", "text_dark": "#451A03",
        "glow": "#FBBF24", "shapes": ["#D97706", "#F59E0B", "#FBBF24"],
    },
    {
        "id": "slate_modern",
        "name": "Modern Slate",
        "bg_gradient": ["#020617", "#0F172A", "#1E293B"],
        "accent1": "#38BDF8", "accent2": "#818CF8", "accent3": "#C084FC",
        "highlight": "#22D3EE", "text_light": "#F8FAFC", "text_dark": "#020617",
        "glow": "#818CF8", "shapes": ["#6366F1", "#818CF8", "#A5B4FC"],
    },
]

# =============================================================================
# DIVERSE LAYOUT STYLES
# =============================================================================

LAYOUT_STYLES = [
    {
        "id": "hero_left",
        "name": "Hero Left",
        "headline_pos": {"x": 8, "y": 30}, "headline_size": {"w": 60, "h": 25},
        "sub_pos": {"x": 8, "y": 58}, "sub_size": {"w": 55, "h": 8},
        "cta_pos": {"x": 8, "y": 75}, "cta_size": {"w": 35, "h": 10},
        "accent_side": "right", "badge_pos": "top_left",
    },
    {
        "id": "centered_bold",
        "name": "Centered Bold",
        "headline_pos": {"x": 10, "y": 35}, "headline_size": {"w": 80, "h": 20},
        "sub_pos": {"x": 15, "y": 58}, "sub_size": {"w": 70, "h": 8},
        "cta_pos": {"x": 30, "y": 78}, "cta_size": {"w": 40, "h": 10},
        "accent_side": "both", "badge_pos": "top_center",
    },
    {
        "id": "bottom_heavy",
        "name": "Bottom Heavy",
        "headline_pos": {"x": 8, "y": 55}, "headline_size": {"w": 84, "h": 20},
        "sub_pos": {"x": 8, "y": 78}, "sub_size": {"w": 60, "h": 6},
        "cta_pos": {"x": 65, "y": 85}, "cta_size": {"w": 30, "h": 8},
        "accent_side": "top", "badge_pos": "top_right",
    },
    {
        "id": "split_diagonal",
        "name": "Split Diagonal",
        "headline_pos": {"x": 5, "y": 20}, "headline_size": {"w": 50, "h": 25},
        "sub_pos": {"x": 5, "y": 48}, "sub_size": {"w": 45, "h": 8},
        "cta_pos": {"x": 5, "y": 65}, "cta_size": {"w": 35, "h": 10},
        "accent_side": "diagonal", "badge_pos": "bottom_right",
    },
    {
        "id": "minimal_center",
        "name": "Minimal Center",
        "headline_pos": {"x": 15, "y": 40}, "headline_size": {"w": 70, "h": 15},
        "sub_pos": {"x": 20, "y": 58}, "sub_size": {"w": 60, "h": 6},
        "cta_pos": {"x": 35, "y": 72}, "cta_size": {"w": 30, "h": 8},
        "accent_side": "minimal", "badge_pos": "none",
    },
    {
        "id": "right_aligned",
        "name": "Right Aligned",
        "headline_pos": {"x": 30, "y": 30}, "headline_size": {"w": 65, "h": 22},
        "sub_pos": {"x": 35, "y": 55}, "sub_size": {"w": 60, "h": 8},
        "cta_pos": {"x": 55, "y": 75}, "cta_size": {"w": 38, "h": 10},
        "accent_side": "left", "badge_pos": "top_right",
    },
    {
        "id": "story_vertical",
        "name": "Story Vertical",
        "headline_pos": {"x": 8, "y": 25}, "headline_size": {"w": 84, "h": 18},
        "sub_pos": {"x": 8, "y": 45}, "sub_size": {"w": 84, "h": 6},
        "cta_pos": {"x": 20, "y": 85}, "cta_size": {"w": 60, "h": 8},
        "accent_side": "vertical", "badge_pos": "top_center",
    },
    {
        "id": "card_style",
        "name": "Card Style",
        "headline_pos": {"x": 12, "y": 32}, "headline_size": {"w": 76, "h": 18},
        "sub_pos": {"x": 12, "y": 52}, "sub_size": {"w": 76, "h": 8},
        "cta_pos": {"x": 25, "y": 70}, "cta_size": {"w": 50, "h": 10},
        "accent_side": "frame", "badge_pos": "floating",
    },
]

# =============================================================================
# DIVERSE HEADLINES BY CATEGORY
# =============================================================================

HEADLINES_BY_CATEGORY = {
    "coffee": [
        "BREW\nPERFECTION", "COFFEE\nCULTURE", "WAKE UP\nIN STYLE",
        "ARTISAN\nBREWS", "TASTE THE\nDIFFERENCE", "DAILY\nRITUAL",
        "ROASTED\nFRESH", "CAFÉ\nVIBES", "ESPRESSO\nYOURSELF",
    ],
    "tech": [
        "FUTURE\nIS HERE", "NEXT GEN\nTECH", "INNOVATE\nTODAY",
        "SMART\nSOLUTIONS", "POWER UP", "DIGITAL\nEVOLUTION",
        "CODE THE\nFUTURE", "TECH\nREDEFINED", "CONNECT\nSMARTER",
    ],
    "fashion": [
        "DEFINE\nLUXURY", "NEW\nCOLLECTION", "TIMELESS\nSTYLE",
        "ELEVATE\nYOUR LOOK", "PURE\nELEGANCE", "TREND\nSETTER",
        "WEAR YOUR\nSTORY", "STYLE\nSPEAKS", "BE BOLD",
    ],
    "food": [
        "TASTE\nPERFECTION", "FRESH &\nDELICIOUS", "SAVOR\nTHE MOMENT",
        "FLAVOR\nEXPLOSION", "CHEF'S\nSPECIAL", "FOOD IS\nLOVE",
        "EAT\nAMAZING", "FRESH\nDAILY", "DINE\nDIFFERENT",
    ],
    "fitness": [
        "UNLEASH\nPOWER", "STRONGER\nDAILY", "NO LIMITS",
        "TRANSFORM\nNOW", "PEAK\nPERFORMANCE", "TRAIN\nHARDER",
        "LEVEL UP", "BEAST\nMODE", "SWEAT\nSUCCEED",
    ],
    "beauty": [
        "GLOW\nDIFFERENT", "RADIANT\nBEAUTY", "PURE\nGLOW",
        "SKIN\nPERFECTION", "REVEAL\nYOU", "BEAUTY\nUNLOCKED",
        "SHINE\nBRIGHT", "NATURAL\nGLAM", "SELF LOVE",
    ],
    "travel": [
        "EXPLORE\nMORE", "ADVENTURE\nAWAITS", "DISCOVER\nPARADISE",
        "DREAM\nDESTINATIONS", "ESCAPE\nNOW", "WANDER\nOFTEN",
        "GO\nFARTHER", "TRAVEL\nFREE", "NEW\nHORIZONS",
    ],
    "sale": [
        "MEGA\nSALE", "BIG\nSAVINGS", "LIMITED\nTIME",
        "FLASH\nDEAL", "SAVE\nBIG", "HOT\nOFFER",
        "BEST\nPRICES", "GRAB IT\nNOW", "DON'T\nMISS OUT",
    ],
    "business": [
        "GROW\nYOUR BIZ", "SUCCESS\nSTARTS HERE", "SCALE\nUP",
        "BUILD\nEMPIRES", "LEAD THE\nMARKET", "BUSINESS\nELITE",
        "PROFIT\nMORE", "SMART\nMOVES", "WIN\nBIG",
    ],
    "default": [
        "DISCOVER\nNEW", "EXPERIENCE\nMORE", "THE BEST\nCHOICE",
        "QUALITY\nFIRST", "START\nTODAY", "MAKE IT\nHAPPEN",
        "BE\nDIFFERENT", "NEXT\nLEVEL", "CREATE\nIMPACT",
    ],
}

SUBHEADLINES = {
    "coffee": ["Premium Artisan Coffee", "Freshly Roasted Daily", "Handcrafted Excellence", "Where Coffee is Art", "Your Perfect Cup Awaits"],
    "tech": ["Revolutionary Technology", "Built for Tomorrow", "Experience Innovation", "The Smart Choice", "Powered by AI"],
    "fashion": ["Exclusive Designer Collection", "Luxury Redefined", "Where Fashion Meets Art", "Curated for Excellence", "Make a Statement"],
    "food": ["Fresh Ingredients Daily", "Crafted by Master Chefs", "Unforgettable Taste", "Quality You Can Taste", "Made with Love"],
    "fitness": ["Train Like a Champion", "Results Guaranteed", "Push Your Limits", "Your Fitness Journey", "Strength Within"],
    "beauty": ["Clinically Proven Results", "Nature Meets Science", "Luxury Skincare", "Your Natural Glow", "Feel Beautiful"],
    "travel": ["Unforgettable Experiences", "Your Perfect Getaway", "Create Lasting Memories", "Where Dreams Come True", "Adventure Calling"],
    "sale": ["Unbeatable Prices", "While Stocks Last", "Exclusive Offers", "Members Only", "Today Only"],
    "business": ["Trusted by Thousands", "Industry Leaders", "Results Driven", "Your Success Partner", "Expert Solutions"],
    "default": ["Experience Excellence", "Quality You Deserve", "Built for You", "Your Success, Our Priority", "Join the Journey"],
}

CTAS = {
    "coffee": ["Order Now", "Visit Us", "Try Our Blend", "Get 20% Off", "Book a Table", "Find Us"],
    "tech": ["Get Started", "Learn More", "Try Free", "Pre-Order", "Download Now", "Sign Up Free"],
    "fashion": ["Shop Now", "Explore", "View Collection", "Get 30% Off", "Shop the Look", "Buy Now"],
    "food": ["Order Now", "View Menu", "Book Table", "Get Delivery", "Try Today", "Reserve Now"],
    "fitness": ["Join Now", "Start Free", "Get Fit", "Sign Up", "Book Class", "Try Free Week"],
    "beauty": ["Shop Now", "Try Free", "Get Yours", "Save 25%", "Discover More", "Buy Now"],
    "travel": ["Book Now", "Explore Deals", "Plan Trip", "Save 40%", "Start Adventure", "Get Quote"],
    "sale": ["Shop Sale", "Grab Now", "Buy Today", "Claim Offer", "Add to Cart", "Get Deal"],
    "business": ["Get Started", "Contact Us", "Free Quote", "Book Demo", "Learn More", "Join Now"],
    "default": ["Get Started", "Learn More", "Shop Now", "Try Free", "Contact Us", "Sign Up"],
}

BADGES = {
    "coffee": ["☕ PREMIUM", "★ ARTISAN", "✦ FRESH ROAST", "● ORGANIC", "◆ LOCAL"],
    "tech": ["⚡ NEW", "🚀 FAST", "✦ AI POWERED", "★ #1 RATED", "● SECURE"],
    "fashion": ["✦ EXCLUSIVE", "★ LIMITED", "◆ PREMIUM", "● NEW IN", "✧ LUXURY"],
    "food": ["🔥 HOT", "★ FRESH", "✦ SPECIAL", "● POPULAR", "◆ CHEF'S PICK"],
    "fitness": ["💪 PRO", "⚡ POWER", "★ #1 RATED", "● RESULTS", "◆ ELITE"],
    "beauty": ["✦ NATURAL", "★ BESTSELLER", "◆ ORGANIC", "● CRUELTY FREE", "✧ GLOW"],
    "travel": ["✈ DEALS", "★ TOP RATED", "◆ EXCLUSIVE", "● HOT SPOT", "✦ FEATURED"],
    "sale": ["🔥 HOT DEAL", "⚡ FLASH", "★ BEST PRICE", "● LIMITED", "◆ SAVE BIG"],
    "business": ["★ TRUSTED", "✦ EXPERT", "◆ CERTIFIED", "● PRO", "⚡ FAST"],
    "default": ["★ PREMIUM", "✦ TRUSTED", "◆ QUALITY", "● NEW", "⚡ HOT"],
}

ICONS_BY_CATEGORY = {
    "coffee": ["☕", "✦", "●", "◆"],
    "tech": ["⚡", "◆", "▲", "●", "★"],
    "fashion": ["◆", "✦", "★", "●", "✧"],
    "food": ["●", "✦", "★", "◆", "🍽️"],
    "fitness": ["▲", "◆", "●", "★", "💪"],
    "beauty": ["✦", "◆", "●", "★", "✧"],
    "travel": ["✦", "◆", "▲", "●", "✈"],
    "sale": ["⚡", "★", "●", "◆", "🔥"],
    "business": ["◆", "★", "●", "▲", "✦"],
    "default": ["●", "◆", "✦", "★", "▲"],
}

INDUSTRY_EMOJIS = {
    "coffee": ["☕", "🫘", "☕"],
    "tech": ["💻", "🚀", "📱", "⚡"],
    "fashion": ["👗", "👠", "✨", "💎"],
    "food": ["🍽️", "🍕", "🍔", "🥗"],
    "fitness": ["💪", "🏋️", "🔥", "⚡"],
    "beauty": ["✨", "💄", "🌸", "💅"],
    "travel": ["✈️", "🌴", "🏖️", "🗺️"],
    "sale": ["🔥", "💥", "⚡", "🎉"],
    "business": ["📈", "💼", "🎯", "🏆"],
    "default": ["⭐", "✨", "🎯", "💡"],
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_prompt_hash(prompt: str) -> int:
    """Generate a hash from the prompt for consistent randomization"""
    return int(hashlib.md5(prompt.encode()).hexdigest(), 16)

def detect_category(prompt: str) -> str:
    """Detect category from prompt keywords"""
    prompt_lower = prompt.lower()
    
    keywords = {
        "coffee": ["coffee", "cafe", "café", "espresso", "latte", "brew", "roast", "barista", "cappuccino", "mocha"],
        "tech": ["tech", "software", "app", "digital", "ai", "smart", "startup", "saas", "cloud", "code", "developer"],
        "fashion": ["fashion", "style", "clothing", "wear", "collection", "luxury", "designer", "boutique", "outfit", "dress"],
        "food": ["food", "restaurant", "delivery", "menu", "taste", "chef", "cuisine", "eat", "delicious", "pizza", "burger"],
        "fitness": ["fitness", "gym", "workout", "training", "health", "exercise", "muscle", "protein", "sports", "yoga"],
        "beauty": ["beauty", "skincare", "cosmetic", "makeup", "glow", "skin", "cream", "serum", "spa", "facial"],
        "travel": ["travel", "vacation", "trip", "destination", "hotel", "flight", "adventure", "explore", "tourism", "beach"],
        "sale": ["sale", "discount", "offer", "deal", "save", "off", "promo", "clearance", "black friday", "flash"],
        "business": ["business", "corporate", "company", "enterprise", "b2b", "professional", "consulting", "agency"],
    }
    
    for category, kw_list in keywords.items():
        for kw in kw_list:
            if kw in prompt_lower:
                return category
    return "default"

def extract_brand_name(prompt: str) -> Optional[str]:
    """Extract brand name from prompt"""
    patterns = [
        r"(?:named|called|for|brand)\s+['\"]?([A-Z][a-zA-Z0-9']+(?:\s+[A-Z][a-zA-Z0-9']+)?)['\"]?",
        r"([A-Z][a-zA-Z']+(?:'s)?)\s+(?:coffee|shop|store|brand|business|company)",
        r"my\s+(?:brand|company|business|shop|store)\s+(?:named|called)?\s*['\"]?([A-Za-z][a-zA-Z0-9']+)['\"]?",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            name = match.group(1).strip().strip("'\"")
            if len(name) > 1:
                return name
    return None

def get_random_with_seed(items: list, seed: int, offset: int = 0) -> Any:
    """Get random item using seed for consistency"""
    idx = (seed + offset) % len(items)
    return items[idx]

# =============================================================================
# DECORATIVE ELEMENTS GENERATORS
# =============================================================================

def generate_background_shapes(palette: Dict, seed: int, style: str) -> List[Dict]:
    """Generate varied background decorative elements based on style"""
    shapes = []
    random.seed(seed)
    
    # Large glow circles (position varies)
    glow_positions = [
        [(-15, -15), (75, 70)],
        [(80, -10), (-10, 80)],
        [(50, -20), (20, 85)],
        [(-20, 50), (85, 20)],
    ]
    glow_pos = glow_positions[seed % len(glow_positions)]
    
    for i, (x, y) in enumerate(glow_pos):
        shapes.append({
            "type": "shape", "shape_type": "circle",
            "position": {"x": x, "y": y},
            "size": {"width": 45 + random.randint(0, 15), "height": 45 + random.randint(0, 15)},
            "fill_color": palette["glow"] if i == 0 else palette["accent2"],
            "opacity": 0.08 + random.random() * 0.05,
        })
    
    # Style-specific elements
    if style in ["hero_left", "right_aligned"]:
        # Vertical accent line
        shapes.append({
            "type": "shape", "shape_type": "rect",
            "position": {"x": 92 if style == "hero_left" else 5, "y": 20},
            "size": {"width": 0.6, "height": 60},
            "fill_color": palette["accent1"],
            "opacity": 0.5,
        })
    
    if style in ["centered_bold", "card_style"]:
        # Top and bottom accent lines
        shapes.append({
            "type": "shape", "shape_type": "rect",
            "position": {"x": 20, "y": 8},
            "size": {"width": 60, "height": 0.4},
            "fill_color": palette["accent1"],
            "opacity": 0.4,
        })
        shapes.append({
            "type": "shape", "shape_type": "rect",
            "position": {"x": 20, "y": 92},
            "size": {"width": 60, "height": 0.4},
            "fill_color": palette["accent1"],
            "opacity": 0.4,
        })
    
    # Random decorative dots
    num_dots = 4 + (seed % 4)
    for i in range(num_dots):
        x = 5 + ((seed + i * 17) % 85)
        y = 5 + ((seed + i * 23) % 85)
        shapes.append({
            "type": "shape", "shape_type": "circle",
            "position": {"x": x, "y": y},
            "size": {"width": 2 + (i % 3), "height": 2 + (i % 3)},
            "fill_color": palette["shapes"][i % len(palette["shapes"])],
            "opacity": 0.3 + (i % 3) * 0.1,
        })
    
    # Corner accents (varied by seed)
    corner_styles = seed % 4
    if corner_styles == 0:
        # L-shaped corners
        shapes.extend([
            {"type": "shape", "shape_type": "rect", "position": {"x": 5, "y": 5}, "size": {"width": 12, "height": 0.4}, "fill_color": palette["accent1"], "opacity": 0.7},
            {"type": "shape", "shape_type": "rect", "position": {"x": 5, "y": 5}, "size": {"width": 0.4, "height": 12}, "fill_color": palette["accent1"], "opacity": 0.7},
            {"type": "shape", "shape_type": "rect", "position": {"x": 83, "y": 95}, "size": {"width": 12, "height": 0.4}, "fill_color": palette["accent1"], "opacity": 0.7},
            {"type": "shape", "shape_type": "rect", "position": {"x": 95, "y": 83}, "size": {"width": 0.4, "height": 12}, "fill_color": palette["accent1"], "opacity": 0.7},
        ])
    elif corner_styles == 1:
        # Circle corners
        shapes.extend([
            {"type": "shape", "shape_type": "circle", "position": {"x": 5, "y": 5}, "size": {"width": 8, "height": 8}, "fill_color": palette["accent1"], "opacity": 0.3},
            {"type": "shape", "shape_type": "circle", "position": {"x": 87, "y": 87}, "size": {"width": 8, "height": 8}, "fill_color": palette["accent1"], "opacity": 0.3},
        ])
    elif corner_styles == 2:
        # Full frame
        shapes.extend([
            {"type": "shape", "shape_type": "rect", "position": {"x": 4, "y": 4}, "size": {"width": 92, "height": 0.3}, "fill_color": palette["accent1"], "opacity": 0.2},
            {"type": "shape", "shape_type": "rect", "position": {"x": 4, "y": 96}, "size": {"width": 92, "height": 0.3}, "fill_color": palette["accent1"], "opacity": 0.2},
            {"type": "shape", "shape_type": "rect", "position": {"x": 4, "y": 4}, "size": {"width": 0.3, "height": 92}, "fill_color": palette["accent1"], "opacity": 0.2},
            {"type": "shape", "shape_type": "rect", "position": {"x": 96, "y": 4}, "size": {"width": 0.3, "height": 92}, "fill_color": palette["accent1"], "opacity": 0.2},
        ])
    
    return shapes

def generate_accent_shapes(palette: Dict, seed: int, accent_side: str) -> List[Dict]:
    """Generate accent shapes on specified side"""
    shapes = []
    random.seed(seed + 100)
    
    if accent_side == "right":
        shapes.extend([
            {"type": "shape", "shape_type": "circle", "position": {"x": 65, "y": 25}, "size": {"width": 40, "height": 40}, "fill_color": palette["accent1"], "opacity": 0.12},
            {"type": "shape", "shape_type": "circle", "position": {"x": 72, "y": 32}, "size": {"width": 28, "height": 28}, "fill_color": palette["accent2"], "opacity": 0.1},
        ])
    elif accent_side == "left":
        shapes.extend([
            {"type": "shape", "shape_type": "circle", "position": {"x": -5, "y": 30}, "size": {"width": 35, "height": 35}, "fill_color": palette["accent1"], "opacity": 0.12},
            {"type": "shape", "shape_type": "circle", "position": {"x": 2, "y": 38}, "size": {"width": 22, "height": 22}, "fill_color": palette["accent2"], "opacity": 0.1},
        ])
    elif accent_side == "top":
        shapes.extend([
            {"type": "shape", "shape_type": "circle", "position": {"x": 50, "y": -15}, "size": {"width": 50, "height": 50}, "fill_color": palette["accent1"], "opacity": 0.1},
        ])
    elif accent_side == "diagonal":
        shapes.extend([
            {"type": "shape", "shape_type": "circle", "position": {"x": 70, "y": 60}, "size": {"width": 45, "height": 45}, "fill_color": palette["accent1"], "opacity": 0.15},
            {"type": "shape", "shape_type": "circle", "position": {"x": 78, "y": 68}, "size": {"width": 30, "height": 30}, "fill_color": palette["accent2"], "opacity": 0.12},
        ])
    elif accent_side == "both":
        shapes.extend([
            {"type": "shape", "shape_type": "circle", "position": {"x": -10, "y": 60}, "size": {"width": 30, "height": 30}, "fill_color": palette["accent1"], "opacity": 0.1},
            {"type": "shape", "shape_type": "circle", "position": {"x": 80, "y": 10}, "size": {"width": 30, "height": 30}, "fill_color": palette["accent2"], "opacity": 0.1},
        ])
    elif accent_side == "frame":
        # Inner frame effect
        shapes.extend([
            {"type": "shape", "shape_type": "rect", "position": {"x": 8, "y": 8}, "size": {"width": 84, "height": 84}, "fill_color": "#000000", "opacity": 0.3},
        ])
    
    return shapes

# =============================================================================
# MAIN DESIGN GENERATOR
# =============================================================================

def generate_premium_design(prompt: str, platform: str = "instagram", 
                            format: str = "post") -> Dict[str, Any]:
    """
    Generate a UNIQUE, premium graphic design.
    Each prompt generates a visually different design.
    """
    
    # Get seed from prompt for consistent but unique randomization
    seed = get_prompt_hash(prompt)
    random.seed(seed)
    
    # Detect category from prompt
    category = detect_category(prompt)
    
    # Select UNIQUE palette based on prompt seed
    palette_idx = seed % len(ALL_PALETTES)
    palette = ALL_PALETTES[palette_idx]
    
    # Select UNIQUE layout based on prompt seed
    layout_idx = (seed // 7) % len(LAYOUT_STYLES)
    layout = LAYOUT_STYLES[layout_idx]
    
    # Canvas size
    FORMAT_SIZES = {
        "post": (1080, 1080), "square": (1080, 1080),
        "story": (1080, 1920), "reel": (1080, 1920),
        "landscape": (1200, 628), "portrait": (1080, 1350),
    }
    width, height = FORMAT_SIZES.get(format.lower(), (1080, 1080))
    
    # Extract brand name
    brand_name = extract_brand_name(prompt)
    
    # Select content with seed for variety
    headlines = HEADLINES_BY_CATEGORY.get(category, HEADLINES_BY_CATEGORY["default"])
    headline = get_random_with_seed(headlines, seed, 0)
    
    subs = SUBHEADLINES.get(category, SUBHEADLINES["default"])
    subheadline = get_random_with_seed(subs, seed, 1)
    
    ctas = CTAS.get(category, CTAS["default"])
    cta_text = get_random_with_seed(ctas, seed, 2)
    
    badges = BADGES.get(category, BADGES["default"])
    badge_text = get_random_with_seed(badges, seed, 3)
    
    icons = ICONS_BY_CATEGORY.get(category, ICONS_BY_CATEGORY["default"])
    icon = get_random_with_seed(icons, seed, 4)
    
    emojis = INDUSTRY_EMOJIS.get(category, INDUSTRY_EMOJIS["default"])
    emoji = get_random_with_seed(emojis, seed, 5)
    
    # Build elements
    elements = []
    
    # 1. BACKGROUND DECORATIVE SHAPES
    elements.extend(generate_background_shapes(palette, seed, layout["id"]))
    
    # 2. OVERLAY for depth
    overlay_opacity = 0.2 + (seed % 3) * 0.05
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": 0, "y": 0},
        "size": {"width": 100, "height": 100},
        "fill_color": "#000000",
        "opacity": overlay_opacity,
    })
    
    # 3. ACCENT SHAPES
    elements.extend(generate_accent_shapes(palette, seed, layout["accent_side"]))
    
    # 4. BADGE (position varies by layout)
    badge_positions = {
        "top_left": {"x": 6, "y": 6},
        "top_center": {"x": 35, "y": 6},
        "top_right": {"x": 65, "y": 6},
        "bottom_right": {"x": 65, "y": 88},
        "floating": {"x": 75, "y": 15},
        "none": None,
    }
    badge_pos = badge_positions.get(layout["badge_pos"])
    if badge_pos:
        elements.append({
            "type": "shape", "shape_type": "rect",
            "position": badge_pos,
            "size": {"width": 28, "height": 5},
            "fill_color": palette["accent1"],
            "corner_radius": 25,
            "opacity": 0.95,
        })
        elements.append({
            "type": "text",
            "position": {"x": badge_pos["x"], "y": badge_pos["y"] + 0.5},
            "size": {"width": 28, "height": 4},
            "content": badge_text,
            "font_size": 13,
            "font_weight": 700,
            "font_family": "Inter",
            "color": palette["text_dark"],
            "align": "center",
            "letter_spacing": 1,
        })
    
    # 5. BRAND NAME (if detected)
    if brand_name:
        elements.append({
            "type": "text",
            "position": {"x": layout["headline_pos"]["x"], "y": layout["headline_pos"]["y"] - 10},
            "size": {"width": 60, "height": 5},
            "content": brand_name.upper(),
            "font_size": 15,
            "font_weight": 600,
            "font_family": "Inter",
            "color": palette["accent1"],
            "align": "left" if "left" in layout["id"] else "center",
            "letter_spacing": 4,
        })
    
    # 6. DECORATIVE ICON
    icon_y = layout["headline_pos"]["y"] - 5 if brand_name else layout["headline_pos"]["y"] - 8
    elements.append({
        "type": "text",
        "position": {"x": layout["headline_pos"]["x"], "y": icon_y},
        "size": {"width": 10, "height": 8},
        "content": icon,
        "font_size": 32,
        "color": palette["accent1"],
        "align": "left",
        "opacity": 0.7,
    })
    
    # 7. MAIN HEADLINE
    headline_align = "left"
    if "center" in layout["id"]:
        headline_align = "center"
    elif "right" in layout["id"]:
        headline_align = "right"
    
    elements.append({
        "type": "text",
        "position": layout["headline_pos"],
        "size": {"width": layout["headline_size"]["w"], "height": layout["headline_size"]["h"]},
        "content": headline,
        "font_size": 68 + (seed % 10),
        "font_weight": 900,
        "font_family": "Montserrat",
        "color": palette["text_light"],
        "align": headline_align,
        "line_height": 0.95,
        "letter_spacing": -1,
    })
    
    # 8. ACCENT LINE under headline
    line_y = layout["headline_pos"]["y"] + layout["headline_size"]["h"] + 2
    line_x = layout["headline_pos"]["x"]
    if headline_align == "center":
        line_x = 40
    elif headline_align == "right":
        line_x = 60
    
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": {"x": line_x, "y": line_y},
        "size": {"width": 18, "height": 0.8},
        "fill_color": palette["accent1"],
        "opacity": 1,
    })
    
    # 9. SUBHEADLINE
    elements.append({
        "type": "text",
        "position": layout["sub_pos"],
        "size": {"width": layout["sub_size"]["w"], "height": layout["sub_size"]["h"]},
        "content": subheadline,
        "font_size": 18 + (seed % 4),
        "font_weight": 400,
        "font_family": "Inter",
        "color": palette["text_light"],
        "align": headline_align,
        "opacity": 0.9,
    })
    
    # 10. FEATURE BADGES (vary by seed)
    if seed % 3 != 0:  # Show 2/3 of the time
        features = ["✓ Premium", "✓ Fast", "✓ Quality"]
        feature_y = layout["sub_pos"]["y"] + 10
        for i, feature in enumerate(features):
            fx = layout["headline_pos"]["x"] + (i * 25)
            if headline_align == "center":
                fx = 15 + (i * 25)
            elements.append({
                "type": "text",
                "position": {"x": fx, "y": feature_y},
                "size": {"width": 24, "height": 4},
                "content": feature,
                "font_size": 11,
                "font_weight": 500,
                "font_family": "Inter",
                "color": palette["accent1"],
                "align": "left",
                "opacity": 0.85,
            })
    
    # 11. CTA BUTTON
    elements.append({
        "type": "shape", "shape_type": "rect",
        "position": layout["cta_pos"],
        "size": {"width": layout["cta_size"]["w"], "height": layout["cta_size"]["h"]},
        "fill_color": palette["accent1"],
        "corner_radius": 6 + (seed % 4),
    })
    elements.append({
        "type": "text",
        "position": {"x": layout["cta_pos"]["x"], "y": layout["cta_pos"]["y"] + 2},
        "size": {"width": layout["cta_size"]["w"], "height": 6},
        "content": cta_text.upper(),
        "font_size": 15,
        "font_weight": 700,
        "font_family": "Inter",
        "color": palette["text_dark"],
        "align": "center",
        "letter_spacing": 2,
    })
    
    # 12. SECONDARY CTA (50% of designs)
    if seed % 2 == 0:
        sec_cta_x = layout["cta_pos"]["x"] + layout["cta_size"]["w"] + 5
        elements.append({
            "type": "text",
            "position": {"x": sec_cta_x, "y": layout["cta_pos"]["y"] + 2.5},
            "size": {"width": 25, "height": 5},
            "content": "Learn More →",
            "font_size": 13,
            "font_weight": 500,
            "font_family": "Inter",
            "color": palette["text_light"],
            "align": "left",
            "opacity": 0.75,
        })
    
    # 13. LARGE EMOJI/ICON
    emoji_x = 72 if layout["accent_side"] == "right" else 15
    emoji_y = 40 if layout["accent_side"] == "right" else 70
    elements.append({
        "type": "text",
        "position": {"x": emoji_x, "y": emoji_y},
        "size": {"width": 15, "height": 15},
        "content": emoji,
        "font_size": 64,
        "align": "center",
        "opacity": 0.85,
    })
    
    # Gradient angle varies by seed
    gradient_angle = 120 + (seed % 90)
    
    # Build blueprint
    blueprint = {
        "metadata": {
            "platform": platform,
            "format": format,
            "width": width,
            "height": height,
            "category": category,
            "layout": layout["name"],
            "palette": palette["name"],
            "design_quality": "premium_unique",
            "elements_count": len(elements),
            "seed": seed % 10000,
        },
        "background": {
            "type": "gradient",
            "colors": palette["bg_gradient"],
            "angle": gradient_angle,
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
    colors = bg.get("colors", ["#1a1a2e", "#16213e", "#0f3460"])
    angle = bg.get("angle", 135)
    
    # Calculate gradient coordinates
    rad = math.radians(angle)
    cx, cy = width / 2, height / 2
    length = max(width, height) * 1.5
    x1 = cx - math.cos(rad) * length / 2
    y1 = cy - math.sin(rad) * length / 2
    x2 = cx + math.cos(rad) * length / 2
    y2 = cy + math.sin(rad) * length / 2
    
    # Create color stops
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
