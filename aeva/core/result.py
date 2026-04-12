"""
AEVA Evaluation Result

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
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


@dataclass
class GateResult:
    """Quality gate result"""
    passed: bool
    threshold: float
    score: float
    blocked: bool = False
    reason: Optional[str] = None


@dataclass
class Analysis:
    """Intelligent analysis result from AEVA-Brain"""
    summary: str
    root_causes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    severity: str = "info"  # info, warning, error, critical
    confidence: float = 0.0


class EvaluationResult:
    """
    Comprehensive evaluation result from AEVA platform
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
        # Analyze if there are failures, warnings, or blocked status
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
                name: {
                    "value": m.value,
                    "threshold": m.threshold,
                    "passed": m.passed,
                    "unit": m.unit,
                    "description": m.description,
                }
                for name, m in self.metrics.items()
            },
            "gate_result": {
                "passed": self.gate_result.passed,
                "score": self.gate_result.score,
                "threshold": self.gate_result.threshold,
                "blocked": self.gate_result.blocked,
                "reason": self.gate_result.reason,
            } if self.gate_result else None,
            "analysis": {
                "summary": self.analysis.summary,
                "root_causes": self.analysis.root_causes,
                "recommendations": self.analysis.recommendations,
                "severity": self.analysis.severity,
                "confidence": self.analysis.confidence,
            } if self.analysis else None,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return f"EvaluationResult(pipeline='{self.pipeline_name}', status={self.status.value}, score={self.get_overall_score():.2%})"
