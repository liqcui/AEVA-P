"""
Bias Detection and Fairness Analysis

Detect bias in ML models and provide detailed analysis
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from aeva.fairness.metrics import FairnessMetrics, BiasMetrics

logger = logging.getLogger(__name__)


@dataclass
class BiasDetectionResult:
    """Result of bias detection"""
    biased: bool
    severity: str  # 'none', 'low', 'medium', 'high', 'critical'
    metrics: BiasMetrics
    group_metrics: Dict[Any, Dict[str, float]]
    privileged_group: Any
    unprivileged_groups: List[Any]
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'biased': self.biased,
            'severity': self.severity,
            'metrics': self.metrics.to_dict(),
            'group_metrics': self.group_metrics,
            'privileged_group': str(self.privileged_group),
            'unprivileged_groups': [str(g) for g in self.unprivileged_groups],
            'violations': self.violations,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp.isoformat()
        }


class BiasDetector:
    """
    Detect bias in ML model predictions

    Features:
    - Multiple fairness criteria
    - Severity classification
    - Violation detection
    - Mitigation recommendations
    """

    def __init__(
        self,
        thresholds: Optional[Dict[str, float]] = None,
        strict_mode: bool = False
    ):
        """
        Initialize bias detector

        Args:
            thresholds: Custom thresholds for fairness metrics
            strict_mode: Use stricter thresholds
        """
        self.metrics_calculator = FairnessMetrics()

        # Default thresholds
        if thresholds is None:
            if strict_mode:
                # Stricter thresholds
                thresholds = {
                    'demographic_parity_difference': 0.05,  # ±5%
                    'equalized_odds_difference': 0.05,
                    'disparate_impact_ratio_min': 0.90,  # 90% rule
                    'disparate_impact_ratio_max': 1.10,
                    'equal_opportunity_difference': 0.05,
                    'predictive_parity_difference': 0.05
                }
            else:
                # Standard thresholds
                thresholds = {
                    'demographic_parity_difference': 0.10,  # ±10%
                    'equalized_odds_difference': 0.10,
                    'disparate_impact_ratio_min': 0.80,  # 80% rule (legal standard)
                    'disparate_impact_ratio_max': 1.25,
                    'equal_opportunity_difference': 0.10,
                    'predictive_parity_difference': 0.10
                }

        self.thresholds = thresholds
        self.strict_mode = strict_mode

        logger.info(f"Bias detector initialized (strict_mode={strict_mode})")

    def detect_bias(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        positive_label: int = 1,
        privileged_group: Optional[Any] = None,
        attribute_name: str = "sensitive_attribute"
    ) -> BiasDetectionResult:
        """
        Detect bias in model predictions

        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            sensitive_attribute: Protected attribute values
            positive_label: Positive class label
            privileged_group: Privileged group value (auto-detected if None)
            attribute_name: Name of the sensitive attribute

        Returns:
            BiasDetectionResult
        """
        logger.info(f"Detecting bias in {len(y_true)} predictions")

        # Calculate all fairness metrics
        bias_metrics = self.metrics_calculator.calculate_all_metrics(
            y_true=y_true,
            y_pred=y_pred,
            sensitive_attribute=sensitive_attribute,
            positive_label=positive_label,
            privileged_group=privileged_group
        )

        # Calculate group-specific metrics
        group_metrics = self.metrics_calculator.calculate_group_metrics(
            y_true=y_true,
            y_pred=y_pred,
            sensitive_attribute=sensitive_attribute,
            positive_label=positive_label
        )

        # Detect privileged group
        if privileged_group is None:
            privileged_group = self.metrics_calculator._detect_privileged_group(
                y_true, y_pred, sensitive_attribute, positive_label
            )

        # Get unprivileged groups
        all_groups = set(sensitive_attribute)
        unprivileged_groups = list(all_groups - {privileged_group})

        # Check for violations
        violations = self._check_violations(bias_metrics, attribute_name)

        # Determine if biased
        biased = len(violations) > 0

        # Determine severity
        severity = self._determine_severity(violations, bias_metrics)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            violations, bias_metrics, group_metrics, privileged_group, unprivileged_groups
        )

        result = BiasDetectionResult(
            biased=biased,
            severity=severity,
            metrics=bias_metrics,
            group_metrics=group_metrics,
            privileged_group=privileged_group,
            unprivileged_groups=unprivileged_groups,
            violations=violations,
            recommendations=recommendations
        )

        logger.info(
            f"Bias detection complete: biased={biased}, severity={severity}, "
            f"violations={len(violations)}"
        )

        return result

    def _check_violations(
        self,
        metrics: BiasMetrics,
        attribute_name: str
    ) -> List[Dict[str, Any]]:
        """Check for fairness violations"""
        violations = []

        # Demographic Parity
        if abs(metrics.demographic_parity_difference) > self.thresholds['demographic_parity_difference']:
            violations.append({
                'metric': 'demographic_parity_difference',
                'value': metrics.demographic_parity_difference,
                'threshold': self.thresholds['demographic_parity_difference'],
                'description': f"Demographic parity violated: {abs(metrics.demographic_parity_difference):.2%} difference in positive prediction rates"
            })

        # Disparate Impact
        if (metrics.disparate_impact_ratio < self.thresholds['disparate_impact_ratio_min'] or
            metrics.disparate_impact_ratio > self.thresholds['disparate_impact_ratio_max']):
            violations.append({
                'metric': 'disparate_impact_ratio',
                'value': metrics.disparate_impact_ratio,
                'threshold': f"{self.thresholds['disparate_impact_ratio_min']}-{self.thresholds['disparate_impact_ratio_max']}",
                'description': f"Disparate impact detected: ratio={metrics.disparate_impact_ratio:.2f} (legal threshold: 0.80)"
            })

        # Equalized Odds
        if metrics.equalized_odds_difference > self.thresholds['equalized_odds_difference']:
            violations.append({
                'metric': 'equalized_odds_difference',
                'value': metrics.equalized_odds_difference,
                'threshold': self.thresholds['equalized_odds_difference'],
                'description': f"Equalized odds violated: {metrics.equalized_odds_difference:.2%} difference"
            })

        # Equal Opportunity
        if abs(metrics.equal_opportunity_difference) > self.thresholds['equal_opportunity_difference']:
            violations.append({
                'metric': 'equal_opportunity_difference',
                'value': metrics.equal_opportunity_difference,
                'threshold': self.thresholds['equal_opportunity_difference'],
                'description': f"Equal opportunity violated: {abs(metrics.equal_opportunity_difference):.2%} TPR difference"
            })

        # Predictive Parity
        if abs(metrics.predictive_parity_difference) > self.thresholds['predictive_parity_difference']:
            violations.append({
                'metric': 'predictive_parity_difference',
                'value': metrics.predictive_parity_difference,
                'threshold': self.thresholds['predictive_parity_difference'],
                'description': f"Predictive parity violated: {abs(metrics.predictive_parity_difference):.2%} precision difference"
            })

        return violations

    def _determine_severity(
        self,
        violations: List[Dict[str, Any]],
        metrics: BiasMetrics
    ) -> str:
        """Determine bias severity level"""
        if not violations:
            return 'none'

        # Count violations
        num_violations = len(violations)

        # Check for critical violations
        critical_threshold = 0.25  # 25% difference
        critical_violations = [
            v for v in violations
            if isinstance(v['value'], (int, float)) and abs(v['value']) > critical_threshold
        ]

        # Check disparate impact
        di_violation = metrics.disparate_impact_ratio < 0.6 or metrics.disparate_impact_ratio > 1.67

        if critical_violations or di_violation:
            return 'critical'
        elif num_violations >= 4:
            return 'high'
        elif num_violations >= 2:
            return 'medium'
        else:
            return 'low'

    def _generate_recommendations(
        self,
        violations: List[Dict[str, Any]],
        metrics: BiasMetrics,
        group_metrics: Dict[Any, Dict[str, float]],
        privileged_group: Any,
        unprivileged_groups: List[Any]
    ) -> List[str]:
        """Generate bias mitigation recommendations"""
        recommendations = []

        if not violations:
            recommendations.append("No significant bias detected. Model meets fairness criteria.")
            return recommendations

        # General recommendations
        recommendations.append("⚠️ Bias detected in model predictions.")
        recommendations.append("")
        recommendations.append("Immediate Actions:")

        # Specific recommendations based on violations
        violation_types = [v['metric'] for v in violations]

        if 'demographic_parity_difference' in violation_types or 'disparate_impact_ratio' in violation_types:
            recommendations.append("• Re-balance training data across demographic groups")
            recommendations.append("• Apply reweighting to underrepresented groups")
            recommendations.append("• Use fairness-aware learning algorithms")

        if 'equalized_odds_difference' in violation_types or 'equal_opportunity_difference' in violation_types:
            recommendations.append("• Adjust decision thresholds per group (post-processing)")
            recommendations.append("• Use equalized odds post-processing methods")
            recommendations.append("• Retrain with fairness constraints")

        if 'predictive_parity_difference' in violation_types:
            recommendations.append("• Improve model calibration across groups")
            recommendations.append("• Apply calibration techniques (Platt scaling, isotonic regression)")

        # Data recommendations
        recommendations.append("")
        recommendations.append("Data Collection:")
        recommendations.append("• Collect more data from underrepresented groups")
        recommendations.append("• Ensure representative sampling across demographics")
        recommendations.append("• Review data collection process for bias")

        # Model recommendations
        recommendations.append("")
        recommendations.append("Model Development:")
        recommendations.append("• Incorporate fairness metrics in model selection")
        recommendations.append("• Use adversarial debiasing techniques")
        recommendations.append("• Consider fairness-aware ensemble methods")

        # Monitoring recommendations
        recommendations.append("")
        recommendations.append("Ongoing Monitoring:")
        recommendations.append("• Implement continuous fairness monitoring")
        recommendations.append("• Set up alerts for fairness metric violations")
        recommendations.append("• Conduct regular fairness audits")

        return recommendations


class FairnessAnalyzer:
    """
    Comprehensive fairness analysis across multiple attributes

    Features:
    - Multi-attribute analysis
    - Intersectional bias detection
    - Group disparity analysis
    - Comparative fairness assessment
    """

    def __init__(self, strict_mode: bool = False):
        """
        Initialize fairness analyzer

        Args:
            strict_mode: Use stricter fairness thresholds
        """
        self.detector = BiasDetector(strict_mode=strict_mode)
        self.strict_mode = strict_mode

    def analyze_fairness(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attributes: Dict[str, List[Any]],
        positive_label: int = 1
    ) -> Dict[str, BiasDetectionResult]:
        """
        Analyze fairness across multiple sensitive attributes

        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            sensitive_attributes: Dictionary mapping attribute names to values
            positive_label: Positive class label

        Returns:
            Dictionary mapping attribute names to BiasDetectionResult
        """
        logger.info(f"Analyzing fairness across {len(sensitive_attributes)} attributes")

        results = {}

        for attr_name, attr_values in sensitive_attributes.items():
            logger.info(f"Analyzing attribute: {attr_name}")

            result = self.detector.detect_bias(
                y_true=y_true,
                y_pred=y_pred,
                sensitive_attribute=attr_values,
                positive_label=positive_label,
                attribute_name=attr_name
            )

            results[attr_name] = result

        logger.info(f"Fairness analysis complete for {len(results)} attributes")

        return results

    def detect_intersectional_bias(
        self,
        y_true: List[int],
        y_pred: List[int],
        attribute1: List[Any],
        attribute2: List[Any],
        attribute1_name: str = "attribute1",
        attribute2_name: str = "attribute2",
        positive_label: int = 1
    ) -> BiasDetectionResult:
        """
        Detect bias at the intersection of two attributes

        Example: Gender + Race

        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            attribute1: First sensitive attribute
            attribute2: Second sensitive attribute
            attribute1_name: Name of first attribute
            attribute2_name: Name of second attribute
            positive_label: Positive class label

        Returns:
            BiasDetectionResult
        """
        logger.info(f"Detecting intersectional bias: {attribute1_name} × {attribute2_name}")

        # Create intersectional groups
        intersectional = [
            f"{a1}_{a2}" for a1, a2 in zip(attribute1, attribute2)
        ]

        result = self.detector.detect_bias(
            y_true=y_true,
            y_pred=y_pred,
            sensitive_attribute=intersectional,
            positive_label=positive_label,
            attribute_name=f"{attribute1_name}_{attribute2_name}"
        )

        logger.info(f"Intersectional bias analysis complete")

        return result

    def compare_group_performance(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        positive_label: int = 1
    ) -> Dict[str, Any]:
        """
        Compare performance metrics across demographic groups

        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            sensitive_attribute: Protected attribute values
            positive_label: Positive class label

        Returns:
            Comparison report
        """
        group_metrics = self.detector.metrics_calculator.calculate_group_metrics(
            y_true=y_true,
            y_pred=y_pred,
            sensitive_attribute=sensitive_attribute,
            positive_label=positive_label
        )

        # Find best and worst performing groups
        groups_by_accuracy = sorted(
            group_metrics.items(),
            key=lambda x: x[1]['accuracy'],
            reverse=True
        )

        best_group = groups_by_accuracy[0] if groups_by_accuracy else None
        worst_group = groups_by_accuracy[-1] if groups_by_accuracy else None

        # Calculate disparities
        disparities = {}
        if len(groups_by_accuracy) > 1:
            for metric in ['accuracy', 'precision', 'recall', 'f1']:
                values = [g[1][metric] for g in groups_by_accuracy]
                disparities[metric] = {
                    'min': min(values),
                    'max': max(values),
                    'range': max(values) - min(values),
                    'std': self._calculate_std(values)
                }

        return {
            'group_metrics': group_metrics,
            'best_performing_group': best_group[0] if best_group else None,
            'worst_performing_group': worst_group[0] if worst_group else None,
            'performance_gap': (best_group[1]['accuracy'] - worst_group[1]['accuracy']) if best_group and worst_group else 0.0,
            'disparities': disparities
        }

    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if not values:
            return 0.0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
