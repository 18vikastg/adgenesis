from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import PyPDF2
import json

from app.models import User, Base
from app.model_adapter import get_model_adapter

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model setup (OpenAI or Custom ML)
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")  # "openai" or "custom"
model_adapter = get_model_adapter()

# Legacy OpenAI client (for backward compatibility if needed)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if MODEL_PROVIDER == "openai" else None

# Demo user ID
DEMO_USER_ID = os.getenv("DEMO_USER_ID", "demo-user-001")


def get_db() -> Generator[Session, None, None]:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_demo_user(db: Session) -> User:
    """Get or create demo user for hackathon"""
    user = db.query(User).filter(User.user_id == DEMO_USER_ID).first()
    if not user:
        user = User(
            user_id=DEMO_USER_ID,
            email="demo@adgenesis.ai",
            name="Demo User"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


# Platform specifications
PLATFORM_SPECS = {
    "meta": {
        "square": {"width": 1080, "height": 1080, "min_text_ratio": 0.2},
        "landscape": {"width": 1200, "height": 628, "min_text_ratio": 0.2},
        "portrait": {"width": 1080, "height": 1350, "min_text_ratio": 0.2},
        "story": {"width": 1080, "height": 1920, "min_text_ratio": 0.2},
    },
    "google": {
        "square": {"width": 1200, "height": 1200, "max_file_size": 150000},
        "landscape": {"width": 1200, "height": 628, "max_file_size": 150000},
    },
    "linkedin": {
        "square": {"width": 1200, "height": 1200},
        "landscape": {"width": 1200, "height": 627},
    },
}


async def generate_ai_design(prompt: str, platform: str, format: str) -> dict:
    """
    Generate ad design using AI model (OpenAI or Custom ML)
    Returns Fabric.js canvas JSON structure
    """
    try:
        # Get platform specifications
        specs = PLATFORM_SPECS.get(platform, {}).get(format, {"width": 1080, "height": 1080})
        
        # Generate design using model adapter
        result = await model_adapter.generate_design_spec(
            prompt=prompt,
            platform=platform,
            format=format,
            specs=specs,
        )
        
        # If custom model returned modern design with fabric_json, use it directly
        if "fabric_json" in result:
            return result["fabric_json"]
        
        # If blueprint structure exists (from modern design system), use it
        if "blueprint" in result:
            blueprint = result["blueprint"]
            return convert_modern_blueprint_to_fabric(blueprint, specs)
        
        # Fallback: Old-style design_spec conversion
        design_spec = result
        canvas_data = {
            "version": "5.3.0",
            "objects": [],
            "background": design_spec.get("background_color", "#ffffff"),
            "width": specs["width"],
            "height": specs["height"],
        }
        
        # Add design elements (old format)
        for element in design_spec.get("elements", []):
            if element["type"] == "text":
                canvas_data["objects"].append({
                    "type": "textbox",
                    "text": element["text"],
                    "left": element.get("x", 100),
                    "top": element.get("y", 100),
                    "fontSize": element.get("fontSize", 24),
                    "fill": element.get("color", "#000000"),
                    "fontFamily": element.get("fontFamily", "Arial"),
                })
            elif element["type"] == "rectangle":
                canvas_data["objects"].append({
                    "type": "rect",
                    "left": element.get("x", 0),
                    "top": element.get("y", 0),
                    "width": element.get("width", 100),
                    "height": element.get("height", 100),
                    "fill": element.get("color", "#0000ff"),
                })
        
        return canvas_data
    except Exception as e:
        print(f"Error generating design: {e}")
        import traceback
        traceback.print_exc()
        # Return a simple fallback design
        return {
            "version": "5.3.0",
            "objects": [
                {
                    "type": "textbox",
                    "text": prompt,
                    "left": 100,
                    "top": 100,
                    "fontSize": 48,
                    "fill": "#000000",
                }
            ],
            "background": "#ffffff",
            "width": specs.get("width", 1080),
            "height": specs.get("height", 1080),
        }


def convert_modern_blueprint_to_fabric(blueprint: dict, specs: dict) -> dict:
    """
    Convert modern design blueprint to Fabric.js format
    Handles our new modern professional designs
    """
    metadata = blueprint.get("metadata", {})
    elements = blueprint.get("elements", [])
    background = blueprint.get("background", {})
    
    width = metadata.get("width", specs.get("width", 1080))
    height = metadata.get("height", specs.get("height", 1080))
    
    # Handle gradient backgrounds
    bg_color = background.get("color", "#ffffff")
    
    fabric_objects = []
    
    # Convert each element to Fabric.js object
    for element in elements:
        elem_type = element.get("type")
        position = element.get("position", {})
        size = element.get("size", {})
        
        # Convert percentage positions to pixels
        left = (position.get("x", 0) / 100) * width
        top = (position.get("y", 0) / 100) * height
        elem_width = (size.get("width", 10) / 100) * width
        elem_height = (size.get("height", 10) / 100) * height
        
        if elem_type == "text":
            fabric_objects.append({
                "type": "textbox",
                "text": element.get("content", ""),
                "left": left,
                "top": top,
                "width": elem_width,
                "fontSize": element.get("font_size", 24),
                "fontFamily": element.get("font_family", "Arial"),
                "fontWeight": element.get("font_weight", 400),
                "fill": element.get("color", "#000000"),
                "textAlign": element.get("align", "left"),
                "lineHeight": element.get("line_height", 1.2),
                "charSpacing": element.get("letter_spacing", 0) * 10,  # Convert to Fabric units
                "opacity": element.get("opacity", 1),
            })
        
        elif elem_type == "shape":
            shape_type = element.get("shape_type", "rectangle")
            
            if shape_type == "circle":
                fabric_objects.append({
                    "type": "circle",
                    "left": left,
                    "top": top,
                    "radius": elem_width / 2,  # Use width as diameter
                    "fill": element.get("fill_color", "#000000"),
                    "stroke": element.get("stroke_color"),
                    "strokeWidth": element.get("stroke_width", 0),
                    "opacity": element.get("opacity", 1),
                })
            
            elif shape_type == "rectangle" or shape_type == "line":
                fabric_objects.append({
                    "type": "rect",
                    "left": left,
                    "top": top,
                    "width": elem_width,
                    "height": elem_height,
                    "fill": element.get("fill_color", "#000000"),
                    "stroke": element.get("stroke_color"),
                    "strokeWidth": element.get("stroke_width", 0),
                    "rx": element.get("corner_radius", 0),
                    "ry": element.get("corner_radius", 0),
                    "opacity": element.get("opacity", 1),
                    "angle": element.get("rotation", 0),
                })
        
        elif elem_type == "cta_button":
            # CTA button as rounded rectangle with text
            button_bg = {
                "type": "rect",
                "left": left,
                "top": top,
                "width": elem_width,
                "height": elem_height,
                "fill": element.get("background_color", "#0000ff"),
                "rx": element.get("corner_radius", 8),
                "ry": element.get("corner_radius", 8),
                "opacity": 1,
            }
            fabric_objects.append(button_bg)
            
            # Button text
            button_text = {
                "type": "textbox",
                "text": element.get("text", "Click Here"),
                "left": left + elem_width / 2,
                "top": top + elem_height / 2,
                "fontSize": element.get("font_size", 18),
                "fontWeight": element.get("font_weight", 600),
                "fill": element.get("text_color", "#ffffff"),
                "textAlign": "center",
                "originX": "center",
                "originY": "center",
            }
            fabric_objects.append(button_text)
    
    return {
        "version": "5.3.0",
        "objects": fabric_objects,
        "background": bg_color,
        "width": width,
        "height": height,
    }


async def extract_guideline_data(file_path: str) -> dict:
    """
    Extract brand guideline data from uploaded PDF/image
    Uses OpenAI Vision API for extraction
    """
    try:
        # For PDF, extract text and images
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
            
            # Use OpenAI to extract structured data
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Extract brand guidelines from this text. Return JSON with: colors (hex codes), fonts (names), logo_description, tone, style_notes."
                    },
                    {"role": "user", "content": text_content[:4000]}  # Limit token usage
                ],
                response_format={"type": "json_object"}
            )
            
            extracted = json.loads(response.choices[0].message.content)
            return extracted
        
        # For images, use vision API (simplified for hackathon)
        else:
            return {
                "colors": ["#0066cc", "#ff6600", "#00cc66"],
                "fonts": ["Arial", "Helvetica"],
                "logos": [],
                "tone": "professional",
            }
    except Exception as e:
        print(f"Error extracting guideline data: {e}")
        return {
            "colors": [],
            "fonts": [],
            "logos": [],
        }


async def check_platform_compliance(design, platform: str) -> dict:
    """
    Check if design meets platform compliance requirements
    """
    from datetime import datetime
    from app.schemas import ComplianceIssue
    
    issues = []
    specs = PLATFORM_SPECS.get(platform, {}).get(design.format.value, {})
    
    # Check dimensions
    canvas_data = design.canvas_data or {}
    width = canvas_data.get("width", 0)
    height = canvas_data.get("height", 0)
    
    if width != specs.get("width") or height != specs.get("height"):
        issues.append(
            ComplianceIssue(
                type="dimensions",
                message=f"Expected {specs.get('width')}x{specs.get('height')}, got {width}x{height}",
                severity="error"
            )
        )
    
    # Check text ratio (for Meta)
    if platform == "meta":
        text_objects = [obj for obj in canvas_data.get("objects", []) if obj.get("type") == "textbox"]
        if len(text_objects) == 0:
            issues.append(
                ComplianceIssue(
                    type="text_content",
                    message="No text found in design",
                    severity="warning"
                )
            )
    
    is_compliant = len([i for i in issues if i.severity == "error"]) == 0
    
    return {
        "design_id": design.id,
        "platform": platform,
        "is_compliant": is_compliant,
        "issues": issues,
        "checked_at": datetime.utcnow(),
    }


def export_design_file(design, format: str):
    """
    Export design to specified format
    Returns file data for download
    """
    from fastapi.responses import StreamingResponse
    import io
    from PIL import Image, ImageDraw, ImageFont
    
    if format in ["png", "jpg"]:
        # Get canvas data
        canvas_data = design.canvas_data or {}
        width = canvas_data.get("width", 1080)
        height = canvas_data.get("height", 1080)
        background = canvas_data.get("background", "#ffffff")
        
        # Convert hex color to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Create image with background color
        bg_color = hex_to_rgb(background) if background.startswith('#') else (255, 255, 255)
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw objects
        objects = canvas_data.get("objects", [])
        for obj in objects:
            try:
                obj_type = obj.get("type", "")
                
                if obj_type in ["textbox", "text"]:
                    # Draw text
                    text = obj.get("text", "")
                    x = int(obj.get("left", 0))
                    y = int(obj.get("top", 0))
                    font_size = int(obj.get("fontSize", 16))
                    fill_color = obj.get("fill", "#000000")
                    fill_rgb = hex_to_rgb(fill_color) if fill_color.startswith('#') else (0, 0, 0)
                    
                    # Try to load font, fallback to default
                    try:
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                    except:
                        try:
                            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                        except:
                            font = ImageFont.load_default()
                    
                    draw.text((x, y), text, fill=fill_rgb, font=font)
                
                elif obj_type in ["rect", "rectangle"]:
                    # Draw rectangle
                    x = int(obj.get("left", 0))
                    y = int(obj.get("top", 0))
                    w = int(obj.get("width", 100))
                    h = int(obj.get("height", 100))
                    fill_color = obj.get("fill", "#000000")
                    fill_rgb = hex_to_rgb(fill_color) if fill_color.startswith('#') else (0, 0, 0)
                    
                    draw.rectangle([x, y, x + w, y + h], fill=fill_rgb)
            except Exception as e:
                print(f"Error drawing object: {e}")
                continue
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG' if format == 'png' else 'JPEG')
        img_byte_arr.seek(0)
        
        return StreamingResponse(
            img_byte_arr,
            media_type=f"image/{format}",
            headers={"Content-Disposition": f"attachment; filename=design_{design.id}.{format}"}
        )
    
    elif format == "svg":
        # Generate SVG from canvas data
        canvas_data = design.canvas_data or {}
        width = canvas_data.get("width", 1080)
        height = canvas_data.get("height", 1080)
        background = canvas_data.get("background", "#ffffff")
        
        svg_parts = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
        svg_parts.append(f'<rect width="{width}" height="{height}" fill="{background}"/>')
        
        objects = canvas_data.get("objects", [])
        for obj in objects:
            obj_type = obj.get("type", "")
            
            if obj_type in ["textbox", "text"]:
                text = obj.get("text", "")
                x = obj.get("left", 0)
                y = obj.get("top", 0)
                font_size = obj.get("fontSize", 16)
                fill = obj.get("fill", "#000000")
                svg_parts.append(f'<text x="{x}" y="{y + font_size}" font-size="{font_size}" fill="{fill}">{text}</text>')
            
            elif obj_type in ["rect", "rectangle"]:
                x = obj.get("left", 0)
                y = obj.get("top", 0)
                w = obj.get("width", 100)
                h = obj.get("height", 100)
                fill = obj.get("fill", "#000000")
                svg_parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')
        
        svg_parts.append('</svg>')
        svg_content = ''.join(svg_parts)
        
        return StreamingResponse(
            io.BytesIO(svg_content.encode()),
            media_type="image/svg+xml",
            headers={"Content-Disposition": f"attachment; filename=design_{design.id}.svg"}
        )
    
    else:  # PDF
        return {"error": "PDF export not implemented yet"}
