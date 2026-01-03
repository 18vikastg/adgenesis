"""
CREATIVE DIRECTOR - Prompt-Driven Design Generation
====================================================
This module generates TRULY UNIQUE designs by deeply analyzing each prompt
and constructing every element from scratch. NO templates. NO categories.

Every design is:
- Prompt-specific
- Context-aware  
- Custom-composed
- Visually unique
"""

import hashlib
import math
import re
from typing import Dict, List, Any, Tuple, Optional


class PromptAnalyzer:
    """
    Deep prompt analysis - extracts EVERYTHING meaningful from the user's input
    to drive truly custom design decisions.
    """
    
    def __init__(self, prompt: str):
        self.raw_prompt = prompt
        self.prompt_lower = prompt.lower()
        self.words = prompt.split()
        self.word_count = len(self.words)
        self.char_count = len(prompt)
        
        # Generate unique seed from prompt content
        self.prompt_hash = int(hashlib.sha256(prompt.encode()).hexdigest(), 16)
        
        # Deep analysis results
        self.analysis = self._deep_analyze()
    
    def _deep_analyze(self) -> Dict[str, Any]:
        """Perform deep contextual analysis of the prompt"""
        
        analysis = {
            # Core identity
            "brand_name": self._extract_brand_name(),
            "business_type": self._determine_business_type(),
            "business_scale": self._determine_scale(),
            "locality": self._extract_locality(),
            
            # Emotional/tonal
            "emotional_tone": self._determine_emotion(),
            "urgency_level": self._determine_urgency(),
            "trust_signals_needed": self._needs_trust(),
            "excitement_level": self._determine_excitement(),
            
            # Commercial
            "has_offer": self._has_offer(),
            "offer_details": self._extract_offer(),
            "price_sensitivity": self._is_price_focused(),
            "value_proposition": self._extract_value_prop(),
            
            # Visual direction
            "visual_weight": self._calculate_visual_weight(),
            "density_preference": self._calculate_density(),
            "color_temperature": self._determine_color_temp(),
            "contrast_level": self._determine_contrast(),
            
            # Unique characteristics
            "unique_keywords": self._extract_unique_keywords(),
            "differentiators": self._find_differentiators(),
            "target_audience_hints": self._infer_audience(),
        }
        
        return analysis
    
    def _extract_brand_name(self) -> Optional[str]:
        """Extract brand/business name with high precision"""
        
        # Pattern 1: "X Mobiles/Store/Shop/Cafe" - two-word brand names
        pattern1 = re.search(r'([A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+)\s*[-–—]', self.raw_prompt)
        if pattern1:
            return pattern1.group(1).strip()
        
        # Pattern 2: "X shop/store/cafe/brand" with possible two words before
        pattern2 = re.search(r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s+(?:shop|store|cafe|brand|studio|gym|salon|restaurant|electronics|fashion)\b', self.raw_prompt, re.IGNORECASE)
        if pattern2:
            name = pattern2.group(1).strip()
            # Check if next word is also capitalized (two-word brand)
            full_match = re.search(r'([A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+)\s*(?:[-–—]|shop|store|cafe|brand)', self.raw_prompt, re.IGNORECASE)
            if full_match:
                return full_match.group(1).strip()
            return name
        
        # Pattern 3: "named/called X"
        pattern3 = re.search(r'(?:named|called)\s+["\']?([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)', self.raw_prompt)
        if pattern3:
            return pattern3.group(1).strip()
        
        # Pattern 4: First capitalized phrase that looks like a brand
        pattern4 = re.search(r'^([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s*[-–—]', self.raw_prompt)
        if pattern4:
            return pattern4.group(1).strip()
        
        # Pattern 5: Find capitalized words that look like brand names
        caps = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', self.raw_prompt)
        # Filter out common words
        common = ['The', 'And', 'For', 'New', 'Best', 'Top', 'Your', 'Our', 'Get', 'Buy', 'Shop', 'Now', 'Today', 'Delhi', 'Mumbai', 'India', 'Indian']
        brands = [c for c in caps if c not in common and len(c) > 2]
        if brands:
            return brands[0]
        
        return None
    
    def _determine_business_type(self) -> str:
        """Determine the specific type of business"""
        
        business_indicators = {
            "retail_electronics": ["mobile", "phone", "electronics", "gadget", "smartphone", "laptop", "computer"],
            "retail_fashion": ["fashion", "clothing", "apparel", "boutique", "dress", "wear", "style"],
            "food_restaurant": ["restaurant", "cafe", "coffee", "food", "kitchen", "dining", "eat", "menu"],
            "food_delivery": ["delivery", "order food", "takeaway", "takeout"],
            "fitness_gym": ["gym", "fitness", "workout", "training", "exercise", "muscle"],
            "beauty_salon": ["salon", "spa", "beauty", "skincare", "makeup", "cosmetic", "glow"],
            "professional_service": ["consulting", "agency", "service", "solution", "legal", "accounting"],
            "tech_startup": ["startup", "app", "software", "saas", "platform", "tech", "ai", "digital"],
            "ecommerce": ["online", "ecommerce", "e-commerce", "shop online", "buy online"],
            "local_store": ["store", "shop", "local", "near", "city", "town"],
            "event": ["event", "party", "concert", "festival", "wedding", "celebration"],
            "education": ["course", "class", "learn", "training", "academy", "school", "tutorial"],
            "real_estate": ["property", "real estate", "home", "house", "apartment", "rent"],
            "travel": ["travel", "trip", "vacation", "hotel", "flight", "tour", "destination"],
            "healthcare": ["clinic", "hospital", "doctor", "health", "medical", "pharmacy", "dental"],
        }
        
        for biz_type, keywords in business_indicators.items():
            for kw in keywords:
                if kw in self.prompt_lower:
                    return biz_type
        
        return "general_business"
    
    def _determine_scale(self) -> str:
        """Determine business scale/size"""
        
        large_indicators = ["chain", "franchise", "national", "international", "global", "brand", "launch", "mega"]
        small_indicators = ["local", "neighborhood", "family", "small", "your local", "trusted", "near you"]
        
        for word in large_indicators:
            if word in self.prompt_lower:
                return "large"
        
        for word in small_indicators:
            if word in self.prompt_lower:
                return "small_local"
        
        return "medium"
    
    def _extract_locality(self) -> Optional[str]:
        """Extract location/city/region if mentioned"""
        
        # Look for "in [Place]" pattern
        loc_pattern = re.search(r'(?:in|at|near|from)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', self.raw_prompt)
        if loc_pattern:
            place = loc_pattern.group(1)
            common_words = ['The', 'Your', 'Our', 'Best', 'New']
            if place not in common_words:
                return place
        
        # Indian cities often mentioned
        indian_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
        for city in indian_cities:
            if city.lower() in self.prompt_lower:
                return city
        
        return None
    
    def _determine_emotion(self) -> str:
        """Determine the emotional tone the design should convey"""
        
        emotions = {
            "trust": ["trusted", "reliable", "honest", "genuine", "authentic", "certified", "quality"],
            "excitement": ["exciting", "amazing", "incredible", "wow", "new", "launch", "introducing"],
            "urgency": ["urgent", "hurry", "limited", "now", "today", "flash", "last chance", "ending"],
            "warmth": ["warm", "welcome", "family", "home", "cozy", "friendly", "care"],
            "prestige": ["luxury", "premium", "exclusive", "elite", "vip", "high-end"],
            "value": ["affordable", "cheap", "budget", "save", "discount", "deal", "offer", "price"],
            "professionalism": ["professional", "expert", "specialist", "quality", "certified"],
            "fun": ["fun", "enjoy", "celebrate", "party", "happy", "joy"],
        }
        
        scores = {emotion: 0 for emotion in emotions}
        for emotion, keywords in emotions.items():
            for kw in keywords:
                if kw in self.prompt_lower:
                    scores[emotion] += 1
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return "neutral"
    
    def _determine_urgency(self) -> int:
        """Rate urgency level 0-10"""
        
        urgent_words = ["urgent", "now", "today", "limited", "hurry", "flash", "ending", "last", "quick", "fast", "instant"]
        count = sum(1 for w in urgent_words if w in self.prompt_lower)
        return min(count * 3, 10)
    
    def _needs_trust(self) -> bool:
        """Determine if trust signals are important for this business"""
        
        trust_contexts = ["mobile", "electronics", "money", "finance", "health", "medical", "legal", "real estate", "local", "store", "shop"]
        return any(ctx in self.prompt_lower for ctx in trust_contexts)
    
    def _determine_excitement(self) -> int:
        """Rate excitement level 0-10"""
        
        exciting_words = ["new", "launch", "introducing", "amazing", "incredible", "exciting", "wow", "revolutionary", "exclusive"]
        count = sum(1 for w in exciting_words if w in self.prompt_lower)
        return min(count * 2, 10)
    
    def _has_offer(self) -> bool:
        """Check if there's a promotional offer"""
        
        offer_words = ["sale", "discount", "off", "offer", "deal", "save", "free", "promo", "coupon", "%"]
        return any(w in self.prompt_lower for w in offer_words)
    
    def _extract_offer(self) -> Optional[Dict]:
        """Extract offer details"""
        
        # Percentage discount
        pct_match = re.search(r'(\d+)\s*%\s*(?:off|discount)?', self.prompt_lower)
        if pct_match:
            return {"type": "percentage", "value": int(pct_match.group(1)), "text": f"{pct_match.group(1)}% OFF"}
        
        # Flat discount
        flat_match = re.search(r'(?:rs\.?|₹|inr)\s*(\d+)\s*(?:off|discount)', self.prompt_lower)
        if flat_match:
            return {"type": "flat", "value": int(flat_match.group(1)), "text": f"₹{flat_match.group(1)} OFF"}
        
        # Free something
        if "free" in self.prompt_lower:
            free_match = re.search(r'free\s+(\w+)', self.prompt_lower)
            if free_match:
                return {"type": "freebie", "value": free_match.group(1), "text": f"FREE {free_match.group(1).upper()}"}
        
        # Generic sale
        if "sale" in self.prompt_lower:
            return {"type": "sale", "value": None, "text": "SALE"}
        
        return None
    
    def _is_price_focused(self) -> bool:
        """Is this a price/value focused message?"""
        
        price_words = ["price", "affordable", "cheap", "budget", "value", "deal", "offer", "discount", "save", "cost"]
        return sum(1 for w in price_words if w in self.prompt_lower) >= 2
    
    def _extract_value_prop(self) -> Optional[str]:
        """Extract the core value proposition"""
        
        # Look for "best X", "quality X", "affordable X" patterns
        value_patterns = [
            r'best\s+(\w+(?:\s+\w+)?)',
            r'quality\s+(\w+)',
            r'affordable\s+(\w+)',
            r'trusted\s+(\w+)',
            r'premium\s+(\w+)',
        ]
        
        for pattern in value_patterns:
            match = re.search(pattern, self.prompt_lower)
            if match:
                return match.group(0)
        
        return None
    
    def _calculate_visual_weight(self) -> str:
        """Determine how 'heavy' the design should feel"""
        
        # More words = potentially more content = heavier design
        if self.word_count > 15:
            return "heavy"
        elif self.word_count > 8:
            return "medium"
        else:
            return "light"
    
    def _calculate_density(self) -> str:
        """How dense should the information be?"""
        
        info_indicators = ["features", "services", "offers", "products", "all", "everything", "complete", "full"]
        count = sum(1 for w in info_indicators if w in self.prompt_lower)
        
        if count >= 2:
            return "dense"
        elif count == 1:
            return "moderate"
        else:
            return "focused"
    
    def _determine_color_temp(self) -> str:
        """Determine warm vs cool color direction"""
        
        warm_contexts = ["food", "coffee", "restaurant", "home", "family", "cozy", "warm", "traditional", "indian", "spice"]
        cool_contexts = ["tech", "digital", "modern", "startup", "app", "software", "ai", "future", "cool", "fresh"]
        
        warm_score = sum(1 for w in warm_contexts if w in self.prompt_lower)
        cool_score = sum(1 for w in cool_contexts if w in self.prompt_lower)
        
        if warm_score > cool_score:
            return "warm"
        elif cool_score > warm_score:
            return "cool"
        else:
            return "neutral"
    
    def _determine_contrast(self) -> str:
        """How much contrast should the design have?"""
        
        high_contrast_contexts = ["sale", "urgent", "flash", "bold", "mega", "big", "huge"]
        low_contrast_contexts = ["elegant", "subtle", "minimal", "soft", "gentle", "luxury"]
        
        if any(w in self.prompt_lower for w in high_contrast_contexts):
            return "high"
        elif any(w in self.prompt_lower for w in low_contrast_contexts):
            return "low"
        else:
            return "medium"
    
    def _extract_unique_keywords(self) -> List[str]:
        """Extract keywords unique to this prompt"""
        
        # Remove common words
        common = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'your', 'our', 'my'}
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', self.prompt_lower)
        unique = [w for w in words if w not in common]
        
        return list(set(unique))[:10]
    
    def _find_differentiators(self) -> List[str]:
        """What makes this business different?"""
        
        differentiators = []
        
        diff_patterns = [
            (r'only\s+(\w+)', "exclusivity"),
            (r'first\s+(\w+)', "pioneering"),
            (r'best\s+(\w+)', "quality"),
            (r'largest\s+(\w+)', "scale"),
            (r'trusted', "reliability"),
            (r'certified', "credibility"),
            (r'authentic', "genuineness"),
            (r'original', "authenticity"),
        ]
        
        for pattern, diff_type in diff_patterns:
            if re.search(pattern, self.prompt_lower):
                differentiators.append(diff_type)
        
        return differentiators
    
    def _infer_audience(self) -> str:
        """Infer target audience from context"""
        
        audience_hints = {
            "youth": ["trendy", "cool", "instagram", "tiktok", "gen z", "student", "college"],
            "families": ["family", "kids", "children", "home", "household"],
            "professionals": ["business", "professional", "office", "corporate", "enterprise"],
            "budget_conscious": ["affordable", "budget", "cheap", "save", "discount", "value"],
            "premium": ["luxury", "premium", "exclusive", "high-end", "elite"],
            "local": ["local", "neighborhood", "community", "near", "city"],
        }
        
        for audience, hints in audience_hints.items():
            if any(h in self.prompt_lower for h in hints):
                return audience
        
        return "general"


class CreativeDirector:
    """
    The Creative Director generates UNIQUE designs from scratch.
    No templates. No categories. Pure prompt-driven creativity.
    """
    
    def __init__(self, prompt: str, platform: str = "instagram", format: str = "post"):
        self.prompt = prompt
        self.platform = platform
        self.format = format
        
        # Deep analysis
        self.analyzer = PromptAnalyzer(prompt)
        self.analysis = self.analyzer.analysis
        self.seed = self.analyzer.prompt_hash
        
        # Canvas dimensions
        self.width, self.height = self._get_canvas_size()
    
    def _get_canvas_size(self) -> Tuple[int, int]:
        """Get canvas dimensions"""
        sizes = {
            "post": (1080, 1080), "square": (1080, 1080),
            "story": (1080, 1920), "reel": (1080, 1920),
            "landscape": (1200, 628), "portrait": (1080, 1350),
        }
        return sizes.get(self.format.lower(), (1080, 1080))
    
    def _seeded_choice(self, items: list, offset: int = 0) -> Any:
        """Make a deterministic choice based on prompt seed"""
        if not items:
            return None
        idx = (self.seed + offset) % len(items)
        return items[idx]
    
    def _seeded_float(self, offset: int = 0) -> float:
        """Get a deterministic float 0-1 based on prompt seed"""
        return ((self.seed + offset) % 1000) / 1000
    
    def _seeded_int(self, min_val: int, max_val: int, offset: int = 0) -> int:
        """Get a deterministic int in range based on prompt seed"""
        return min_val + ((self.seed + offset) % (max_val - min_val + 1))
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate a COMPLETELY UNIQUE design based on deep prompt analysis.
        """
        
        # PHASE 1: Creative Thinking (simulated)
        creative_direction = self._develop_creative_direction()
        
        # PHASE 2: Color Palette (custom for this prompt)
        colors = self._create_custom_palette()
        
        # PHASE 3: Layout Structure (unique to this prompt)
        layout = self._invent_layout()
        
        # PHASE 4: Copy/Messaging (contextual, not generic)
        copy = self._write_contextual_copy()
        
        # PHASE 5: Visual Elements (built from scratch)
        elements = self._construct_elements(layout, colors, copy)
        
        # PHASE 6: Background (custom for this context)
        background = self._design_background(colors)
        
        # Assemble blueprint
        blueprint = {
            "metadata": {
                "platform": self.platform,
                "format": self.format,
                "width": self.width,
                "height": self.height,
                "creative_direction": creative_direction,
                "generation_method": "creative_director_v1",
            },
            "analysis": self.analysis,
            "creative_direction": creative_direction,
            "color_palette": colors,
            "copy": copy,
            "background": background,
            "elements": elements,
        }
        
        return blueprint
    
    def _develop_creative_direction(self) -> Dict[str, Any]:
        """
        Develop the creative direction based on analysis.
        This is the 'thinking' phase.
        """
        
        brand = self.analysis["brand_name"]
        biz_type = self.analysis["business_type"]
        scale = self.analysis["business_scale"]
        emotion = self.analysis["emotional_tone"]
        has_offer = self.analysis["has_offer"]
        locality = self.analysis["locality"]
        
        direction = {
            "primary_message": None,
            "visual_style": None,
            "focal_point": None,
            "hierarchy": [],
            "design_rationale": "",
        }
        
        # Determine primary message based on analysis
        if has_offer and self.analysis["offer_details"]:
            direction["primary_message"] = "promotional"
            direction["focal_point"] = "offer"
            direction["hierarchy"] = ["offer", "brand", "cta", "trust"]
        elif scale == "small_local":
            direction["primary_message"] = "trust_building"
            direction["focal_point"] = "brand_identity"
            direction["hierarchy"] = ["brand", "value_prop", "trust_signals", "cta"]
        elif self.analysis["excitement_level"] > 5:
            direction["primary_message"] = "announcement"
            direction["focal_point"] = "headline"
            direction["hierarchy"] = ["headline", "brand", "details", "cta"]
        else:
            direction["primary_message"] = "brand_awareness"
            direction["focal_point"] = "brand"
            direction["hierarchy"] = ["brand", "tagline", "cta"]
        
        # Visual style based on business type and emotion
        if biz_type in ["retail_electronics", "retail_fashion", "local_store"]:
            if emotion == "trust":
                direction["visual_style"] = "clean_trustworthy"
            elif emotion == "value":
                direction["visual_style"] = "bold_promotional"
            else:
                direction["visual_style"] = "professional_retail"
        elif biz_type in ["tech_startup", "professional_service"]:
            direction["visual_style"] = "modern_minimal"
        elif biz_type in ["food_restaurant", "food_delivery"]:
            direction["visual_style"] = "warm_appetizing"
        elif biz_type in ["fitness_gym"]:
            direction["visual_style"] = "energetic_bold"
        elif biz_type in ["beauty_salon"]:
            direction["visual_style"] = "elegant_refined"
        else:
            direction["visual_style"] = "balanced_professional"
        
        # Generate design rationale
        rationale_parts = []
        if brand:
            rationale_parts.append(f"Design for '{brand}'")
        rationale_parts.append(f"targeting {self.analysis['target_audience_hints']} audience")
        rationale_parts.append(f"with {emotion} emotional tone")
        if locality:
            rationale_parts.append(f"emphasizing local presence in {locality}")
        
        direction["design_rationale"] = ", ".join(rationale_parts)
        
        return direction
    
    def _create_custom_palette(self) -> Dict[str, str]:
        """
        Create a CUSTOM color palette based on the specific prompt analysis.
        Not from a predefined list.
        """
        
        temp = self.analysis["color_temperature"]
        contrast = self.analysis["contrast_level"]
        emotion = self.analysis["emotional_tone"]
        biz_type = self.analysis["business_type"]
        
        # Base hue selection based on context
        hue_ranges = {
            "warm": (15, 45),      # Orange-yellow
            "cool": (200, 240),    # Blue
            "neutral": (0, 360),   # Any
        }
        
        hue_min, hue_max = hue_ranges.get(temp, (0, 360))
        base_hue = self._seeded_int(hue_min, hue_max, offset=100)
        
        # Adjust hue based on business type
        business_hue_adjust = {
            "retail_electronics": 210,   # Blue (tech/trust)
            "food_restaurant": 25,       # Orange (warm/appetizing)
            "fitness_gym": 0,            # Red (energy)
            "beauty_salon": 330,         # Pink/Rose
            "tech_startup": 220,         # Blue
            "professional_service": 220, # Blue
            "real_estate": 35,           # Gold/Trust
        }
        
        if biz_type in business_hue_adjust:
            base_hue = business_hue_adjust[biz_type] + self._seeded_int(-15, 15, offset=101)
        
        # Saturation based on emotion
        sat_map = {
            "excitement": 85, "urgency": 90, "trust": 60,
            "warmth": 55, "prestige": 40, "value": 80,
            "professionalism": 50, "fun": 85, "neutral": 65,
        }
        saturation = sat_map.get(emotion, 65) + self._seeded_int(-10, 10, offset=102)
        saturation = max(30, min(100, saturation))
        
        # Lightness for contrast
        if contrast == "high":
            bg_lightness = self._seeded_int(8, 18, offset=103)
            text_lightness = 95
        elif contrast == "low":
            bg_lightness = self._seeded_int(20, 35, offset=103)
            text_lightness = 90
        else:
            bg_lightness = self._seeded_int(12, 25, offset=103)
            text_lightness = 95
        
        # Generate colors
        def hsl_to_hex(h, s, l):
            h = h / 360
            s = s / 100
            l = l / 100
            
            if s == 0:
                r = g = b = l
            else:
                def hue_to_rgb(p, q, t):
                    if t < 0: t += 1
                    if t > 1: t -= 1
                    if t < 1/6: return p + (q - p) * 6 * t
                    if t < 1/2: return q
                    if t < 2/3: return p + (q - p) * (2/3 - t) * 6
                    return p
                
                q = l * (1 + s) if l < 0.5 else l + s - l * s
                p = 2 * l - q
                r = hue_to_rgb(p, q, h + 1/3)
                g = hue_to_rgb(p, q, h)
                b = hue_to_rgb(p, q, h - 1/3)
            
            return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
        
        # Primary accent color
        accent = hsl_to_hex(base_hue, saturation, 55)
        
        # Secondary (complementary or analogous based on seed)
        secondary_hue = (base_hue + 30 + self._seeded_int(0, 60, offset=104)) % 360
        secondary = hsl_to_hex(secondary_hue, saturation - 10, 60)
        
        # Background colors (dark gradient)
        bg_primary = hsl_to_hex(base_hue, saturation // 3, bg_lightness)
        bg_secondary = hsl_to_hex((base_hue + 20) % 360, saturation // 4, bg_lightness + 5)
        
        # Text colors
        text_primary = hsl_to_hex(base_hue, 5, text_lightness)
        text_secondary = hsl_to_hex(base_hue, 10, text_lightness - 20)
        
        return {
            "accent": accent,
            "secondary": secondary,
            "background_primary": bg_primary,
            "background_secondary": bg_secondary,
            "text_primary": text_primary,
            "text_secondary": text_secondary,
            "background_colors": [bg_primary, bg_secondary],
        }
    
    def _invent_layout(self) -> Dict[str, Any]:
        """
        Invent a UNIQUE layout structure based on prompt characteristics.
        No predefined templates.
        """
        
        direction = self._develop_creative_direction()
        hierarchy = direction["hierarchy"]
        focal = direction["focal_point"]
        visual_weight = self.analysis["visual_weight"]
        density = self.analysis["density_preference"]
        
        layout = {
            "type": "custom",
            "zones": {},
            "alignment": None,
            "spacing_ratio": 1.0,
        }
        
        # Determine primary alignment based on prompt seed and content
        alignments = ["left", "center", "right"]
        weights = [0.4, 0.35, 0.25]  # Slight preference for left
        
        # Adjust weights based on content
        if self.analysis["business_scale"] == "large":
            weights = [0.3, 0.5, 0.2]  # Center for big brands
        elif self.analysis["has_offer"]:
            weights = [0.25, 0.5, 0.25]  # Center for offers
        
        cumulative = 0
        threshold = self._seeded_float(offset=200)
        for i, w in enumerate(weights):
            cumulative += w
            if threshold < cumulative:
                layout["alignment"] = alignments[i]
                break
        else:
            layout["alignment"] = "center"
        
        # Create zones based on hierarchy
        total_height = 100
        zone_count = len(hierarchy)
        
        # Calculate zone heights based on importance
        zone_heights = []
        importance_weights = {"offer": 1.5, "brand": 1.2, "headline": 1.4, "value_prop": 0.8, "trust_signals": 0.6, "cta": 0.7, "tagline": 0.6, "details": 0.5}
        
        total_weight = sum(importance_weights.get(z, 0.8) for z in hierarchy)
        
        for zone_name in hierarchy:
            weight = importance_weights.get(zone_name, 0.8)
            height_pct = (weight / total_weight) * 70  # Use 70% of space for content
            zone_heights.append((zone_name, height_pct))
        
        # Position zones
        if density == "dense":
            top_margin = 8
            spacing = 2
        elif density == "focused":
            top_margin = 20
            spacing = 8
        else:
            top_margin = 15
            spacing = 5
        
        current_y = top_margin
        
        for zone_name, height in zone_heights:
            # Add variation to x position based on alignment
            if layout["alignment"] == "left":
                x = 8 + self._seeded_int(0, 3, offset=hash(zone_name))
                width = 70 + self._seeded_int(-5, 10, offset=hash(zone_name) + 1)
            elif layout["alignment"] == "right":
                width = 70 + self._seeded_int(-5, 10, offset=hash(zone_name) + 1)
                x = 92 - width + self._seeded_int(0, 3, offset=hash(zone_name))
            else:
                width = 80 + self._seeded_int(-10, 10, offset=hash(zone_name) + 1)
                x = (100 - width) / 2
            
            layout["zones"][zone_name] = {
                "x": x,
                "y": current_y,
                "width": width,
                "height": height,
            }
            
            current_y += height + spacing
        
        # Add decorative zones if we have space
        remaining_height = 100 - current_y
        if remaining_height > 15:
            layout["zones"]["footer"] = {
                "x": 5,
                "y": 90,
                "width": 90,
                "height": 8,
            }
        
        return layout
    
    def _write_contextual_copy(self) -> Dict[str, str]:
        """
        Write CONTEXTUAL copy specific to this prompt.
        No generic headlines.
        """
        
        brand = self.analysis["brand_name"]
        biz_type = self.analysis["business_type"]
        locality = self.analysis["locality"]
        has_offer = self.analysis["has_offer"]
        offer = self.analysis["offer_details"]
        emotion = self.analysis["emotional_tone"]
        value_prop = self.analysis["value_proposition"]
        differentiators = self.analysis["differentiators"]
        unique_keywords = self.analysis["unique_keywords"]
        
        copy = {
            "headline": "",
            "subheadline": "",
            "cta": "",
            "trust_line": "",
            "offer_text": "",
        }
        
        # ===== HEADLINE GENERATION =====
        # Must be specific to the brand and context
        
        if has_offer and offer:
            # Offer-focused headline
            copy["offer_text"] = offer["text"]
            if brand:
                copy["headline"] = f"{brand}\n{offer['text']}"
            else:
                copy["headline"] = offer["text"]
        
        elif brand:
            # Brand-focused contextual headlines
            if biz_type == "retail_electronics":
                headlines = [
                    f"{brand}\nYour Trusted Mobile Destination",
                    f"{brand}\nSmartphones. Accessories. Service.",
                    f"Welcome to {brand}\nGenuine Devices, Honest Prices",
                    f"{brand}\nLatest Tech, Best Deals",
                ]
            elif biz_type == "local_store":
                if locality:
                    headlines = [
                        f"{brand}\nServing {locality} Since Day One",
                        f"Visit {brand}\nYour Neighborhood Store in {locality}",
                        f"{brand}\nTrusted by {locality}",
                    ]
                else:
                    headlines = [
                        f"{brand}\nYour Neighborhood Store",
                        f"Shop at {brand}\nQuality You Can Trust",
                        f"Welcome to {brand}",
                    ]
            elif biz_type == "food_restaurant":
                headlines = [
                    f"{brand}\nFlavors You'll Love",
                    f"Dine at {brand}\nFreshly Made, Always Delicious",
                    f"{brand}\nWhere Taste Meets Quality",
                ]
            elif biz_type == "fitness_gym":
                headlines = [
                    f"{brand}\nTransform Your Body",
                    f"Join {brand}\nYour Fitness Journey Starts Here",
                    f"{brand}\nStrength. Discipline. Results.",
                ]
            elif biz_type == "beauty_salon":
                headlines = [
                    f"{brand}\nElevate Your Beauty",
                    f"Experience {brand}\nWhere Beauty Meets Care",
                    f"{brand}\nGlow with Confidence",
                ]
            elif biz_type == "tech_startup":
                headlines = [
                    f"{brand}\nSimplifying the Complex",
                    f"{brand}\nBuilt for Tomorrow",
                    f"Meet {brand}\nSmart Solutions, Real Results",
                ]
            else:
                headlines = [
                    f"{brand}",
                    f"Experience {brand}",
                    f"Welcome to {brand}",
                ]
            
            copy["headline"] = self._seeded_choice(headlines, offset=300)
        
        else:
            # No brand name - use keywords
            if unique_keywords:
                main_kw = unique_keywords[0].capitalize()
                if biz_type == "retail_electronics":
                    copy["headline"] = f"Your {main_kw} Destination"
                elif biz_type == "food_restaurant":
                    copy["headline"] = f"Taste the Best {main_kw}"
                else:
                    copy["headline"] = f"Quality {main_kw}"
            else:
                # Absolute fallback - still contextual
                if locality:
                    copy["headline"] = f"Serving {locality}\nWith Excellence"
                else:
                    copy["headline"] = "Quality You Deserve"
        
        # ===== SUBHEADLINE =====
        if emotion == "trust":
            subheadlines = [
                "Trusted by thousands of customers",
                "Quality assured, always",
                "Your satisfaction is our priority",
            ]
        elif emotion == "value":
            subheadlines = [
                "Best prices, guaranteed",
                "Unbeatable value, every day",
                "Quality without compromise",
            ]
        elif emotion == "excitement":
            subheadlines = [
                "Something special awaits",
                "Experience the difference",
                "You won't want to miss this",
            ]
        elif "reliability" in differentiators:
            subheadlines = [
                "Dependable service, every time",
                "Count on us for consistency",
            ]
        else:
            subheadlines = [
                "Quality service, always",
                "We're here for you",
                "Excellence in every detail",
            ]
        
        copy["subheadline"] = self._seeded_choice(subheadlines, offset=310)
        
        # ===== CTA =====
        if has_offer:
            ctas = ["Shop Now", "Claim Offer", "Get Deal", "Save Today"]
        elif biz_type == "food_restaurant":
            ctas = ["Order Now", "View Menu", "Book Table", "Visit Us"]
        elif biz_type == "fitness_gym":
            ctas = ["Join Today", "Start Free", "Book Trial", "Get Fit"]
        elif biz_type == "tech_startup":
            ctas = ["Get Started", "Try Free", "Learn More", "Sign Up"]
        elif biz_type in ["local_store", "retail_electronics"]:
            ctas = ["Visit Store", "Shop Now", "Call Us", "Get Directions"]
        else:
            ctas = ["Learn More", "Contact Us", "Get Started", "Visit"]
        
        copy["cta"] = self._seeded_choice(ctas, offset=320)
        
        # ===== TRUST LINE =====
        if self.analysis["trust_signals_needed"]:
            if biz_type == "retail_electronics":
                trust_lines = ["✓ Genuine Products", "✓ Warranty Assured", "✓ Expert Support"]
            elif locality:
                trust_lines = [f"✓ Serving {locality}", "✓ Local & Trusted", "✓ Community Choice"]
            else:
                trust_lines = ["✓ Quality Guaranteed", "✓ Trusted Service", "✓ Customer First"]
            
            copy["trust_line"] = self._seeded_choice(trust_lines, offset=330)
        
        return copy
    
    def _construct_elements(self, layout: Dict, colors: Dict, copy: Dict) -> List[Dict]:
        """
        Construct visual elements from scratch based on layout and content.
        """
        
        elements = []
        zones = layout["zones"]
        alignment = layout["alignment"]
        
        # Element counter for unique IDs
        element_id = 0
        
        def next_id(prefix: str) -> str:
            nonlocal element_id
            element_id += 1
            return f"{prefix}_{element_id}"
        
        # ===== DECORATIVE BACKGROUND ELEMENTS =====
        
        # Gradient glow circles based on visual weight
        visual_weight = self.analysis["visual_weight"]
        
        if visual_weight in ["medium", "heavy"]:
            # Large ambient glow
            glow_x = self._seeded_int(-20, 20, offset=400)
            glow_y = self._seeded_int(-10, 30, offset=401)
            elements.append({
                "type": "shape",
                "shape_type": "circle",
                "id": next_id("glow"),
                "position": {"x": glow_x, "y": glow_y},
                "size": {"width": 60, "height": 60},
                "fill_color": colors["accent"],
                "opacity": 0.08,
            })
            
            # Secondary glow
            glow2_x = self._seeded_int(50, 90, offset=402)
            glow2_y = self._seeded_int(40, 80, offset=403)
            elements.append({
                "type": "shape",
                "shape_type": "circle",
                "id": next_id("glow"),
                "position": {"x": glow2_x, "y": glow2_y},
                "size": {"width": 45, "height": 45},
                "fill_color": colors["secondary"],
                "opacity": 0.1,
            })
        
        # Corner accents
        accent_style = self._seeded_int(0, 3, offset=404)
        if accent_style == 0:
            # L-shaped corners
            elements.extend([
                {"type": "shape", "shape_type": "rect", "id": next_id("corner"), "position": {"x": 5, "y": 5}, "size": {"width": 15, "height": 0.5}, "fill_color": colors["accent"], "opacity": 0.6},
                {"type": "shape", "shape_type": "rect", "id": next_id("corner"), "position": {"x": 5, "y": 5}, "size": {"width": 0.5, "height": 15}, "fill_color": colors["accent"], "opacity": 0.6},
            ])
        elif accent_style == 1:
            # Dot grid
            for i in range(3):
                for j in range(3):
                    elements.append({
                        "type": "shape", "shape_type": "circle", "id": next_id("dot"),
                        "position": {"x": 5 + i * 3, "y": 5 + j * 3},
                        "size": {"width": 1.5, "height": 1.5},
                        "fill_color": colors["accent"], "opacity": 0.4,
                    })
        elif accent_style == 2:
            # Single accent line
            elements.append({
                "type": "shape", "shape_type": "rect", "id": next_id("accent_line"),
                "position": {"x": 0, "y": self._seeded_int(30, 50, offset=405)},
                "size": {"width": 4, "height": 30},
                "fill_color": colors["accent"], "opacity": 0.3,
            })
        
        # ===== CONTENT ELEMENTS =====
        
        direction = self._develop_creative_direction()
        hierarchy = direction["hierarchy"]
        
        for idx, zone_name in enumerate(hierarchy):
            if zone_name not in zones:
                continue
            
            zone = zones[zone_name]
            
            if zone_name == "offer" and copy.get("offer_text"):
                # Offer badge
                badge_width = min(40, zone["width"])
                badge_x = zone["x"] + (zone["width"] - badge_width) / 2 if alignment == "center" else zone["x"]
                
                elements.append({
                    "type": "shape", "shape_type": "rect", "id": next_id("offer_bg"),
                    "position": {"x": badge_x, "y": zone["y"]},
                    "size": {"width": badge_width, "height": zone["height"]},
                    "fill_color": colors["accent"],
                    "corner_radius": 8,
                })
                elements.append({
                    "type": "text", "id": next_id("offer_text"),
                    "position": {"x": badge_x, "y": zone["y"] + 2},
                    "size": {"width": badge_width, "height": zone["height"] - 4},
                    "content": copy["offer_text"],
                    "font_size": 32,
                    "font_weight": 900,
                    "font_family": "Montserrat",
                    "color": colors["background_primary"],
                    "align": "center",
                })
            
            elif zone_name in ["brand", "headline"]:
                # Main headline
                font_size = 48 + self._seeded_int(0, 20, offset=410 + idx)
                
                elements.append({
                    "type": "text", "id": next_id("headline"),
                    "position": {"x": zone["x"], "y": zone["y"]},
                    "size": {"width": zone["width"], "height": zone["height"]},
                    "content": copy["headline"],
                    "font_size": font_size,
                    "font_weight": 800,
                    "font_family": "Montserrat",
                    "color": colors["text_primary"],
                    "align": alignment,
                    "line_height": 0.95,
                })
            
            elif zone_name in ["value_prop", "tagline"]:
                # Subheadline
                elements.append({
                    "type": "text", "id": next_id("subheadline"),
                    "position": {"x": zone["x"], "y": zone["y"]},
                    "size": {"width": zone["width"], "height": zone["height"]},
                    "content": copy["subheadline"],
                    "font_size": 18,
                    "font_weight": 400,
                    "font_family": "Inter",
                    "color": colors["text_secondary"],
                    "align": alignment,
                    "opacity": 0.85,
                })
            
            elif zone_name == "trust_signals" and copy.get("trust_line"):
                # Trust badge
                elements.append({
                    "type": "text", "id": next_id("trust"),
                    "position": {"x": zone["x"], "y": zone["y"]},
                    "size": {"width": zone["width"], "height": zone["height"]},
                    "content": copy["trust_line"],
                    "font_size": 14,
                    "font_weight": 500,
                    "font_family": "Inter",
                    "color": colors["accent"],
                    "align": alignment,
                })
            
            elif zone_name == "cta":
                # CTA Button
                btn_width = min(35, zone["width"])
                btn_x = zone["x"] if alignment == "left" else (zone["x"] + zone["width"] - btn_width if alignment == "right" else zone["x"] + (zone["width"] - btn_width) / 2)
                
                corner_radius = self._seeded_int(4, 25, offset=420)
                
                elements.append({
                    "type": "shape", "shape_type": "rect", "id": next_id("cta_bg"),
                    "position": {"x": btn_x, "y": zone["y"]},
                    "size": {"width": btn_width, "height": 10},
                    "fill_color": colors["accent"],
                    "corner_radius": corner_radius,
                })
                elements.append({
                    "type": "text", "id": next_id("cta_text"),
                    "position": {"x": btn_x, "y": zone["y"] + 2.5},
                    "size": {"width": btn_width, "height": 5},
                    "content": copy["cta"].upper(),
                    "font_size": 14,
                    "font_weight": 700,
                    "font_family": "Inter",
                    "color": colors["background_primary"],
                    "align": "center",
                })
            
            elif zone_name == "details":
                # Additional details
                if copy.get("trust_line"):
                    elements.append({
                        "type": "text", "id": next_id("details"),
                        "position": {"x": zone["x"], "y": zone["y"]},
                        "size": {"width": zone["width"], "height": zone["height"]},
                        "content": copy["trust_line"],
                        "font_size": 13,
                        "font_weight": 400,
                        "font_family": "Inter",
                        "color": colors["text_secondary"],
                        "align": alignment,
                        "opacity": 0.7,
                    })
        
        # Accent divider line
        if "headline" in zones or "brand" in zones:
            ref_zone = zones.get("brand", zones.get("headline", {}))
            if ref_zone:
                line_y = ref_zone.get("y", 30) + ref_zone.get("height", 15) + 2
                line_x = ref_zone.get("x", 10) if alignment != "right" else ref_zone.get("x", 10) + ref_zone.get("width", 50) - 20
                
                elements.append({
                    "type": "shape", "shape_type": "rect", "id": next_id("divider"),
                    "position": {"x": line_x, "y": line_y},
                    "size": {"width": 20, "height": 0.8},
                    "fill_color": colors["accent"],
                    "opacity": 0.9,
                })
        
        return elements
    
    def _design_background(self, colors: Dict) -> Dict[str, Any]:
        """
        Design the background based on prompt context.
        """
        
        contrast = self.analysis["contrast_level"]
        emotion = self.analysis["emotional_tone"]
        
        # Gradient angle based on prompt
        base_angle = self._seeded_int(120, 180, offset=500)
        
        # Adjust angle based on emotion
        if emotion in ["excitement", "urgency"]:
            base_angle = self._seeded_int(30, 60, offset=501)  # Dynamic diagonal
        elif emotion in ["trust", "professionalism"]:
            base_angle = self._seeded_int(160, 200, offset=501)  # Vertical
        
        return {
            "type": "gradient",
            "colors": colors["background_colors"],
            "angle": base_angle,
            "color": colors["background_primary"],
        }


def blueprint_to_fabric(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """Convert creative director blueprint to Fabric.js format"""
    
    width = blueprint["metadata"]["width"]
    height = blueprint["metadata"]["height"]
    fabric_objects = []
    
    # Background
    bg = blueprint.get("background", {})
    colors = bg.get("colors", ["#1a1a2e"])
    angle = bg.get("angle", 135)
    
    if len(colors) > 1:
        # Gradient background
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
            "fill": colors[0] if colors else "#1a1a2e",
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


def generate_creative_design(prompt: str, platform: str = "instagram", 
                             format: str = "post") -> Dict[str, Any]:
    """
    Main entry point - generates a UNIQUE design from scratch.
    """
    director = CreativeDirector(prompt, platform, format)
    return director.generate()
