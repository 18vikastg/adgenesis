"""
Professional Poster Templates - Canva-like High-Quality Designs
"""

import random
import re
from typing import Dict, List, Any

# Professional Color Palettes
COLOR_PALETTES = {
    "tech_dark": {
        "background": "linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%)",
        "primary": "#3b82f6",
        "secondary": "#60a5fa",
        "text": "#ffffff",
        "accent": "#818cf8",
        "muted": "#94a3b8"
    },
    "tech_light": {
        "background": "linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%)",
        "primary": "#0284c7",
        "secondary": "#0ea5e9",
        "text": "#0c4a6e",
        "accent": "#06b6d4",
        "muted": "#64748b"
    },
    "fashion_vibrant": {
        "background": "linear-gradient(135deg, #ff6b9d 0%, #ff8fab 50%, #ffc2d1 100%)",
        "primary": "#ffffff",
        "secondary": "#ffe66d",
        "text": "#ffffff",
        "accent": "#ff1744",
        "muted": "#ffc2d1"
    },
    "fashion_minimal": {
        "background": "#faf5f0",
        "primary": "#1a1a1a",
        "secondary": "#8b7355",
        "text": "#1a1a1a",
        "accent": "#d4a574",
        "muted": "#a89984"
    },
    "sale_urgent": {
        "background": "linear-gradient(135deg, #dc2626 0%, #ef4444 50%, #f87171 100%)",
        "primary": "#fbbf24",
        "secondary": "#ffffff",
        "text": "#ffffff",
        "accent": "#fef08a",
        "muted": "#fca5a5"
    },
    "sale_black_friday": {
        "background": "#000000",
        "primary": "#fbbf24",
        "secondary": "#f59e0b",
        "text": "#ffffff",
        "accent": "#ef4444",
        "muted": "#71717a"
    },
    "business_corporate": {
        "background": "linear-gradient(180deg, #1e3a5f 0%, #0a1929 100%)",
        "primary": "#fbbf24",
        "secondary": "#ffffff",
        "text": "#ffffff",
        "accent": "#3b82f6",
        "muted": "#94a3b8"
    },
    "business_modern": {
        "background": "#ffffff",
        "primary": "#1e40af",
        "secondary": "#3b82f6",
        "text": "#1e293b",
        "accent": "#06b6d4",
        "muted": "#64748b"
    },
    "food_warm": {
        "background": "linear-gradient(180deg, #fef3c7 0%, #fde68a 100%)",
        "primary": "#ef4444",
        "secondary": "#f97316",
        "text": "#78350f",
        "accent": "#22c55e",
        "muted": "#92400e"
    },
    "food_fresh": {
        "background": "linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%)",
        "primary": "#16a34a",
        "secondary": "#22c55e",
        "text": "#14532d",
        "accent": "#f97316",
        "muted": "#166534"
    },
    "wellness_calm": {
        "background": "linear-gradient(180deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%)",
        "primary": "#059669",
        "secondary": "#10b981",
        "text": "#064e3b",
        "accent": "#f59e0b",
        "muted": "#6b7280"
    },
    "luxury_gold": {
        "background": "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)",
        "primary": "#d4af37",
        "secondary": "#ffd700",
        "text": "#ffffff",
        "accent": "#b8860b",
        "muted": "#a3a3a3"
    },
    "creative_gradient": {
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
        "primary": "#ffffff",
        "secondary": "#fef08a",
        "text": "#ffffff",
        "accent": "#22d3ee",
        "muted": "#c4b5fd"
    },
    "minimalist_clean": {
        "background": "#ffffff",
        "primary": "#18181b",
        "secondary": "#3f3f46",
        "text": "#18181b",
        "accent": "#ef4444",
        "muted": "#a1a1aa"
    },
    "event_party": {
        "background": "linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #d946ef 100%)",
        "primary": "#ffffff",
        "secondary": "#fef08a",
        "text": "#ffffff",
        "accent": "#22d3ee",
        "muted": "#c4b5fd"
    },
    "education_bright": {
        "background": "linear-gradient(180deg, #dbeafe 0%, #bfdbfe 100%)",
        "primary": "#1d4ed8",
        "secondary": "#3b82f6",
        "text": "#1e3a8a",
        "accent": "#f59e0b",
        "muted": "#6b7280"
    }
}

# Professional Font Combinations
FONT_COMBOS = {
    "modern": {"heading": "Montserrat", "subheading": "Inter", "body": "Inter"},
    "classic": {"heading": "Playfair Display", "subheading": "Lora", "body": "Georgia"},
    "bold": {"heading": "Anton", "subheading": "Roboto", "body": "Roboto"},
    "elegant": {"heading": "Cormorant Garamond", "subheading": "Raleway", "body": "Raleway"},
    "tech": {"heading": "Space Grotesk", "subheading": "DM Sans", "body": "DM Sans"},
    "fun": {"heading": "Bebas Neue", "subheading": "Poppins", "body": "Poppins"},
    "minimal": {"heading": "Helvetica Neue", "subheading": "Arial", "body": "Arial"},
    "luxury": {"heading": "Didot", "subheading": "Futura", "body": "Futura"},
}

# Layout Templates
def create_hero_layout(width: int, height: int, palette: Dict, fonts: Dict, content: Dict) -> List[Dict]:
    """Hero layout with big headline at center"""
    elements = []
    
    # Decorative shape top
    elements.append({
        "type": "circle",
        "x": width * 0.8,
        "y": -height * 0.1,
        "width": width * 0.4,
        "height": width * 0.4,
        "color": palette["accent"],
        "opacity": 0.3
    })
    
    # Main headline
    elements.append({
        "type": "textbox",
        "text": content.get("headline", "YOUR HEADLINE HERE"),
        "x": width * 0.08,
        "y": height * 0.28,
        "width": width * 0.84,
        "fontSize": int(width * 0.085),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center",
        "lineHeight": 1.1
    })
    
    # Subheadline
    elements.append({
        "type": "textbox",
        "text": content.get("subheadline", "Supporting text goes here"),
        "x": width * 0.1,
        "y": height * 0.48,
        "width": width * 0.8,
        "fontSize": int(width * 0.032),
        "color": palette["muted"],
        "fontFamily": fonts["subheading"],
        "fontWeight": "normal",
        "textAlign": "center",
        "lineHeight": 1.4
    })
    
    # CTA Button
    btn_width = width * 0.4
    btn_height = height * 0.07
    btn_x = (width - btn_width) / 2
    btn_y = height * 0.62
    
    elements.append({
        "type": "rect",
        "x": btn_x,
        "y": btn_y,
        "width": btn_width,
        "height": btn_height,
        "color": palette["primary"],
        "borderRadius": 8,
        "shadow": True
    })
    
    elements.append({
        "type": "textbox",
        "text": content.get("cta", "GET STARTED"),
        "x": btn_x,
        "y": btn_y + btn_height * 0.25,
        "width": btn_width,
        "fontSize": int(width * 0.028),
        "color": "#ffffff" if palette["primary"] != "#ffffff" else "#000000",
        "fontFamily": fonts["body"],
        "fontWeight": "600",
        "textAlign": "center"
    })
    
    # Brand/Logo area
    elements.append({
        "type": "textbox",
        "text": content.get("brand", "BRAND"),
        "x": width * 0.35,
        "y": height * 0.82,
        "width": width * 0.3,
        "fontSize": int(width * 0.035),
        "color": palette["muted"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center",
        "letterSpacing": 4
    })
    
    return elements


def create_split_layout(width: int, height: int, palette: Dict, fonts: Dict, content: Dict) -> List[Dict]:
    """Split layout - left text, right decorative"""
    elements = []
    
    # Right side accent block
    elements.append({
        "type": "rect",
        "x": width * 0.55,
        "y": 0,
        "width": width * 0.45,
        "height": height,
        "color": palette["primary"],
        "opacity": 0.9
    })
    
    # Decorative circles
    elements.append({
        "type": "circle",
        "x": width * 0.65,
        "y": height * 0.2,
        "width": width * 0.25,
        "height": width * 0.25,
        "color": palette["accent"],
        "opacity": 0.5
    })
    
    elements.append({
        "type": "circle",
        "x": width * 0.75,
        "y": height * 0.55,
        "width": width * 0.15,
        "height": width * 0.15,
        "color": palette["secondary"],
        "opacity": 0.6
    })
    
    # Tag/Category
    elements.append({
        "type": "textbox",
        "text": content.get("tag", "FEATURED"),
        "x": width * 0.05,
        "y": height * 0.12,
        "width": width * 0.4,
        "fontSize": int(width * 0.022),
        "color": palette["accent"],
        "fontFamily": fonts["body"],
        "fontWeight": "600",
        "letterSpacing": 3
    })
    
    # Main headline
    elements.append({
        "type": "textbox",
        "text": content.get("headline", "Make Your\nMark"),
        "x": width * 0.05,
        "y": height * 0.2,
        "width": width * 0.48,
        "fontSize": int(width * 0.075),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "lineHeight": 1.05
    })
    
    # Description
    elements.append({
        "type": "textbox",
        "text": content.get("description", "Transform your ideas into reality with our powerful platform."),
        "x": width * 0.05,
        "y": height * 0.52,
        "width": width * 0.45,
        "fontSize": int(width * 0.026),
        "color": palette["muted"],
        "fontFamily": fonts["body"],
        "lineHeight": 1.5
    })
    
    # CTA Button
    btn_width = width * 0.28
    btn_height = height * 0.065
    
    elements.append({
        "type": "rect",
        "x": width * 0.05,
        "y": height * 0.72,
        "width": btn_width,
        "height": btn_height,
        "color": palette["primary"],
        "borderRadius": 6
    })
    
    elements.append({
        "type": "textbox",
        "text": content.get("cta", "Learn More"),
        "x": width * 0.05,
        "y": height * 0.72 + btn_height * 0.28,
        "width": btn_width,
        "fontSize": int(width * 0.024),
        "color": "#ffffff",
        "fontFamily": fonts["body"],
        "fontWeight": "600",
        "textAlign": "center"
    })
    
    # Brand
    elements.append({
        "type": "textbox",
        "text": content.get("brand", "BRAND"),
        "x": width * 0.05,
        "y": height * 0.88,
        "width": width * 0.3,
        "fontSize": int(width * 0.028),
        "color": palette["muted"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "letterSpacing": 2
    })
    
    return elements


def create_sale_layout(width: int, height: int, palette: Dict, fonts: Dict, content: Dict) -> List[Dict]:
    """Bold sale/discount layout"""
    elements = []
    
    # Top banner stripe
    elements.append({
        "type": "rect",
        "x": 0,
        "y": 0,
        "width": width,
        "height": height * 0.12,
        "color": palette["primary"]
    })
    
    elements.append({
        "type": "textbox",
        "text": "★ " + content.get("banner", "LIMITED TIME OFFER") + " ★",
        "x": 0,
        "y": height * 0.035,
        "width": width,
        "fontSize": int(width * 0.028),
        "color": palette["text"] if palette["primary"] == "#fbbf24" else "#000000",
        "fontFamily": fonts["body"],
        "fontWeight": "bold",
        "textAlign": "center",
        "letterSpacing": 2
    })
    
    # Big discount number
    elements.append({
        "type": "textbox",
        "text": content.get("discount", "50%"),
        "x": 0,
        "y": height * 0.18,
        "width": width,
        "fontSize": int(width * 0.22),
        "color": palette["primary"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center"
    })
    
    elements.append({
        "type": "textbox",
        "text": "OFF",
        "x": 0,
        "y": height * 0.42,
        "width": width,
        "fontSize": int(width * 0.1),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center"
    })
    
    # Sale name
    elements.append({
        "type": "textbox",
        "text": content.get("headline", "MEGA SALE"),
        "x": 0,
        "y": height * 0.56,
        "width": width,
        "fontSize": int(width * 0.072),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center",
        "letterSpacing": 4
    })
    
    # Subtext
    elements.append({
        "type": "textbox",
        "text": content.get("subheadline", "On selected items. While stocks last."),
        "x": width * 0.1,
        "y": height * 0.68,
        "width": width * 0.8,
        "fontSize": int(width * 0.028),
        "color": palette["muted"],
        "fontFamily": fonts["body"],
        "textAlign": "center"
    })
    
    # CTA Button
    btn_width = width * 0.5
    btn_height = height * 0.08
    btn_x = (width - btn_width) / 2
    
    elements.append({
        "type": "rect",
        "x": btn_x,
        "y": height * 0.78,
        "width": btn_width,
        "height": btn_height,
        "color": palette["primary"],
        "borderRadius": 8
    })
    
    elements.append({
        "type": "textbox",
        "text": content.get("cta", "SHOP NOW"),
        "x": btn_x,
        "y": height * 0.78 + btn_height * 0.25,
        "width": btn_width,
        "fontSize": int(width * 0.032),
        "color": "#000000" if palette["primary"] == "#fbbf24" else "#ffffff",
        "fontFamily": fonts["body"],
        "fontWeight": "bold",
        "textAlign": "center"
    })
    
    # Bottom brand
    elements.append({
        "type": "textbox",
        "text": content.get("brand", "STORE"),
        "x": 0,
        "y": height * 0.92,
        "width": width,
        "fontSize": int(width * 0.025),
        "color": palette["muted"],
        "fontFamily": fonts["heading"],
        "textAlign": "center",
        "letterSpacing": 3
    })
    
    return elements


def create_minimal_layout(width: int, height: int, palette: Dict, fonts: Dict, content: Dict) -> List[Dict]:
    """Clean minimal layout"""
    elements = []
    
    # Thin accent line
    elements.append({
        "type": "rect",
        "x": width * 0.1,
        "y": height * 0.25,
        "width": width * 0.15,
        "height": 4,
        "color": palette["accent"]
    })
    
    # Main headline
    elements.append({
        "type": "textbox",
        "text": content.get("headline", "Less is More"),
        "x": width * 0.1,
        "y": height * 0.3,
        "width": width * 0.8,
        "fontSize": int(width * 0.08),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "lineHeight": 1.1
    })
    
    # Subheadline
    elements.append({
        "type": "textbox",
        "text": content.get("subheadline", "Embrace simplicity in design"),
        "x": width * 0.1,
        "y": height * 0.5,
        "width": width * 0.7,
        "fontSize": int(width * 0.032),
        "color": palette["muted"],
        "fontFamily": fonts["body"],
        "lineHeight": 1.5
    })
    
    # CTA - text only with arrow
    elements.append({
        "type": "textbox",
        "text": content.get("cta", "Discover →"),
        "x": width * 0.1,
        "y": height * 0.68,
        "width": width * 0.5,
        "fontSize": int(width * 0.028),
        "color": palette["primary"],
        "fontFamily": fonts["body"],
        "fontWeight": "600"
    })
    
    # Bottom line
    elements.append({
        "type": "rect",
        "x": width * 0.1,
        "y": height * 0.85,
        "width": width * 0.8,
        "height": 1,
        "color": palette["muted"],
        "opacity": 0.3
    })
    
    # Brand
    elements.append({
        "type": "textbox",
        "text": content.get("brand", "BRAND"),
        "x": width * 0.1,
        "y": height * 0.88,
        "width": width * 0.3,
        "fontSize": int(width * 0.022),
        "color": palette["muted"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "letterSpacing": 3
    })
    
    return elements


def create_story_layout(width: int, height: int, palette: Dict, fonts: Dict, content: Dict) -> List[Dict]:
    """Story format (9:16) optimized layout"""
    elements = []
    
    # Top gradient overlay effect
    elements.append({
        "type": "rect",
        "x": 0,
        "y": 0,
        "width": width,
        "height": height * 0.3,
        "gradient": f"linear-gradient(180deg, {palette['primary']}40 0%, transparent 100%)"
    })
    
    # Brand at top
    elements.append({
        "type": "textbox",
        "text": content.get("brand", "BRAND"),
        "x": 0,
        "y": height * 0.05,
        "width": width,
        "fontSize": int(width * 0.045),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center",
        "letterSpacing": 4
    })
    
    # Main visual area (middle)
    elements.append({
        "type": "circle",
        "x": width * 0.15,
        "y": height * 0.25,
        "width": width * 0.7,
        "height": width * 0.7,
        "color": palette["accent"],
        "opacity": 0.2
    })
    
    # Big headline
    elements.append({
        "type": "textbox",
        "text": content.get("headline", "SWIPE UP"),
        "x": width * 0.05,
        "y": height * 0.52,
        "width": width * 0.9,
        "fontSize": int(width * 0.12),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center"
    })
    
    # Subtext
    elements.append({
        "type": "textbox",
        "text": content.get("subheadline", "For exclusive content"),
        "x": width * 0.1,
        "y": height * 0.65,
        "width": width * 0.8,
        "fontSize": int(width * 0.045),
        "color": palette["muted"],
        "fontFamily": fonts["body"],
        "textAlign": "center"
    })
    
    # Swipe up indicator
    elements.append({
        "type": "textbox",
        "text": "↑",
        "x": 0,
        "y": height * 0.85,
        "width": width,
        "fontSize": int(width * 0.1),
        "color": palette["primary"],
        "fontFamily": "Arial",
        "textAlign": "center"
    })
    
    elements.append({
        "type": "textbox",
        "text": content.get("cta", "SWIPE UP"),
        "x": 0,
        "y": height * 0.92,
        "width": width,
        "fontSize": int(width * 0.035),
        "color": palette["muted"],
        "fontFamily": fonts["body"],
        "fontWeight": "600",
        "textAlign": "center",
        "letterSpacing": 2
    })
    
    return elements


def create_event_layout(width: int, height: int, palette: Dict, fonts: Dict, content: Dict) -> List[Dict]:
    """Event/Announcement layout"""
    elements = []
    
    # Decorative shapes
    elements.append({
        "type": "circle",
        "x": -width * 0.1,
        "y": -width * 0.1,
        "width": width * 0.4,
        "height": width * 0.4,
        "color": palette["accent"],
        "opacity": 0.3
    })
    
    elements.append({
        "type": "circle",
        "x": width * 0.75,
        "y": height * 0.7,
        "width": width * 0.35,
        "height": width * 0.35,
        "color": palette["secondary"],
        "opacity": 0.3
    })
    
    # Event type tag
    elements.append({
        "type": "rect",
        "x": width * 0.35,
        "y": height * 0.12,
        "width": width * 0.3,
        "height": height * 0.045,
        "color": palette["accent"],
        "borderRadius": 20
    })
    
    elements.append({
        "type": "textbox",
        "text": content.get("tag", "WEBINAR"),
        "x": width * 0.35,
        "y": height * 0.128,
        "width": width * 0.3,
        "fontSize": int(width * 0.022),
        "color": "#ffffff",
        "fontFamily": fonts["body"],
        "fontWeight": "bold",
        "textAlign": "center",
        "letterSpacing": 2
    })
    
    # Event name
    elements.append({
        "type": "textbox",
        "text": content.get("headline", "The Future of Design"),
        "x": width * 0.08,
        "y": height * 0.22,
        "width": width * 0.84,
        "fontSize": int(width * 0.065),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center",
        "lineHeight": 1.1
    })
    
    # Date and time
    elements.append({
        "type": "textbox",
        "text": content.get("date", "December 15, 2025"),
        "x": 0,
        "y": height * 0.45,
        "width": width,
        "fontSize": int(width * 0.04),
        "color": palette["primary"],
        "fontFamily": fonts["body"],
        "fontWeight": "bold",
        "textAlign": "center"
    })
    
    elements.append({
        "type": "textbox",
        "text": content.get("time", "2:00 PM EST"),
        "x": 0,
        "y": height * 0.52,
        "width": width,
        "fontSize": int(width * 0.032),
        "color": palette["muted"],
        "fontFamily": fonts["body"],
        "textAlign": "center"
    })
    
    # Description
    elements.append({
        "type": "textbox",
        "text": content.get("description", "Join industry experts as they share insights on the latest trends."),
        "x": width * 0.12,
        "y": height * 0.6,
        "width": width * 0.76,
        "fontSize": int(width * 0.026),
        "color": palette["muted"],
        "fontFamily": fonts["body"],
        "textAlign": "center",
        "lineHeight": 1.5
    })
    
    # Register button
    btn_width = width * 0.45
    btn_height = height * 0.07
    btn_x = (width - btn_width) / 2
    
    elements.append({
        "type": "rect",
        "x": btn_x,
        "y": height * 0.76,
        "width": btn_width,
        "height": btn_height,
        "color": palette["primary"],
        "borderRadius": 8
    })
    
    elements.append({
        "type": "textbox",
        "text": content.get("cta", "REGISTER FREE"),
        "x": btn_x,
        "y": height * 0.76 + btn_height * 0.25,
        "width": btn_width,
        "fontSize": int(width * 0.028),
        "color": "#ffffff",
        "fontFamily": fonts["body"],
        "fontWeight": "bold",
        "textAlign": "center"
    })
    
    # Brand
    elements.append({
        "type": "textbox",
        "text": content.get("brand", "COMPANY"),
        "x": 0,
        "y": height * 0.9,
        "width": width,
        "fontSize": int(width * 0.025),
        "color": palette["muted"],
        "fontFamily": fonts["heading"],
        "textAlign": "center",
        "letterSpacing": 3
    })
    
    return elements


def create_product_layout(width: int, height: int, palette: Dict, fonts: Dict, content: Dict) -> List[Dict]:
    """Product showcase layout"""
    elements = []
    
    # Product image placeholder (circle)
    elements.append({
        "type": "circle",
        "x": width * 0.2,
        "y": height * 0.08,
        "width": width * 0.6,
        "height": width * 0.6,
        "color": palette["secondary"],
        "opacity": 0.15
    })
    
    # Product name
    elements.append({
        "type": "textbox",
        "text": content.get("headline", "New Arrival"),
        "x": width * 0.05,
        "y": height * 0.52,
        "width": width * 0.9,
        "fontSize": int(width * 0.07),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center"
    })
    
    # Product description
    elements.append({
        "type": "textbox",
        "text": content.get("subheadline", "Premium quality you can trust"),
        "x": width * 0.1,
        "y": height * 0.62,
        "width": width * 0.8,
        "fontSize": int(width * 0.03),
        "color": palette["muted"],
        "fontFamily": fonts["body"],
        "textAlign": "center",
        "lineHeight": 1.4
    })
    
    # Price
    elements.append({
        "type": "textbox",
        "text": content.get("price", "$99"),
        "x": 0,
        "y": height * 0.72,
        "width": width,
        "fontSize": int(width * 0.08),
        "color": palette["primary"],
        "fontFamily": fonts["heading"],
        "fontWeight": "bold",
        "textAlign": "center"
    })
    
    # Buy button
    btn_width = width * 0.5
    btn_height = height * 0.07
    btn_x = (width - btn_width) / 2
    
    elements.append({
        "type": "rect",
        "x": btn_x,
        "y": height * 0.82,
        "width": btn_width,
        "height": btn_height,
        "color": palette["primary"],
        "borderRadius": 8
    })
    
    elements.append({
        "type": "textbox",
        "text": content.get("cta", "BUY NOW"),
        "x": btn_x,
        "y": height * 0.82 + btn_height * 0.25,
        "width": btn_width,
        "fontSize": int(width * 0.03),
        "color": "#ffffff",
        "fontFamily": fonts["body"],
        "fontWeight": "bold",
        "textAlign": "center"
    })
    
    # Brand
    elements.append({
        "type": "textbox",
        "text": content.get("brand", "BRAND"),
        "x": 0,
        "y": height * 0.93,
        "width": width,
        "fontSize": int(width * 0.022),
        "color": palette["muted"],
        "fontFamily": fonts["heading"],
        "textAlign": "center",
        "letterSpacing": 3
    })
    
    return elements


def create_quote_layout(width: int, height: int, palette: Dict, fonts: Dict, content: Dict) -> List[Dict]:
    """Inspirational quote layout"""
    elements = []
    
    # Large quotation mark
    elements.append({
        "type": "textbox",
        "text": "\u201C",
        "x": width * 0.05,
        "y": height * 0.15,
        "width": width * 0.3,
        "fontSize": int(width * 0.3),
        "color": palette["accent"],
        "fontFamily": "Georgia",
        "opacity": 0.3
    })
    
    # Quote text
    elements.append({
        "type": "textbox",
        "text": content.get("headline", "Design is not just what it looks like. Design is how it works."),
        "x": width * 0.1,
        "y": height * 0.32,
        "width": width * 0.8,
        "fontSize": int(width * 0.055),
        "color": palette["text"],
        "fontFamily": fonts["heading"],
        "fontWeight": "normal",
        "textAlign": "center",
        "lineHeight": 1.4,
        "fontStyle": "italic"
    })
    
    # Decorative line
    elements.append({
        "type": "rect",
        "x": width * 0.4,
        "y": height * 0.68,
        "width": width * 0.2,
        "height": 3,
        "color": palette["accent"]
    })
    
    # Author
    elements.append({
        "type": "textbox",
        "text": content.get("author", "— Steve Jobs"),
        "x": 0,
        "y": height * 0.73,
        "width": width,
        "fontSize": int(width * 0.032),
        "color": palette["muted"],
        "fontFamily": fonts["body"],
        "textAlign": "center"
    })
    
    # Brand
    elements.append({
        "type": "textbox",
        "text": content.get("brand", "BRAND"),
        "x": 0,
        "y": height * 0.88,
        "width": width,
        "fontSize": int(width * 0.022),
        "color": palette["muted"],
        "fontFamily": fonts["heading"],
        "textAlign": "center",
        "letterSpacing": 3
    })
    
    return elements


# Layout mapping
LAYOUTS = {
    "hero": create_hero_layout,
    "split": create_split_layout,
    "sale": create_sale_layout,
    "minimal": create_minimal_layout,
    "story": create_story_layout,
    "event": create_event_layout,
    "product": create_product_layout,
    "quote": create_quote_layout
}


def extract_content_from_prompt(prompt: str) -> Dict[str, str]:
    """Extract meaningful content from user prompt using NLP patterns"""
    content = {}
    prompt_lower = prompt.lower()
    
    # Extract discount percentages
    discount_match = re.search(r'(\d+)\s*%\s*(off|discount)?', prompt_lower)
    if discount_match:
        content["discount"] = f"{discount_match.group(1)}%"
    
    # Extract prices
    price_match = re.search(r'\$\s*(\d+(?:\.\d{2})?)', prompt)
    if price_match:
        content["price"] = f"${price_match.group(1)}"
    
    # Extract dates
    date_patterns = [
        r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s*\d{4})?',
        r'\d{1,2}/\d{1,2}/\d{2,4}',
        r'\d{1,2}-\d{1,2}-\d{2,4}'
    ]
    for pattern in date_patterns:
        date_match = re.search(pattern, prompt_lower)
        if date_match:
            content["date"] = date_match.group(0).title()
            break
    
    # Extract time
    time_match = re.search(r'\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)', prompt)
    if time_match:
        content["time"] = time_match.group(0).upper()
    
    # Extract brand names (capitalized words that might be brands)
    words = prompt.split()
    for i, word in enumerate(words):
        if word.isupper() and len(word) > 2 and word not in ["FOR", "THE", "AND", "WITH"]:
            content["brand"] = word
            break
    
    # Generate headline from prompt
    # Remove common instruction words
    cleaned = re.sub(r'\b(create|design|make|generate|an?|the|for|with|using|that|has|is)\b', '', prompt_lower, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Take meaningful words for headline
    headline_words = []
    skip_words = {'ad', 'poster', 'banner', 'flyer', 'image', 'graphic', 'format', 'square', 'landscape', 'portrait', 'story', 'meta', 'instagram', 'facebook', 'google', 'linkedin'}
    for word in cleaned.split()[:6]:
        if word.lower() not in skip_words and len(word) > 2:
            headline_words.append(word.capitalize())
    
    if headline_words:
        content["headline"] = ' '.join(headline_words[:4])
    
    return content


def select_palette_for_prompt(prompt: str) -> str:
    """Select appropriate color palette based on prompt keywords"""
    prompt_lower = prompt.lower()
    
    keyword_mapping = {
        "tech_dark": ["tech", "startup", "ai", "software", "app", "digital", "cyber", "innovation", "code", "developer"],
        "tech_light": ["saas", "cloud", "platform", "b2b"],
        "fashion_vibrant": ["fashion", "style", "clothing", "trendy", "summer", "spring", "colorful"],
        "fashion_minimal": ["elegant", "luxury fashion", "boutique", "minimal fashion", "fall", "autumn", "winter"],
        "sale_urgent": ["sale", "discount", "offer", "deal", "limited", "hurry", "flash", "clearance"],
        "sale_black_friday": ["black friday", "cyber monday", "mega sale", "biggest"],
        "business_corporate": ["business", "corporate", "professional", "enterprise", "consulting", "finance"],
        "business_modern": ["agency", "services", "solution", "team"],
        "food_warm": ["food", "restaurant", "pizza", "burger", "fast food", "delivery", "hungry"],
        "food_fresh": ["healthy", "organic", "vegan", "salad", "fresh", "green", "smoothie"],
        "wellness_calm": ["wellness", "yoga", "meditation", "spa", "relax", "health", "fitness", "calm"],
        "luxury_gold": ["luxury", "premium", "exclusive", "vip", "gold", "diamond", "high-end"],
        "creative_gradient": ["creative", "design", "art", "portfolio", "music", "festival", "party"],
        "event_party": ["event", "party", "celebration", "concert", "dj", "night"],
        "education_bright": ["education", "course", "learn", "school", "university", "webinar", "workshop"],
        "minimalist_clean": ["minimal", "clean", "simple", "modern", "basic"]
    }
    
    for palette_name, keywords in keyword_mapping.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                return palette_name
    
    return "creative_gradient"  # Default


def select_layout_for_prompt(prompt: str, format: str) -> str:
    """Select appropriate layout based on prompt and format"""
    prompt_lower = prompt.lower()
    
    # Story format always uses story layout
    if format in ["story", "portrait"]:
        return "story"
    
    # Keyword-based selection
    if any(word in prompt_lower for word in ["sale", "discount", "off", "deal", "offer", "clearance"]):
        return "sale"
    
    if any(word in prompt_lower for word in ["event", "webinar", "conference", "workshop", "seminar", "meetup"]):
        return "event"
    
    if any(word in prompt_lower for word in ["product", "buy", "shop", "new arrival", "launch", "price"]):
        return "product"
    
    if any(word in prompt_lower for word in ["quote", "inspiration", "motivat", "wisdom", "said"]):
        return "quote"
    
    if any(word in prompt_lower for word in ["minimal", "clean", "simple", "elegant"]):
        return "minimal"
    
    # Default layouts by format
    if format == "landscape":
        return "split"
    
    return random.choice(["hero", "split", "minimal"])


def select_fonts_for_prompt(prompt: str) -> str:
    """Select font combination based on prompt"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["tech", "startup", "modern", "digital"]):
        return "tech"
    if any(word in prompt_lower for word in ["fashion", "elegant", "luxury", "beauty"]):
        return "elegant"
    if any(word in prompt_lower for word in ["sale", "discount", "bold", "urgent"]):
        return "bold"
    if any(word in prompt_lower for word in ["fun", "party", "creative", "festival"]):
        return "fun"
    if any(word in prompt_lower for word in ["minimal", "clean", "simple"]):
        return "minimal"
    if any(word in prompt_lower for word in ["business", "corporate", "professional"]):
        return "classic"
    
    return "modern"


def generate_professional_design(prompt: str, platform: str, format: str, specs: dict) -> dict:
    """Generate a professional Canva-like design based on prompt"""
    
    width = specs.get("width", 1080)
    height = specs.get("height", 1080)
    
    # Select design parameters
    palette_name = select_palette_for_prompt(prompt)
    palette = COLOR_PALETTES[palette_name]
    
    fonts_name = select_fonts_for_prompt(prompt)
    fonts = FONT_COMBOS[fonts_name]
    
    layout_name = select_layout_for_prompt(prompt, format)
    layout_func = LAYOUTS[layout_name]
    
    # Extract content from prompt
    content = extract_content_from_prompt(prompt)
    
    # Set defaults if not extracted
    defaults = {
        "headline": "Your Message Here",
        "subheadline": "Add your supporting text",
        "cta": "Learn More",
        "brand": "BRAND",
        "tag": "FEATURED",
        "banner": "LIMITED TIME",
        "description": "Transform your ideas into stunning visuals",
        "discount": "50%",
        "price": "$99",
        "date": "Coming Soon",
        "time": "",
        "author": "— Unknown"
    }
    
    for key, value in defaults.items():
        if key not in content:
            content[key] = value
    
    # Generate elements using selected layout
    elements = layout_func(width, height, palette, fonts, content)
    
    # Determine background
    background = palette["background"]
    
    return {
        "background_color": background if not background.startswith("linear") else background.split()[0].replace("linear-gradient(135deg,", "").replace("linear-gradient(180deg,", "").strip(),
        "background_gradient": background if background.startswith("linear") else None,
        "elements": elements,
        "layout": {
            "type": layout_name,
            "palette": palette_name,
            "fonts": fonts_name,
            "prompt": prompt,
            "width": width,
            "height": height
        },
        "metadata": {
            "template_version": "2.0",
            "generator": "AdGenesis Pro",
            "editable": True
        }
    }


# Template Gallery Data
TEMPLATE_GALLERY = [
    {
        "id": "tech-startup-hero",
        "name": "Tech Startup Hero",
        "category": "Technology",
        "preview_prompt": "Create a tech startup ad",
        "palette": "tech_dark",
        "layout": "hero",
        "fonts": "tech"
    },
    {
        "id": "fashion-sale",
        "name": "Fashion Sale",
        "category": "Fashion",
        "preview_prompt": "Create a fashion sale ad with 50% off",
        "palette": "fashion_vibrant",
        "layout": "sale",
        "fonts": "fun"
    },
    {
        "id": "business-corporate",
        "name": "Business Corporate",
        "category": "Business",
        "preview_prompt": "Create a business consulting ad",
        "palette": "business_corporate",
        "layout": "split",
        "fonts": "classic"
    },
    {
        "id": "food-delivery",
        "name": "Food Delivery",
        "category": "Food",
        "preview_prompt": "Create a food delivery ad",
        "palette": "food_warm",
        "layout": "product",
        "fonts": "bold"
    },
    {
        "id": "event-webinar",
        "name": "Event Webinar",
        "category": "Events",
        "preview_prompt": "Create a webinar event ad",
        "palette": "education_bright",
        "layout": "event",
        "fonts": "modern"
    },
    {
        "id": "minimal-elegant",
        "name": "Minimal Elegant",
        "category": "Minimal",
        "preview_prompt": "Create a minimal elegant ad",
        "palette": "minimalist_clean",
        "layout": "minimal",
        "fonts": "minimal"
    },
    {
        "id": "luxury-premium",
        "name": "Luxury Premium",
        "category": "Luxury",
        "preview_prompt": "Create a luxury premium ad",
        "palette": "luxury_gold",
        "layout": "hero",
        "fonts": "luxury"
    },
    {
        "id": "creative-gradient",
        "name": "Creative Gradient",
        "category": "Creative",
        "preview_prompt": "Create a creative portfolio ad",
        "palette": "creative_gradient",
        "layout": "hero",
        "fonts": "fun"
    },
    {
        "id": "wellness-calm",
        "name": "Wellness Calm",
        "category": "Wellness",
        "preview_prompt": "Create a wellness spa ad",
        "palette": "wellness_calm",
        "layout": "minimal",
        "fonts": "elegant"
    },
    {
        "id": "black-friday",
        "name": "Black Friday Sale",
        "category": "Sales",
        "preview_prompt": "Create a black friday sale ad",
        "palette": "sale_black_friday",
        "layout": "sale",
        "fonts": "bold"
    },
    {
        "id": "inspirational-quote",
        "name": "Inspirational Quote",
        "category": "Quotes",
        "preview_prompt": "Create an inspirational quote poster",
        "palette": "minimalist_clean",
        "layout": "quote",
        "fonts": "elegant"
    },
    {
        "id": "story-swipe",
        "name": "Story Swipe Up",
        "category": "Social",
        "preview_prompt": "Create an Instagram story ad",
        "palette": "creative_gradient",
        "layout": "story",
        "fonts": "fun"
    }
]


def get_template_by_id(template_id: str) -> dict:
    """Get a specific template by ID"""
    for template in TEMPLATE_GALLERY:
        if template["id"] == template_id:
            return template
    return None


def generate_from_template(template_id: str, custom_content: dict, specs: dict) -> dict:
    """Generate design from a specific template with custom content"""
    template = get_template_by_id(template_id)
    if not template:
        raise ValueError(f"Template not found: {template_id}")
    
    width = specs.get("width", 1080)
    height = specs.get("height", 1080)
    
    palette = COLOR_PALETTES[template["palette"]]
    fonts = FONT_COMBOS[template["fonts"]]
    layout_func = LAYOUTS[template["layout"]]
    
    elements = layout_func(width, height, palette, fonts, custom_content)
    
    background = palette["background"]
    
    return {
        "background_color": background if not background.startswith("linear") else "#1a1a2e",
        "background_gradient": background if background.startswith("linear") else None,
        "elements": elements,
        "layout": {
            "type": template["layout"],
            "palette": template["palette"],
            "fonts": template["fonts"],
            "template_id": template_id,
            "width": width,
            "height": height
        }
    }
