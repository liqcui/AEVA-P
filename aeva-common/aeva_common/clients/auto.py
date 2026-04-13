"""
AEVA Auto Pipeline Service Client

HTTP client for AEVA-Auto microservice.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any
from .base import BaseServiceClient
from ..models import EvaluationResult
from ..interfaces import PipelineConfig, PipelineStatus


class AutoClient(BaseServiceClient):
    """Client for AEVA-Auto service"""

    async def create_pipeline(self, config: PipelineConfig) -> str:
        """Create a new pipeline"""
        response = await self.post(
            "/pipeline/create",
            json=config.model_dump()
        )
        return response["pipeline_id"]

    async def execute_pipeline(
        self,
        pipeline_id: str,
        params: Dict[str, Any] = {}
    ) -> str:
        """Execute a pipeline"""
        response = await self.post(
            f"/pipeline/{pipeline_id}/execute",
            json={"params": params}
        )
        return response["execution_id"]

    async def get_status(self, execution_id: str) -> PipelineStatus:
        """Get pipeline execution status"""
        response = await self.get(f"/pipeline/execution/{execution_id}/status")
        return PipelineStatus(**response["status"])

    async def get_results(self, execution_id: str) -> EvaluationResult:
        """Get pipeline execution results"""
        response = await self.get(f"/pipeline/execution/{execution_id}/results")
        return EvaluationResult.from_dict(response["result"])

    async def schedule_pipeline(
        self,
        pipeline_id: str,
        cron_expr: str
    ) -> bool:
        """Schedule pipeline for periodic execution"""
        response = await self.post(
            f"/pipeline/{pipeline_id}/schedule",
            json={"cron": cron_expr}
        )
        return response["success"]

    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a running pipeline execution"""
        response = await self.post(
            f"/pipeline/execution/{execution_id}/cancel"
        )
        return response["success"]
