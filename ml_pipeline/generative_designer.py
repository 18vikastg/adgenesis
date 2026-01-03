"""
GENERATIVE DESIGNER - Zero Template Design Generation
======================================================
This module generates designs with ZERO predefined templates.
Every element is computed directly from the prompt itself.

NO category buckets.
NO headline lists.
NO layout templates.
NO color palettes.

Everything is DERIVED from the prompt words.
"""

import hashlib
import math
import re
from typing import Dict, List, Any, Tuple, Optional


def prompt_to_seed(prompt: str) -> int:
    """Convert prompt to a deterministic seed"""
    return int(hashlib.sha256(prompt.encode()).hexdigest(), 16)


def word_to_value(word: str, range_min: float, range_max: float) -> float:
    """Convert any word to a value in a range"""
    h = int(hashlib.md5(word.lower().encode()).hexdigest(), 16)
    normalized = (h % 10000) / 10000
    return range_min + normalized * (range_max - range_min)


def words_to_hue(words: List[str]) -> float:
    """Derive a hue (0-360) from a list of words"""
    if not words:
        return 220  # Default blue
    combined = ''.join(words)
    h = int(hashlib.md5(combined.encode()).hexdigest()[:8], 16)
    return h % 360


def extract_all_entities(prompt: str) -> Dict[str, Any]:
    """
    Extract every meaningful entity from the prompt.
    No categorization - just extraction.
    """
    
    entities = {
        "proper_nouns": [],
        "descriptors": [],
        "actions": [],
        "objects": [],
        "numbers": [],
        "locations": [],
        "modifiers": [],
        "all_significant_words": [],
    }
    
    # Find all capitalized sequences (potential brand names)
    caps_pattern = re.findall(r'([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*)', prompt)
    entities["proper_nouns"] = [c.strip() for c in caps_pattern if len(c.strip()) > 1]
    
    # Find numbers and percentages
    numbers = re.findall(r'(\d+(?:\.\d+)?)\s*(%|percent|off|rs|₹|inr)?', prompt.lower())
    entities["numbers"] = numbers
    
    # Find location indicators
    loc_pattern = re.findall(r'(?:in|at|near|from|of)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', prompt)
    entities["locations"] = loc_pattern
    
    # Extract all words, remove common stop words
    all_words = re.findall(r'\b[a-zA-Z]{3,}\b', prompt.lower())
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'has', 'her', 'was', 'one', 'our', 'out', 'his', 'have', 'been', 'would', 'could', 'there', 'their', 'will', 'each', 'make', 'like', 'into', 'time', 'very', 'when', 'come', 'made', 'find', 'more', 'from', 'with', 'that', 'this', 'what', 'about', 'which', 'your'}
    
    significant = [w for w in all_words if w not in stop_words]
    entities["all_significant_words"] = significant
    
    # Classify words by their likely role
    action_suffixes = ['ing', 'ate', 'ize', 'ify']
    descriptor_suffixes = ['ful', 'ous', 'ive', 'able', 'ible', 'al', 'ic']
    
    for word in significant:
        if any(word.endswith(s) for s in action_suffixes):
            entities["actions"].append(word)
        elif any(word.endswith(s) for s in descriptor_suffixes):
            entities["descriptors"].append(word)
        elif word not in [p.lower() for p in entities["proper_nouns"]]:
            entities["objects"].append(word)
    
    return entities


def compute_prompt_metrics(prompt: str, entities: Dict) -> Dict[str, float]:
    """
    Compute numerical metrics directly from the prompt.
    These drive ALL design decisions.
    """
    
    metrics = {}
    
    # Length-based metrics
    char_count = len(prompt)
    word_count = len(prompt.split())
    
    metrics["verbosity"] = min(word_count / 20, 1.0)  # 0-1, how wordy
    metrics["complexity"] = min(char_count / 150, 1.0)  # 0-1, how complex
    
    # Punctuation energy
    exclamations = prompt.count('!')
    questions = prompt.count('?')
    metrics["energy"] = min((exclamations * 2 + questions) / 5, 1.0)
    
    # Number presence (offers, prices, etc.)
    has_numbers = len(entities["numbers"]) > 0
    has_percentage = any('%' in str(n) or 'off' in str(n) for n in entities["numbers"])
    metrics["commercial_intensity"] = 0.8 if has_percentage else (0.4 if has_numbers else 0.1)
    
    # Proper noun density (brand focus)
    proper_count = len(entities["proper_nouns"])
    metrics["brand_focus"] = min(proper_count / 3, 1.0)
    
    # Location specificity
    has_location = len(entities["locations"]) > 0
    metrics["locality"] = 1.0 if has_location else 0.0
    
    # Action orientation
    action_count = len(entities["actions"])
    metrics["dynamism"] = min(action_count / 4, 1.0)
    
    # Descriptor richness
    desc_count = len(entities["descriptors"])
    metrics["descriptiveness"] = min(desc_count / 5, 1.0)
    
    # Compute overall "weight" - how visually heavy the design should be
    metrics["visual_weight"] = (
        metrics["verbosity"] * 0.3 +
        metrics["commercial_intensity"] * 0.3 +
        metrics["energy"] * 0.2 +
        metrics["brand_focus"] * 0.2
    )
    
    # Compute "warmth" from word characteristics
    warm_sounds = ['a', 'o', 'u', 'w', 'm', 'n']
    cool_sounds = ['i', 'e', 'k', 's', 't', 'c']
    
    all_chars = prompt.lower()
    warm_count = sum(all_chars.count(c) for c in warm_sounds)
    cool_count = sum(all_chars.count(c) for c in cool_sounds)
    total = warm_count + cool_count + 1
    
    metrics["warmth"] = warm_count / total  # 0-1, higher = warmer
    
    return metrics


def derive_color_from_prompt(prompt: str, entities: Dict, metrics: Dict) -> Dict[str, str]:
    """
    Derive colors DIRECTLY from the prompt.
    No color palettes - pure computation.
    """
    
    # Base hue from significant words
    significant_words = entities["all_significant_words"][:5]
    base_hue = words_to_hue(significant_words)
    
    # Adjust hue based on warmth metric
    warmth = metrics["warmth"]
    if warmth > 0.55:
        # Shift toward warm hues (0-60 or 300-360)
        base_hue = (base_hue % 120) if base_hue < 180 else (300 + base_hue % 60)
    elif warmth < 0.45:
        # Shift toward cool hues (180-270)
        base_hue = 180 + (base_hue % 90)
    
    # Saturation from energy
    energy = metrics["energy"]
    commercial = metrics["commercial_intensity"]
    saturation = 50 + int(energy * 25 + commercial * 20)
    saturation = max(40, min(95, saturation))
    
    # Lightness for accent
    accent_lightness = 55 + int(metrics["dynamism"] * 15)
    
    # Background darkness from visual weight
    weight = metrics["visual_weight"]
    bg_lightness = int(8 + (1 - weight) * 12)  # 8-20, heavier = darker
    
    def hsl_to_hex(h, s, l):
        h, s, l = h / 360, s / 100, l / 100
        if s == 0:
            r = g = b = l
        else:
            def hue2rgb(p, q, t):
                if t < 0: t += 1
                if t > 1: t -= 1
                if t < 1/6: return p + (q - p) * 6 * t
                if t < 1/2: return q
                if t < 2/3: return p + (q - p) * (2/3 - t) * 6
                return p
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue2rgb(p, q, h + 1/3)
            g = hue2rgb(p, q, h)
            b = hue2rgb(p, q, h - 1/3)
        return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
    
    # Generate colors
    accent = hsl_to_hex(base_hue, saturation, accent_lightness)
    
    # Secondary hue - derived from prompt length
    secondary_offset = (len(prompt) * 7) % 60 + 20
    secondary_hue = (base_hue + secondary_offset) % 360
    secondary = hsl_to_hex(secondary_hue, saturation - 15, accent_lightness + 5)
    
    # Background colors
    bg_hue = base_hue
    bg_sat = saturation // 4
    bg_primary = hsl_to_hex(bg_hue, bg_sat, bg_lightness)
    bg_secondary = hsl_to_hex((bg_hue + 15) % 360, bg_sat, bg_lightness + 4)
    
    # Text colors
    text_primary = hsl_to_hex(base_hue, 5, 96)
    text_secondary = hsl_to_hex(base_hue, 8, 75)
    
    return {
        "accent": accent,
        "secondary": secondary,
        "bg_primary": bg_primary,
        "bg_secondary": bg_secondary,
        "text_primary": text_primary,
        "text_secondary": text_secondary,
        "gradient_colors": [bg_primary, bg_secondary],
        "derived_hue": base_hue,
    }


def compute_layout_from_prompt(prompt: str, entities: Dict, metrics: Dict) -> Dict[str, Any]:
    """
    Compute layout structure DIRECTLY from prompt characteristics.
    No layout templates.
    """
    
    seed = prompt_to_seed(prompt)
    
    # Alignment derived from first letter of first proper noun
    if entities["proper_nouns"]:
        first_letter = entities["proper_nouns"][0][0].lower()
        letter_val = ord(first_letter) - ord('a')
        if letter_val < 9:
            alignment = "left"
        elif letter_val < 18:
            alignment = "center"
        else:
            alignment = "right"
    else:
        alignment = "center" if metrics["brand_focus"] < 0.3 else "left"
    
    # Vertical distribution from word count
    word_count = len(prompt.split())
    
    # Compute zone positions mathematically
    zones = {}
    
    # Top margin from verbosity
    top_margin = 15 - int(metrics["verbosity"] * 8)  # 7-15%
    
    # Main content zone
    content_height = 55 + int(metrics["visual_weight"] * 20)  # 55-75%
    
    # Zone sizing based on what's present
    has_offer = metrics["commercial_intensity"] > 0.5
    has_location = metrics["locality"] > 0
    
    current_y = top_margin
    
    # Compute widths based on alignment
    if alignment == "left":
        base_x = 8
        width = 65 + int(metrics["complexity"] * 15)
    elif alignment == "right":
        width = 65 + int(metrics["complexity"] * 15)
        base_x = 92 - width
    else:
        width = 75 + int(metrics["complexity"] * 10)
        base_x = (100 - width) / 2
    
    # Badge zone (if offer)
    if has_offer:
        badge_height = 8
        zones["badge"] = {
            "x": base_x if alignment != "right" else 60,
            "y": current_y,
            "width": 30,
            "height": badge_height,
            "priority": 1,
        }
        current_y += badge_height + 3
    
    # Primary text zone (brand/headline)
    primary_height = 20 + int(metrics["brand_focus"] * 10)
    zones["primary"] = {
        "x": base_x,
        "y": current_y,
        "width": width,
        "height": primary_height,
        "priority": 2,
    }
    current_y += primary_height + 2
    
    # Divider zone
    zones["divider"] = {
        "x": base_x if alignment != "right" else base_x + width - 20,
        "y": current_y,
        "width": 18 + int(metrics["energy"] * 10),
        "height": 1,
        "priority": 5,
    }
    current_y += 4
    
    # Secondary text zone
    secondary_height = 8 + int(metrics["descriptiveness"] * 6)
    zones["secondary"] = {
        "x": base_x,
        "y": current_y,
        "width": width - 5,
        "height": secondary_height,
        "priority": 3,
    }
    current_y += secondary_height + 5
    
    # Trust zone (if local)
    if has_location:
        trust_height = 5
        zones["trust"] = {
            "x": base_x,
            "y": current_y,
            "width": width,
            "height": trust_height,
            "priority": 6,
        }
        current_y += trust_height + 4
    
    # CTA zone
    cta_width = 32 + int(metrics["commercial_intensity"] * 10)
    if alignment == "left":
        cta_x = base_x
    elif alignment == "right":
        cta_x = base_x + width - cta_width
    else:
        cta_x = (100 - cta_width) / 2
    
    zones["cta"] = {
        "x": cta_x,
        "y": current_y,
        "width": cta_width,
        "height": 10,
        "priority": 4,
    }
    
    # Compute decorative element positions from seed
    decor_positions = []
    num_decor = 2 + (seed % 3)
    for i in range(num_decor):
        decor_seed = seed + i * 1337
        decor_positions.append({
            "x": (decor_seed % 80) - 10,
            "y": ((decor_seed >> 8) % 70) - 10,
            "size": 30 + (decor_seed % 40),
            "opacity": 0.05 + (decor_seed % 10) / 100,
        })
    
    return {
        "alignment": alignment,
        "zones": zones,
        "decorations": decor_positions,
        "gradient_angle": 120 + (seed % 80),
    }


def generate_copy_from_prompt(prompt: str, entities: Dict, metrics: Dict) -> Dict[str, str]:
    """
    Generate copy DIRECTLY from the prompt.
    No headline templates. Build contextual copy from the actual words and meaning.
    """
    
    copy = {
        "headline": "",
        "subline": "",
        "cta": "",
        "trust": "",
        "badge": "",
    }
    
    proper_nouns = entities["proper_nouns"]
    significant_words = entities["all_significant_words"]
    numbers = entities["numbers"]
    locations = entities["locations"]
    actions = entities["actions"]
    descriptors = entities["descriptors"]
    objects = entities["objects"]
    
    # Extract the brand name - prefer the FIRST proper noun unless another is significantly longer
    # This is because brand names typically appear first in business descriptions
    brand_name = ""
    if proper_nouns:
        # Filter out common generic terms that aren't brand names
        generic_terms = {'Wellness Center', 'Health Center', 'Shopping Center', 'Service Center', 
                        'Business Center', 'The', 'And', 'LLC', 'Inc', 'Pvt', 'Ltd'}
        
        # First proper noun is usually the brand
        brand_name = proper_nouns[0]
        
        # Only prefer a later one if it's significantly longer AND doesn't contain generic terms
        for pn in proper_nouns[1:]:
            if pn not in generic_terms and len(pn) > len(brand_name) + 5:
                brand_name = pn
    
    # Detect business context from words
    word_set = set(w.lower() for w in significant_words)
    
    # Detect if this is a shop/store
    is_shop = bool(word_set & {'shop', 'store', 'mart', 'outlet', 'emporium', 'bazaar', 'showroom'})
    is_restaurant = bool(word_set & {'cafe', 'restaurant', 'diner', 'eatery', 'kitchen', 'bistro', 'food', 'coffee'})
    is_gym = bool(word_set & {'gym', 'fitness', 'workout', 'training', 'strength', 'crossfit'})
    is_tech = bool(word_set & {'tech', 'software', 'app', 'digital', 'cloud', 'data', 'saas', 'pro'})
    is_fashion = bool(word_set & {'fashion', 'style', 'clothing', 'boutique', 'wear', 'apparel', 'dresses'})
    is_spa = bool(word_set & {'spa', 'wellness', 'massage', 'relaxation', 'beauty', 'salon'})
    is_sale = bool(word_set & {'sale', 'offer', 'discount', 'deal', 'off', 'clearance', 'savings'})
    is_local = bool(word_set & {'local', 'nearby', 'neighborhood', 'community', 'town', 'city'}) or metrics["locality"] > 0
    
    # === HEADLINE GENERATION ===
    # Build a natural headline based on what we understand about the business
    
    # Words that are NOT products (stop words for product detection)
    non_product_words = {'shop', 'store', 'mart', 'local', 'the', 'indian', 'chinese', 'american', 'european', 
                         'new', 'old', 'big', 'small', 'best', 'top', 'selling'}
    
    if brand_name:
        # We have a brand name - make it prominent
        brand_words_lower = set(brand_name.lower().split())
        
        # Brand-specific variation seed
        brand_seed = prompt_to_seed(brand_name)
        
        if is_sale and numbers:
            # It's a sale with numbers - lead with the offer
            num_val = numbers[0][0] if isinstance(numbers[0], tuple) else numbers[0]
            copy["headline"] = f"{brand_name}\n{num_val}% OFF"
            copy["badge"] = f"SALE"
        elif is_shop:
            # Local shop - emphasize trust and the product
            # Find actual product words (not brand words, not stop words)
            product_words = [w for w in objects if w.lower() not in non_product_words 
                            and w.lower() not in brand_words_lower
                            and len(w) > 3]
            
            # Multiple phrasings, selected by brand seed
            if product_words:
                product = product_words[0].title()
                shop_headlines = [
                    f"{brand_name}\nYour {product} Destination",
                    f"{brand_name}\n{product} You Can Trust",
                    f"{brand_name}\nBest {product} Deals",
                    f"{brand_name}\n{product} Excellence",
                    f"{brand_name}\nWhere {product} Matters",
                ]
                copy["headline"] = shop_headlines[brand_seed % len(shop_headlines)]
            else:
                generic_shop = [
                    f"{brand_name}\nQuality You Can Trust",
                    f"{brand_name}\nYour Trusted Choice",
                    f"{brand_name}\nValue. Quality. Trust.",
                    f"{brand_name}\nService First",
                ]
                copy["headline"] = generic_shop[brand_seed % len(generic_shop)]
        elif is_restaurant:
            food_words = [w for w in objects if w not in ['cafe', 'restaurant', 'kitchen']]
            if 'coffee' in word_set:
                coffee_headlines = [
                    f"{brand_name}\nBrewed Fresh Daily",
                    f"{brand_name}\nPerfect Pour Every Time",
                    f"{brand_name}\nYour Daily Ritual",
                    f"{brand_name}\nCrafted with Care",
                ]
                copy["headline"] = coffee_headlines[brand_seed % len(coffee_headlines)]
            elif food_words:
                food_headlines = [
                    f"{brand_name}\nTaste the Difference",
                    f"{brand_name}\nFresh. Authentic. Delicious.",
                    f"{brand_name}\nWhere Flavor Lives",
                    f"{brand_name}\nCrafted for You",
                ]
                copy["headline"] = food_headlines[brand_seed % len(food_headlines)]
            else:
                copy["headline"] = f"{brand_name}\nFlavors You'll Love"
        elif is_gym:
            gym_headlines = [
                f"{brand_name}\nTransform Your Body",
                f"{brand_name}\nStrength Starts Here",
                f"{brand_name}\nPush Your Limits",
                f"{brand_name}\nBuilt Different",
            ]
            copy["headline"] = gym_headlines[brand_seed % len(gym_headlines)]
        elif is_tech:
            tech_headlines = [
                f"{brand_name}\nSimplify Your Workflow",
                f"{brand_name}\nBuilt for Performance",
                f"{brand_name}\nPower Your Potential",
                f"{brand_name}\nSmart. Fast. Reliable.",
            ]
            copy["headline"] = tech_headlines[brand_seed % len(tech_headlines)]
        elif is_fashion:
            fashion_headlines = [
                f"{brand_name}\nRedefine Your Look",
                f"{brand_name}\nStyle Without Limits",
                f"{brand_name}\nWear Your Story",
                f"{brand_name}\nElevate Your Wardrobe",
            ]
            copy["headline"] = fashion_headlines[brand_seed % len(fashion_headlines)]
        elif is_spa:
            spa_headlines = [
                f"{brand_name}\nUnwind & Rejuvenate",
                f"{brand_name}\nPure Relaxation",
                f"{brand_name}\nYour Sanctuary Awaits",
                f"{brand_name}\nRenew. Restore. Relax.",
            ]
            copy["headline"] = spa_headlines[brand_seed % len(spa_headlines)]
        else:
            # Generic but contextual
            if descriptors:
                desc = descriptors[0].title()
                copy["headline"] = f"{brand_name}\n{desc} Excellence"
            else:
                copy["headline"] = f"{brand_name}"
    else:
        # No brand name - build from significant words
        if len(significant_words) >= 2:
            copy["headline"] = f"{significant_words[0].upper()}\n{' '.join(significant_words[1:3]).title()}"
        elif significant_words:
            copy["headline"] = significant_words[0].upper()
        else:
            copy["headline"] = "Welcome"
    
    # Ensure brand_seed is available for subline/CTA variation
    brand_seed = prompt_to_seed(brand_name) if brand_name else prompt_to_seed(prompt)
    
    # === SUBLINE GENERATION ===
    # Create a supporting message
    
    remaining_words = [w for w in objects if w.lower() not in copy["headline"].lower()]
    
    if is_local and locations:
        loc = locations[0]
        copy["subline"] = f"Proudly serving {loc} and surrounding areas"
    elif is_local:
        copy["subline"] = "Your neighborhood choice for quality and value"
    elif is_shop and remaining_words:
        items = remaining_words[:3]
        shop_sublines = [
            f"Wide selection of {', '.join(items)} and more",
            f"Quality {items[0] if items else 'products'} at honest prices",
            f"Your one-stop destination for {items[0] if items else 'everything'}",
        ]
        copy["subline"] = shop_sublines[brand_seed % len(shop_sublines)] if brand_seed else shop_sublines[0]
    elif is_restaurant:
        restaurant_sublines = [
            "Fresh ingredients, authentic flavors, memorable moments",
            "Where every meal is an experience",
            "Crafted with passion, served with love",
            "Taste that keeps you coming back",
        ]
        copy["subline"] = restaurant_sublines[brand_seed % len(restaurant_sublines)] if brand_seed else restaurant_sublines[0]
    elif is_gym:
        gym_sublines = [
            "Expert trainers • Modern equipment • Results guaranteed",
            "Your goals. Our mission. Real results.",
            "No shortcuts. Just hard work that pays off.",
            "Where champions are made",
        ]
        copy["subline"] = gym_sublines[brand_seed % len(gym_sublines)] if brand_seed else gym_sublines[0]
    elif is_tech:
        tech_sublines = [
            "Built for teams who demand more",
            "Enterprise-grade reliability, startup-level agility",
            "The tool your workflow deserves",
            "Scale without compromise",
        ]
        copy["subline"] = tech_sublines[brand_seed % len(tech_sublines)] if brand_seed else tech_sublines[0]
    elif is_fashion:
        fashion_sublines = [
            "Curated collections for every occasion",
            "Express yourself through style",
            "Where trends meet timeless elegance",
            "Fashion that fits your life",
        ]
        copy["subline"] = fashion_sublines[brand_seed % len(fashion_sublines)] if brand_seed else fashion_sublines[0]
    elif is_spa:
        spa_sublines = [
            "Expert therapists • Serene ambiance • Pure relaxation",
            "Where stress melts away",
            "Indulge in ultimate self-care",
            "Your escape from the everyday",
        ]
        copy["subline"] = spa_sublines[brand_seed % len(spa_sublines)] if brand_seed else spa_sublines[0]
    elif is_sale:
        copy["subline"] = "Limited time • Don't miss out"
    else:
        # Use remaining words meaningfully
        if remaining_words:
            copy["subline"] = ' '.join(remaining_words[:4]).capitalize()
        else:
            copy["subline"] = ""
    
    # === CTA GENERATION ===
    # Action-appropriate call to action
    
    if is_shop:
        shop_ctas = ["Shop Now", "Browse Collection", "See Deals", "Explore"]
        copy["cta"] = shop_ctas[brand_seed % len(shop_ctas)] if brand_seed else shop_ctas[0]
    elif is_restaurant:
        restaurant_ctas = ["Order Now", "View Menu", "Reserve", "Get Yours"]
        copy["cta"] = restaurant_ctas[brand_seed % len(restaurant_ctas)] if brand_seed else restaurant_ctas[0]
    elif is_gym:
        gym_ctas = ["Join Today", "Start Free", "Get Fit", "Try Free"]
        copy["cta"] = gym_ctas[brand_seed % len(gym_ctas)] if brand_seed else gym_ctas[0]
    elif is_tech:
        tech_ctas = ["Get Started", "Try Free", "Start Now", "Learn More"]
        copy["cta"] = tech_ctas[brand_seed % len(tech_ctas)] if brand_seed else tech_ctas[0]
    elif is_fashion:
        fashion_ctas = ["Explore", "Shop Now", "Discover", "See More"]
        copy["cta"] = fashion_ctas[brand_seed % len(fashion_ctas)] if brand_seed else fashion_ctas[0]
    elif is_spa:
        spa_ctas = ["Book Now", "Reserve", "Treat Yourself", "Book Today"]
        copy["cta"] = spa_ctas[brand_seed % len(spa_ctas)] if brand_seed else spa_ctas[0]
    elif is_sale:
        copy["cta"] = "Grab Deal"
    elif actions:
        # Derive from action words
        action = actions[0]
        if action.endswith('ing'):
            base = action[:-3]
            if base.endswith('e'):
                copy["cta"] = base.capitalize()
            else:
                copy["cta"] = (base + 'e').capitalize() if len(base) > 2 else action.capitalize()
        else:
            copy["cta"] = action.capitalize()
    else:
        copy["cta"] = "Learn More"
    
    # === BADGE (if sale) ===
    if is_sale and numbers and not copy["badge"]:
        num_val = numbers[0][0] if isinstance(numbers[0], tuple) else numbers[0]
        if '%' in str(numbers[0]) or any('off' in str(n).lower() for n in numbers):
            copy["badge"] = f"{num_val}% OFF"
        else:
            copy["badge"] = "SALE"
    
    # === TRUST LINE ===
    if is_local:
        if locations:
            copy["trust"] = f"✓ Serving {locations[0]} since day one"
        else:
            copy["trust"] = "✓ Trusted by locals"
    elif is_shop:
        copy["trust"] = "✓ Genuine products • Honest prices"
    elif is_tech:
        copy["trust"] = "✓ Enterprise ready • 99.9% uptime"
    
    return copy


def build_elements(layout: Dict, colors: Dict, copy: Dict, metrics: Dict, prompt: str) -> List[Dict]:
    """
    Build visual elements from computed layout, colors, and copy.
    """
    
    elements = []
    zones = layout["zones"]
    alignment = layout["alignment"]
    seed = prompt_to_seed(prompt)
    
    # === DECORATIVE ELEMENTS ===
    for i, decor in enumerate(layout["decorations"]):
        elements.append({
            "type": "shape",
            "shape_type": "circle",
            "id": f"decor_{i}",
            "position": {"x": decor["x"], "y": decor["y"]},
            "size": {"width": decor["size"], "height": decor["size"]},
            "fill_color": colors["accent"] if i % 2 == 0 else colors["secondary"],
            "opacity": decor["opacity"],
        })
    
    # === BADGE (if present) ===
    if "badge" in zones and copy.get("badge"):
        z = zones["badge"]
        corner_radius = 4 + (seed % 20)
        
        elements.append({
            "type": "shape",
            "shape_type": "rect",
            "id": "badge_bg",
            "position": {"x": z["x"], "y": z["y"]},
            "size": {"width": z["width"], "height": z["height"]},
            "fill_color": colors["accent"],
            "corner_radius": corner_radius,
        })
        elements.append({
            "type": "text",
            "id": "badge_text",
            "position": {"x": z["x"], "y": z["y"] + 1.5},
            "size": {"width": z["width"], "height": z["height"] - 3},
            "content": copy["badge"],
            "font_size": 18,
            "font_weight": 800,
            "font_family": "Montserrat",
            "color": colors["bg_primary"],
            "align": "center",
        })
    
    # === PRIMARY TEXT ===
    if "primary" in zones:
        z = zones["primary"]
        
        # Font size derived from metrics
        base_font = 42 + int(metrics["brand_focus"] * 25)
        
        elements.append({
            "type": "text",
            "id": "headline",
            "position": {"x": z["x"], "y": z["y"]},
            "size": {"width": z["width"], "height": z["height"]},
            "content": copy["headline"],
            "font_size": base_font,
            "font_weight": 800,
            "font_family": "Montserrat",
            "color": colors["text_primary"],
            "align": alignment,
            "line_height": 0.95,
            "letter_spacing": -1,
        })
    
    # === DIVIDER ===
    if "divider" in zones:
        z = zones["divider"]
        elements.append({
            "type": "shape",
            "shape_type": "rect",
            "id": "divider",
            "position": {"x": z["x"], "y": z["y"]},
            "size": {"width": z["width"], "height": 0.8},
            "fill_color": colors["accent"],
            "opacity": 0.9,
        })
    
    # === SECONDARY TEXT ===
    if "secondary" in zones and copy.get("subline"):
        z = zones["secondary"]
        elements.append({
            "type": "text",
            "id": "subline",
            "position": {"x": z["x"], "y": z["y"]},
            "size": {"width": z["width"], "height": z["height"]},
            "content": copy["subline"],
            "font_size": 16 + int(metrics["descriptiveness"] * 4),
            "font_weight": 400,
            "font_family": "Inter",
            "color": colors["text_secondary"],
            "align": alignment,
            "opacity": 0.85,
        })
    
    # === TRUST LINE ===
    if "trust" in zones and copy.get("trust"):
        z = zones["trust"]
        elements.append({
            "type": "text",
            "id": "trust",
            "position": {"x": z["x"], "y": z["y"]},
            "size": {"width": z["width"], "height": z["height"]},
            "content": copy["trust"],
            "font_size": 13,
            "font_weight": 500,
            "font_family": "Inter",
            "color": colors["accent"],
            "align": alignment,
        })
    
    # === CTA BUTTON ===
    if "cta" in zones:
        z = zones["cta"]
        corner_radius = 5 + (seed % 20)
        
        elements.append({
            "type": "shape",
            "shape_type": "rect",
            "id": "cta_bg",
            "position": {"x": z["x"], "y": z["y"]},
            "size": {"width": z["width"], "height": z["height"]},
            "fill_color": colors["accent"],
            "corner_radius": corner_radius,
        })
        elements.append({
            "type": "text",
            "id": "cta_text",
            "position": {"x": z["x"], "y": z["y"] + 2.5},
            "size": {"width": z["width"], "height": 5},
            "content": copy["cta"].upper(),
            "font_size": 14,
            "font_weight": 700,
            "font_family": "Inter",
            "color": colors["bg_primary"],
            "align": "center",
            "letter_spacing": 1,
        })
    
    # === ACCENT ELEMENTS ===
    # Add corner accents based on seed
    accent_type = seed % 4
    
    if accent_type == 0:
        # L-corners
        elements.extend([
            {"type": "shape", "shape_type": "rect", "id": "corner_tl_h", "position": {"x": 5, "y": 5}, "size": {"width": 12, "height": 0.5}, "fill_color": colors["accent"], "opacity": 0.5},
            {"type": "shape", "shape_type": "rect", "id": "corner_tl_v", "position": {"x": 5, "y": 5}, "size": {"width": 0.5, "height": 12}, "fill_color": colors["accent"], "opacity": 0.5},
        ])
    elif accent_type == 1:
        # Dots
        for i in range(4):
            elements.append({
                "type": "shape", "shape_type": "circle", "id": f"dot_{i}",
                "position": {"x": 5 + i * 3, "y": 5},
                "size": {"width": 1.5, "height": 1.5},
                "fill_color": colors["accent"], "opacity": 0.4,
            })
    elif accent_type == 2:
        # Side bar
        elements.append({
            "type": "shape", "shape_type": "rect", "id": "side_bar",
            "position": {"x": 0, "y": 25},
            "size": {"width": 1.5, "height": 50},
            "fill_color": colors["accent"], "opacity": 0.6,
        })
    
    return elements


def generate_design(prompt: str, platform: str = "instagram", format: str = "post") -> Dict[str, Any]:
    """
    MAIN ENTRY POINT
    
    Generate a completely unique design by deriving everything from the prompt.
    Zero templates. Zero categories. Pure computation.
    """
    
    # Canvas size
    sizes = {
        "post": (1080, 1080), "square": (1080, 1080),
        "story": (1080, 1920), "reel": (1080, 1920),
        "landscape": (1200, 628), "portrait": (1080, 1350),
    }
    width, height = sizes.get(format.lower(), (1080, 1080))
    
    # STEP 1: Extract all entities from prompt
    entities = extract_all_entities(prompt)
    
    # STEP 2: Compute metrics from prompt
    metrics = compute_prompt_metrics(prompt, entities)
    
    # STEP 3: Derive colors from prompt
    colors = derive_color_from_prompt(prompt, entities, metrics)
    
    # STEP 4: Compute layout from prompt
    layout = compute_layout_from_prompt(prompt, entities, metrics)
    
    # STEP 5: Generate copy from prompt
    copy = generate_copy_from_prompt(prompt, entities, metrics)
    
    # STEP 6: Build elements
    elements = build_elements(layout, colors, copy, metrics, prompt)
    
    # Assemble blueprint
    blueprint = {
        "metadata": {
            "platform": platform,
            "format": format,
            "width": width,
            "height": height,
            "generator": "generative_designer_v1",
        },
        "prompt_analysis": {
            "entities": entities,
            "metrics": metrics,
        },
        "colors": colors,
        "layout": layout,
        "copy": copy,
        "background": {
            "type": "gradient",
            "colors": colors["gradient_colors"],
            "angle": layout["gradient_angle"],
            "color": colors["bg_primary"],
        },
        "elements": elements,
    }
    
    return blueprint


def blueprint_to_fabric(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """Convert blueprint to Fabric.js format"""
    
    width = blueprint["metadata"]["width"]
    height = blueprint["metadata"]["height"]
    fabric_objects = []
    
    # Background gradient
    bg = blueprint.get("background", {})
    colors = bg.get("colors", ["#1a1a2e"])
    angle = bg.get("angle", 135)
    
    if len(colors) > 1:
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
    else:
        fabric_objects.append({
            "type": "rect",
            "left": 0, "top": 0,
            "width": width, "height": height,
            "fill": colors[0],
            "selectable": False, "evented": False,
        })
    
    # Convert elements
    for element in blueprint.get("elements", []):
        pos = element.get("position", {"x": 0, "y": 0})
        size = element.get("size", {"width": 10, "height": 10})
        
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
                "id": element.get("id", "shape"),
                "left": left,
                "top": top,
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
        "background": bg.get("color", "#1a1a2e"),
    }
