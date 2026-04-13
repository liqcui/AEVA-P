"""
AEVA Brain Service Interface

API contract for AEVA-Brain microservice.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Protocol, Optional, Dict, Any
from pydantic import BaseModel
from ..models import EvaluationResult, Analysis


class AnalysisRequest(BaseModel):
    """Request for intelligent analysis"""
    result: Dict[str, Any]  # EvaluationResult as dict
    analysis_type: str = "full"  # full, root_cause, suggestions
    context: Optional[str] = None

    model_config = {"arbitrary_types_allowed": True}


class IBrainService(Protocol):
    """
    Brain Service Interface

    Defines the API contract for the AEVA-Brain microservice.
    """

    async def analyze(self, request: AnalysisRequest) -> Analysis:
        """
        Perform intelligent analysis on evaluation result

        Args:
            request: Analysis request with result and context

        Returns:
            analysis: AI-generated analysis with insights
        """
        ...

    async def analyze_root_cause(
        self,
        result: EvaluationResult
    ) -> Analysis:
        """
        Analyze root causes of failures

        Args:
            result: Evaluation result with failures

        Returns:
            analysis: Root cause analysis
        """
        ...

    async def get_suggestions(
        self,
        result: EvaluationResult
    ) -> Analysis:
        """
        Get improvement suggestions

        Args:
            result: Evaluation result

        Returns:
            analysis: Suggestions for improvement
        """
        ...

    async def batch_analyze(
        self,
        results: list[EvaluationResult]
    ) -> list[Analysis]:
        """
        Analyze multiple results in batch

        Args:
            results: List of evaluation results

        Returns:
            analyses: List of analyses
        """
        ...
