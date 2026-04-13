"""
Gate Pydantic Schemas

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, UUID4

from app.models.gate import GateStatus


# Request Schemas
class GateCreate(BaseModel):
    """Schema for creating a gate"""
    name: str = Field(..., min_length=1, max_length=255, description="Gate name")
    description: Optional[str] = Field(None, description="Gate description")
    threshold: float = Field(..., ge=0.0, le=1.0, description="Quality threshold (0-1)")
    metrics: List[str] = Field(..., min_length=1, description="Metrics to validate")
    strict_mode: bool = Field(False, description="Strict validation mode")
    auto_block: bool = Field(True, description="Auto block on failure")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "production_gate",
                "description": "Production deployment quality gate",
                "threshold": 0.85,
                "metrics": ["accuracy", "f1_score"],
                "strict_mode": False,
                "auto_block": True
            }
        }


class GateUpdate(BaseModel):
    """Schema for updating a gate"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    metrics: Optional[List[str]] = None
    strict_mode: Optional[bool] = None
    auto_block: Optional[bool] = None
    enabled: Optional[bool] = None
    status: Optional[GateStatus] = None


class ValidationRequest(BaseModel):
    """Schema for validation request"""
    metrics: Dict[str, float] = Field(..., description="Metrics to validate")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "metrics": {
                    "accuracy": 0.95,
                    "f1_score": 0.92,
                    "precision": 0.93
                },
                "metadata": {
                    "model": "RandomForest",
                    "dataset": "test_v2"
                }
            }
        }


# Response Schemas
class GateResponse(BaseModel):
    """Schema for gate response"""
    id: UUID4
    name: str
    description: Optional[str]
    threshold: float
    metrics: List[str]
    strict_mode: bool
    auto_block: bool
    status: GateStatus
    enabled: bool
    total_validations: int
    passed_validations: int
    failed_validations: int
    blocked_validations: int
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]

    class Config:
        from_attributes = True


class GateListResponse(BaseModel):
    """Schema for paginated gate list"""
    gates: List[GateResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "gates": [],
                "total": 5
            }
        }


class ValidationResponse(BaseModel):
    """Schema for validation response"""
    id: UUID4
    gate_id: UUID4
    passed: bool
    score: float
    threshold: float
    blocked: bool
    reason: Optional[str]
    metrics: Dict[str, float]
    validated_at: datetime
    metadata: Dict[str, Any]

    class Config:
        from_attributes = True
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
                "validated_at": "2026-04-13T10:00:00Z",
                "metadata": {}
            }
        }


class GateStatistics(BaseModel):
    """Schema for gate statistics"""
    gate_id: UUID4
    gate_name: str
    total_validations: int
    passed_validations: int
    failed_validations: int
    blocked_validations: int
    success_rate: float
    block_rate: float

    class Config:
        json_schema_extra = {
            "example": {
                "gate_id": "550e8400-e29b-41d4-a716-446655440000",
                "gate_name": "production_gate",
                "total_validations": 156,
                "passed_validations": 142,
                "failed_validations": 11,
                "blocked_validations": 3,
                "success_rate": 91.03,
                "block_rate": 1.92
            }
        }
