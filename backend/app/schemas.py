from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class PlatformType(str, Enum):
    META = "meta"
    GOOGLE = "google"
    LINKEDIN = "linkedin"


class FormatType(str, Enum):
    SQUARE = "square"
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    STORY = "story"


class ExportFormat(str, Enum):
    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    PDF = "pdf"


# Design Schemas
class DesignCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)
    platform: PlatformType
    format: FormatType
    guideline_id: Optional[int] = None


class DesignResponse(BaseModel):
    id: int
    prompt: str
    platform: str
    format: str
    canvas_data: Optional[Dict[str, Any]] = None
    preview_url: Optional[str] = None
    is_compliant: int
    created_at: datetime

    class Config:
        from_attributes = True


# Guideline Schemas
class GuidelineResponse(BaseModel):
    id: int
    name: str
    file_url: Optional[str] = None
    colors: Optional[List[str]] = None
    fonts: Optional[List[str]] = None
    logo_urls: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Export Schemas
class ExportRequest(BaseModel):
    design_id: int
    format: ExportFormat


class ExportResponse(BaseModel):
    id: int
    design_id: int
    format: str
    file_url: str
    file_size: int
    created_at: datetime

    class Config:
        from_attributes = True


# Compliance Schemas
class ComplianceCheckRequest(BaseModel):
    design_id: int
    platform: PlatformType


class ComplianceIssue(BaseModel):
    type: str
    message: str
    severity: str  # "error", "warning"


class ComplianceCheckResponse(BaseModel):
    design_id: int
    platform: str
    is_compliant: bool
    issues: List[ComplianceIssue]
    checked_at: datetime
