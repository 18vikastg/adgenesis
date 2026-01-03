"""
Modern Professional Design System for AdGenesis
Creates high-quality, advertising-ready poster designs
"""

import random
from typing import Dict, List, Any

# =============================================================================
# MODERN COLOR SCHEMES - Professional & Trendy
# =============================================================================

MODERN_COLOR_SCHEMES = {
    "tech_gradient": {
        "background": {"type": "gradient", "colors": ["#667eea", "#764ba2"], "angle": 135},
        "primary": "#667eea",
        "secondary": "#764ba2",
        "text_primary": "#FFFFFF",
        "text_secondary": "#E0E7FF",
        "accent": "#F59E0B",
        "overlay": "rgba(0, 0, 0, 0.3)"
    },
    "modern_minimal": {
        "background": {"type": "solid", "colors": ["#F8FAFC"]},
        "primary": "#0F172A",
        "secondary": "#334155",
        "text_primary": "#0F172A",
        "text_secondary": "#64748B",
        "accent": "#3B82F6",
        "overlay": "rgba(15, 23, 42, 0.05)"
    },
    "vibrant_energy": {
        "background": {"type": "gradient", "colors": ["#FF6B9D", "#C44569"], "angle": 45},
        "primary": "#FF6B9D",
        "secondary": "#C44569",
        "text_primary": "#FFFFFF",
        "text_secondary": "#FFF1F5",
        "accent": "#FDE68A",
        "overlay": "rgba(0, 0, 0, 0.2)"
    },
    "luxury_gold": {
        "background": {"type": "gradient", "colors": ["#1a1a2e", "#16213e"], "angle": 180},
        "primary": "#D4AF37",
        "secondary": "#FFD700",
        "text_primary": "#FFD700",
        "text_secondary": "#F5DEB3",
        "accent": "#FFFFFF",
        "overlay": "rgba(212, 175, 55, 0.1)"
    },
    "fresh_green": {
        "background": {"type": "gradient", "colors": ["#11998e", "#38ef7d"], "angle": 90},
        "primary": "#11998e",
        "secondary": "#38ef7d",
        "text_primary": "#FFFFFF",
        "text_secondary": "#E0FFF4",
        "accent": "#FCD34D",
        "overlay": "rgba(0, 0, 0, 0.25)"
    },
    "sunset_warm": {
        "background": {"type": "gradient", "colors": ["#FA8BFF", "#2BD2FF", "#2BFF88"], "angle": 120},
        "primary": "#FA8BFF",
        "secondary": "#2BD2FF",
        "text_primary": "#FFFFFF",
        "text_secondary": "#F3E8FF",
        "accent": "#FBBF24",
        "overlay": "rgba(0, 0, 0, 0.2)"
    },
    "corporate_blue": {
        "background": {"type": "gradient", "colors": ["#1E3A8A", "#3B82F6"], "angle": 135},
        "primary": "#3B82F6",
        "secondary": "#60A5FA",
        "text_primary": "#FFFFFF",
        "text_secondary": "#DBEAFE",
        "accent": "#F59E0B",
        "overlay": "rgba(0, 0, 0, 0.3)"
    },
    "neon_dark": {
        "background": {"type": "solid", "colors": ["#0A0A0A"]},
        "primary": "#00F5FF",
        "secondary": "#FF10F0",
        "text_primary": "#FFFFFF",
        "text_secondary": "#B0B0B0",
        "accent": "#39FF14",
        "overlay": "rgba(0, 245, 255, 0.1)"
    }
}

# =============================================================================
# MODERN LAYOUTS - Professional Grid-Based
# =============================================================================

MODERN_LAYOUTS = {
    "hero_split": {
        "name": "Hero Split",
        "description": "Bold headline on left, visual space on right",
        "headline": {"x": 8, "y": 30, "w": 45, "h": 25, "align": "left"},
        "subheadline": {"x": 8, "y": 58, "w": 40, "h": 12, "align": "left"},
        "body": {"x": 8, "y": 72, "w": 40, "h": 8, "align": "left"},
        "cta": {"x": 8, "y": 85, "w": 25, "h": 7, "align": "left"},
        "image_area": {"x": 55, "y": 15, "w": 40, "h": 70},
        "decoration": [
            {"type": "rect", "x": 0, "y": 0, "w": 50, "h": 100, "opacity": 0.05},
            {"type": "line", "x": 52, "y": 10, "w": 2, "h": 80, "opacity": 0.2}
        ]
    },
    "centered_hero": {
        "name": "Centered Hero",
        "description": "Central focal point with surrounding elements",
        "headline": {"x": 10, "y": 35, "w": 80, "h": 20, "align": "center"},
        "subheadline": {"x": 15, "y": 58, "w": 70, "h": 10, "align": "center"},
        "body": {"x": 20, "y": 70, "w": 60, "h": 8, "align": "center"},
        "cta": {"x": 35, "y": 82, "w": 30, "h": 7, "align": "center"},
        "decoration": [
            {"type": "circle", "x": 85, "y": 10, "w": 20, "h": 20, "opacity": 0.15},
            {"type": "circle", "x": -5, "y": 75, "w": 25, "h": 25, "opacity": 0.12},
            {"type": "rect", "x": 5, "y": 5, "w": 90, "h": 90, "opacity": 0, "stroke": 2}
        ]
    },
    "asymmetric_bold": {
        "name": "Asymmetric Bold",
        "description": "Off-center design for visual interest",
        "headline": {"x": 12, "y": 20, "w": 60, "h": 30, "align": "left"},
        "subheadline": {"x": 12, "y": 53, "w": 50, "h": 12, "align": "left"},
        "body": {"x": 12, "y": 68, "w": 45, "h": 10, "align": "left"},
        "cta": {"x": 12, "y": 82, "w": 30, "h": 8, "align": "left"},
        "decoration": [
            {"type": "rect", "x": 70, "y": 0, "w": 30, "h": 100, "opacity": 0.08},
            {"type": "circle", "x": 75, "y": 30, "w": 35, "h": 35, "opacity": 0.12}
        ]
    },
    "magazine_style": {
        "name": "Magazine Style",
        "description": "Editorial-inspired layout",
        "headline": {"x": 8, "y": 15, "w": 55, "h": 22, "align": "left"},
        "subheadline": {"x": 8, "y": 40, "w": 50, "h": 8, "align": "left"},
        "body": {"x": 8, "y": 50, "w": 45, "h": 15, "align": "left"},
        "cta": {"x": 8, "y": 70, "w": 28, "h": 7, "align": "left"},
        "image_area": {"x": 55, "y": 30, "w": 40, "h": 55},
        "decoration": [
            {"type": "line", "x": 8, "y": 12, "w": 15, "h": 0.5, "opacity": 0.8},
            {"type": "rect", "x": 0, "y": 0, "w": 100, "h": 3, "opacity": 0.1}
        ]
    },
    "minimal_modern": {
        "name": "Minimal Modern",
        "description": "Clean, spacious, modern",
        "headline": {"x": 10, "y": 40, "w": 80, "h": 18, "align": "center"},
        "subheadline": {"x": 20, "y": 62, "w": 60, "h": 8, "align": "center"},
        "body": {"x": 25, "y": 72, "w": 50, "h": 8, "align": "center"},
        "cta": {"x": 37.5, "y": 85, "w": 25, "h": 6, "align": "center"},
        "decoration": [
            {"type": "rect", "x": 10, "y": 35, "w": 80, "h": 0.3, "opacity": 0.2},
            {"type": "rect", "x": 10, "y": 90, "w": 80, "h": 0.3, "opacity": 0.2}
        ]
    },
    "impact_banner": {
        "name": "Impact Banner",
        "description": "Large text with striking visuals",
        "headline": {"x": 5, "y": 25, "w": 90, "h": 35, "align": "center"},
        "subheadline": {"x": 15, "y": 63, "w": 70, "h": 10, "align": "center"},
        "body": None,
        "cta": {"x": 32.5, "y": 78, "w": 35, "h": 9, "align": "center"},
        "decoration": [
            {"type": "rect", "x": 0, "y": 0, "w": 100, "h": 20, "opacity": 0.05},
            {"type": "rect", "x": 0, "y": 80, "w": 100, "h": 20, "opacity": 0.05}
        ]
    }
}

# =============================================================================
# MODERN TYPOGRAPHY
# =============================================================================

MODERN_FONTS = [
    {"name": "Inter", "weights": [400, 500, 600, 700, 800, 900], "style": "modern"},
    {"name": "Montserrat", "weights": [400, 600, 700, 800, 900], "style": "bold"},
    {"name": "Playfair Display", "weights": [400, 600, 700, 900], "style": "elegant"},
    {"name": "Poppins", "weights": [400, 500, 600, 700, 800], "style": "friendly"},
    {"name": "Bebas Neue", "weights": [400], "style": "impact"},
    {"name": "Space Grotesk", "weights": [400, 500, 600, 700], "style": "tech"},
]

# =============================================================================
# VISUAL EFFECTS & DECORATIONS
# =============================================================================

def generate_modern_decorations(color_scheme: Dict, layout_name: str, format_size: tuple) -> List[Dict]:
    """Generate modern visual decorations"""
    decorations = []
    width, height = format_size
    
    # Geometric shapes
    shapes = [
        # Corner accents
        {"type": "circle", "x": -5, "y": -5, "w": 20, "h": 20, "opacity": 0.15, "blur": 30},
        {"type": "circle", "x": 90, "y": 88, "w": 25, "h": 25, "opacity": 0.12, "blur": 40},
        
        # Grid lines (subtle)
        {"type": "line", "x": 10, "y": 0, "w": 0.2, "h": 100, "opacity": 0.05},
        {"type": "line", "x": 90, "y": 0, "w": 0.2, "h": 100, "opacity": 0.05},
        
        # Floating elements
        {"type": "rect", "x": 75, "y": 15, "w": 18, "h": 18, "opacity": 0.08, "rotation": 45},
        {"type": "circle", "x": 8, "y": 70, "w": 12, "h": 12, "opacity": 0.1},
        
        # Pattern overlay
        {"type": "dots_pattern", "opacity": 0.03},
    ]
    
    # Randomly select 3-5 decorations
    selected = random.sample(shapes[:6], k=random.randint(3, 5))
    return selected

# =============================================================================
# ENHANCED CONTENT GENERATION
# =============================================================================

MODERN_HEADLINES = {
    "tech": [
        "Transform Your Tomorrow",
        "Innovation Starts Here",
        "Power Your Vision",
        "Built for the Future",
        "Elevate Your Experience",
        "Where Ideas Come Alive",
        "Redefine Possible"
    ],
    "sale": [
        "Unmissable Deals Inside",
        "Your Best Price Ever",
        "Shop Smarter, Save Bigger",
        "Limited Time Magic",
        "The Sale You've Waited For",
        "Exclusive Offers Await"
    ],
    "fashion": [
        "Style Redefined",
        "Wear Your Confidence",
        "Elegance Meets Edge",
        "Your Signature Look",
        "Fashion Forward",
        "Curated for You"
    ],
    "fitness": [
        "Unleash Your Strength",
        "Transform Your Body",
        "Be Unstoppable",
        "Your Journey Begins",
        "Power Through Limits",
        "Achieve the Extraordinary"
    ],
    "food": [
        "Taste the Difference",
        "Flavor Beyond Imagination",
        "Fresh. Bold. Delicious.",
        "Your Next Craving",
        "Culinary Excellence",
        "Savor Every Moment"
    ],
    "business": [
        "Success Delivered",
        "Your Growth Partner",
        "Results That Matter",
        "Excellence in Action",
        "Strategic Solutions",
        "Empowering Your Success"
    ],
    "default": [
        "Experience the Difference",
        "Your Perfect Choice",
        "Discover Something Amazing",
        "Make It Happen",
        "Join the Movement",
        "Start Your Journey"
    ]
}

MODERN_SUBHEADLINES = {
    "tech": [
        "Powered by cutting-edge technology",
        "Join 100,000+ innovators worldwide",
        "The future is now, and it's yours",
        "Transform how you work and create"
    ],
    "sale": [
        "Up to 70% off your favorite brands",
        "Free shipping on all orders today",
        "Limited stock • Shop before it's gone",
        "Exclusive member pricing unlocked"
    ],
    "fashion": [
        "New collection • Limited edition",
        "Handpicked styles just for you",
        "From runway to your wardrobe",
        "Timeless pieces, modern prices"
    ],
    "fitness": [
        "Proven results in 30 days",
        "Train with champion athletes",
        "Your personalized fitness journey",
        "Science-backed, results-driven"
    ],
    "food": [
        "Made fresh daily with love",
        "Farm-to-table quality guaranteed",
        "Award-winning flavors await",
        "Local ingredients, global inspiration"
    ],
    "business": [
        "Trusted by industry leaders",
        "Scale faster, work smarter",
        "ROI guaranteed or money back",
        "Join 50,000+ successful companies"
    ],
    "default": [
        "Limited time offer • Act now",
        "Join thousands of happy customers",
        "Quality you can trust",
        "Get started in minutes"
    ]
}

MODERN_CTAS = [
    "Get Started Free",
    "Shop Now",
    "Learn More",
    "Join Today",
    "Claim Offer",
    "Explore Collection",
    "Start Free Trial",
    "Book Appointment",
    "Download Now",
    "See How It Works",
    "Try Risk-Free",
    "Unlock Access"
]

def detect_category(prompt: str) -> str:
    """Detect category from prompt"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['tech', 'ai', 'software', 'app', 'digital', 'startup']):
        return 'tech'
    elif any(word in prompt_lower for word in ['sale', 'discount', 'offer', 'deal', 'save']):
        return 'sale'
    elif any(word in prompt_lower for word in ['fashion', 'clothing', 'wear', 'style', 'outfit']):
        return 'fashion'
    elif any(word in prompt_lower for word in ['fitness', 'gym', 'workout', 'health', 'exercise']):
        return 'fitness'
    elif any(word in prompt_lower for word in ['food', 'restaurant', 'cafe', 'meal', 'recipe']):
        return 'food'
    elif any(word in prompt_lower for word in ['business', 'corporate', 'company', 'enterprise']):
        return 'business'
    
    return 'default'
