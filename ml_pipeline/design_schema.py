"""
Design Blueprint Schema for AdGenesis
Defines the JSON structure that the LLM generates for ad designs
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from enum import Enum

# =============================================================================
# ENUMS
# =============================================================================

class Platform(str, Enum):
    META = "meta"
    GOOGLE = "google"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"

class AdFormat(str, Enum):
    SQUARE = "square"           # 1080x1080
    STORY = "story"             # 1080x1920
    LANDSCAPE = "landscape"     # 1200x628
    PORTRAIT = "portrait"       # 1080x1350
    WIDE = "wide"               # 1920x1080
    BANNER = "banner"           # 1200x300

class ElementType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    SHAPE = "shape"
    LOGO = "logo"
    CTA_BUTTON = "cta_button"
    BACKGROUND = "background"

class TextStyle(str, Enum):
    HEADLINE = "headline"
    SUBHEADLINE = "subheadline"
    BODY = "body"
    CTA = "cta"
    CAPTION = "caption"

class ShapeType(str, Enum):
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    ROUNDED_RECT = "rounded_rect"
    LINE = "line"
    TRIANGLE = "triangle"

class HorizontalAlign(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class VerticalAlign(str, Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"

# =============================================================================
# DESIGN ELEMENTS
# =============================================================================

class Position(BaseModel):
    """Position as percentage of canvas (0-100)"""
    x: float = Field(ge=0, le=100, description="X position as % of canvas width")
    y: float = Field(ge=0, le=100, description="Y position as % of canvas height")

class Size(BaseModel):
    """Size as percentage of canvas"""
    width: float = Field(ge=0, le=100, description="Width as % of canvas width")
    height: float = Field(ge=0, le=100, description="Height as % of canvas height")

class TextElement(BaseModel):
    """Text element in the design"""
    type: Literal["text"] = "text"
    id: str = Field(description="Unique element ID")
    content: str = Field(description="The actual text content")
    style: TextStyle = Field(description="Text style/role")
    position: Position
    size: Size
    font_family: str = Field(default="Inter")
    font_size: int = Field(ge=8, le=200, description="Font size in pixels")
    font_weight: int = Field(default=400, ge=100, le=900)
    color: str = Field(description="Hex color code")
    align: HorizontalAlign = Field(default=HorizontalAlign.CENTER)
    line_height: float = Field(default=1.2, ge=0.8, le=3.0)
    letter_spacing: float = Field(default=0, ge=-5, le=20)

class ShapeElement(BaseModel):
    """Shape element in the design"""
    type: Literal["shape"] = "shape"
    id: str
    shape_type: ShapeType
    position: Position
    size: Size
    fill_color: str = Field(description="Hex color code")
    stroke_color: Optional[str] = None
    stroke_width: int = Field(default=0, ge=0, le=20)
    opacity: float = Field(default=1.0, ge=0, le=1)
    corner_radius: int = Field(default=0, ge=0, le=100)

class ImageElement(BaseModel):
    """Image/logo element in the design"""
    type: Literal["image"] = "image"
    id: str
    position: Position
    size: Size
    placeholder: str = Field(description="Description of what image should be")
    opacity: float = Field(default=1.0, ge=0, le=1)
    fit: Literal["cover", "contain", "fill"] = "cover"

class CTAButtonElement(BaseModel):
    """Call-to-action button element"""
    type: Literal["cta_button"] = "cta_button"
    id: str
    text: str = Field(description="Button text")
    position: Position
    size: Size
    background_color: str
    text_color: str
    font_size: int = Field(default=16)
    font_weight: int = Field(default=600)
    corner_radius: int = Field(default=8)
    padding: int = Field(default=16)

class BackgroundElement(BaseModel):
    """Background configuration"""
    type: Literal["background"] = "background"
    color: Optional[str] = Field(default=None, description="Solid color hex")
    gradient: Optional[dict] = Field(default=None, description="Gradient config")
    image_placeholder: Optional[str] = Field(default=None, description="Background image description")

# Union type for all elements
DesignElement = TextElement | ShapeElement | ImageElement | CTAButtonElement

# =============================================================================
# DESIGN BLUEPRINT
# =============================================================================

class ColorPalette(BaseModel):
    """Color scheme for the design"""
    primary: str = Field(description="Primary brand/accent color")
    secondary: str = Field(description="Secondary color")
    background: str = Field(description="Background color")
    text_primary: str = Field(description="Primary text color")
    text_secondary: str = Field(description="Secondary text color")
    accent: Optional[str] = Field(default=None, description="Accent/highlight color")

class DesignMetadata(BaseModel):
    """Metadata about the design"""
    platform: Platform
    format: AdFormat
    width: int
    height: int
    industry: Optional[str] = None
    campaign_type: Optional[str] = None
    target_audience: Optional[str] = None

class DesignBlueprint(BaseModel):
    """
    Complete design blueprint that the LLM generates.
    This is the structured output that represents an entire ad design.
    """
    # Metadata
    metadata: DesignMetadata
    
    # Design content
    headline: str = Field(description="Main headline text")
    subheadline: Optional[str] = Field(default=None, description="Supporting text")
    body_text: Optional[str] = Field(default=None, description="Body copy")
    cta_text: str = Field(description="Call-to-action text")
    
    # Visual design
    background: BackgroundElement
    color_palette: ColorPalette
    
    # All design elements with positions
    elements: List[DesignElement] = Field(description="All positioned elements")
    
    # Design rationale (for learning/iteration)
    design_notes: Optional[str] = Field(default=None, description="Why this design works")

# =============================================================================
# FORMAT SPECIFICATIONS
# =============================================================================

FORMAT_SPECS = {
    AdFormat.SQUARE: {"width": 1080, "height": 1080, "aspect": "1:1"},
    AdFormat.STORY: {"width": 1080, "height": 1920, "aspect": "9:16"},
    AdFormat.LANDSCAPE: {"width": 1200, "height": 628, "aspect": "1.91:1"},
    AdFormat.PORTRAIT: {"width": 1080, "height": 1350, "aspect": "4:5"},
    AdFormat.WIDE: {"width": 1920, "height": 1080, "aspect": "16:9"},
    AdFormat.BANNER: {"width": 1200, "height": 300, "aspect": "4:1"},
}

PLATFORM_GUIDELINES = {
    Platform.META: {
        "text_ratio_limit": 0.20,  # Max 20% text
        "safe_zone": 0.05,  # 5% margin
        "min_contrast": 4.5,
        "forbidden_words": ["free", "guarantee", "best"],
    },
    Platform.GOOGLE: {
        "text_ratio_limit": 0.25,
        "safe_zone": 0.03,
        "min_contrast": 4.5,
        "forbidden_words": ["click here"],
    },
    Platform.LINKEDIN: {
        "text_ratio_limit": 0.30,
        "safe_zone": 0.05,
        "min_contrast": 4.5,
        "forbidden_words": [],
    },
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_canvas_size(format: AdFormat) -> tuple[int, int]:
    """Get canvas dimensions for a format"""
    spec = FORMAT_SPECS[format]
    return spec["width"], spec["height"]

def blueprint_to_fabric_json(blueprint: DesignBlueprint) -> dict:
    """
    Convert a DesignBlueprint to Fabric.js JSON format.
    This is what the frontend uses to render the design.
    """
    width, height = blueprint.metadata.width, blueprint.metadata.height
    
    fabric_objects = []
    
    # Background
    if blueprint.background.color:
        fabric_objects.append({
            "type": "rect",
            "left": 0,
            "top": 0,
            "width": width,
            "height": height,
            "fill": blueprint.background.color,
            "selectable": False,
            "evented": False,
        })
    
    # Convert each element
    for element in blueprint.elements:
        # Convert percentage positions to pixels
        left = (element.position.x / 100) * width
        top = (element.position.y / 100) * height
        el_width = (element.size.width / 100) * width
        el_height = (element.size.height / 100) * height
        
        if element.type == "text":
            fabric_objects.append({
                "type": "textbox",
                "id": element.id,
                "left": left,
                "top": top,
                "width": el_width,
                "text": element.content,
                "fontSize": element.font_size,
                "fontFamily": element.font_family,
                "fontWeight": element.font_weight,
                "fill": element.color,
                "textAlign": element.align.value,
                "lineHeight": element.line_height,
                "charSpacing": element.letter_spacing * 10,
            })
        
        elif element.type == "shape":
            shape_obj = {
                "id": element.id,
                "left": left,
                "top": top,
                "width": el_width,
                "height": el_height,
                "fill": element.fill_color,
                "opacity": element.opacity,
            }
            
            if element.shape_type == ShapeType.CIRCLE:
                shape_obj["type"] = "circle"
                shape_obj["radius"] = min(el_width, el_height) / 2
            elif element.shape_type == ShapeType.RECTANGLE:
                shape_obj["type"] = "rect"
                shape_obj["rx"] = element.corner_radius
                shape_obj["ry"] = element.corner_radius
            elif element.shape_type == ShapeType.ROUNDED_RECT:
                shape_obj["type"] = "rect"
                shape_obj["rx"] = element.corner_radius or 16
                shape_obj["ry"] = element.corner_radius or 16
            
            if element.stroke_color:
                shape_obj["stroke"] = element.stroke_color
                shape_obj["strokeWidth"] = element.stroke_width
            
            fabric_objects.append(shape_obj)
        
        elif element.type == "cta_button":
            # CTA as a group: rect + text
            fabric_objects.append({
                "type": "rect",
                "id": f"{element.id}_bg",
                "left": left,
                "top": top,
                "width": el_width,
                "height": el_height,
                "fill": element.background_color,
                "rx": element.corner_radius,
                "ry": element.corner_radius,
            })
            fabric_objects.append({
                "type": "textbox",
                "id": f"{element.id}_text",
                "left": left,
                "top": top + (el_height - element.font_size) / 2,
                "width": el_width,
                "text": element.text,
                "fontSize": element.font_size,
                "fontWeight": element.font_weight,
                "fill": element.text_color,
                "textAlign": "center",
            })
        
        elif element.type == "image":
            # Placeholder for image
            fabric_objects.append({
                "type": "rect",
                "id": element.id,
                "left": left,
                "top": top,
                "width": el_width,
                "height": el_height,
                "fill": "#333333",
                "opacity": element.opacity,
                "placeholder": element.placeholder,
            })
    
    return {
        "version": "5.3.0",
        "objects": fabric_objects,
        "background": blueprint.background.color or "#ffffff",
    }

# =============================================================================
# EXAMPLE BLUEPRINT
# =============================================================================

EXAMPLE_BLUEPRINT = {
    "metadata": {
        "platform": "meta",
        "format": "square",
        "width": 1080,
        "height": 1080,
        "industry": "e-commerce",
        "campaign_type": "product_launch",
        "target_audience": "young_professionals"
    },
    "headline": "Summer Sale",
    "subheadline": "Up to 50% off selected items",
    "body_text": None,
    "cta_text": "Shop Now",
    "background": {
        "type": "background",
        "color": "#1a1a2e",
        "gradient": None,
        "image_placeholder": None
    },
    "color_palette": {
        "primary": "#8B5CF6",
        "secondary": "#06B6D4",
        "background": "#1a1a2e",
        "text_primary": "#ffffff",
        "text_secondary": "#a0aec0",
        "accent": "#F59E0B"
    },
    "elements": [
        {
            "type": "text",
            "id": "headline_1",
            "content": "Summer Sale",
            "style": "headline",
            "position": {"x": 10, "y": 35},
            "size": {"width": 80, "height": 15},
            "font_family": "Inter",
            "font_size": 72,
            "font_weight": 700,
            "color": "#ffffff",
            "align": "center",
            "line_height": 1.1,
            "letter_spacing": -1
        },
        {
            "type": "text",
            "id": "subheadline_1",
            "content": "Up to 50% off selected items",
            "style": "subheadline",
            "position": {"x": 15, "y": 52},
            "size": {"width": 70, "height": 8},
            "font_family": "Inter",
            "font_size": 28,
            "font_weight": 400,
            "color": "#a0aec0",
            "align": "center",
            "line_height": 1.3,
            "letter_spacing": 0
        },
        {
            "type": "cta_button",
            "id": "cta_1",
            "text": "Shop Now",
            "position": {"x": 30, "y": 70},
            "size": {"width": 40, "height": 6},
            "background_color": "#8B5CF6",
            "text_color": "#ffffff",
            "font_size": 18,
            "font_weight": 600,
            "corner_radius": 100,
            "padding": 16
        },
        {
            "type": "shape",
            "id": "accent_circle",
            "shape_type": "circle",
            "position": {"x": 75, "y": 10},
            "size": {"width": 20, "height": 20},
            "fill_color": "#8B5CF6",
            "stroke_color": None,
            "stroke_width": 0,
            "opacity": 0.3,
            "corner_radius": 0
        }
    ],
    "design_notes": "Clean, modern design with strong headline hierarchy. Purple accent color draws attention to CTA. Sufficient contrast for accessibility."
}
