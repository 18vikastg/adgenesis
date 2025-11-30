from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os

from app.schemas import (
    DesignCreateRequest,
    DesignResponse,
    GuidelineResponse,
    ComplianceCheckRequest,
    ComplianceCheckResponse,
    ExportFormat,
)
from app.models import Design, Guideline, User, Export
from app.utils import (
    get_db,
    get_demo_user,
    generate_ai_design,
    extract_guideline_data,
    check_platform_compliance,
    export_design_file,
)

# In-memory storage for demo (hackathon mode - no database needed)
in_memory_designs = []
in_memory_guidelines = []
design_id_counter = 1
guideline_id_counter = 1

router = APIRouter()


# Design Endpoints
@router.post("/designs/generate", response_model=DesignResponse)
async def generate_design(
    request: DesignCreateRequest
):
    """Generate a new ad design using AI"""
    global design_id_counter
    try:
        # Generate design using OpenAI
        canvas_data = await generate_ai_design(
            prompt=request.prompt,
            platform=request.platform.value,
            format=request.format.value
        )
        
        # Create design record in memory
        from datetime import datetime
        design_dict = {
            "id": design_id_counter,
            "prompt": request.prompt,
            "platform": request.platform.value,
            "format": request.format.value,
            "canvas_data": canvas_data,
            "preview_url": None,
            "is_compliant": 0,
            "created_at": datetime.utcnow()
        }
        in_memory_designs.append(design_dict)
        design_id_counter += 1
        
        return design_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/designs", response_model=List[DesignResponse])
async def get_designs():
    """Get all designs for demo user"""
    return list(reversed(in_memory_designs))  # Most recent first


@router.get("/designs/{design_id}", response_model=DesignResponse)
async def get_design(design_id: int):
    """Get a specific design"""
    design = next((d for d in in_memory_designs if d["id"] == design_id), None)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return design


@router.get("/designs/{design_id}/export")
async def export_design(
    design_id: int,
    format: ExportFormat
):
    """Export design in specified format"""
    design = next((d for d in in_memory_designs if d["id"] == design_id), None)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    
    try:
        # Create a mock design object for export
        class MockDesign:
            def __init__(self, data):
                self.id = data["id"]
                self.canvas_data = data["canvas_data"]
        
        file_data = export_design_file(MockDesign(design), format.value)
        return file_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Guideline Endpoints
@router.post("/guidelines/upload", response_model=GuidelineResponse)
async def upload_guideline(
    file: UploadFile = File(...)
):
    """Upload and process brand guidelines"""
    global guideline_id_counter
    try:
        # Save file temporarily
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Extract guideline data (colors, fonts, etc.)
        extracted_data = await extract_guideline_data(file_path)
        
        # Create guideline record in memory
        from datetime import datetime
        guideline_dict = {
            "id": guideline_id_counter,
            "name": file.filename,
            "file_url": None,
            "colors": extracted_data.get("colors", []),
            "fonts": extracted_data.get("fonts", []),
            "logo_urls": extracted_data.get("logos", []),
            "created_at": datetime.utcnow()
        }
        in_memory_guidelines.append(guideline_dict)
        guideline_id_counter += 1
        
        # Clean up temp file
        os.remove(file_path)
        
        return guideline_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/guidelines", response_model=List[GuidelineResponse])
async def get_guidelines():
    """Get all guidelines for demo user"""
    return list(reversed(in_memory_guidelines))  # Most recent first


@router.get("/guidelines/{guideline_id}", response_model=GuidelineResponse)
async def get_guideline(guideline_id: int):
    """Get a specific guideline"""
    guideline = next((g for g in in_memory_guidelines if g["id"] == guideline_id), None)
    if not guideline:
        raise HTTPException(status_code=404, detail="Guideline not found")
    return guideline


# Compliance Endpoints
@router.post("/compliance/check", response_model=ComplianceCheckResponse)
async def check_compliance(
    request: ComplianceCheckRequest
):
    """Check design compliance for a specific platform"""
    design = next((d for d in in_memory_designs if d["id"] == request.design_id), None)
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    
    try:
        # Create a mock design object for compliance check
        class MockDesign:
            def __init__(self, data):
                self.id = data["id"]
                self.canvas_data = data["canvas_data"]
                self.format = type('obj', (object,), {'value': data["format"]})
        
        compliance_result = await check_platform_compliance(
            design=MockDesign(design),
            platform=request.platform.value
        )
        return compliance_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
