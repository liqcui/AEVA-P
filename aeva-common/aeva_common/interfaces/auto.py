"""
AEVA Auto Pipeline Service Interface

API contract for AEVA-Auto microservice.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Protocol, List, Dict, Any, Optional
from pydantic import BaseModel
from ..models import EvaluationResult


class PipelineConfig(BaseModel):
    """Pipeline configuration"""
    name: str
    stages: List[Dict[str, Any]]
    schedule: Optional[str] = None  # cron expression
    enabled: bool = True


class PipelineStatus(BaseModel):
    """Pipeline execution status"""
    id: str
    pipeline_name: str
    status: str  # pending, running, completed, failed
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    current_stage: Optional[str] = None
    progress: float = 0.0


class IAutoService(Protocol):
    """
    Auto Pipeline Service Interface

    Defines the API contract for the AEVA-Auto microservice.
    """

    async def create_pipeline(self, config: PipelineConfig) -> str:
        """
        Create a new pipeline

        Args:
            config: Pipeline configuration

        Returns:
            pipeline_id: Unique identifier for the pipeline
        """
        ...

    async def execute_pipeline(
        self,
        pipeline_id: str,
        params: Dict[str, Any] = {}
    ) -> str:
        """
        Execute a pipeline

        Args:
            pipeline_id: Unique identifier
            params: Execution parameters

        Returns:
            execution_id: Unique execution identifier
        """
        ...

    async def get_status(self, execution_id: str) -> PipelineStatus:
        """
        Get pipeline execution status

        Args:
            execution_id: Unique execution identifier

        Returns:
            status: Current execution status
        """
        ...

    async def get_results(self, execution_id: str) -> EvaluationResult:
        """
        Get pipeline execution results

        Args:
            execution_id: Unique execution identifier

        Returns:
            result: Evaluation result
        """
        ...

    async def schedule_pipeline(
        self,
        pipeline_id: str,
        cron_expr: str
    ) -> bool:
        """
        Schedule pipeline for periodic execution

        Args:
            pipeline_id: Unique identifier
            cron_expr: Cron expression for schedule

        Returns:
            success: True if scheduled successfully
        """
        ...

    async def cancel_execution(self, execution_id: str) -> bool:
        """
        Cancel a running pipeline execution

        Args:
            execution_id: Unique execution identifier

        Returns:
            success: True if cancelled successfully
        """
        ...
