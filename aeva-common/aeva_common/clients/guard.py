"""
AEVA Guard Service Client

HTTP client for AEVA-Guard microservice.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import List
from .base import BaseServiceClient
from ..models import EvaluationResult, GateResult
from ..interfaces import GateConfig, GateStatus


class GuardClient(BaseServiceClient):
    """Client for AEVA-Guard service"""

    async def register_gate(self, config: GateConfig) -> str:
        """Register a new quality gate"""
        response = await self.post(
            "/gate/register",
            json=config.model_dump()
        )
        return response["gate_id"]

    async def validate(
        self,
        result: EvaluationResult,
        gate_id: str
    ) -> GateResult:
        """Validate result against quality gate"""
        response = await self.post(
            f"/gate/{gate_id}/validate",
            json=result.to_dict()
        )
        return GateResult.from_dict(response["gate_result"])

    async def get_gate_status(self, gate_id: str) -> GateStatus:
        """Get quality gate status"""
        response = await self.get(f"/gate/{gate_id}/status")
        return GateStatus(**response["status"])

    async def get_history(
        self,
        gate_id: str,
        limit: int = 100
    ) -> List[GateResult]:
        """Get gate validation history"""
        response = await self.get(
            f"/gate/{gate_id}/history",
            params={"limit": limit}
        )
        return [
            GateResult.from_dict(r)
            for r in response["history"]
        ]

    async def update_gate(
        self,
        gate_id: str,
        config: GateConfig
    ) -> bool:
        """Update quality gate configuration"""
        response = await self.put(
            f"/gate/{gate_id}",
            json=config.model_dump()
        )
        return response["success"]

    async def delete_gate(self, gate_id: str) -> bool:
        """Delete a quality gate"""
        response = await self.delete(f"/gate/{gate_id}")
        return response["success"]
