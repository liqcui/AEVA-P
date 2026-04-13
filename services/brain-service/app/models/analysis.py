"""
Analysis Database Models

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Integer, Float, JSON, Text
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class AnalysisType(str, enum.Enum):
    """Analysis type enumeration"""
    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    COMPARATIVE = "comparative"
    PREDICTIVE = "predictive"
    DIAGNOSTIC = "diagnostic"


class AnalysisStatus(str, enum.Enum):
    """Analysis status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Analysis(Base):
    """Analysis model for AI-powered evaluations"""

    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    analysis_type = Column(SQLEnum(AnalysisType), nullable=False, index=True)
    status = Column(SQLEnum(AnalysisStatus), default=AnalysisStatus.PENDING, nullable=False, index=True)

    # Input data
    input_data = Column(JSON, nullable=False, default=dict)
    config = Column(JSON, nullable=False, default=dict)

    # LLM Configuration
    llm_provider = Column(String(50), nullable=True)
    llm_model = Column(String(100), nullable=True)
    prompt = Column(Text, nullable=True)

    # Results
    analysis_text = Column(Text, nullable=True)
    findings = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)

    # Execution tracking
    processing_time = Column(Float, nullable=True)  # seconds
    tokens_used = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)

    # Metadata
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
