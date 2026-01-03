"""
ENHANCED generate_design_blueprint function for modern advertising posters
This replaces the old basic template function
"""

from typing import Dict, Any
import random

def generate_modern_design_blueprint(request, MODERN_COLOR_SCHEMES, MODERN_LAYOUTS, 
                                     MODERN_HEADLINES, MODERN_SUBHEADLINES, MODERN_CTAS, 
                                     MODERN_FONTS, detect_category) -> Dict[str, Any]:
    """
    Generate a MODERN, PROFESSIONAL design blueprint
    Creates advertising-quality posters with rich visual elements
    """
    print(f"\n🎨 Generating MODERN design for: {request.prompt}")
    
    # Detect category from prompt
    category = detect_category(request.prompt)
    print(f"   Category detected: {category}")
    
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
    
    # Select MODERN color scheme
    scheme_names = list(MODERN_COLOR_SCHEMES.keys())
    scheme_name = random.choice(scheme_names)
    color_scheme = MODERN_COLOR_SCHEMES[scheme_name]
    print(f"   Color scheme: {scheme_name}")
    
    # Override with brand colors if provided
    if request.brand_colors and len(request.brand_colors) >= 2:
        color_scheme["primary"] = request.brand_colors[0]
        color_scheme["secondary"] = request.brand_colors[1]
        if len(request.brand_colors) >= 3:
            color_scheme["accent"] = request.brand_colors[2]
    
    # Select MODERN layout
    layout_names = list(MODERN_LAYOUTS.keys())
    layout_name = random.choice(layout_names)
    layout = MODERN_LAYOUTS[layout_name]
    print(f"   Layout: {layout['name']}")
    
    # Generate MODERN content based on category
    headlines = MODERN_HEADLINES.get(category, MODERN_HEADLINES["default"])
    subheadlines = MODERN_SUBHEADLINES.get(category, MODERN_SUBHEADLINES["default"])
    
    headline = random.choice(headlines)
    subheadline = random.choice(subheadlines)
    cta = random.choice(MODERN_CTAS)
    
    # MODERN font selection
    font_data = random.choice(MODERN_FONTS)
    font_family = font_data["name"]
    headline_weight = max(font_data["weights"])
    subheadline_weight = min([w for w in font_data["weights"] if w >= 400])
    print(f"   Font: {font_family} ({font_data['style']} style)")
    
    # Font sizes - LARGER for impact
    headline_size = 82 if format_key == "square" else (68 if format_key == "story" else 58)
    subheadline_size = 28 if format_key == "square" else 24
    body_size = 18
    
    # Build modern elements
    elements = []
    
    # === HEADLINE ===
    hl = layout["headline"]
    elements.append({
        "type": "text",
        "id": "headline_1",
        "content": headline,
        "style": "headline",
        "position": {"x": hl["x"], "y": hl["y"]},
        "size": {"width": hl["w"], "height": hl["h"]},
        "font_family": font_family,
        "font_size": headline_size,
        "font_weight": headline_weight,
        "color": color_scheme["text_primary"],
        "align": hl["align"],
        "line_height": 1.05,
        "letter_spacing": -1.5,
        "text_shadow": "0 4px 12px rgba(0,0,0,0.15)"
    })
    
    # === SUBHEADLINE ===
    sh = layout["subheadline"]
    elements.append({
        "type": "text",
        "id": "subheadline_1",
        "content": subheadline,
        "style": "subheadline",
        "position": {"x": sh["x"], "y": sh["y"]},
        "size": {"width": sh["w"], "height": sh["h"]},
        "font_family": font_family,
        "font_size": subheadline_size,
        "font_weight": subheadline_weight,
        "color": color_scheme["text_secondary"],
        "align": sh["align"],
        "line_height": 1.4,
        "letter_spacing": 0.3,
        "opacity": 0.9
    })
    
    # === BODY TEXT (if layout supports it) ===
    body_text = None
    if layout.get("body"):
        body = layout["body"]
        # Generate contextual body text
        body_texts = {
            "tech": "Experience innovation that adapts to your needs",
            "sale": "Premium quality at unbeatable prices",
            "fashion": "Discover your unique style today",
            "fitness": "Personalized training for real results",
            "food": "Crafted with passion, served with love",
            "business": "Trusted solutions for modern challenges",
            "default": "Quality you can count on"
        }
        body_text = body_texts.get(category, body_texts["default"])
        
        elements.append({
            "type": "text",
            "id": "body_1",
            "content": body_text,
            "style": "body",
            "position": {"x": body["x"], "y": body["y"]},
            "size": {"width": body["w"], "height": body["h"]},
            "font_family": font_family,
            "font_size": body_size,
            "font_weight": 400,
            "color": color_scheme["text_secondary"],
            "align": body["align"],
            "line_height": 1.6,
            "letter_spacing": 0.2,
            "opacity": 0.8
        })
    
    # === CTA BUTTON (MODERN STYLE) ===
    cta_pos = layout["cta"]
    # Modern button styles
    button_styles = [
        {"radius": 8, "shadow": "0 4px 20px rgba(0,0,0,0.25)", "style": "sharp"},
        {"radius": 32, "shadow": "0 8px 24px rgba(0,0,0,0.2)", "style": "pill"},
        {"radius": 12, "shadow": "0 6px 28px rgba(0,0,0,0.18)", "style": "rounded"},
    ]
    button_style = random.choice(button_styles)
    
    elements.append({
        "type": "cta_button",
        "id": "cta_1",
        "text": cta,
        "position": {"x": cta_pos["x"], "y": cta_pos["y"]},
        "size": {"width": cta_pos["w"], "height": cta_pos["h"]},
        "background_color": color_scheme["accent"],
        "text_color": "#FFFFFF",
        "font_size": 20,
        "font_weight": 700,
        "corner_radius": button_style["radius"],
        "padding": 20,
        "box_shadow": button_style["shadow"],
        "hover_effect": True
    })
    
    # === DECORATIVE ELEMENTS ===
    # Add layout-specific decorations
    if layout.get("decoration"):
        for i, deco in enumerate(layout["decoration"]):
            deco_type = deco["type"]
            
            if deco_type == "circle":
                elements.append({
                    "type": "shape",
                    "id": f"deco_circle_{i}",
                    "shape_type": "circle",
                    "position": {"x": deco["x"], "y": deco["y"]},
                    "size": {"width": deco["w"], "height": deco["h"]},
                    "fill_color": color_scheme["primary"],
                    "stroke_color": None,
                    "stroke_width": 0,
                    "opacity": deco.get("opacity", 0.15),
                    "blur": deco.get("blur", 0),
                    "corner_radius": 0
                })
            
            elif deco_type == "rect":
                elements.append({
                    "type": "shape",
                    "id": f"deco_rect_{i}",
                    "shape_type": "rectangle",
                    "position": {"x": deco["x"], "y": deco["y"]},
                    "size": {"width": deco["w"], "height": deco["h"]},
                    "fill_color": color_scheme["secondary"] if deco.get("stroke") else color_scheme["primary"],
                    "stroke_color": color_scheme["primary"] if deco.get("stroke") else None,
                    "stroke_width": deco.get("stroke", 0),
                    "opacity": deco.get("opacity", 0.1),
                    "corner_radius": deco.get("radius", 0),
                    "rotation": deco.get("rotation", 0)
                })
            
            elif deco_type == "line":
                elements.append({
                    "type": "shape",
                    "id": f"deco_line_{i}",
                    "shape_type": "line",
                    "position": {"x": deco["x"], "y": deco["y"]},
                    "size": {"width": deco["w"], "height": deco["h"]},
                    "fill_color": None,
                    "stroke_color": color_scheme["primary"],
                    "stroke_width": max(deco["w"], deco["h"]) * 10,  # Scale for visibility
                    "opacity": deco.get("opacity", 0.2),
                    "corner_radius": 0
                })
    
    # === ADDITIONAL MODERN ACCENTS ===
    # Floating geometric shapes
    accent_shapes = [
        {"type": "circle", "x": random.randint(70, 85), "y": random.randint(5, 20), 
         "w": random.randint(15, 25), "h": random.randint(15, 25), "opacity": 0.12, "blur": 30},
        {"type": "circle", "x": random.randint(5, 15), "y": random.randint(70, 85), 
         "w": random.randint(18, 28), "h": random.randint(18, 28), "opacity": 0.1, "blur": 40},
        {"type": "rect", "x": random.randint(75, 88), "y": random.randint(40, 60), 
         "w": 15, "h": 15, "opacity": 0.08, "rotation": 45, "radius": 3},
    ]
    
    # Add 2-3 random accent shapes
    selected_accents = random.sample(accent_shapes, k=random.randint(2, 3))
    for i, shape in enumerate(selected_accents):
        if shape["type"] == "circle":
            elements.append({
                "type": "shape",
                "id": f"accent_circle_{i}",
                "shape_type": "circle",
                "position": {"x": shape["x"], "y": shape["y"]},
                "size": {"width": shape["w"], "height": shape["h"]},
                "fill_color": color_scheme["secondary"],
                "stroke_color": None,
                "stroke_width": 0,
                "opacity": shape["opacity"],
                "blur": shape.get("blur", 0),
                "corner_radius": 0
            })
        else:
            elements.append({
                "type": "shape",
                "id": f"accent_rect_{i}",
                "shape_type": "rectangle",
                "position": {"x": shape["x"], "y": shape["y"]},
                "size": {"width": shape["w"], "height": shape["h"]},
                "fill_color": color_scheme["accent"],
                "stroke_color": None,
                "stroke_width": 0,
                "opacity": shape["opacity"],
                "corner_radius": shape.get("radius", 0),
                "rotation": shape.get("rotation", 0)
            })
    
    # === BACKGROUND OVERLAY (for gradient schemes) ===
    background_config = color_scheme["background"]
    if background_config["type"] == "gradient":
        background_gradient = {
            "type": "linear",
            "colors": background_config["colors"],
            "angle": background_config["angle"]
        }
        background_color = background_config["colors"][0]
    else:
        background_gradient = None
        background_color = background_config["colors"][0]
    
    # Add subtle texture overlay
    if color_scheme.get("overlay"):
        elements.insert(0, {
            "type": "shape",
            "id": "overlay_texture",
            "shape_type": "rectangle",
            "position": {"x": 0, "y": 0},
            "size": {"width": 100, "height": 100},
            "fill_color": color_scheme["overlay"],
            "stroke_color": None,
            "stroke_width": 0,
            "opacity": 0.5,
            "corner_radius": 0
        })
    
    # Build blueprint
    blueprint = {
        "metadata": {
            "platform": request.platform,
            "format": request.format,
            "width": width,
            "height": height,
            "industry": request.industry or category,
            "campaign_type": "advertising",
            "target_audience": "general",
            "design_style": f"{layout['name']} - {scheme_name}",
            "font_family": font_family
        },
        "headline": headline,
        "subheadline": subheadline,
        "body_text": body_text,
        "cta_text": cta,
        "background": {
            "type": "background",
            "color": background_color,
            "gradient": background_gradient,
            "image_placeholder": None
        },
        "color_palette": {
            "primary": color_scheme["primary"],
            "secondary": color_scheme["secondary"],
            "accent": color_scheme["accent"],
            "background": background_color,
            "text_primary": color_scheme["text_primary"],
            "text_secondary": color_scheme["text_secondary"]
        },
        "elements": elements,
        "design_notes": f"Modern {category} design with {layout['name']} layout and {scheme_name} color scheme."
    }
    
    return blueprint
