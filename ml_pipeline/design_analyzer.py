"""
DESIGN REVERSE-ENGINEERING ENGINE
=================================
Analyzes uploaded images/posters and converts them into
fully editable design structures (layers) for a Canva/Figma-like editor.

This module:
- Detects all visual elements
- Identifies editable text via OCR
- Identifies images, shapes, icons, backgrounds
- Preserves layout, spacing, hierarchy
- Converts everything into independent editable layers
"""

import os
import io
import re
import json
import base64
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from PIL import Image
import colorsys

# Try to import vision/OCR libraries
try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


# ============================================================================
# COLOR ANALYSIS UTILITIES
# ============================================================================

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex color"""
    return f"#{r:02x}{g:02x}{b:02x}".upper()


def extract_dominant_colors(image: Image.Image, num_colors: int = 5) -> List[str]:
    """Extract dominant colors from an image"""
    # Resize for faster processing
    img = image.copy()
    img.thumbnail((150, 150))
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Get all pixels
    pixels = list(img.getdata())
    
    # Simple color quantization
    color_counts = {}
    for pixel in pixels:
        # Quantize to reduce unique colors
        quantized = (pixel[0] // 32 * 32, pixel[1] // 32 * 32, pixel[2] // 32 * 32)
        color_counts[quantized] = color_counts.get(quantized, 0) + 1
    
    # Sort by frequency
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Get top colors
    dominant = []
    for color, count in sorted_colors[:num_colors]:
        hex_color = rgb_to_hex(*color)
        dominant.append(hex_color)
    
    return dominant


def detect_background_type(image: Image.Image) -> Dict[str, Any]:
    """Detect if background is solid, gradient, or image"""
    img = image.copy()
    img.thumbnail((100, 100))
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    pixels = list(img.getdata())
    width, height = img.size
    
    # Sample edges
    top_row = pixels[:width]
    bottom_row = pixels[-width:]
    left_col = [pixels[i * width] for i in range(height)]
    right_col = [pixels[i * width + width - 1] for i in range(height)]
    
    # Check color variance
    def color_variance(pixel_list):
        if not pixel_list:
            return 0
        rs = [p[0] for p in pixel_list]
        gs = [p[1] for p in pixel_list]
        bs = [p[2] for p in pixel_list]
        return max(max(rs) - min(rs), max(gs) - min(gs), max(bs) - min(bs))
    
    edge_variance = color_variance(top_row + bottom_row + left_col + right_col)
    
    # Get corner colors
    corners = [
        pixels[0],  # top-left
        pixels[width - 1],  # top-right
        pixels[-width],  # bottom-left
        pixels[-1],  # bottom-right
    ]
    
    corner_variance = color_variance(corners)
    
    if corner_variance < 30 and edge_variance < 50:
        # Likely solid color
        avg_color = (
            sum(c[0] for c in corners) // 4,
            sum(c[1] for c in corners) // 4,
            sum(c[2] for c in corners) // 4,
        )
        return {
            "type": "solid",
            "color": rgb_to_hex(*avg_color)
        }
    elif corner_variance > 30 and corner_variance < 150:
        # Likely gradient
        colors = [rgb_to_hex(*c) for c in corners]
        unique_colors = list(set(colors))
        
        # Detect gradient direction
        top_avg = sum(corners[0][i] + corners[1][i] for i in range(3)) // 6
        bottom_avg = sum(corners[2][i] + corners[3][i] for i in range(3)) // 6
        left_avg = sum(corners[0][i] + corners[2][i] for i in range(3)) // 6
        right_avg = sum(corners[1][i] + corners[3][i] for i in range(3)) // 6
        
        if abs(top_avg - bottom_avg) > abs(left_avg - right_avg):
            angle = 180  # Vertical gradient
        else:
            angle = 90  # Horizontal gradient
        
        return {
            "type": "gradient",
            "colors": unique_colors[:2] if len(unique_colors) >= 2 else [unique_colors[0], unique_colors[0]],
            "angle": angle
        }
    else:
        # Likely image background
        return {
            "type": "image",
            "dominant_colors": extract_dominant_colors(image, 3)
        }


# ============================================================================
# TEXT DETECTION (OCR)
# ============================================================================

def detect_text_regions_tesseract(image: Image.Image) -> List[Dict[str, Any]]:
    """Detect text using Tesseract OCR - improved for diagrams and technical images"""
    if not TESSERACT_AVAILABLE:
        print("⚠️ Tesseract not available")
        return []
    
    try:
        # Preprocess image for better OCR
        img = image.convert('RGB')
        
        # Try multiple OCR configurations for better detection
        configs = [
            '--oem 3 --psm 11',  # Sparse text - good for diagrams
            '--oem 3 --psm 6',   # Uniform block of text
            '--oem 3 --psm 3',   # Fully automatic
        ]
        
        all_regions = []
        seen_texts = set()
        
        for config in configs:
            try:
                # Get detailed OCR data
                data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=config)
                
                n_boxes = len(data['text'])
                
                for i in range(n_boxes):
                    text = data['text'][i].strip()
                    conf = int(data['conf'][i]) if data['conf'][i] != '-1' else 0
                    
                    # Lower confidence threshold for diagrams
                    if text and len(text) > 1 and conf > 20:
                        x = data['left'][i]
                        y = data['top'][i]
                        w = data['width'][i]
                        h = data['height'][i]
                        
                        # Skip very small text
                        if w < 10 or h < 8:
                            continue
                        
                        # Create unique key to avoid duplicates
                        text_key = f"{text.lower()}_{x//20}_{y//20}"
                        if text_key in seen_texts:
                            continue
                        seen_texts.add(text_key)
                        
                        all_regions.append({
                            "text": text,
                            "position": {"x": x, "y": y},
                            "size": {"width": w, "height": h},
                            "confidence": conf
                        })
                        print(f"   Found text: '{text}' at ({x}, {y}) conf={conf}")
                        
            except Exception as e:
                print(f"OCR config {config} failed: {e}")
                continue
        
        # Sort by position (top to bottom, left to right)
        all_regions.sort(key=lambda r: (r["position"]["y"] // 50, r["position"]["x"]))
        
        # Merge nearby text into lines
        merged = _merge_nearby_text(all_regions, image.width)
        
        print(f"   Total text regions: {len(merged)}")
        return merged
        
    except Exception as e:
        print(f"OCR error: {e}")
        import traceback
        traceback.print_exc()
        return []


def _merge_nearby_text(regions: List[Dict], img_width: int) -> List[Dict]:
    """Merge text regions that are on the same line"""
    if not regions:
        return []
    
    merged = []
    used = set()
    
    for i, r1 in enumerate(regions):
        if i in used:
            continue
        
        # Find all regions on the same approximate line
        line_regions = [r1]
        used.add(i)
        
        for j, r2 in enumerate(regions):
            if j in used:
                continue
            
            # Check if on same line (within 15 pixels vertically)
            y_diff = abs(r1["position"]["y"] - r2["position"]["y"])
            if y_diff < 15:
                line_regions.append(r2)
                used.add(j)
        
        # Sort line by x position
        line_regions.sort(key=lambda r: r["position"]["x"])
        
        # Merge into single region if close enough
        if len(line_regions) == 1:
            merged.append(line_regions[0])
        else:
            # Check if regions are close horizontally
            combined_text = []
            min_x = line_regions[0]["position"]["x"]
            min_y = min(r["position"]["y"] for r in line_regions)
            max_x = 0
            max_y = 0
            total_conf = 0
            
            for r in line_regions:
                combined_text.append(r["text"])
                max_x = max(max_x, r["position"]["x"] + r["size"]["width"])
                max_y = max(max_y, r["position"]["y"] + r["size"]["height"])
                total_conf += r["confidence"]
            
            merged.append({
                "text": " ".join(combined_text),
                "position": {"x": min_x, "y": min_y},
                "size": {"width": max_x - min_x, "height": max_y - min_y},
                "confidence": total_conf // len(line_regions)
            })
    
    return merged


def classify_text_role(text: str, position: Dict, canvas_size: Tuple[int, int], font_size: int) -> str:
    """Classify text as headline, subheadline, body, CTA, etc."""
    text_lower = text.lower()
    y_ratio = position["y"] / canvas_size[1]
    
    # CTA detection
    cta_keywords = ["shop", "buy", "get", "order", "learn", "discover", "try", "start", 
                    "subscribe", "download", "join", "click", "view", "explore", "now"]
    if any(kw in text_lower for kw in cta_keywords) and len(text.split()) <= 4:
        return "cta"
    
    # Legal/fine print (small text at bottom)
    if y_ratio > 0.85 and font_size < 14:
        return "legal"
    
    # Headline (large text, usually upper portion)
    if font_size > 40 and y_ratio < 0.5:
        return "headline"
    
    # Subheadline
    if font_size > 24 and font_size <= 40:
        return "subheadline"
    
    # Badge/label (short text)
    if len(text) <= 15 and font_size < 20:
        return "badge"
    
    # Body text
    return "body"


# ============================================================================
# ELEMENT DETECTION
# ============================================================================

def detect_shapes_and_regions(image: Image.Image) -> List[Dict[str, Any]]:
    """Detect shapes and visual regions in the image"""
    # This is a simplified version - for production, use ML-based detection
    
    img = image.copy()
    width, height = img.size
    
    shapes = []
    
    # Try to detect rectangular regions using edge detection
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Simple region detection based on color uniformity
    # Divide image into grid and check for uniform color regions
    grid_size = 8
    cell_w = width // grid_size
    cell_h = height // grid_size
    
    uniform_regions = []
    
    for gy in range(grid_size):
        for gx in range(grid_size):
            x1, y1 = gx * cell_w, gy * cell_h
            x2, y2 = x1 + cell_w, y1 + cell_h
            
            region = img.crop((x1, y1, x2, y2))
            colors = extract_dominant_colors(region, 1)
            
            # Check if region is mostly one color
            pixels = list(region.getdata())
            if colors:
                main_color = colors[0]
                # This is a uniform region marker
                uniform_regions.append({
                    "grid": (gx, gy),
                    "bounds": (x1, y1, x2, y2),
                    "color": main_color
                })
    
    return shapes


def estimate_font_properties(text_region: Dict, image: Image.Image) -> Dict[str, Any]:
    """Estimate font properties from a text region"""
    h = text_region["size"]["height"]
    text = text_region["text"]
    
    # Estimate font size from bounding box height
    font_size = int(h * 0.85)  # Approximate
    
    # Detect if text is likely bold (crude heuristic)
    is_bold = len(text) < 20 and font_size > 30
    
    # Detect style
    if text.isupper():
        text_transform = "uppercase"
    elif text.istitle():
        text_transform = "capitalize"
    else:
        text_transform = "none"
    
    return {
        "font_size": font_size,
        "font_weight": "bold" if is_bold else "normal",
        "text_transform": text_transform,
        "font_family": "sans-serif"  # Default assumption
    }


# ============================================================================
# MAIN ANALYZER CLASS
# ============================================================================

class DesignAnalyzer:
    """
    Analyzes uploaded images and converts them into editable design structures.
    """
    
    def __init__(self, hf_token: Optional[str] = None):
        self.hf_token = hf_token or os.getenv("HUGGINGFACE_API_KEY", "")
        self.hf_client = None
        
        if HF_AVAILABLE and self.hf_token:
            try:
                self.hf_client = InferenceClient(token=self.hf_token)
            except Exception as e:
                print(f"Could not initialize HF client: {e}")
    
    def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Main entry point: Analyze an image and return editable blueprint.
        """
        width, height = image.size
        
        print(f"🔍 Analyzing image: {width}x{height}")
        
        # Step 1: Detect background
        print("   📋 Detecting background...")
        background = detect_background_type(image)
        
        # Step 2: Extract color palette
        print("   🎨 Extracting colors...")
        color_palette = extract_dominant_colors(image, 6)
        
        # Step 3: Detect text regions
        print("   📝 Detecting text (OCR)...")
        text_regions = detect_text_regions_tesseract(image)
        
        # Step 4: Build layers
        print("   🧱 Building editable layers...")
        layers = self._build_layers(image, text_regions, color_palette)
        
        # Step 5: Assemble blueprint
        blueprint = {
            "canvas": {
                "width": width,
                "height": height,
                "background": background
            },
            "color_palette": color_palette,
            "layers": layers,
            "metadata": {
                "source": "image_analysis",
                "ocr_available": TESSERACT_AVAILABLE,
                "text_regions_detected": len(text_regions),
                "total_layers": len(layers)
            }
        }
        
        print(f"   ✅ Analysis complete: {len(layers)} layers detected")
        
        return blueprint
    
    def _build_layers(
        self, 
        image: Image.Image, 
        text_regions: List[Dict], 
        color_palette: List[str]
    ) -> List[Dict[str, Any]]:
        """Build editable layers from detected elements"""
        
        layers = []
        layer_id = 0
        width, height = image.size
        
        # Background layer (always first)
        layers.append({
            "id": f"background_{layer_id}",
            "type": "background",
            "role": "background",
            "position": {"x": 0, "y": 0},
            "size": {"width": width, "height": height},
            "z_index": 0,
            "editable": True,
            "locked": False
        })
        layer_id += 1
        
        # Text layers
        for i, region in enumerate(text_regions):
            font_props = estimate_font_properties(region, image)
            role = classify_text_role(
                region["text"], 
                region["position"], 
                (width, height),
                font_props["font_size"]
            )
            
            # Estimate text color (use contrasting color from palette)
            text_color = self._estimate_text_color(
                region["position"], 
                image, 
                color_palette
            )
            
            layer = {
                "id": f"text_{layer_id}",
                "type": "text",
                "role": role,
                "content": region["text"],
                "font_family": font_props["font_family"],
                "font_size": font_props["font_size"],
                "font_weight": font_props["font_weight"],
                "text_transform": font_props["text_transform"],
                "color": text_color,
                "position": region["position"],
                "size": region["size"],
                "alignment": self._detect_alignment(region["position"], width),
                "z_index": 10 + i,
                "editable": True,
                "confidence": region.get("confidence", 100) / 100,
                # Add background color to cover original text when editing
                "background_color": self._detect_region_background(region, image),
            }
            
            # Add role-specific properties
            if role == "cta":
                layer["background_color"] = color_palette[1] if len(color_palette) > 1 else "#8B5CF6"
                layer["border_radius"] = 8
                layer["padding"] = {"x": 24, "y": 12}
            
            layers.append(layer)
            layer_id += 1
        
        # Detect non-text image regions (areas that likely contain graphics/photos)
        # These are areas NOT covered by text
        image_regions = self._detect_image_regions(image, text_regions, width, height)
        for region in image_regions:
            layers.append({
                "id": f"image_{layer_id}",
                "type": "image",
                "role": region.get("role", "graphic"),
                "position": region["position"],
                "size": region["size"],
                "z_index": 5,
                "replaceable": True,
                "placeholder": False,  # Real detected region
                "crop_from_original": True,  # Tell frontend to crop this from image
            })
            layer_id += 1
        
        return layers
    
    def _detect_image_regions(self, image: Image.Image, text_regions: List[Dict], width: int, height: int) -> List[Dict]:
        """
        Detect image/graphic regions that are NOT text.
        These are areas the user might want to move or edit.
        """
        regions = []
        
        # Simple heuristic: divide image into grid and find non-text areas
        # that have visual content (not uniform color)
        
        # For now, detect a center region if there's no text in the middle
        center_x = width // 4
        center_y = height // 4
        center_w = width // 2
        center_h = height // 2
        
        # Check if center is covered by text
        center_has_text = False
        for tr in text_regions:
            tx, ty = tr["position"]["x"], tr["position"]["y"]
            tw, th = tr["size"]["width"], tr["size"]["height"]
            # Check overlap with center
            if (tx < center_x + center_w and tx + tw > center_x and
                ty < center_y + center_h and ty + th > center_y):
                center_has_text = True
                break
        
        if not center_has_text:
            # Add center region as potential image/graphic area
            regions.append({
                "position": {"x": center_x, "y": center_y},
                "size": {"width": center_w, "height": center_h},
                "role": "main_graphic"
            })
        
        return regions
    
    def _estimate_text_color(
        self, 
        position: Dict, 
        image: Image.Image, 
        palette: List[str]
    ) -> str:
        """Estimate text color based on background at that position"""
        x, y = position["x"], position["y"]
        
        # Sample background color at text position
        try:
            img = image.convert('RGB')
            bg_pixel = img.getpixel((min(x, img.width - 1), min(y, img.height - 1)))
            
            # Calculate luminance
            luminance = (0.299 * bg_pixel[0] + 0.587 * bg_pixel[1] + 0.114 * bg_pixel[2]) / 255
            
            # Return contrasting color
            if luminance > 0.5:
                return "#1A1A2E"  # Dark text on light bg
            else:
                return "#FFFFFF"  # Light text on dark bg
        except:
            return "#FFFFFF"
    
    def _detect_region_background(self, region: Dict, image: Image.Image) -> str:
        """
        Detect the background color behind a text region.
        This is used to cover the original text when making it editable.
        """
        try:
            img = image.convert('RGB')
            x = region["position"]["x"]
            y = region["position"]["y"]
            w = region["size"]["width"]
            h = region["size"]["height"]
            
            # Sample colors from around the text region (edges)
            # to avoid sampling the text itself
            samples = []
            
            # Sample above the text
            if y > 5:
                for sx in range(max(0, x), min(img.width, x + w), max(1, w // 5)):
                    samples.append(img.getpixel((sx, max(0, y - 3))))
            
            # Sample below the text
            if y + h < img.height - 5:
                for sx in range(max(0, x), min(img.width, x + w), max(1, w // 5)):
                    samples.append(img.getpixel((sx, min(img.height - 1, y + h + 3))))
            
            # Sample left of text
            if x > 5:
                samples.append(img.getpixel((max(0, x - 3), min(img.height - 1, y + h // 2))))
            
            # Sample right of text
            if x + w < img.width - 5:
                samples.append(img.getpixel((min(img.width - 1, x + w + 3), min(img.height - 1, y + h // 2))))
            
            if not samples:
                return "transparent"
            
            # Average the samples
            avg_r = sum(s[0] for s in samples) // len(samples)
            avg_g = sum(s[1] for s in samples) // len(samples)
            avg_b = sum(s[2] for s in samples) // len(samples)
            
            return rgb_to_hex(avg_r, avg_g, avg_b)
        except Exception as e:
            print(f"Error detecting region background: {e}")
            return "transparent"
    
    def _detect_alignment(self, position: Dict, canvas_width: int) -> str:
        """Detect text alignment based on position"""
        x = position["x"]
        ratio = x / canvas_width
        
        if ratio < 0.2:
            return "left"
        elif ratio > 0.6:
            return "right"
        else:
            return "center"
    
    async def analyze_with_vision_ai(self, image: Image.Image) -> Dict[str, Any]:
        """
        Use AI vision model for more accurate analysis.
        Falls back to basic analysis if AI not available.
        """
        if not self.hf_client:
            print("⚠️ Vision AI not available, using basic analysis")
            return self.analyze_image(image)
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Use HuggingFace vision model for analysis
        # This would require a vision-language model like BLIP or LLaVA
        
        # For now, fall back to basic analysis
        return self.analyze_image(image)


def convert_blueprint_to_fabric(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert analyzed blueprint to Fabric.js format for the editor.
    """
    canvas = blueprint["canvas"]
    layers = blueprint["layers"]
    
    fabric_objects = []
    
    # Background
    bg = canvas.get("background", {})
    if bg.get("type") == "solid":
        fabric_objects.append({
            "type": "rect",
            "id": "background",
            "left": 0,
            "top": 0,
            "width": canvas["width"],
            "height": canvas["height"],
            "fill": bg.get("color", "#1A1A2E"),
            "selectable": False,
            "evented": False
        })
    elif bg.get("type") == "gradient":
        colors = bg.get("colors", ["#1A1A2E", "#0F172A"])
        angle = bg.get("angle", 180)
        
        # Calculate gradient coords
        import math
        rad = math.radians(angle)
        w, h = canvas["width"], canvas["height"]
        cx, cy = w / 2, h / 2
        length = max(w, h) * 1.5
        
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
            "id": "background",
            "left": 0,
            "top": 0,
            "width": canvas["width"],
            "height": canvas["height"],
            "fill": {
                "type": "linear",
                "coords": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "colorStops": color_stops
            },
            "selectable": False,
            "evented": False
        })
    
    # Convert layers
    for layer in layers:
        if layer["type"] == "background":
            continue  # Already handled
        
        if layer["type"] == "text":
            fabric_obj = {
                "type": "textbox",
                "id": layer["id"],
                "left": layer["position"]["x"],
                "top": layer["position"]["y"],
                "width": layer["size"]["width"],
                "text": layer["content"],
                "fontSize": layer["font_size"],
                "fontFamily": layer.get("font_family", "Inter"),
                "fontWeight": layer.get("font_weight", "normal"),
                "fill": layer["color"],
                "textAlign": layer.get("alignment", "left"),
                "selectable": True,
                "editable": True,
                "role": layer["role"]
            }
            
            # CTA button styling
            if layer["role"] == "cta" and layer.get("background_color"):
                # Add background rect for CTA
                padding = layer.get("padding", {"x": 20, "y": 10})
                fabric_objects.append({
                    "type": "rect",
                    "id": f"{layer['id']}_bg",
                    "left": layer["position"]["x"] - padding["x"],
                    "top": layer["position"]["y"] - padding["y"],
                    "width": layer["size"]["width"] + padding["x"] * 2,
                    "height": layer["size"]["height"] + padding["y"] * 2,
                    "fill": layer["background_color"],
                    "rx": layer.get("border_radius", 8),
                    "ry": layer.get("border_radius", 8),
                    "selectable": True
                })
            
            fabric_objects.append(fabric_obj)
        
        elif layer["type"] == "image":
            fabric_objects.append({
                "type": "image",
                "id": layer["id"],
                "left": layer["position"]["x"],
                "top": layer["position"]["y"],
                "width": layer["size"]["width"],
                "height": layer["size"]["height"],
                "selectable": True,
                "replaceable": layer.get("replaceable", True),
                "placeholder": layer.get("placeholder", False)
            })
        
        elif layer["type"] == "shape":
            fabric_objects.append({
                "type": layer.get("shape_type", "rect"),
                "id": layer["id"],
                "left": layer["position"]["x"],
                "top": layer["position"]["y"],
                "width": layer["size"]["width"],
                "height": layer["size"]["height"],
                "fill": layer.get("fill", "#8B5CF6"),
                "rx": layer.get("border_radius", 0),
                "ry": layer.get("border_radius", 0),
                "selectable": True
            })
    
    return {
        "version": "5.3.0",
        "objects": fabric_objects,
        "background": canvas.get("background", {}).get("color", "#1A1A2E")
    }


# Singleton instance
design_analyzer = DesignAnalyzer()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def analyze_image_from_base64(base64_data: str) -> Dict[str, Any]:
    """Analyze an image from base64 data"""
    # Remove data URL prefix if present
    if "," in base64_data:
        base64_data = base64_data.split(",")[1]
    
    image_data = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(image_data))
    
    return design_analyzer.analyze_image(image)


def analyze_image_from_file(file_path: str) -> Dict[str, Any]:
    """Analyze an image from file path"""
    image = Image.open(file_path)
    return design_analyzer.analyze_image(image)


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    # Test with a sample image
    print("Design Analyzer Test")
    print("=" * 50)
    
    # Create a simple test image
    test_img = Image.new('RGB', (1080, 1080), color='#1A1A2E')
    
    result = design_analyzer.analyze_image(test_img)
    print(json.dumps(result, indent=2))
