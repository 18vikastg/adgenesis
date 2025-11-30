from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, index=True)
    email = Column(String(255))
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    designs = relationship("Design", back_populates="user")
    guidelines = relationship("Guideline", back_populates="user")


class PlatformType(str, enum.Enum):
    META = "meta"
    GOOGLE = "google"
    LINKEDIN = "linkedin"


class FormatType(str, enum.Enum):
    SQUARE = "square"
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    STORY = "story"


class Design(Base):
    __tablename__ = "designs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prompt = Column(Text)
    platform = Column(Enum(PlatformType))
    format = Column(Enum(FormatType))
    canvas_data = Column(JSON)  # Fabric.js canvas JSON
    preview_url = Column(String(500))
    s3_key = Column(String(500))
    is_compliant = Column(Integer, default=0)  # 0: not checked, 1: compliant, -1: non-compliant
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="designs")
    exports = relationship("Export", back_populates="design")
    compliance_logs = relationship("ComplianceLog", back_populates="design")


class Guideline(Base):
    __tablename__ = "guidelines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255))
    file_url = Column(String(500))
    s3_key = Column(String(500))
    extracted_data = Column(JSON)  # Colors, fonts, logos, etc.
    colors = Column(JSON)
    fonts = Column(JSON)
    logo_urls = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="guidelines")


class ExportFormat(str, enum.Enum):
    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    PDF = "pdf"


class Export(Base):
    __tablename__ = "exports"

    id = Column(Integer, primary_key=True, index=True)
    design_id = Column(Integer, ForeignKey("designs.id"))
    format = Column(Enum(ExportFormat))
    file_url = Column(String(500))
    s3_key = Column(String(500))
    file_size = Column(Integer)  # in bytes
    created_at = Column(DateTime, default=datetime.utcnow)

    design = relationship("Design", back_populates="exports")


class ComplianceLog(Base):
    __tablename__ = "compliance_logs"

    id = Column(Integer, primary_key=True, index=True)
    design_id = Column(Integer, ForeignKey("designs.id"))
    platform = Column(Enum(PlatformType))
    is_compliant = Column(Integer)  # 1: compliant, 0: non-compliant
    issues = Column(JSON)  # List of compliance issues
    checked_at = Column(DateTime, default=datetime.utcnow)

    design = relationship("Design", back_populates="compliance_logs")
