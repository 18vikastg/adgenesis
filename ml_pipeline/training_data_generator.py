"""
Training Data Generator for AdGenesis Design Model
Generates synthetic training pairs: (prompt + context) -> design blueprint JSON
"""

import json
import random
from typing import List, Dict, Any
from pathlib import Path
from itertools import product

# =============================================================================
# DESIGN COMPONENTS LIBRARY
# =============================================================================

# Industry/vertical variations
INDUSTRIES = [
    "e-commerce", "saas", "fitness", "food_delivery", "fashion",
    "real_estate", "automotive", "travel", "finance", "healthcare",
    "education", "entertainment", "beauty", "tech_startup", "retail"
]

# Campaign types
CAMPAIGN_TYPES = [
    "product_launch", "sale_promotion", "brand_awareness", "lead_generation",
    "event_announcement", "seasonal", "flash_sale", "new_feature", 
    "testimonial", "comparison", "how_to", "limited_offer"
]

# Target audiences
AUDIENCES = [
    "young_professionals", "parents", "students", "seniors", "entrepreneurs",
    "fitness_enthusiasts", "tech_savvy", "budget_conscious", "luxury_seekers",
    "small_business_owners", "millennials", "gen_z", "working_moms"
]

# Tones/styles
TONES = [
    "professional", "playful", "urgent", "luxurious", "minimalist",
    "bold", "friendly", "sophisticated", "energetic", "calm"
]

# Color palettes by tone
COLOR_PALETTES = {
    "professional": [
        {"primary": "#2563EB", "secondary": "#1E40AF", "background": "#0F172A", "text_primary": "#F8FAFC", "text_secondary": "#94A3B8", "accent": "#3B82F6"},
        {"primary": "#0D9488", "secondary": "#115E59", "background": "#042F2E", "text_primary": "#F0FDFA", "text_secondary": "#5EEAD4", "accent": "#14B8A6"},
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
    "sophisticated": [
        {"primary": "#6366F1", "secondary": "#818CF8", "background": "#0F0F23", "text_primary": "#E0E7FF", "text_secondary": "#A5B4FC", "accent": "#C084FC"},
        {"primary": "#0EA5E9", "secondary": "#38BDF8", "background": "#0C1222", "text_primary": "#F0F9FF", "text_secondary": "#7DD3FC", "accent": "#E879F9"},
    ],
    "energetic": [
        {"primary": "#EF4444", "secondary": "#F87171", "background": "#1A1A2E", "text_primary": "#FFFFFF", "text_secondary": "#FCA5A5", "accent": "#FBBF24"},
        {"primary": "#F97316", "secondary": "#FB923C", "background": "#18181B", "text_primary": "#FFFBEB", "text_secondary": "#FDBA74", "accent": "#A3E635"},
    ],
    "calm": [
        {"primary": "#2DD4BF", "secondary": "#5EEAD4", "background": "#0D1B2A", "text_primary": "#F0FDFA", "text_secondary": "#99F6E4", "accent": "#A78BFA"},
        {"primary": "#60A5FA", "secondary": "#93C5FD", "background": "#0F172A", "text_primary": "#EFF6FF", "text_secondary": "#BFDBFE", "accent": "#34D399"},
    ],
}

# Headlines by campaign type
HEADLINES = {
    "product_launch": [
        "Introducing {product}", "Meet the New {product}", "The Future of {category}",
        "Finally, {product} That Works", "Discover {product}", "{product} Is Here",
        "Your New Favorite {product}", "Reimagined {category}"
    ],
    "sale_promotion": [
        "Up to {discount}% Off", "Big {season} Sale", "Save on {product}",
        "{discount}% Off Everything", "Flash Sale: {discount}% Off", 
        "Limited Time: {discount}% Off", "Don't Miss Out"
    ],
    "brand_awareness": [
        "{brand}: {tagline}", "Experience {brand}", "Why {brand}?",
        "The {brand} Difference", "{brand} For Everyone", "Powered by {brand}"
    ],
    "lead_generation": [
        "Get Your Free {offer}", "Download Now", "Start Your Journey",
        "Join {number}+ {users}", "Get Started Today", "Claim Your {offer}"
    ],
    "event_announcement": [
        "Save the Date", "You're Invited", "Don't Miss {event}",
        "Join Us for {event}", "{event} Is Coming", "Register Now"
    ],
    "seasonal": [
        "{season} Collection", "Celebrate {holiday}", "{holiday} Special",
        "This {season}, {action}", "Get Ready for {season}"
    ],
    "flash_sale": [
        "24 Hours Only", "Ends Tonight", "Last Chance",
        "Today Only: {discount}% Off", "Final Hours", "Quick! {discount}% Off"
    ],
    "limited_offer": [
        "Limited Edition", "Only {number} Left", "Exclusive Offer",
        "While Supplies Last", "Members Only", "VIP Access"
    ]
}

# Subheadlines
SUBHEADLINES = {
    "product_launch": [
        "The smarter way to {benefit}", "Built for {audience}",
        "Everything you need to {benefit}", "{feature} meets {feature}"
    ],
    "sale_promotion": [
        "Use code {code} at checkout", "Free shipping on orders over ${amount}",
        "No strings attached", "Your wallet will thank you"
    ],
    "brand_awareness": [
        "Trusted by {number}+ customers", "Since {year}",
        "Quality you can count on", "Made with love"
    ],
    "lead_generation": [
        "Join our community", "No credit card required",
        "Takes just {time} minutes", "100% free forever"
    ],
    "event_announcement": [
        "{date} | {location}", "Online & In-Person",
        "Limited spots available", "Early bird pricing ends soon"
    ],
    "seasonal": [
        "New arrivals weekly", "Curated just for you",
        "Fresh styles for the season", "Limited time only"
    ],
    "flash_sale": [
        "Don't wait - shop now", "Once it's gone, it's gone",
        "Set your alarms", "Best prices of the year"
    ],
    "limited_offer": [
        "First come, first served", "Act fast",
        "Exclusive to subscribers", "Never offered again"
    ]
}

# CTA texts
CTA_TEXTS = [
    "Shop Now", "Get Started", "Learn More", "Sign Up Free", "Download Now",
    "Buy Now", "Explore", "Try Free", "Join Now", "Claim Offer",
    "Book Now", "Register", "Subscribe", "Get Yours", "Start Free Trial"
]

# Font pairings
FONT_PAIRINGS = [
    {"headline": "Inter", "body": "Inter"},
    {"headline": "Poppins", "body": "Inter"},
    {"headline": "Playfair Display", "body": "Source Sans Pro"},
    {"headline": "Montserrat", "body": "Open Sans"},
    {"headline": "Oswald", "body": "Lato"},
    {"headline": "Roboto", "body": "Roboto"},
    {"headline": "DM Sans", "body": "DM Sans"},
    {"headline": "Space Grotesk", "body": "Inter"},
]

# Layout templates (element positions as % of canvas)
LAYOUT_TEMPLATES = {
    "centered_stack": {
        "description": "Center-aligned vertical stack",
        "headline": {"x": 10, "y": 30, "w": 80, "h": 15},
        "subheadline": {"x": 15, "y": 48, "w": 70, "h": 10},
        "cta": {"x": 30, "y": 68, "w": 40, "h": 8},
        "accent_shapes": [
            {"type": "circle", "x": 5, "y": 5, "w": 15, "h": 15, "opacity": 0.2},
            {"type": "circle", "x": 80, "y": 75, "w": 20, "h": 20, "opacity": 0.15},
        ]
    },
    "left_aligned": {
        "description": "Left-aligned with accent on right",
        "headline": {"x": 8, "y": 25, "w": 55, "h": 18},
        "subheadline": {"x": 8, "y": 48, "w": 50, "h": 10},
        "cta": {"x": 8, "y": 68, "w": 35, "h": 8},
        "accent_shapes": [
            {"type": "rounded_rect", "x": 65, "y": 20, "w": 30, "h": 60, "opacity": 0.8},
        ]
    },
    "split_horizontal": {
        "description": "Split layout - text left, image right",
        "headline": {"x": 5, "y": 35, "w": 45, "h": 15},
        "subheadline": {"x": 5, "y": 52, "w": 42, "h": 8},
        "cta": {"x": 5, "y": 70, "w": 30, "h": 7},
        "image_placeholder": {"x": 52, "y": 10, "w": 43, "h": 80},
        "accent_shapes": []
    },
    "hero_top": {
        "description": "Large headline at top",
        "headline": {"x": 5, "y": 10, "w": 90, "h": 25},
        "subheadline": {"x": 10, "y": 40, "w": 80, "h": 10},
        "cta": {"x": 25, "y": 75, "w": 50, "h": 10},
        "accent_shapes": [
            {"type": "rectangle", "x": 0, "y": 60, "w": 100, "h": 2, "opacity": 0.3},
        ]
    },
    "bottom_heavy": {
        "description": "Content at bottom with space for image",
        "headline": {"x": 8, "y": 55, "w": 84, "h": 12},
        "subheadline": {"x": 12, "y": 70, "w": 76, "h": 8},
        "cta": {"x": 30, "y": 85, "w": 40, "h": 7},
        "image_placeholder": {"x": 10, "y": 5, "w": 80, "h": 45},
        "accent_shapes": []
    },
    "diagonal_accent": {
        "description": "Diagonal accent element",
        "headline": {"x": 10, "y": 25, "w": 60, "h": 15},
        "subheadline": {"x": 10, "y": 45, "w": 55, "h": 8},
        "cta": {"x": 10, "y": 65, "w": 35, "h": 8},
        "accent_shapes": [
            {"type": "rounded_rect", "x": 60, "y": -10, "w": 60, "h": 120, "opacity": 0.15, "rotation": 15},
        ]
    },
}

# Format specifications
FORMAT_SPECS = {
    "square": {"width": 1080, "height": 1080},
    "story": {"width": 1080, "height": 1920},
    "landscape": {"width": 1200, "height": 628},
    "portrait": {"width": 1080, "height": 1350},
    "wide": {"width": 1920, "height": 1080},
}

# =============================================================================
# TRAINING DATA GENERATION
# =============================================================================

def generate_prompt(industry: str, campaign_type: str, audience: str, 
                   tone: str, platform: str, format: str) -> str:
    """Generate a natural language prompt for the training pair"""
    
    prompt_templates = [
        f"Create a {tone} {format} ad for {industry}. Campaign type: {campaign_type}. Target: {audience}. Platform: {platform}.",
        f"Design a {campaign_type} ad targeting {audience} in the {industry} industry. Style: {tone}. Format: {format} for {platform}.",
        f"I need a {tone} {platform} ad ({format}) for my {industry} business. It's a {campaign_type} campaign for {audience}.",
        f"Generate a {format} ad design for {platform}. Industry: {industry}. Goal: {campaign_type}. Audience: {audience}. Tone: {tone}.",
        f"Make me a {tone} {industry} ad. Type: {campaign_type}. Size: {format}. Platform: {platform}. Targeting: {audience}.",
    ]
    
    return random.choice(prompt_templates)

def generate_design_blueprint(industry: str, campaign_type: str, audience: str,
                             tone: str, platform: str, format: str) -> Dict[str, Any]:
    """Generate a complete design blueprint"""
    
    # Get format dimensions
    dims = FORMAT_SPECS.get(format, FORMAT_SPECS["square"])
    width, height = dims["width"], dims["height"]
    
    # Select random elements
    palette = random.choice(COLOR_PALETTES.get(tone, COLOR_PALETTES["professional"]))
    fonts = random.choice(FONT_PAIRINGS)
    layout = random.choice(list(LAYOUT_TEMPLATES.values()))
    
    # Generate text content
    headline_template = random.choice(HEADLINES.get(campaign_type, HEADLINES["product_launch"]))
    subheadline_template = random.choice(SUBHEADLINES.get(campaign_type, SUBHEADLINES["product_launch"]))
    cta = random.choice(CTA_TEXTS)
    
    # Fill in placeholders
    replacements = {
        "{product}": random.choice(["Widget", "App", "Service", "Solution", "Tool"]),
        "{category}": industry.replace("_", " ").title(),
        "{discount}": str(random.choice([20, 25, 30, 40, 50, 60, 70])),
        "{brand}": "YourBrand",
        "{tagline}": "Innovation Delivered",
        "{offer}": random.choice(["Guide", "eBook", "Trial", "Demo", "Consultation"]),
        "{number}": str(random.choice([1000, 5000, 10000, 50000, 100000])),
        "{users}": random.choice(["customers", "users", "subscribers", "members"]),
        "{event}": random.choice(["Summit", "Conference", "Webinar", "Launch Event"]),
        "{season}": random.choice(["Summer", "Winter", "Spring", "Fall"]),
        "{holiday}": random.choice(["New Year", "Valentine's", "Black Friday", "Holidays"]),
        "{action}": random.choice(["Save Big", "Look Great", "Get Inspired"]),
        "{code}": "SAVE" + str(random.randint(10, 50)),
        "{amount}": str(random.choice([25, 50, 75, 100])),
        "{year}": str(random.randint(2010, 2020)),
        "{time}": str(random.choice([2, 3, 5])),
        "{date}": "March 15, 2025",
        "{location}": random.choice(["San Francisco", "Online", "New York"]),
        "{benefit}": random.choice(["succeed", "grow", "save time", "achieve more"]),
        "{audience}": audience.replace("_", " "),
        "{feature}": random.choice(["simplicity", "power", "elegance", "efficiency"]),
    }
    
    headline = headline_template
    subheadline = subheadline_template
    for key, value in replacements.items():
        headline = headline.replace(key, value)
        subheadline = subheadline.replace(key, value)
    
    # Build elements list
    elements = []
    
    # Add headline
    hl = layout["headline"]
    headline_size = 72 if format == "square" else (64 if format == "story" else 56)
    elements.append({
        "type": "text",
        "id": "headline_1",
        "content": headline,
        "style": "headline",
        "position": {"x": hl["x"], "y": hl["y"]},
        "size": {"width": hl["w"], "height": hl["h"]},
        "font_family": fonts["headline"],
        "font_size": headline_size,
        "font_weight": 700,
        "color": palette["text_primary"],
        "align": "left" if "left" in layout.get("description", "") else "center",
        "line_height": 1.1,
        "letter_spacing": -1
    })
    
    # Add subheadline
    sh = layout["subheadline"]
    subheadline_size = 24 if format == "square" else (22 if format == "story" else 20)
    elements.append({
        "type": "text",
        "id": "subheadline_1",
        "content": subheadline,
        "style": "subheadline",
        "position": {"x": sh["x"], "y": sh["y"]},
        "size": {"width": sh["w"], "height": sh["h"]},
        "font_family": fonts["body"],
        "font_size": subheadline_size,
        "font_weight": 400,
        "color": palette["text_secondary"],
        "align": "left" if "left" in layout.get("description", "") else "center",
        "line_height": 1.4,
        "letter_spacing": 0
    })
    
    # Add CTA button
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
    for i, shape in enumerate(layout.get("accent_shapes", [])):
        elements.append({
            "type": "shape",
            "id": f"accent_{i}",
            "shape_type": shape["type"],
            "position": {"x": shape["x"], "y": shape["y"]},
            "size": {"width": shape["w"], "height": shape["h"]},
            "fill_color": palette["primary"],
            "stroke_color": None,
            "stroke_width": 0,
            "opacity": shape.get("opacity", 0.2),
            "corner_radius": random.choice([0, 8, 16]) if shape["type"] == "rounded_rect" else 0
        })
    
    # Add image placeholder if in layout
    if "image_placeholder" in layout:
        img = layout["image_placeholder"]
        elements.append({
            "type": "image",
            "id": "image_1",
            "position": {"x": img["x"], "y": img["y"]},
            "size": {"width": img["w"], "height": img["h"]},
            "placeholder": f"Product image for {industry} {campaign_type}",
            "opacity": 1.0,
            "fit": "cover"
        })
    
    # Build the complete blueprint
    blueprint = {
        "metadata": {
            "platform": platform,
            "format": format,
            "width": width,
            "height": height,
            "industry": industry,
            "campaign_type": campaign_type,
            "target_audience": audience
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
        "design_notes": f"{tone.title()} {campaign_type.replace('_', ' ')} design for {audience.replace('_', ' ')}. Uses {layout['description'].lower()} layout with {fonts['headline']} headlines."
    }
    
    return blueprint

def generate_training_pair() -> Dict[str, Any]:
    """Generate a single training pair (prompt, blueprint)"""
    
    # Random selections
    industry = random.choice(INDUSTRIES)
    campaign_type = random.choice(CAMPAIGN_TYPES)
    audience = random.choice(AUDIENCES)
    tone = random.choice(TONES)
    platform = random.choice(["meta", "google", "linkedin"])
    format = random.choice(["square", "story", "landscape"])
    
    prompt = generate_prompt(industry, campaign_type, audience, tone, platform, format)
    blueprint = generate_design_blueprint(industry, campaign_type, audience, tone, platform, format)
    
    return {
        "prompt": prompt,
        "blueprint": blueprint
    }

def generate_training_dataset(n_samples: int = 5000) -> List[Dict[str, Any]]:
    """Generate a full training dataset"""
    
    print(f"Generating {n_samples} training samples...")
    dataset = []
    
    for i in range(n_samples):
        pair = generate_training_pair()
        dataset.append(pair)
        
        if (i + 1) % 500 == 0:
            print(f"  Generated {i + 1}/{n_samples} samples")
    
    return dataset

def format_for_training(dataset: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Format dataset for LLM fine-tuning.
    Each sample becomes: input (prompt) -> output (JSON blueprint)
    """
    
    formatted = []
    
    for sample in dataset:
        # Create instruction-following format
        instruction = f"""You are an AI ad design assistant. Given a prompt describing an ad, generate a complete design blueprint in JSON format.

The blueprint should include:
- metadata (platform, format, dimensions)
- headline and subheadline text
- CTA button text
- background configuration
- color palette
- positioned design elements (text, shapes, buttons)

Prompt: {sample['prompt']}

Generate the design blueprint JSON:"""
        
        output = json.dumps(sample['blueprint'], indent=2)
        
        formatted.append({
            "instruction": instruction,
            "input": "",
            "output": output
        })
    
    return formatted

def save_training_data(dataset: List[Dict], output_path: str = "data/design_training_data.json"):
    """Save the training dataset to a file"""
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Saved {len(dataset)} training samples to {output_path}")
    
    # Also save a formatted version for fine-tuning
    formatted = format_for_training([d for d in dataset if 'prompt' in d])
    formatted_path = output_path.replace('.json', '_formatted.json')
    
    with open(formatted_path, 'w') as f:
        json.dump(formatted, f, indent=2)
    
    print(f"Saved formatted training data to {formatted_path}")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Generate training data
    dataset = generate_training_dataset(n_samples=5000)
    
    # Save to file
    save_training_data(dataset)
    
    # Print a sample
    print("\n" + "="*60)
    print("SAMPLE TRAINING PAIR:")
    print("="*60)
    sample = dataset[0]
    print(f"\nPROMPT:\n{sample['prompt']}")
    print(f"\nBLUEPRINT (truncated):\n{json.dumps(sample['blueprint'], indent=2)[:1000]}...")
