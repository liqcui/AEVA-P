"""
Analysis Pydantic Schemas

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, UUID4

from app.models.analysis import AnalysisType, AnalysisStatus


# Request Schemas
class AnalysisCreate(BaseModel):
    """Schema for creating an analysis"""
    analysis_type: AnalysisType = Field(..., description="Type of analysis to perform")
    input_data: Dict[str, Any] = Field(..., description="Input data for analysis")
    config: Dict[str, Any] = Field(default_factory=dict, description="Analysis configuration")

    class Config:
        json_schema_extra = {
            "example": {
                "analysis_type": "comprehensive",
                "input_data": {
                    "benchmark": {
                        "accuracy": 0.92,
                        "f1_score": 0.88
                    },
                    "validation": {
                        "passed": True,
                        "score": 0.90
                    }
                },
                "config": {
                    "focus_areas": ["performance", "quality"],
                    "include_recommendations": True
                }
            }
        }


class QuickAnalysisRequest(BaseModel):
    """Schema for quick analysis without persistence"""
    analysis_type: AnalysisType = Field(default=AnalysisType.BASIC, description="Type of analysis")
    data: Dict[str, Any] = Field(..., description="Data to analyze")
    config: Dict[str, Any] = Field(default_factory=dict, description="Configuration")

    class Config:
        json_schema_extra = {
            "example": {
                "analysis_type": "basic",
                "data": {
                    "metrics": {
                        "accuracy": 0.95,
                        "precision": 0.93,
                        "recall": 0.92
                    }
                },
                "config": {
                    "include_recommendations": True
                }
            }
        }


# Response Schemas
class AnalysisResponse(BaseModel):
    """Schema for analysis response"""
    id: UUID4
    analysis_type: AnalysisType
    status: AnalysisStatus
    input_data: Dict[str, Any]
    config: Dict[str, Any]
    llm_provider: Optional[str]
    llm_model: Optional[str]
    prompt: Optional[str]
    analysis_text: Optional[str]
    findings: Optional[List[str]]
    recommendations: Optional[List[str]]
    confidence_score: Optional[float]
    processing_time: Optional[float]
    tokens_used: Optional[int]
    error_message: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalysisListResponse(BaseModel):
    """Schema for paginated analysis list"""
    analyses: List[AnalysisResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "analyses": [],
                "total": 15
            }
        }


class QuickAnalysisResponse(BaseModel):
    """Schema for quick analysis response"""
    analysis_type: AnalysisType
    summary: str
    findings: List[str]
    recommendations: List[str]
    confidence_score: float
    processing_time: float

    class Config:
        json_schema_extra = {
            "example": {
                "analysis_type": "basic",
                "summary": "Model performance is good with high accuracy and balanced precision-recall.",
                "findings": [
                    "Accuracy of 0.95 exceeds typical benchmarks",
                    "Precision and recall are well-balanced",
                    "No significant performance issues detected"
                ],
                "recommendations": [
                    "Monitor performance on edge cases",
                    "Consider A/B testing in production",
                    "Implement gradual rollout strategy"
                ],
                "confidence_score": 0.88,
                "processing_time": 1.23
            }
        }
