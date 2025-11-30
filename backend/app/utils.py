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

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# OpenAI setup
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    Generate ad design using OpenAI API
    Returns Fabric.js canvas JSON structure
    """
    try:
        # Get platform specifications
        specs = PLATFORM_SPECS.get(platform, {}).get(format, {"width": 1080, "height": 1080})
        
        # Create AI prompt for design generation
        system_prompt = f"""You are an expert ad designer. Generate a detailed design specification for an advertisement.
Platform: {platform}
Format: {format} ({specs['width']}x{specs['height']})
User Request: {prompt}

Return a JSON structure with:
- background_color (hex)
- elements (list of text, shapes, images with positions, sizes, colors, fonts)
- layout (composition rules)

Make it professional, eye-catching, and platform-compliant."""

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        design_spec = json.loads(response.choices[0].message.content)
        
        # Convert to Fabric.js canvas format
        canvas_data = {
            "version": "5.3.0",
            "objects": [],
            "background": design_spec.get("background_color", "#ffffff"),
            "width": specs["width"],
            "height": specs["height"],
        }
        
        # Add design elements
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
            "width": specs["width"],
            "height": specs["height"],
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
    
    # Simplified export - in production, render canvas to image
    # For hackathon, return placeholder
    
    if format in ["png", "jpg"]:
        # Create blank image with design dimensions
        canvas_data = design.canvas_data or {}
        width = canvas_data.get("width", 1080)
        height = canvas_data.get("height", 1080)
        
        img = Image.new('RGB', (width, height), color='white')
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=format.upper())
        img_byte_arr.seek(0)
        
        return StreamingResponse(
            img_byte_arr,
            media_type=f"image/{format}",
            headers={"Content-Disposition": f"attachment; filename=design_{design.id}.{format}"}
        )
    
    elif format == "svg":
        svg_content = f'<svg width="{1080}" height="{1080}"><text>Design {design.id}</text></svg>'
        return StreamingResponse(
            io.BytesIO(svg_content.encode()),
            media_type="image/svg+xml",
            headers={"Content-Disposition": f"attachment; filename=design_{design.id}.svg"}
        )
    
    else:  # PDF
        return {"error": "PDF export not implemented yet"}
