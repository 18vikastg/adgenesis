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


class ElementType(str, Enum):
    IMAGE = "image"
    TEXT = "text"
    SHAPE = "shape"
    CTA_BUTTON = "cta_button"


class DesignElement(BaseModel):
    id: str
    type: ElementType
    x: float
    y: float
    width: float
    height: float
    rotation: float = 0
    # Image-specific
    src: Optional[str] = None
    crop: Optional[Dict[str, float]] = None
    # Text-specific
    content: Optional[str] = None
    fontFamily: Optional[str] = None
    fontSize: Optional[float] = None
    fontWeight: Optional[str] = None
    fill: Optional[str] = None
    textAlign: Optional[str] = None
    editable: bool = True
    # Shape-specific
    shape: Optional[str] = None  # rectangle, circle, etc.


class CTAConfig(BaseModel):
    text: str
    style: str = "primary"  # primary, secondary
    color: str = "#0066FF"
    ctaLink: Optional[str] = None


class LayoutConfig(BaseModel):
    grid: Optional[str] = None
    artifact_positions: List[Dict[str, Any]] = []


class DesignMetadata(BaseModel):
    createdAt: datetime
    updatedAt: datetime
    version: int = 1


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
