"""
AEVA-Guard Quality Gates
Different types of quality gates for validation
"""

from typing import Optional, Callable, Dict, Any
from abc import ABC, abstractmethod

from aeva.core.result import EvaluationResult, GateResult


class QualityGate(ABC):
    """Abstract base class for quality gates"""

    def __init__(self, name: str, is_blocking: bool = False):
        self.name = name
        self.is_blocking = is_blocking

    @abstractmethod
    def evaluate(self, result: EvaluationResult) -> GateResult:
        """
        Evaluate the result against this gate

        Args:
            result: Evaluation result to check

        Returns:
            GateResult with pass/fail status
        """
        pass


class ThresholdGate(QualityGate):
    """
    Gate that checks if a metric exceeds a threshold
    """

    def __init__(
        self,
        name: str,
        threshold: float,
        metric_name: str,
        is_blocking: bool = True
    ):
        super().__init__(name, is_blocking)
        self.threshold = threshold
        self.metric_name = metric_name

    def evaluate(self, result: EvaluationResult) -> GateResult:
        """Evaluate threshold gate"""
        # Check if metric exists
        if self.metric_name not in result.metrics:
            return GateResult(
                passed=False,
                threshold=self.threshold,
                score=0.0,
                blocked=self.is_blocking,
                reason=f"Metric '{self.metric_name}' not found"
            )

        metric = result.metrics[self.metric_name]
        passed = metric.value >= self.threshold

        return GateResult(
            passed=passed,
            threshold=self.threshold,
            score=metric.value,
            blocked=self.is_blocking and not passed,
            reason=None if passed else f"{self.metric_name} ({metric.value:.4f}) below threshold ({self.threshold})"
        )


class MultiMetricGate(QualityGate):
    """
    Gate that checks multiple metrics
    All metrics must pass for gate to pass
    """

    def __init__(
        self,
        name: str,
        metric_thresholds: Dict[str, float],
        is_blocking: bool = True
    ):
        super().__init__(name, is_blocking)
        self.metric_thresholds = metric_thresholds

    def evaluate(self, result: EvaluationResult) -> GateResult:
        """Evaluate multi-metric gate"""
        failed_metrics = []
        total_score = 0.0
        count = 0

        for metric_name, threshold in self.metric_thresholds.items():
            if metric_name not in result.metrics:
                failed_metrics.append(f"{metric_name} (not found)")
                continue

            metric = result.metrics[metric_name]
            total_score += metric.value
            count += 1

            if metric.value < threshold:
                failed_metrics.append(
                    f"{metric_name} ({metric.value:.4f} < {threshold})"
                )

        avg_score = total_score / count if count > 0 else 0.0
        avg_threshold = sum(self.metric_thresholds.values()) / len(self.metric_thresholds)
        passed = len(failed_metrics) == 0

        return GateResult(
            passed=passed,
            threshold=avg_threshold,
            score=avg_score,
            blocked=self.is_blocking and not passed,
            reason=None if passed else f"Failed metrics: {', '.join(failed_metrics)}"
        )


class CustomGate(QualityGate):
    """
    Gate with custom evaluation function
    """

    def __init__(
        self,
        name: str,
        evaluate_fn: Callable[[EvaluationResult], GateResult],
        is_blocking: bool = False
    ):
        super().__init__(name, is_blocking)
        self.evaluate_fn = evaluate_fn

    def evaluate(self, result: EvaluationResult) -> GateResult:
        """Evaluate using custom function"""
        try:
            gate_result = self.evaluate_fn(result)
            if self.is_blocking and not gate_result.passed:
                gate_result.blocked = True
            return gate_result
        except Exception as e:
            return GateResult(
                passed=False,
                threshold=0.0,
                score=0.0,
                blocked=self.is_blocking,
                reason=f"Custom gate evaluation failed: {str(e)}"
            )


class PerformanceGate(QualityGate):
    """
    Gate that checks performance metrics (speed, memory, etc.)
    """

    def __init__(
        self,
        name: str,
        max_duration: Optional[float] = None,
        max_memory: Optional[float] = None,
        is_blocking: bool = False
    ):
        super().__init__(name, is_blocking)
        self.max_duration = max_duration
        self.max_memory = max_memory

    def evaluate(self, result: EvaluationResult) -> GateResult:
        """Evaluate performance gate"""
        reasons = []
        passed = True

        # Check duration
        if self.max_duration is not None and result.duration > self.max_duration:
            passed = False
            reasons.append(
                f"Duration ({result.duration:.2f}s) exceeds limit ({self.max_duration}s)"
            )

        # Check memory if available in metadata
        if self.max_memory is not None:
            memory_used = result.metadata.get("memory_mb", 0)
            if memory_used > self.max_memory:
                passed = False
                reasons.append(
                    f"Memory ({memory_used:.2f}MB) exceeds limit ({self.max_memory}MB)"
                )

        return GateResult(
            passed=passed,
            threshold=self.max_duration or 0.0,
            score=result.duration,
            blocked=self.is_blocking and not passed,
            reason="; ".join(reasons) if reasons else None
        )
