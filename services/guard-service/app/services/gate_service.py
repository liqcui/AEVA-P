"""
Gate Service Layer

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
import uuid

from app.models.gate import Gate, GateStatus, ValidationResult
from app.schemas.gate import GateCreate, GateUpdate, ValidationRequest
from app.core.redis_client import RedisClient
from app.core.config import settings


class GateService:
    """Service for gate operations"""

    GATE_PREFIX = "gate:"
    HISTORY_PREFIX = "history:"
    GATES_LIST_KEY = "gates:all"

    @staticmethod
    async def create_gate(redis: RedisClient, gate_create: GateCreate) -> Gate:
        """Create a new gate"""
        gate = Gate(
            name=gate_create.name,
            description=gate_create.description,
            threshold=gate_create.threshold,
            metrics=gate_create.metrics,
            strict_mode=gate_create.strict_mode,
            auto_block=gate_create.auto_block,
        )

        # Store gate in Redis
        gate_key = f"{GateService.GATE_PREFIX}{gate.id}"
        await redis.set(gate_key, gate.model_dump())

        # Add to gates list
        gate_ids = await redis.get(GateService.GATES_LIST_KEY) or []
        gate_ids.append(str(gate.id))
        await redis.set(GateService.GATES_LIST_KEY, gate_ids)

        return gate

    @staticmethod
    async def get_gate(redis: RedisClient, gate_id: UUID) -> Optional[Gate]:
        """Get a gate by ID"""
        gate_key = f"{GateService.GATE_PREFIX}{gate_id}"
        gate_data = await redis.get(gate_key)

        if not gate_data:
            return None

        return Gate(**gate_data)

    @staticmethod
    async def list_gates(redis: RedisClient) -> List[Gate]:
        """List all gates"""
        gate_ids = await redis.get(GateService.GATES_LIST_KEY) or []

        gates = []
        for gate_id in gate_ids:
            gate = await GateService.get_gate(redis, UUID(gate_id))
            if gate:
                gates.append(gate)

        return gates

    @staticmethod
    async def update_gate(
        redis: RedisClient,
        gate_id: UUID,
        gate_update: GateUpdate
    ) -> Optional[Gate]:
        """Update a gate"""
        gate = await GateService.get_gate(redis, gate_id)
        if not gate:
            return None

        # Update fields
        update_data = gate_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(gate, field, value)

        gate.updated_at = datetime.utcnow()

        # Save updated gate
        gate_key = f"{GateService.GATE_PREFIX}{gate_id}"
        await redis.set(gate_key, gate.model_dump())

        return gate

    @staticmethod
    async def delete_gate(redis: RedisClient, gate_id: UUID) -> bool:
        """Delete a gate"""
        gate_key = f"{GateService.GATE_PREFIX}{gate_id}"

        if not await redis.exists(gate_key):
            return False

        # Delete gate
        await redis.delete(gate_key)

        # Remove from gates list
        gate_ids = await redis.get(GateService.GATES_LIST_KEY) or []
        gate_ids = [gid for gid in gate_ids if gid != str(gate_id)]
        await redis.set(GateService.GATES_LIST_KEY, gate_ids)

        # Delete history
        history_key = f"{GateService.HISTORY_PREFIX}{gate_id}"
        await redis.delete(history_key)

        return True

    @staticmethod
    async def validate(
        redis: RedisClient,
        gate_id: UUID,
        validation_request: ValidationRequest
    ) -> Optional[ValidationResult]:
        """Validate metrics against a gate"""
        gate = await GateService.get_gate(redis, gate_id)
        if not gate or not gate.enabled:
            return None

        # Calculate score (average of requested metrics that match gate metrics)
        scores = []
        for metric_name in gate.metrics:
            if metric_name in validation_request.metrics:
                scores.append(validation_request.metrics[metric_name])

        if not scores:
            # No matching metrics
            score = 0.0
            passed = False
            reason = f"No matching metrics found. Expected: {', '.join(gate.metrics)}"
        else:
            # Calculate average score
            score = sum(scores) / len(scores)

            # Check threshold
            if gate.strict_mode:
                # In strict mode, ALL metrics must pass
                passed = all(
                    validation_request.metrics.get(m, 0.0) >= gate.threshold
                    for m in gate.metrics
                    if m in validation_request.metrics
                )
            else:
                # In normal mode, average score must pass
                passed = score >= gate.threshold

            reason = None if passed else f"Score {score:.4f} below threshold {gate.threshold}"

        # Determine if blocked
        blocked = (not passed) and gate.auto_block

        # Create validation result
        result = ValidationResult(
            gate_id=gate_id,
            passed=passed,
            score=score,
            threshold=gate.threshold,
            blocked=blocked,
            reason=reason,
            metrics=validation_request.metrics,
            metadata=validation_request.metadata,
        )

        # Update gate statistics
        gate.total_validations += 1
        if passed:
            gate.passed_validations += 1
        else:
            gate.failed_validations += 1
        if blocked:
            gate.blocked_validations += 1

        gate.updated_at = datetime.utcnow()

        # Save updated gate
        gate_key = f"{GateService.GATE_PREFIX}{gate_id}"
        await redis.set(gate_key, gate.model_dump())

        # Save to history
        history_key = f"{GateService.HISTORY_PREFIX}{gate_id}"
        await redis.lpush(history_key, result.model_dump())

        # Trim history to max size
        await redis.ltrim(history_key, 0, settings.MAX_HISTORY_SIZE - 1)

        return result

    @staticmethod
    async def get_history(
        redis: RedisClient,
        gate_id: UUID,
        limit: int = 100
    ) -> List[ValidationResult]:
        """Get validation history for a gate"""
        history_key = f"{GateService.HISTORY_PREFIX}{gate_id}"
        history_data = await redis.lrange(history_key, 0, limit - 1)

        return [ValidationResult(**data) for data in history_data]

    @staticmethod
    async def get_statistics(redis: RedisClient, gate_id: UUID) -> Optional[Dict[str, Any]]:
        """Get gate statistics"""
        gate = await GateService.get_gate(redis, gate_id)
        if not gate:
            return None

        success_rate = (
            (gate.passed_validations / gate.total_validations * 100)
            if gate.total_validations > 0 else 0.0
        )

        block_rate = (
            (gate.blocked_validations / gate.total_validations * 100)
            if gate.total_validations > 0 else 0.0
        )

        return {
            "gate_id": str(gate.id),
            "gate_name": gate.name,
            "total_validations": gate.total_validations,
            "passed_validations": gate.passed_validations,
            "failed_validations": gate.failed_validations,
            "blocked_validations": gate.blocked_validations,
            "success_rate": round(success_rate, 2),
            "block_rate": round(block_rate, 2),
        }
