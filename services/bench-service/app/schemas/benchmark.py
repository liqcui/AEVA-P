"""
Benchmark Pydantic Schemas

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, UUID4

from app.models.benchmark import BenchmarkStatus


# Request Schemas
class BenchmarkCreate(BaseModel):
    """Schema for creating a benchmark"""
    name: str = Field(..., min_length=1, max_length=255, description="Benchmark name")
    description: Optional[str] = Field(None, description="Benchmark description")
    model_path: str = Field(..., min_length=1, description="Path to model file")
    dataset_path: Optional[str] = Field(None, description="Path to dataset file")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Benchmark configuration")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "RandomForest Accuracy Test",
                "description": "Benchmark for RandomForest model accuracy",
                "model_path": "/models/random_forest.pkl",
                "dataset_path": "/data/test_set.csv",
                "config": {
                    "metrics": ["accuracy", "f1_score"],
                    "test_size": 0.2
                }
            }
        }


class BenchmarkUpdate(BaseModel):
    """Schema for updating a benchmark"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[BenchmarkStatus] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Benchmark Name",
                "description": "Updated description"
            }
        }


# Response Schemas
class BenchmarkResponse(BaseModel):
    """Schema for benchmark response"""
    id: UUID4
    name: str
    description: Optional[str]
    model_path: str
    dataset_path: Optional[str]
    config: Optional[Dict[str, Any]]
    status: BenchmarkStatus
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    results: Optional[Dict[str, Any]]
    accuracy: Optional[float]
    f1_score: Optional[float]
    precision: Optional[float]
    recall: Optional[float]
    duration: Optional[float]
    throughput: Optional[float]
    error_message: Optional[str]
    metadata: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "RandomForest Accuracy Test",
                "description": "Benchmark for RandomForest model",
                "model_path": "/models/random_forest.pkl",
                "dataset_path": "/data/test_set.csv",
                "config": {"metrics": ["accuracy", "f1_score"]},
                "status": "completed",
                "created_at": "2026-04-13T10:00:00",
                "updated_at": "2026-04-13T10:05:00",
                "started_at": "2026-04-13T10:00:30",
                "completed_at": "2026-04-13T10:05:00",
                "results": {"predictions": 1000, "correct": 950},
                "accuracy": 0.95,
                "f1_score": 0.94,
                "precision": 0.93,
                "recall": 0.95,
                "duration": 270.5,
                "throughput": 3.7,
                "error_message": None,
                "metadata": {}
            }
        }


class BenchmarkListResponse(BaseModel):
    """Schema for paginated benchmark list"""
    benchmarks: list[BenchmarkResponse]
    total: int
    page: int
    page_size: int
    pages: int

    class Config:
        json_schema_extra = {
            "example": {
                "benchmarks": [],
                "total": 42,
                "page": 1,
                "page_size": 50,
                "pages": 1
            }
        }


class BenchmarkExecutionResponse(BaseModel):
    """Schema for benchmark execution response"""
    benchmark_id: UUID4
    status: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "benchmark_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "running",
                "message": "Benchmark execution started"
            }
        }
