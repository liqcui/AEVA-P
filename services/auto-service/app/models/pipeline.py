"""
Pipeline Database Models

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Integer, Float, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class PipelineStatus(str, enum.Enum):
    """Pipeline execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class StepStatus(str, enum.Enum):
    """Pipeline step status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


class Pipeline(Base):
    """Pipeline model for orchestrating evaluation workflows"""

    __tablename__ = "pipelines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(PipelineStatus), default=PipelineStatus.PENDING, nullable=False, index=True)

    # Configuration
    config = Column(JSON, nullable=False, default=dict)

    # Execution tracking
    celery_task_id = Column(String(255), nullable=True, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)  # seconds

    # Error tracking
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)

    # Results
    results = Column(JSON, nullable=True)

    # Metadata
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    steps = relationship("PipelineStep", back_populates="pipeline", cascade="all, delete-orphan")


class PipelineStep(Base):
    """Pipeline step model for tracking individual step execution"""

    __tablename__ = "pipeline_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    pipeline_id = Column(UUID(as_uuid=True), ForeignKey("pipelines.id"), nullable=False, index=True)

    # Step information
    name = Column(String(255), nullable=False)
    step_type = Column(String(50), nullable=False)  # benchmark, validate, analyze
    order = Column(Integer, nullable=False)
    status = Column(SQLEnum(StepStatus), default=StepStatus.PENDING, nullable=False)

    # Execution tracking
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)  # seconds

    # Configuration and results
    config = Column(JSON, nullable=False, default=dict)
    results = Column(JSON, nullable=True)

    # Error tracking
    error_message = Column(Text, nullable=True)

    # Service integration
    service_url = Column(String(255), nullable=True)
    service_request_id = Column(String(255), nullable=True)

    # Metadata
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    pipeline = relationship("Pipeline", back_populates="steps")
