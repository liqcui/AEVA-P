"""
AEVA Evaluation Result Models

Shared data structures for evaluation results across all AEVA services.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ResultStatus(Enum):
    """Evaluation result status"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    BLOCKED = "blocked"
    PENDING = "pending"


@dataclass
class MetricResult:
    """Individual metric result"""
    name: str
    value: float
    threshold: Optional[float] = None
    passed: bool = True
    unit: str = ""
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "value": self.value,
            "threshold": self.threshold,
            "passed": self.passed,
            "unit": self.unit,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetricResult":
        """Create from dictionary"""
        return cls(**data)


@dataclass
class GateResult:
    """Quality gate result"""
    passed: bool
    threshold: float
    score: float
    blocked: bool = False
    reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "passed": self.passed,
            "threshold": self.threshold,
            "score": self.score,
            "blocked": self.blocked,
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GateResult":
        """Create from dictionary"""
        return cls(**data)


@dataclass
class Analysis:
    """Intelligent analysis result from AEVA-Brain"""
    summary: str
    root_causes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    severity: str = "info"  # info, warning, error, critical
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "summary": self.summary,
            "root_causes": self.root_causes,
            "recommendations": self.recommendations,
            "severity": self.severity,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Analysis":
        """Create from dictionary"""
        return cls(**data)


class EvaluationResult:
    """
    Comprehensive evaluation result from AEVA platform

    This is the primary data structure shared across all AEVA services.
    """

    def __init__(
        self,
        pipeline_name: str,
        algorithm_name: str = "unknown"
    ):
        self.pipeline_name = pipeline_name
        self.algorithm_name = algorithm_name
        self.timestamp = datetime.now()

        # Results
        self.status = ResultStatus.PENDING
        self.metrics: Dict[str, MetricResult] = {}
        self.gate_result: Optional[GateResult] = None
        self.analysis: Optional[Analysis] = None

        # Metadata
        self.metadata: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []

        # Performance
        self.duration: float = 0.0
        self.stage_results: List[Any] = []

    def add_metric(
        self,
        name: str,
        value: float,
        threshold: Optional[float] = None,
        unit: str = "",
        description: str = ""
    ) -> None:
        """Add a metric result"""
        passed = True
        if threshold is not None:
            passed = value >= threshold

        metric = MetricResult(
            name=name,
            value=value,
            threshold=threshold,
            passed=passed,
            unit=unit,
            description=description
        )
        self.metrics[name] = metric

    def set_gate_result(self, gate_result: GateResult) -> None:
        """Set quality gate result"""
        self.gate_result = gate_result
        if gate_result.blocked:
            self.status = ResultStatus.BLOCKED
        elif not gate_result.passed:
            self.status = ResultStatus.FAILED

    def set_analysis(self, analysis: Analysis) -> None:
        """Set intelligent analysis result"""
        self.analysis = analysis

    def add_error(self, error: str) -> None:
        """Add an error message"""
        self.errors.append(error)
        if self.status == ResultStatus.PASSED:
            self.status = ResultStatus.FAILED

    def add_warning(self, warning: str) -> None:
        """Add a warning message"""
        self.warnings.append(warning)
        if self.status == ResultStatus.PASSED:
            self.status = ResultStatus.WARNING

    def set_status(self, status: ResultStatus) -> None:
        """Set overall status"""
        self.status = status

    def should_analyze(self) -> bool:
        """Determine if intelligent analysis should be performed"""
        return (
            self.status in [ResultStatus.FAILED, ResultStatus.WARNING, ResultStatus.BLOCKED]
            or len(self.errors) > 0
            or len(self.warnings) > 0
        )

    def get_overall_score(self) -> float:
        """Calculate overall score from metrics"""
        if not self.metrics:
            return 0.0

        passed_count = sum(1 for m in self.metrics.values() if m.passed)
        return passed_count / len(self.metrics)

    def summary(self) -> str:
        """Generate a text summary of the result"""
        lines = [
            f"Evaluation Result: {self.pipeline_name}",
            f"Algorithm: {self.algorithm_name}",
            f"Status: {self.status.value}",
            f"Timestamp: {self.timestamp.isoformat()}",
            f"Duration: {self.duration:.2f}s",
            "",
            "Metrics:",
        ]

        for name, metric in self.metrics.items():
            status_icon = "✓" if metric.passed else "✗"
            threshold_str = f" (threshold: {metric.threshold})" if metric.threshold else ""
            lines.append(
                f"  {status_icon} {name}: {metric.value:.4f}{metric.unit}{threshold_str}"
            )

        if self.gate_result:
            lines.extend([
                "",
                "Quality Gate:",
                f"  Score: {self.gate_result.score:.4f}",
                f"  Threshold: {self.gate_result.threshold:.4f}",
                f"  Passed: {'Yes' if self.gate_result.passed else 'No'}",
                f"  Blocked: {'Yes' if self.gate_result.blocked else 'No'}",
            ])

        if self.analysis:
            lines.extend([
                "",
                "Intelligent Analysis:",
                f"  Summary: {self.analysis.summary}",
                f"  Severity: {self.analysis.severity}",
                f"  Confidence: {self.analysis.confidence:.2%}",
            ])

            if self.analysis.root_causes:
                lines.append("  Root Causes:")
                for cause in self.analysis.root_causes:
                    lines.append(f"    - {cause}")

            if self.analysis.recommendations:
                lines.append("  Recommendations:")
                for rec in self.analysis.recommendations:
                    lines.append(f"    - {rec}")

        if self.errors:
            lines.extend(["", "Errors:"])
            for error in self.errors:
                lines.append(f"  - {error}")

        if self.warnings:
            lines.extend(["", "Warnings:"])
            for warning in self.warnings:
                lines.append(f"  - {warning}")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "pipeline_name": self.pipeline_name,
            "algorithm_name": self.algorithm_name,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "duration": self.duration,
            "metrics": {
                name: m.to_dict()
                for name, m in self.metrics.items()
            },
            "gate_result": self.gate_result.to_dict() if self.gate_result else None,
            "analysis": self.analysis.to_dict() if self.analysis else None,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvaluationResult":
        """Create from dictionary"""
        result = cls(
            pipeline_name=data["pipeline_name"],
            algorithm_name=data.get("algorithm_name", "unknown")
        )

        result.status = ResultStatus(data["status"])
        result.duration = data.get("duration", 0.0)
        result.errors = data.get("errors", [])
        result.warnings = data.get("warnings", [])
        result.metadata = data.get("metadata", {})

        # Restore timestamp
        if "timestamp" in data:
            result.timestamp = datetime.fromisoformat(data["timestamp"])

        # Restore metrics
        if "metrics" in data:
            for name, metric_data in data["metrics"].items():
                result.metrics[name] = MetricResult.from_dict(metric_data)

        # Restore gate result
        if data.get("gate_result"):
            result.gate_result = GateResult.from_dict(data["gate_result"])

        # Restore analysis
        if data.get("analysis"):
            result.analysis = Analysis.from_dict(data["analysis"])

        return result

    def __repr__(self) -> str:
        return f"EvaluationResult(pipeline='{self.pipeline_name}', status={self.status.value}, score={self.get_overall_score():.2%})"
