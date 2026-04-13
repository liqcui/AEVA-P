"""
Pipeline Pydantic Schemas

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, UUID4

from app.models.pipeline import PipelineStatus, StepStatus


# Request Schemas
class PipelineCreate(BaseModel):
    """Schema for creating a pipeline"""
    name: str = Field(..., min_length=1, max_length=255, description="Pipeline name")
    description: Optional[str] = Field(None, description="Pipeline description")
    config: Dict[str, Any] = Field(..., description="Pipeline configuration")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "ml_evaluation_pipeline",
                "description": "Complete ML model evaluation pipeline",
                "config": {
                    "steps": [
                        {
                            "name": "run_benchmark",
                            "type": "benchmark",
                            "config": {
                                "benchmark_id": "bench-123"
                            }
                        },
                        {
                            "name": "validate_quality",
                            "type": "validate",
                            "config": {
                                "gate_id": "gate-456"
                            }
                        },
                        {
                            "name": "ai_analysis",
                            "type": "analyze",
                            "config": {
                                "analysis_type": "comprehensive"
                            }
                        }
                    ]
                }
            }
        }


class PipelineUpdate(BaseModel):
    """Schema for updating a pipeline"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    status: Optional[PipelineStatus] = None


class PipelineExecutionRequest(BaseModel):
    """Schema for executing a pipeline"""
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Execution metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "metadata": {
                    "triggered_by": "user",
                    "environment": "production"
                }
            }
        }


# Response Schemas
class PipelineStepResponse(BaseModel):
    """Schema for pipeline step response"""
    id: UUID4
    pipeline_id: UUID4
    name: str
    step_type: str
    order: int
    status: StepStatus
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration: Optional[float]
    config: Dict[str, Any]
    results: Optional[Dict[str, Any]]
    error_message: Optional[str]
    service_url: Optional[str]
    service_request_id: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PipelineResponse(BaseModel):
    """Schema for pipeline response"""
    id: UUID4
    name: str
    description: Optional[str]
    status: PipelineStatus
    config: Dict[str, Any]
    celery_task_id: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration: Optional[float]
    error_message: Optional[str]
    retry_count: int
    results: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    steps: List[PipelineStepResponse] = []

    class Config:
        from_attributes = True


class PipelineListResponse(BaseModel):
    """Schema for paginated pipeline list"""
    pipelines: List[PipelineResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "pipelines": [],
                "total": 10
            }
        }


class PipelineExecutionResponse(BaseModel):
    """Schema for pipeline execution response"""
    pipeline_id: UUID4
    celery_task_id: str
    status: PipelineStatus
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "pipeline_id": "550e8400-e29b-41d4-a716-446655440000",
                "celery_task_id": "a3d8c9e1-4b2a-4c5d-8e9f-1a2b3c4d5e6f",
                "status": "running",
                "message": "Pipeline execution started"
            }
        }
