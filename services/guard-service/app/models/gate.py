"""
Gate Models

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, UUID4
import uuid
import enum


class GateStatus(str, enum.Enum):
    """Gate status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Gate(BaseModel):
    """Quality gate model"""
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

    # Configuration
    threshold: float = Field(..., ge=0.0, le=1.0)
    metrics: List[str] = Field(default_factory=list)
    strict_mode: bool = False
    auto_block: bool = True

    # Status
    status: GateStatus = GateStatus.ACTIVE
    enabled: bool = True

    # Statistics
    total_validations: int = 0
    passed_validations: int = 0
    failed_validations: int = 0
    blocked_validations: int = 0

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "production_gate",
                "description": "Production deployment gate",
                "threshold": 0.85,
                "metrics": ["accuracy", "f1_score"],
                "strict_mode": False,
                "auto_block": True,
                "status": "active",
                "enabled": True,
                "total_validations": 156,
                "passed_validations": 142,
                "failed_validations": 11,
                "blocked_validations": 3
            }
        }


class ValidationResult(BaseModel):
    """Validation result model"""
    id: UUID4 = Field(default_factory=uuid.uuid4)
    gate_id: UUID4

    # Result
    passed: bool
    score: float = Field(..., ge=0.0, le=1.0)
    threshold: float
    blocked: bool = False
    reason: Optional[str] = None

    # Metrics
    metrics: Dict[str, float] = Field(default_factory=dict)

    # Timestamp
    validated_at: datetime = Field(default_factory=datetime.utcnow)

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440001",
                "gate_id": "550e8400-e29b-41d4-a716-446655440000",
                "passed": True,
                "score": 0.93,
                "threshold": 0.85,
                "blocked": False,
                "reason": None,
                "metrics": {
                    "accuracy": 0.95,
                    "f1_score": 0.91
                },
                "validated_at": "2026-04-13T10:00:00Z"
            }
        }
