"""
Benchmark Database Models

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.db.base import Base


class BenchmarkStatus(str, enum.Enum):
    """Benchmark execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Benchmark(Base):
    """Benchmark model"""
    __tablename__ = "benchmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Configuration
    model_path = Column(String(500), nullable=False)
    dataset_path = Column(String(500), nullable=True)
    config = Column(JSON, nullable=True, default={})

    # Status
    status = Column(SQLEnum(BenchmarkStatus), default=BenchmarkStatus.PENDING, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Results (stored as JSON for flexibility)
    results = Column(JSON, nullable=True)

    # Metrics
    accuracy = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)

    # Performance metrics
    duration = Column(Float, nullable=True)  # seconds
    throughput = Column(Float, nullable=True)  # samples/sec

    # Error tracking
    error_message = Column(Text, nullable=True)

    # Metadata
    metadata = Column(JSON, nullable=True, default={})

    def __repr__(self):
        return f"<Benchmark(id={self.id}, name='{self.name}', status='{self.status}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "model_path": self.model_path,
            "dataset_path": self.dataset_path,
            "config": self.config,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "results": self.results,
            "accuracy": self.accuracy,
            "f1_score": self.f1_score,
            "precision": self.precision,
            "recall": self.recall,
            "duration": self.duration,
            "throughput": self.throughput,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }
