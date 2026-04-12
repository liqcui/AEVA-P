"""
AEVA-Guard Validators
Validation logic for different aspects

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod

from aeva.core.result import EvaluationResult


class Validator(ABC):
    """Abstract base validator"""

    @abstractmethod
    def validate(self, result: EvaluationResult) -> List[str]:
        """
        Validate result

        Args:
            result: Evaluation result

        Returns:
            List of validation error messages (empty if valid)
        """
        pass


class MetricValidator(Validator):
    """Validates that required metrics are present"""

    def __init__(self, required_metrics: List[str]):
        self.required_metrics = required_metrics

    def validate(self, result: EvaluationResult) -> List[str]:
        """Check if all required metrics are present"""
        errors = []

        for metric_name in self.required_metrics:
            if metric_name not in result.metrics:
                errors.append(f"Required metric '{metric_name}' is missing")

        return errors


class ComplianceValidator(Validator):
    """Validates compliance with regulations/standards"""

    def __init__(self, compliance_rules: Dict[str, Any]):
        self.compliance_rules = compliance_rules

    def validate(self, result: EvaluationResult) -> List[str]:
        """Check compliance rules"""
        errors = []

        # Example: Check fairness metrics
        if "fairness" in self.compliance_rules:
            if "fairness_score" not in result.metrics:
                errors.append("Fairness evaluation required but not performed")
            else:
                min_fairness = self.compliance_rules["fairness"].get("min_score", 0.8)
                if result.metrics["fairness_score"].value < min_fairness:
                    errors.append(
                        f"Fairness score below required threshold: "
                        f"{result.metrics['fairness_score'].value:.4f} < {min_fairness}"
                    )

        # Example: Check bias metrics
        if "bias" in self.compliance_rules:
            if "bias_score" not in result.metrics:
                errors.append("Bias evaluation required but not performed")

        return errors


class RangeValidator(Validator):
    """Validates that metrics fall within acceptable ranges"""

    def __init__(self, metric_ranges: Dict[str, tuple]):
        """
        Args:
            metric_ranges: Dict mapping metric names to (min, max) tuples
        """
        self.metric_ranges = metric_ranges

    def validate(self, result: EvaluationResult) -> List[str]:
        """Check if metrics are within ranges"""
        errors = []

        for metric_name, (min_val, max_val) in self.metric_ranges.items():
            if metric_name in result.metrics:
                value = result.metrics[metric_name].value

                if value < min_val or value > max_val:
                    errors.append(
                        f"Metric '{metric_name}' ({value:.4f}) outside valid range "
                        f"[{min_val}, {max_val}]"
                    )

        return errors
