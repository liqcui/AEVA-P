"""
AEVA Brain Service Client

HTTP client for AEVA-Brain microservice.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import List
from .base import BaseServiceClient
from ..models import EvaluationResult, Analysis
from ..interfaces import AnalysisRequest


class BrainClient(BaseServiceClient):
    """Client for AEVA-Brain service"""

    async def analyze(self, request: AnalysisRequest) -> Analysis:
        """Perform intelligent analysis"""
        response = await self.post(
            "/analyze",
            json={
                "result": request.result.to_dict(),
                "analysis_type": request.analysis_type,
                "context": request.context
            }
        )
        return Analysis.from_dict(response["analysis"])

    async def analyze_root_cause(
        self,
        result: EvaluationResult
    ) -> Analysis:
        """Analyze root causes of failures"""
        response = await self.post(
            "/analyze/root-cause",
            json=result.to_dict()
        )
        return Analysis.from_dict(response["analysis"])

    async def get_suggestions(
        self,
        result: EvaluationResult
    ) -> Analysis:
        """Get improvement suggestions"""
        response = await self.post(
            "/analyze/suggestions",
            json=result.to_dict()
        )
        return Analysis.from_dict(response["analysis"])

    async def batch_analyze(
        self,
        results: List[EvaluationResult]
    ) -> List[Analysis]:
        """Analyze multiple results in batch"""
        response = await self.post(
            "/analyze/batch",
            json={
                "results": [r.to_dict() for r in results]
            }
        )
        return [
            Analysis.from_dict(a)
            for a in response["analyses"]
        ]
