"""
AEVA Guard Service Interface

API contract for AEVA-Guard microservice.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Protocol, List, Dict, Any
from pydantic import BaseModel
from ..models import EvaluationResult, GateResult


class GateConfig(BaseModel):
    """Quality gate configuration"""
    name: str
    threshold: float
    metrics: List[str]
    strict_mode: bool = False
    auto_block: bool = True


class GateStatus(BaseModel):
    """Quality gate status"""
    id: str
    name: str
    enabled: bool
    threshold: float
    total_validations: int
    passed_validations: int
    blocked_validations: int


class IGuardService(Protocol):
    """
    Guard Service Interface

    Defines the API contract for the AEVA-Guard microservice.
    """

    async def register_gate(self, config: GateConfig) -> str:
        """
        Register a new quality gate

        Args:
            config: Gate configuration

        Returns:
            gate_id: Unique identifier for the gate
        """
        ...

    async def validate(
        self,
        result: EvaluationResult,
        gate_id: str
    ) -> GateResult:
        """
        Validate evaluation result against quality gate

        Args:
            result: Evaluation result to validate
            gate_id: Quality gate identifier

        Returns:
            gate_result: Validation result
        """
        ...

    async def get_gate_status(self, gate_id: str) -> GateStatus:
        """
        Get quality gate status

        Args:
            gate_id: Unique identifier

        Returns:
            status: Gate statistics and metadata
        """
        ...

    async def get_history(
        self,
        gate_id: str,
        limit: int = 100
    ) -> List[GateResult]:
        """
        Get gate validation history

        Args:
            gate_id: Unique identifier
            limit: Maximum number of results

        Returns:
            history: List of gate results
        """
        ...

    async def update_gate(
        self,
        gate_id: str,
        config: GateConfig
    ) -> bool:
        """
        Update quality gate configuration

        Args:
            gate_id: Unique identifier
            config: New configuration

        Returns:
            success: True if updated successfully
        """
        ...

    async def delete_gate(self, gate_id: str) -> bool:
        """
        Delete a quality gate

        Args:
            gate_id: Unique identifier

        Returns:
            success: True if deleted successfully
        """
        ...
