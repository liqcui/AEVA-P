"""
AEVA-Guard Manager
Manages quality gates and validation
"""

from typing import Dict, Any, List, Optional
import logging

from aeva.core.config import GuardConfig
from aeva.core.result import EvaluationResult, GateResult
from aeva.guard.gates import QualityGate

logger = logging.getLogger(__name__)


class GuardManager:
    """
    Manages quality gates and validation processes

    Responsibilities:
    - Apply quality gates to evaluation results
    - Validate against defined thresholds
    - Block deployments when quality standards not met
    - Track quality trends
    """

    def __init__(self, config: GuardConfig):
        self.config = config
        self.gates: List[QualityGate] = []
        self._initialize_default_gates()

    def _initialize_default_gates(self) -> None:
        """Initialize default quality gates"""
        from aeva.guard.gates import ThresholdGate

        # Default accuracy gate
        if self.config.enabled:
            default_gate = ThresholdGate(
                name="default_accuracy",
                threshold=self.config.default_threshold,
                metric_name="accuracy"
            )
            self.gates.append(default_gate)

    def add_gate(self, gate: QualityGate) -> None:
        """Add a quality gate"""
        self.gates.append(gate)
        logger.info(f"Added quality gate: {gate.name}")

    def validate(self, result: EvaluationResult) -> GateResult:
        """
        Validate evaluation result against quality gates

        Args:
            result: Evaluation result to validate

        Returns:
            GateResult indicating pass/fail and any blocks
        """
        logger.info(f"Validating result against {len(self.gates)} quality gates")

        overall_score = result.get_overall_score()
        passed = True
        blocked = False
        reasons = []

        # Apply each gate
        for gate in self.gates:
            gate_result = gate.evaluate(result)

            if not gate_result.passed:
                passed = False
                reasons.append(f"Gate '{gate.name}' failed: {gate_result.reason}")

                if self.config.strict_mode or gate.is_blocking:
                    blocked = True

        # Create gate result
        gate_result = GateResult(
            passed=passed,
            threshold=self.config.default_threshold,
            score=overall_score,
            blocked=blocked and self.config.auto_block,
            reason="; ".join(reasons) if reasons else None
        )

        if blocked:
            logger.warning(f"Quality gate BLOCKED: {gate_result.reason}")
        elif not passed:
            logger.warning(f"Quality gate FAILED: {gate_result.reason}")
        else:
            logger.info("Quality gate PASSED")

        return gate_result

    async def validate_async(self, result: EvaluationResult) -> GateResult:
        """
        Validate evaluation result asynchronously

        Args:
            result: Evaluation result to validate

        Returns:
            GateResult indicating pass/fail and any blocks
        """
        # For now, just call sync version
        # Can be enhanced with true async validation in the future
        return self.validate(result)

    def get_status(self) -> Dict[str, Any]:
        """Get guard manager status"""
        return {
            "enabled": self.config.enabled,
            "gates_count": len(self.gates),
            "strict_mode": self.config.strict_mode,
            "auto_block": self.config.auto_block,
            "default_threshold": self.config.default_threshold,
        }

    def remove_gate(self, gate_name: str) -> bool:
        """Remove a quality gate by name"""
        initial_count = len(self.gates)
        self.gates = [g for g in self.gates if g.name != gate_name]

        removed = len(self.gates) < initial_count
        if removed:
            logger.info(f"Removed quality gate: {gate_name}")
        return removed

    def clear_gates(self) -> None:
        """Remove all quality gates"""
        self.gates.clear()
        logger.info("Cleared all quality gates")

    def get_gate(self, gate_name: str) -> Optional[QualityGate]:
        """Get a quality gate by name"""
        for gate in self.gates:
            if gate.name == gate_name:
                return gate
        return None
