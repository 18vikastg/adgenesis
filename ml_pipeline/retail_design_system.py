"""
Professional Retail Media Design System for AdGenesis
Agency-Grade Creative Templates for D2C, FMCG, and E-commerce

This module provides:
- Premium retail-ready color palettes
- Platform-specific layouts (Instagram, Facebook, Amazon, Flipkart)
- AI compliance rules engine
- Multi-format auto-resizing logic
- Professional typography systems
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json


# =============================================================================
# DESIGN STYLE PRESETS
# =============================================================================

class DesignTone(Enum):
    BOLD_FMCG = "bold_fmcg"
    PREMIUM_MODERN = "premium_modern"
    LUXURY_DARK = "luxury_dark"
    CLEAN_RETAIL = "clean_retail"
    VIBRANT_PLAYFUL = "vibrant_playful"
    TECH_MODERN = "tech_modern"
    TRUST_CORPORATE = "trust_corporate"


class Platform(Enum):
    INSTAGRAM_FEED = "instagram_feed"
    INSTAGRAM_STORY = "instagram_story"
    FACEBOOK_FEED = "facebook_feed"
    FACEBOOK_STORY = "facebook_story"
    AMAZON_MAIN = "amazon_main"
    AMAZON_LIFESTYLE = "amazon_lifestyle"
    FLIPKART_BANNER = "flipkart_banner"
    GOOGLE_DISPLAY = "google_display"


# =============================================================================
# PLATFORM SPECIFICATIONS
# =============================================================================

PLATFORM_SPECS = {
    Platform.INSTAGRAM_FEED: {
        "name": "Instagram Feed",
        "dimensions": [(1080, 1080), (1080, 1350)],
        "aspect_ratios": ["1:1", "4:5"],
        "max_file_size_kb": 500,
        "text_coverage_limit": 0.20,
        "safe_zone_percent": 5,
        "supported_formats": ["jpg", "png"],
    },
    Platform.INSTAGRAM_STORY: {
        "name": "Instagram Story",
        "dimensions": [(1080, 1920)],
        "aspect_ratios": ["9:16"],
        "max_file_size_kb": 500,
        "text_coverage_limit": 0.20,
        "safe_zone_percent": 10,
        "supported_formats": ["jpg", "png"],
    },
    Platform.FACEBOOK_FEED: {
        "name": "Facebook Feed",
        "dimensions": [(1200, 630), (1080, 1080)],
        "aspect_ratios": ["16:9", "1:1"],
        "max_file_size_kb": 500,
        "text_coverage_limit": 0.20,
        "safe_zone_percent": 5,
        "supported_formats": ["jpg", "png"],
    },
    Platform.AMAZON_MAIN: {
        "name": "Amazon Main Image",
        "dimensions": [(1000, 1000), (1500, 1500)],
        "aspect_ratios": ["1:1"],
        "max_file_size_kb": 500,
        "requires_white_bg": True,
        "no_promotional_text": True,
        "min_image_dimension": 1000,
        "supported_formats": ["jpg", "png"],
    },
    Platform.AMAZON_LIFESTYLE: {
        "name": "Amazon Lifestyle",
        "dimensions": [(1500, 1500)],
        "aspect_ratios": ["1:1"],
        "max_file_size_kb": 500,
        "allows_text_overlay": True,
        "supported_formats": ["jpg", "png"],
    },
    Platform.FLIPKART_BANNER: {
        "name": "Flipkart Banner",
        "dimensions": [(1080, 1080), (1200, 628)],
        "aspect_ratios": ["1:1", "16:9"],
        "max_file_size_kb": 500,
        "no_watermarks": True,
        "supported_formats": ["jpg", "png"],
    },
    Platform.GOOGLE_DISPLAY: {
        "name": "Google Display Ads",
        "dimensions": [(300, 250), (728, 90), (160, 600), (300, 600)],
        "aspect_ratios": ["various"],
        "max_file_size_kb": 150,
        "supported_formats": ["jpg", "png", "gif"],
    },
}


# =============================================================================
# PROFESSIONAL COLOR PALETTES - RETAIL FOCUSED
# =============================================================================

RETAIL_COLOR_PALETTES = {
    # FMCG Bold - High-energy, conversion-focused
    "fmcg_bold_energy": {
        "name": "Bold FMCG Energy",
        "description": "High-contrast, energetic palette for snacks, beverages, FMCG",
        "background": {
            "type": "gradient",
            "colors": ["#1E1E2F", "#0D0D15"],
            "angle": 180,
            "css": "linear-gradient(180deg, #1E1E2F 0%, #0D0D15 100%)"
        },
        "primary": "#1E1E2F",
        "accent": "#F5B700",
        "secondary": "#FFFFFF",
        "text_primary": "#FFFFFF",
        "text_secondary": "rgba(255,255,255,0.8)",
        "cta_bg": "#F5B700",
        "cta_text": "#1E1E2F",
        "badge_bg": "#F5B700",
        "badge_text": "#1E1E2F",
        "trust_icon": "#2ECC71",
        "shadows": {
            "product": "0 25px 50px rgba(0,0,0,0.5)",
            "ambient": "0 5px 15px rgba(0,0,0,0.3)",
            "glow": "0 0 60px rgba(245,183,0,0.15)"
        },
        "effects": {
            "energy_burst": "radial-gradient(ellipse at 50% 30%, rgba(45,45,70,1) 0%, transparent 60%)",
            "texture_opacity": 0.03
        }
    },
    
    # Clean Retail - Amazon/Flipkart compliant
    "clean_retail": {
        "name": "Clean Retail",
        "description": "Professional, retail-compliant palette",
        "background": {
            "type": "solid",
            "colors": ["#FFFFFF"],
            "css": "#FFFFFF"
        },
        "primary": "#FFFFFF",
        "accent": "#FF9900",  # Amazon orange
        "secondary": "#232F3E",  # Amazon dark
        "text_primary": "#0F1111",
        "text_secondary": "#565959",
        "cta_bg": "#FFD814",
        "cta_text": "#0F1111",
        "badge_bg": "#CC0C39",
        "badge_text": "#FFFFFF",
        "trust_icon": "#067D62",
        "shadows": {
            "product": "0 4px 12px rgba(0,0,0,0.08)",
            "ambient": "0 2px 4px rgba(0,0,0,0.04)"
        }
    },
    
    # Premium Dark Luxury
    "luxury_dark": {
        "name": "Dark Luxury",
        "description": "Premium, aspirational dark palette",
        "background": {
            "type": "gradient",
            "colors": ["#0A0A0A", "#1A1A1A", "#0D0D0D"],
            "angle": 180,
            "css": "linear-gradient(180deg, #0A0A0A 0%, #1A1A1A 50%, #0D0D0D 100%)"
        },
        "primary": "#0A0A0A",
        "accent": "#D4AF37",
        "secondary": "#FFFFFF",
        "text_primary": "#FFFFFF",
        "text_secondary": "rgba(255,255,255,0.7)",
        "cta_bg": "#D4AF37",
        "cta_text": "#0A0A0A",
        "badge_bg": "#D4AF37",
        "badge_text": "#0A0A0A",
        "trust_icon": "#D4AF37",
        "shadows": {
            "product": "0 30px 60px rgba(0,0,0,0.6)",
            "rim_light": "0 0 40px rgba(212,175,55,0.2)"
        },
        "effects": {
            "grain_opacity": 0.02
        }
    },
    
    # Vibrant Health & Wellness
    "health_vibrant": {
        "name": "Health Vibrant",
        "description": "Fresh, energetic palette for health/fitness products",
        "background": {
            "type": "gradient",
            "colors": ["#11998E", "#38EF7D"],
            "angle": 135,
            "css": "linear-gradient(135deg, #11998E 0%, #38EF7D 100%)"
        },
        "primary": "#11998E",
        "accent": "#FFD93D",
        "secondary": "#FFFFFF",
        "text_primary": "#FFFFFF",
        "text_secondary": "rgba(255,255,255,0.9)",
        "cta_bg": "#FFD93D",
        "cta_text": "#1A1A2E",
        "badge_bg": "#FF6B6B",
        "badge_text": "#FFFFFF",
        "trust_icon": "#FFFFFF",
        "shadows": {
            "product": "0 20px 40px rgba(0,0,0,0.3)"
        }
    },
    
    # Tech Modern
    "tech_modern": {
        "name": "Tech Modern",
        "description": "Modern tech product palette",
        "background": {
            "type": "gradient",
            "colors": ["#667EEA", "#764BA2"],
            "angle": 135,
            "css": "linear-gradient(135deg, #667EEA 0%, #764BA2 100%)"
        },
        "primary": "#667EEA",
        "accent": "#F59E0B",
        "secondary": "#FFFFFF",
        "text_primary": "#FFFFFF",
        "text_secondary": "rgba(255,255,255,0.85)",
        "cta_bg": "#FFFFFF",
        "cta_text": "#667EEA",
        "badge_bg": "#F59E0B",
        "badge_text": "#1A1A2E",
        "trust_icon": "#22D3EE",
        "shadows": {
            "product": "0 25px 50px rgba(102,126,234,0.4)"
        }
    },
    
    # FMCG Red Sale
    "fmcg_sale_red": {
        "name": "Sale Urgent Red",
        "description": "High-urgency sale/offer palette",
        "background": {
            "type": "gradient",
            "colors": ["#DC2626", "#EF4444"],
            "angle": 135,
            "css": "linear-gradient(135deg, #DC2626 0%, #EF4444 100%)"
        },
        "primary": "#DC2626",
        "accent": "#FBBF24",
        "secondary": "#FFFFFF",
        "text_primary": "#FFFFFF",
        "text_secondary": "rgba(255,255,255,0.95)",
        "cta_bg": "#FBBF24",
        "cta_text": "#1A1A2E",
        "badge_bg": "#FBBF24",
        "badge_text": "#DC2626",
        "trust_icon": "#FFFFFF",
        "shadows": {
            "product": "0 20px 40px rgba(0,0,0,0.3)"
        }
    }
}


# =============================================================================
# TYPOGRAPHY SYSTEM
# =============================================================================

TYPOGRAPHY_PRESETS = {
    "bold_fmcg": {
        "heading": {
            "font_family": "Montserrat",
            "font_weight": 800,
            "letter_spacing": "-0.02em",
            "line_height": 1.1,
            "text_transform": "uppercase"
        },
        "subheading": {
            "font_family": "Montserrat",
            "font_weight": 700,
            "letter_spacing": "-0.01em",
            "line_height": 1.2
        },
        "body": {
            "font_family": "Inter",
            "font_weight": 500,
            "letter_spacing": "0.02em",
            "line_height": 1.5
        },
        "cta": {
            "font_family": "Montserrat",
            "font_weight": 700,
            "letter_spacing": "0.05em",
            "text_transform": "uppercase"
        },
        "badge": {
            "font_family": "Montserrat",
            "font_weight": 800,
            "letter_spacing": "0em"
        }
    },
    "premium_modern": {
        "heading": {
            "font_family": "Playfair Display",
            "font_weight": 700,
            "letter_spacing": "-0.01em",
            "line_height": 1.15
        },
        "subheading": {
            "font_family": "Inter",
            "font_weight": 400,
            "letter_spacing": "0.02em",
            "line_height": 1.4
        },
        "body": {
            "font_family": "Inter",
            "font_weight": 400,
            "letter_spacing": "0.01em",
            "line_height": 1.6
        },
        "cta": {
            "font_family": "Inter",
            "font_weight": 600,
            "letter_spacing": "0.1em",
            "text_transform": "uppercase"
        }
    },
    "clean_retail": {
        "heading": {
            "font_family": "Amazon Ember",
            "fallback": "Arial, sans-serif",
            "font_weight": 700,
            "letter_spacing": "0em",
            "line_height": 1.2
        },
        "subheading": {
            "font_family": "Amazon Ember",
            "fallback": "Arial, sans-serif",
            "font_weight": 400,
            "line_height": 1.4
        },
        "body": {
            "font_family": "Amazon Ember",
            "fallback": "Arial, sans-serif",
            "font_weight": 400,
            "line_height": 1.5
        },
        "cta": {
            "font_family": "Amazon Ember",
            "fallback": "Arial, sans-serif",
            "font_weight": 700
        }
    }
}


# =============================================================================
# LAYOUT TEMPLATES - RETAIL FOCUSED
# =============================================================================

@dataclass
class LayoutZone:
    """Defines a zone in the layout (percentages)"""
    x: float  # percentage from left
    y: float  # percentage from top
    width: float  # percentage width
    height: float  # percentage height
    align: str = "center"
    anchor: str = "top-left"


RETAIL_LAYOUTS = {
    # Instagram Feed 1:1 - Bold FMCG
    "instagram_feed_bold": {
        "name": "Bold FMCG Feed",
        "aspect_ratio": "1:1",
        "platform": Platform.INSTAGRAM_FEED,
        "zones": {
            "badge": LayoutZone(x=2, y=2, width=25, height=8, align="left"),
            "headline_primary": LayoutZone(x=5, y=15, width=90, height=15, align="center"),
            "headline_secondary": LayoutZone(x=5, y=32, width=90, height=8, align="center"),
            "product_area": LayoutZone(x=10, y=42, width=80, height=35, align="center"),
            "trust_signals": LayoutZone(x=5, y=78, width=90, height=6, align="center"),
            "cta": LayoutZone(x=25, y=86, width=50, height=8, align="center"),
            "logo": LayoutZone(x=80, y=92, width=18, height=6, align="right"),
        },
        "decorations": [
            {"type": "glow", "position": "center", "color": "accent", "opacity": 0.15, "size": 60},
            {"type": "texture", "opacity": 0.03}
        ]
    },
    
    # Instagram Story 9:16 - Vertical Bold
    "instagram_story_bold": {
        "name": "Bold FMCG Story",
        "aspect_ratio": "9:16",
        "platform": Platform.INSTAGRAM_STORY,
        "safe_zones": {
            "top": 10,
            "bottom": 15
        },
        "zones": {
            "badge": LayoutZone(x=5, y=12, width=30, height=5, align="left"),
            "headline_primary": LayoutZone(x=5, y=18, width=90, height=10, align="center"),
            "headline_secondary": LayoutZone(x=5, y=30, width=90, height=5, align="center"),
            "product_area": LayoutZone(x=5, y=38, width=90, height=35, align="center"),
            "trust_signals": LayoutZone(x=5, y=75, width=90, height=5, align="center"),
            "cta": LayoutZone(x=15, y=82, width=70, height=6, align="center"),
            "logo": LayoutZone(x=35, y=90, width=30, height=5, align="center"),
        }
    },
    
    # Amazon Main - Clean Product Focus
    "amazon_main_clean": {
        "name": "Amazon Clean",
        "aspect_ratio": "1:1",
        "platform": Platform.AMAZON_MAIN,
        "zones": {
            "product_area": LayoutZone(x=10, y=10, width=80, height=80, align="center"),
        },
        "requirements": {
            "background": "white",
            "no_text": True,
            "product_fill": 0.85
        }
    },
    
    # Amazon Lifestyle - With Text
    "amazon_lifestyle": {
        "name": "Amazon Lifestyle",
        "aspect_ratio": "1:1",
        "platform": Platform.AMAZON_LIFESTYLE,
        "zones": {
            "headline": LayoutZone(x=5, y=5, width=60, height=15, align="left"),
            "product_area": LayoutZone(x=40, y=20, width=55, height=60, align="center"),
            "benefits": LayoutZone(x=5, y=25, width=40, height=50, align="left"),
            "cta": LayoutZone(x=5, y=80, width=40, height=8, align="left"),
            "logo": LayoutZone(x=5, y=90, width=20, height=6, align="left"),
        }
    },
    
    # Facebook Feed 16:9 - Horizontal Split
    "facebook_feed_split": {
        "name": "Facebook Split",
        "aspect_ratio": "16:9",
        "platform": Platform.FACEBOOK_FEED,
        "zones": {
            "badge": LayoutZone(x=2, y=5, width=15, height=10, align="left"),
            "headline_primary": LayoutZone(x=5, y=25, width=45, height=20, align="left"),
            "headline_secondary": LayoutZone(x=5, y=48, width=40, height=10, align="left"),
            "trust_signals": LayoutZone(x=5, y=62, width=40, height=8, align="left"),
            "cta": LayoutZone(x=5, y=75, width=25, height=12, align="left"),
            "product_area": LayoutZone(x=50, y=5, width=48, height=90, align="center"),
            "logo": LayoutZone(x=5, y=88, width=15, height=8, align="left"),
        }
    }
}


# =============================================================================
# AI COMPLIANCE ENGINE
# =============================================================================

@dataclass
class ComplianceRule:
    """Defines a compliance check rule"""
    rule_id: str
    name: str
    description: str
    severity: str  # "error", "warning", "info"
    platforms: List[Platform]
    check_function: str
    auto_fix_available: bool = False
    auto_fix_function: Optional[str] = None


COMPLIANCE_RULES = [
    # Brand Rules
    ComplianceRule(
        rule_id="BR-001",
        name="Brand Color Consistency",
        description="All colors must match brand palette",
        severity="error",
        platforms=[p for p in Platform],
        check_function="check_brand_colors",
        auto_fix_available=True,
        auto_fix_function="fix_brand_colors"
    ),
    ComplianceRule(
        rule_id="BR-002",
        name="Logo Minimum Size",
        description="Logo must be at least 60px in height",
        severity="error",
        platforms=[p for p in Platform],
        check_function="check_logo_size"
    ),
    ComplianceRule(
        rule_id="BR-003",
        name="Logo Clear Space",
        description="Logo must have 20px padding around it",
        severity="warning",
        platforms=[p for p in Platform],
        check_function="check_logo_clearspace",
        auto_fix_available=True,
        auto_fix_function="fix_logo_clearspace"
    ),
    
    # Layout Rules
    ComplianceRule(
        rule_id="LY-001",
        name="Element Overlap",
        description="Elements should not overlap more than 10%",
        severity="warning",
        platforms=[p for p in Platform],
        check_function="check_element_overlap",
        auto_fix_available=True,
        auto_fix_function="fix_element_overlap"
    ),
    ComplianceRule(
        rule_id="LY-002",
        name="Safe Zone Compliance",
        description="Critical elements must be within safe zones",
        severity="error",
        platforms=[Platform.INSTAGRAM_STORY, Platform.FACEBOOK_STORY],
        check_function="check_safe_zones",
        auto_fix_available=True,
        auto_fix_function="fix_safe_zones"
    ),
    
    # Text Rules
    ComplianceRule(
        rule_id="TX-001",
        name="Text Coverage Limit",
        description="Text should cover less than 20% of image",
        severity="warning",
        platforms=[Platform.FACEBOOK_FEED, Platform.INSTAGRAM_FEED],
        check_function="check_text_coverage",
        auto_fix_available=True,
        auto_fix_function="fix_text_coverage"
    ),
    ComplianceRule(
        rule_id="TX-002",
        name="Minimum Font Size",
        description="Font size must be at least 14px for mobile",
        severity="error",
        platforms=[p for p in Platform],
        check_function="check_font_size"
    ),
    ComplianceRule(
        rule_id="TX-003",
        name="Text Contrast",
        description="Text must meet WCAG AA contrast ratio (4.5:1)",
        severity="error",
        platforms=[p for p in Platform],
        check_function="check_text_contrast",
        auto_fix_available=True,
        auto_fix_function="fix_text_contrast"
    ),
    
    # Image Rules
    ComplianceRule(
        rule_id="IM-001",
        name="Image Resolution",
        description="Image must be at least 1080px for social media",
        severity="error",
        platforms=[Platform.INSTAGRAM_FEED, Platform.INSTAGRAM_STORY, Platform.FACEBOOK_FEED],
        check_function="check_image_resolution"
    ),
    ComplianceRule(
        rule_id="IM-002",
        name="File Size Limit",
        description="File must be under 500KB for retail platforms",
        severity="error",
        platforms=[p for p in Platform],
        check_function="check_file_size"
    ),
    ComplianceRule(
        rule_id="IM-003",
        name="Aspect Ratio",
        description="Aspect ratio must match platform requirements",
        severity="error",
        platforms=[p for p in Platform],
        check_function="check_aspect_ratio"
    ),
    
    # Amazon Specific
    ComplianceRule(
        rule_id="AM-001",
        name="Amazon White Background",
        description="Main image must have white/clean background",
        severity="error",
        platforms=[Platform.AMAZON_MAIN],
        check_function="check_amazon_white_bg"
    ),
    ComplianceRule(
        rule_id="AM-002",
        name="Amazon No Promotional Text",
        description="Main image cannot have promotional text",
        severity="error",
        platforms=[Platform.AMAZON_MAIN],
        check_function="check_amazon_no_promo_text"
    ),
    
    # Flipkart Specific
    ComplianceRule(
        rule_id="FK-001",
        name="No Watermarks",
        description="Images cannot have watermarks",
        severity="error",
        platforms=[Platform.FLIPKART_BANNER],
        check_function="check_no_watermarks"
    ),
]


class ComplianceEngine:
    """AI-powered compliance checking engine"""
    
    def __init__(self, brand_config: Dict = None):
        self.brand_config = brand_config or {}
        self.rules = COMPLIANCE_RULES
    
    def check_design(self, design: Dict, platform: Platform) -> Dict:
        """Run all compliance checks on a design"""
        results = {
            "passed": [],
            "warnings": [],
            "errors": [],
            "auto_fixes_available": []
        }
        
        applicable_rules = [r for r in self.rules if platform in r.platforms]
        
        for rule in applicable_rules:
            check_result = self._run_check(rule, design)
            
            if check_result["passed"]:
                results["passed"].append({
                    "rule_id": rule.rule_id,
                    "name": rule.name
                })
            else:
                issue = {
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "description": rule.description,
                    "message": check_result.get("message", ""),
                    "severity": rule.severity
                }
                
                if rule.severity == "error":
                    results["errors"].append(issue)
                else:
                    results["warnings"].append(issue)
                
                if rule.auto_fix_available:
                    results["auto_fixes_available"].append({
                        "rule_id": rule.rule_id,
                        "fix_description": check_result.get("fix_suggestion", ""),
                        "fix_function": rule.auto_fix_function
                    })
        
        results["summary"] = {
            "total_checks": len(applicable_rules),
            "passed": len(results["passed"]),
            "warnings": len(results["warnings"]),
            "errors": len(results["errors"]),
            "is_compliant": len(results["errors"]) == 0
        }
        
        return results
    
    def _run_check(self, rule: ComplianceRule, design: Dict) -> Dict:
        """Run individual compliance check"""
        # Placeholder - actual checks would be implemented here
        return {"passed": True}
    
    def auto_fix_all(self, design: Dict, platform: Platform) -> Dict:
        """Apply all available auto-fixes"""
        compliance_result = self.check_design(design, platform)
        
        fixed_design = design.copy()
        fixes_applied = []
        
        for fix in compliance_result["auto_fixes_available"]:
            fix_result = self._apply_fix(fixed_design, fix["fix_function"])
            if fix_result["success"]:
                fixes_applied.append(fix["rule_id"])
        
        return {
            "design": fixed_design,
            "fixes_applied": fixes_applied,
            "remaining_issues": self.check_design(fixed_design, platform)
        }
    
    def _apply_fix(self, design: Dict, fix_function: str) -> Dict:
        """Apply individual fix"""
        # Placeholder - actual fixes would be implemented here
        return {"success": True}


# =============================================================================
# MULTI-FORMAT RESIZING ENGINE
# =============================================================================

class MultiFormatAdapter:
    """Smart resizing engine for multi-platform export"""
    
    RESIZE_RULES = {
        # Element behavior during resize
        "headline": {
            "priority": 1,
            "can_scale": True,
            "min_scale": 0.6,
            "max_scale": 1.4,
            "can_reposition": True,
            "must_be_readable": True
        },
        "product": {
            "priority": 1,
            "can_scale": True,
            "min_scale": 0.7,
            "max_scale": 1.3,
            "can_reposition": True,
            "maintain_aspect": True
        },
        "cta": {
            "priority": 2,
            "can_scale": True,
            "min_scale": 0.8,
            "max_scale": 1.2,
            "can_reposition": True,
            "must_be_visible": True
        },
        "logo": {
            "priority": 3,
            "can_scale": True,
            "min_scale": 0.7,
            "max_scale": 1.0,
            "can_reposition": True,
            "corner_anchor": True
        },
        "badge": {
            "priority": 2,
            "can_scale": True,
            "min_scale": 0.8,
            "max_scale": 1.1,
            "can_reposition": True
        },
        "trust_signals": {
            "priority": 3,
            "can_scale": True,
            "can_reflow": True,  # Can change from row to column
            "can_hide": False
        }
    }
    
    def __init__(self):
        self.layouts = RETAIL_LAYOUTS
    
    def adapt_design(
        self, 
        design: Dict, 
        source_platform: Platform,
        target_platforms: List[Platform]
    ) -> Dict[Platform, Dict]:
        """Adapt design to multiple platforms"""
        results = {}
        
        for target in target_platforms:
            if target == source_platform:
                results[target] = design
            else:
                results[target] = self._transform_design(design, source_platform, target)
        
        return results
    
    def _transform_design(
        self, 
        design: Dict, 
        source: Platform, 
        target: Platform
    ) -> Dict:
        """Transform design from source to target platform"""
        source_spec = PLATFORM_SPECS[source]
        target_spec = PLATFORM_SPECS[target]
        
        # Get appropriate layout for target
        target_layout = self._get_best_layout(target)
        
        transformed = {
            "platform": target,
            "dimensions": target_spec["dimensions"][0],
            "elements": []
        }
        
        # Transform each element
        for element in design.get("elements", []):
            transformed_element = self._transform_element(
                element, 
                source_spec, 
                target_spec,
                target_layout
            )
            if transformed_element:
                transformed["elements"].append(transformed_element)
        
        # Apply target layout zones
        transformed = self._apply_layout_zones(transformed, target_layout)
        
        return transformed
    
    def _get_best_layout(self, platform: Platform) -> Dict:
        """Get the best matching layout for platform"""
        for layout_id, layout in self.layouts.items():
            if layout.get("platform") == platform:
                return layout
        return list(self.layouts.values())[0]
    
    def _transform_element(
        self, 
        element: Dict, 
        source_spec: Dict, 
        target_spec: Dict,
        target_layout: Dict
    ) -> Optional[Dict]:
        """Transform individual element"""
        element_type = element.get("type", "unknown")
        rules = self.RESIZE_RULES.get(element_type, {})
        
        # Calculate scale factor
        source_dims = source_spec["dimensions"][0]
        target_dims = target_spec["dimensions"][0]
        
        scale_x = target_dims[0] / source_dims[0]
        scale_y = target_dims[1] / source_dims[1]
        
        # Apply scaling with limits
        min_scale = rules.get("min_scale", 0.5)
        max_scale = rules.get("max_scale", 2.0)
        
        actual_scale = min(max(min(scale_x, scale_y), min_scale), max_scale)
        
        transformed = element.copy()
        
        if rules.get("can_scale", True):
            if "width" in transformed:
                transformed["width"] = element["width"] * actual_scale
            if "height" in transformed:
                transformed["height"] = element["height"] * actual_scale
            if "fontSize" in transformed:
                transformed["fontSize"] = max(14, element["fontSize"] * actual_scale)
        
        if rules.get("can_reposition", True):
            # Reposition based on target layout zones
            zone = target_layout.get("zones", {}).get(element_type)
            if zone:
                transformed["x"] = target_dims[0] * (zone.x / 100)
                transformed["y"] = target_dims[1] * (zone.y / 100)
        
        return transformed
    
    def _apply_layout_zones(self, design: Dict, layout: Dict) -> Dict:
        """Apply layout zone positioning"""
        # Implementation would map elements to their designated zones
        return design


# =============================================================================
# DESIGN GENERATOR - MAIN ENTRY POINT
# =============================================================================

class RetailDesignGenerator:
    """Main generator for retail-focused designs"""
    
    def __init__(self):
        self.palettes = RETAIL_COLOR_PALETTES
        self.typography = TYPOGRAPHY_PRESETS
        self.layouts = RETAIL_LAYOUTS
        self.compliance = ComplianceEngine()
        self.adapter = MultiFormatAdapter()
    
    def generate_creative(
        self,
        brand_config: Dict,
        content: Dict,
        platform: Platform,
        tone: DesignTone = DesignTone.BOLD_FMCG
    ) -> Dict:
        """Generate a complete retail creative"""
        
        # Select palette based on tone
        palette = self._select_palette(tone, brand_config)
        
        # Select typography
        typography = self._select_typography(tone)
        
        # Get layout
        layout = self._select_layout(platform, tone)
        
        # Build design structure
        design = {
            "platform": platform.value,
            "tone": tone.value,
            "dimensions": PLATFORM_SPECS[platform]["dimensions"][0],
            "palette": palette,
            "typography": typography,
            "layout": layout,
            "elements": self._generate_elements(content, palette, typography, layout),
            "editable_elements": self._define_editable_elements(brand_config),
            "locked_elements": self._define_locked_elements(brand_config),
            "metadata": {
                "generator": "AdGenesis Retail Design System",
                "version": "2.0",
                "compliance_ready": True
            }
        }
        
        # Run compliance check
        design["compliance"] = self.compliance.check_design(design, platform)
        
        return design
    
    def generate_variants(
        self,
        base_design: Dict,
        variant_types: List[str] = ["high_contrast", "minimal_luxury", "bold_experimental"]
    ) -> List[Dict]:
        """Generate design variants for A/B testing"""
        variants = []
        
        for variant_type in variant_types:
            variant = self._create_variant(base_design, variant_type)
            variants.append(variant)
        
        return variants
    
    def generate_all_formats(
        self,
        base_design: Dict,
        target_platforms: List[Platform]
    ) -> Dict[str, Dict]:
        """Generate all platform formats from base design"""
        source_platform = Platform(base_design["platform"])
        return self.adapter.adapt_design(base_design, source_platform, target_platforms)
    
    def _select_palette(self, tone: DesignTone, brand_config: Dict) -> Dict:
        """Select appropriate color palette"""
        tone_to_palette = {
            DesignTone.BOLD_FMCG: "fmcg_bold_energy",
            DesignTone.PREMIUM_MODERN: "luxury_dark",
            DesignTone.LUXURY_DARK: "luxury_dark",
            DesignTone.CLEAN_RETAIL: "clean_retail",
            DesignTone.VIBRANT_PLAYFUL: "health_vibrant",
            DesignTone.TECH_MODERN: "tech_modern",
            DesignTone.TRUST_CORPORATE: "clean_retail"
        }
        
        base_palette = self.palettes.get(tone_to_palette.get(tone, "fmcg_bold_energy")).copy()
        
        # Override with brand colors if provided
        if "brand_colors" in brand_config:
            brand_colors = brand_config["brand_colors"]
            if "primary" in brand_colors:
                base_palette["primary"] = brand_colors["primary"]
            if "accent" in brand_colors:
                base_palette["accent"] = brand_colors["accent"]
            if "secondary" in brand_colors:
                base_palette["secondary"] = brand_colors["secondary"]
        
        return base_palette
    
    def _select_typography(self, tone: DesignTone) -> Dict:
        """Select typography preset"""
        tone_to_typography = {
            DesignTone.BOLD_FMCG: "bold_fmcg",
            DesignTone.PREMIUM_MODERN: "premium_modern",
            DesignTone.CLEAN_RETAIL: "clean_retail",
        }
        return self.typography.get(tone_to_typography.get(tone, "bold_fmcg"))
    
    def _select_layout(self, platform: Platform, tone: DesignTone) -> Dict:
        """Select appropriate layout"""
        # Map platform to layout
        platform_layouts = {
            Platform.INSTAGRAM_FEED: "instagram_feed_bold",
            Platform.INSTAGRAM_STORY: "instagram_story_bold",
            Platform.FACEBOOK_FEED: "facebook_feed_split",
            Platform.AMAZON_MAIN: "amazon_main_clean",
            Platform.AMAZON_LIFESTYLE: "amazon_lifestyle",
        }
        
        layout_id = platform_layouts.get(platform, "instagram_feed_bold")
        return self.layouts.get(layout_id, list(self.layouts.values())[0])
    
    def _generate_elements(
        self, 
        content: Dict, 
        palette: Dict, 
        typography: Dict,
        layout: Dict
    ) -> List[Dict]:
        """Generate design elements based on content and layout"""
        elements = []
        zones = layout.get("zones", {})
        dims = (1080, 1080)  # Default, would be set based on platform
        
        # Background
        elements.append({
            "id": "background",
            "type": "background",
            "style": palette.get("background", {}),
            "locked": True
        })
        
        # Offer Badge
        if "offer" in content and "badge" in zones:
            zone = zones["badge"]
            elements.append({
                "id": "offer_badge",
                "type": "badge",
                "text": content.get("offer", "20% OFF"),
                "x": dims[0] * zone.x / 100,
                "y": dims[1] * zone.y / 100,
                "width": dims[0] * zone.width / 100,
                "height": dims[1] * zone.height / 100,
                "backgroundColor": palette["badge_bg"],
                "textColor": palette["badge_text"],
                "fontFamily": typography["badge"]["font_family"],
                "fontWeight": typography["badge"]["font_weight"],
                "rotation": -5,
                "editable": True,
                "deletable": True
            })
        
        # Primary Headline
        if "headline" in content and "headline_primary" in zones:
            zone = zones["headline_primary"]
            elements.append({
                "id": "headline_primary",
                "type": "text",
                "text": content.get("headline", "Your Headline Here"),
                "x": dims[0] * zone.x / 100,
                "y": dims[1] * zone.y / 100,
                "width": dims[0] * zone.width / 100,
                "fontSize": 72,
                "color": palette["text_primary"],
                "fontFamily": typography["heading"]["font_family"],
                "fontWeight": typography["heading"]["font_weight"],
                "letterSpacing": typography["heading"]["letter_spacing"],
                "textAlign": zone.align,
                "editable": True,
                "colorLocked": True  # Brand color locked
            })
        
        # Secondary Headline
        if "subheadline" in content and "headline_secondary" in zones:
            zone = zones["headline_secondary"]
            elements.append({
                "id": "headline_secondary",
                "type": "text",
                "text": content.get("subheadline", "Supporting text"),
                "x": dims[0] * zone.x / 100,
                "y": dims[1] * zone.y / 100,
                "width": dims[0] * zone.width / 100,
                "fontSize": 48,
                "color": palette["accent"],
                "fontFamily": typography["heading"]["font_family"],
                "fontWeight": 700,
                "textAlign": zone.align,
                "editable": True,
                "colorLocked": True
            })
        
        # Product Area
        if "product_area" in zones:
            zone = zones["product_area"]
            elements.append({
                "id": "product_container",
                "type": "product_zone",
                "x": dims[0] * zone.x / 100,
                "y": dims[1] * zone.y / 100,
                "width": dims[0] * zone.width / 100,
                "height": dims[1] * zone.height / 100,
                "products": content.get("products", []),
                "shadow": palette.get("shadows", {}).get("product"),
                "editable": True,
                "replaceable": True
            })
        
        # Trust Signals
        if "trust_signals" in content and "trust_signals" in zones:
            zone = zones["trust_signals"]
            elements.append({
                "id": "trust_signals",
                "type": "trust_bar",
                "signals": content.get("trust_signals", []),
                "x": dims[0] * zone.x / 100,
                "y": dims[1] * zone.y / 100,
                "width": dims[0] * zone.width / 100,
                "iconColor": palette["trust_icon"],
                "textColor": palette["text_secondary"],
                "editable": True,
                "deletable": True
            })
        
        # CTA Button
        if "cta" in content and "cta" in zones:
            zone = zones["cta"]
            elements.append({
                "id": "cta_button",
                "type": "button",
                "text": content.get("cta", "Shop Now"),
                "x": dims[0] * zone.x / 100,
                "y": dims[1] * zone.y / 100,
                "width": dims[0] * zone.width / 100,
                "height": dims[1] * zone.height / 100,
                "backgroundColor": palette["cta_bg"],
                "textColor": palette["cta_text"],
                "fontFamily": typography["cta"]["font_family"],
                "fontWeight": typography["cta"]["font_weight"],
                "borderRadius": 50,
                "shadow": "0 4px 15px rgba(245,183,0,0.4)",
                "editable": True,
                "colorLocked": True
            })
        
        # Logo
        if "logo" in zones:
            zone = zones["logo"]
            elements.append({
                "id": "brand_logo",
                "type": "image",
                "src": content.get("logo_url", ""),
                "x": dims[0] * zone.x / 100,
                "y": dims[1] * zone.y / 100,
                "width": dims[0] * zone.width / 100,
                "height": dims[1] * zone.height / 100,
                "locked": True,
                "deletable": False
            })
        
        return elements
    
    def _define_editable_elements(self, brand_config: Dict) -> List[str]:
        """Define which elements users can edit"""
        return [
            "headline_primary",
            "headline_secondary",
            "offer_badge",
            "trust_signals",
            "cta_button",
            "product_container"
        ]
    
    def _define_locked_elements(self, brand_config: Dict) -> List[str]:
        """Define which elements are locked/brand-protected"""
        return [
            "background",
            "brand_logo",
            "color_palette"  # Users can't change brand colors
        ]
    
    def _create_variant(self, base_design: Dict, variant_type: str) -> Dict:
        """Create design variant"""
        variant = base_design.copy()
        variant["variant_type"] = variant_type
        
        if variant_type == "high_contrast":
            # Increase contrast, bolder colors
            variant["palette"] = self._adjust_contrast(variant["palette"], 1.3)
        elif variant_type == "minimal_luxury":
            # More whitespace, elegant typography
            variant["palette"] = self.palettes["luxury_dark"]
            variant["typography"] = self.typography["premium_modern"]
        elif variant_type == "bold_experimental":
            # Asymmetric layout, stronger visual effects
            variant["effects"] = {
                "grain": 0.05,
                "glow_intensity": 1.5,
                "shadow_depth": 1.4
            }
        
        return variant
    
    def _adjust_contrast(self, palette: Dict, factor: float) -> Dict:
        """Adjust palette contrast"""
        adjusted = palette.copy()
        # Implementation would adjust color values
        return adjusted


# =============================================================================
# EXPORT FUNCTIONS
# =============================================================================

def create_protein_bar_creative() -> Dict:
    """Create the protein bar creative based on user brief"""
    
    generator = RetailDesignGenerator()
    
    brand_config = {
        "brand_name": "CleanFuel",
        "brand_colors": {
            "primary": "#1E1E2F",
            "accent": "#F5B700",
            "secondary": "#FFFFFF"
        },
        "logo_url": "/assets/logos/cleanfuel-logo.png"
    }
    
    content = {
        "headline": "Clean Energy. Real Protein.",
        "subheadline": "Zero Compromise.",
        "offer": "20% OFF",
        "offer_subtitle": "LIMITED TIME",
        "cta": "BUY ON AMAZON",
        "trust_signals": [
            {"icon": "🌱", "text": "Plant-Based"},
            {"icon": "💪", "text": "20g Protein"},
            {"icon": "✓", "text": "No Added Sugar"}
        ],
        "products": [
            {
                "name": "Chocolate Almond",
                "image": "/assets/products/choco-almond.png",
                "rotation": -15,
                "scale": 1.05,
                "z_index": 2
            },
            {
                "name": "Peanut Butter",
                "image": "/assets/products/peanut-butter.png",
                "rotation": 12,
                "scale": 1.0,
                "z_index": 1
            }
        ]
    }
    
    # Generate primary design (Instagram Feed)
    primary_design = generator.generate_creative(
        brand_config=brand_config,
        content=content,
        platform=Platform.INSTAGRAM_FEED,
        tone=DesignTone.BOLD_FMCG
    )
    
    # Generate variants
    variants = generator.generate_variants(primary_design)
    
    # Generate all platform formats
    all_formats = generator.generate_all_formats(
        primary_design,
        [
            Platform.INSTAGRAM_FEED,
            Platform.INSTAGRAM_STORY,
            Platform.FACEBOOK_FEED,
            Platform.AMAZON_LIFESTYLE
        ]
    )
    
    return {
        "primary_design": primary_design,
        "variants": variants,
        "all_formats": all_formats,
        "export_ready": True
    }


# Quick test
if __name__ == "__main__":
    result = create_protein_bar_creative()
    print(json.dumps(result["primary_design"], indent=2, default=str))
