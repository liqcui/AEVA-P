"""
Drift Detection for ML Models

Detect data drift and model performance drift

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
import statistics
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from collections import Counter
import math

logger = logging.getLogger(__name__)


@dataclass
class DriftReport:
    """Drift detection report"""
    drift_type: str  # 'data' or 'model'
    detected: bool
    severity: str  # 'none', 'low', 'medium', 'high', 'critical'
    metrics: Dict[str, float]
    details: Dict[str, Any]
    timestamp: datetime
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'drift_type': self.drift_type,
            'detected': self.detected,
            'severity': self.severity,
            'metrics': self.metrics,
            'details': self.details,
            'timestamp': self.timestamp.isoformat(),
            'recommendations': self.recommendations
        }


class DataDriftAnalyzer:
    """
    Analyze data distribution drift

    Methods:
    - Population Stability Index (PSI)
    - Kullback-Leibler Divergence
    - Kolmogorov-Smirnov Test
    - Feature distribution comparison
    """

    def __init__(self):
        """Initialize data drift analyzer"""
        pass

    def detect_drift(
        self,
        reference_data: List[Any],
        current_data: List[Any],
        feature_key: Optional[str] = None,
        threshold: float = 0.2
    ) -> DriftReport:
        """
        Detect data drift between reference and current data

        Args:
            reference_data: Baseline/training data
            current_data: Recent/production data
            feature_key: Key for feature extraction (if dict)
            threshold: PSI threshold for drift detection

        Returns:
            DriftReport
        """
        logger.info(f"Detecting data drift (reference: {len(reference_data)}, current: {len(current_data)})")

        # Extract features
        if feature_key:
            reference_values = [d[feature_key] for d in reference_data if isinstance(d, dict)]
            current_values = [d[feature_key] for d in current_data if isinstance(d, dict)]
        else:
            reference_values = reference_data
            current_values = current_data

        # Calculate PSI
        psi = self._calculate_psi(reference_values, current_values)

        # Calculate KL divergence
        kl_div = self._calculate_kl_divergence(reference_values, current_values)

        # Determine severity
        severity = self._determine_severity(psi)
        detected = psi > threshold

        # Generate recommendations
        recommendations = self._generate_recommendations(psi, kl_div, severity)

        report = DriftReport(
            drift_type='data',
            detected=detected,
            severity=severity,
            metrics={
                'psi': psi,
                'kl_divergence': kl_div
            },
            details={
                'reference_size': len(reference_values),
                'current_size': len(current_values),
                'threshold': threshold
            },
            timestamp=datetime.now(),
            recommendations=recommendations
        )

        logger.info(f"Data drift: PSI={psi:.4f}, detected={detected}, severity={severity}")

        return report

    def _calculate_psi(
        self,
        reference: List[Any],
        current: List[Any],
        num_bins: int = 10
    ) -> float:
        """
        Calculate Population Stability Index (PSI)

        PSI < 0.1: No significant change
        0.1 <= PSI < 0.2: Moderate change
        PSI >= 0.2: Significant change
        """
        # For categorical data
        if isinstance(reference[0], str):
            return self._calculate_psi_categorical(reference, current)

        # For numerical data
        return self._calculate_psi_numerical(reference, current, num_bins)

    def _calculate_psi_categorical(self, reference: List[str], current: List[str]) -> float:
        """Calculate PSI for categorical features"""
        ref_counts = Counter(reference)
        curr_counts = Counter(current)

        # Get all categories
        all_categories = set(ref_counts.keys()) | set(curr_counts.keys())

        ref_total = len(reference)
        curr_total = len(current)

        psi = 0.0

        for category in all_categories:
            ref_pct = ref_counts.get(category, 0.5) / ref_total  # Add 0.5 to avoid zero
            curr_pct = curr_counts.get(category, 0.5) / curr_total

            psi += (curr_pct - ref_pct) * math.log(curr_pct / ref_pct)

        return abs(psi)

    def _calculate_psi_numerical(
        self,
        reference: List[float],
        current: List[float],
        num_bins: int
    ) -> float:
        """Calculate PSI for numerical features"""
        # Create bins based on reference data
        ref_sorted = sorted(reference)
        bin_edges = [
            ref_sorted[int(i * len(ref_sorted) / num_bins)]
            for i in range(num_bins + 1)
        ]

        # Ensure unique bin edges
        bin_edges = sorted(set(bin_edges))

        # Count samples in each bin
        ref_counts = [0] * (len(bin_edges) - 1)
        curr_counts = [0] * (len(bin_edges) - 1)

        for value in reference:
            for i in range(len(bin_edges) - 1):
                if bin_edges[i] <= value < bin_edges[i + 1]:
                    ref_counts[i] += 1
                    break

        for value in current:
            for i in range(len(bin_edges) - 1):
                if bin_edges[i] <= value < bin_edges[i + 1]:
                    curr_counts[i] += 1
                    break

        # Calculate PSI
        ref_total = len(reference)
        curr_total = len(current)

        psi = 0.0

        for ref_count, curr_count in zip(ref_counts, curr_counts):
            ref_pct = (ref_count + 0.5) / ref_total
            curr_pct = (curr_count + 0.5) / curr_total

            if ref_pct > 0 and curr_pct > 0:
                psi += (curr_pct - ref_pct) * math.log(curr_pct / ref_pct)

        return abs(psi)

    def _calculate_kl_divergence(
        self,
        reference: List[Any],
        current: List[Any]
    ) -> float:
        """Calculate Kullback-Leibler divergence"""
        if isinstance(reference[0], str):
            # Categorical
            ref_counts = Counter(reference)
            curr_counts = Counter(current)

            all_categories = set(ref_counts.keys()) | set(curr_counts.keys())

            ref_total = len(reference)
            curr_total = len(current)

            kl = 0.0

            for category in all_categories:
                p = (ref_counts.get(category, 0.5) + 0.5) / ref_total
                q = (curr_counts.get(category, 0.5) + 0.5) / curr_total

                kl += p * math.log(p / q)

            return max(0.0, kl)
        else:
            # Numerical - use binned approach
            num_bins = 10
            ref_sorted = sorted(reference)
            bin_edges = [
                ref_sorted[int(i * len(ref_sorted) / num_bins)]
                for i in range(num_bins + 1)
            ]
            bin_edges = sorted(set(bin_edges))

            ref_counts = [0] * (len(bin_edges) - 1)
            curr_counts = [0] * (len(bin_edges) - 1)

            for value in reference:
                for i in range(len(bin_edges) - 1):
                    if bin_edges[i] <= value < bin_edges[i + 1]:
                        ref_counts[i] += 1
                        break

            for value in current:
                for i in range(len(bin_edges) - 1):
                    if bin_edges[i] <= value < bin_edges[i + 1]:
                        curr_counts[i] += 1
                        break

            ref_total = len(reference)
            curr_total = len(current)

            kl = 0.0

            for ref_count, curr_count in zip(ref_counts, curr_counts):
                p = (ref_count + 0.5) / ref_total
                q = (curr_count + 0.5) / curr_total

                kl += p * math.log(p / q)

            return max(0.0, kl)

    def _determine_severity(self, psi: float) -> str:
        """Determine drift severity based on PSI"""
        if psi < 0.1:
            return 'none'
        elif psi < 0.15:
            return 'low'
        elif psi < 0.25:
            return 'medium'
        elif psi < 0.35:
            return 'high'
        else:
            return 'critical'

    def _generate_recommendations(
        self,
        psi: float,
        kl_div: float,
        severity: str
    ) -> List[str]:
        """Generate recommendations based on drift metrics"""
        recommendations = []

        if severity == 'none':
            recommendations.append("No significant drift detected. Continue monitoring.")
        elif severity == 'low':
            recommendations.append("Minor drift detected. Monitor closely for trends.")
        elif severity in ['medium', 'high']:
            recommendations.extend([
                "Moderate to significant drift detected.",
                "Investigate data distribution changes.",
                "Consider retraining the model with recent data.",
                "Review data collection process for changes."
            ])
        elif severity == 'critical':
            recommendations.extend([
                "CRITICAL drift detected!",
                "Immediate action required.",
                "Model predictions may be unreliable.",
                "Retrain model with current data distribution.",
                "Investigate root cause of distribution shift."
            ])

        return recommendations


class ModelDriftAnalyzer:
    """
    Analyze model performance drift

    Monitors degradation in model metrics over time
    """

    def __init__(self, baseline_metrics: Optional[Dict[str, float]] = None):
        """
        Initialize model drift analyzer

        Args:
            baseline_metrics: Baseline performance metrics
        """
        self.baseline_metrics = baseline_metrics or {}

    def detect_drift(
        self,
        current_metrics: Dict[str, float],
        threshold: float = 0.05,
        metric_direction: Optional[Dict[str, str]] = None
    ) -> DriftReport:
        """
        Detect model performance drift

        Args:
            current_metrics: Current model metrics
            threshold: Relative threshold for drift (5% default)
            metric_direction: Direction of improvement per metric ('higher' or 'lower')

        Returns:
            DriftReport
        """
        if not self.baseline_metrics:
            logger.warning("No baseline metrics set. Using current metrics as baseline.")
            self.baseline_metrics = current_metrics
            return DriftReport(
                drift_type='model',
                detected=False,
                severity='none',
                metrics={},
                details={'message': 'Baseline established'},
                timestamp=datetime.now(),
                recommendations=['Baseline metrics recorded. Continue monitoring.']
            )

        logger.info(f"Detecting model drift against baseline")

        # Calculate drift for each metric
        drift_metrics = {}
        max_drift = 0.0
        degraded_metrics = []

        metric_direction = metric_direction or {}

        for metric_name, current_value in current_metrics.items():
            if metric_name in self.baseline_metrics:
                baseline_value = self.baseline_metrics[metric_name]

                # Calculate relative change
                if baseline_value != 0:
                    relative_change = (current_value - baseline_value) / abs(baseline_value)
                else:
                    relative_change = 0.0

                drift_metrics[metric_name] = relative_change

                # Determine if this is degradation
                direction = metric_direction.get(metric_name, 'higher')  # Default: higher is better

                is_degraded = False
                if direction == 'higher' and relative_change < -threshold:
                    is_degraded = True
                elif direction == 'lower' and relative_change > threshold:
                    is_degraded = True

                if is_degraded:
                    degraded_metrics.append(metric_name)
                    max_drift = max(max_drift, abs(relative_change))

        # Determine overall drift
        detected = len(degraded_metrics) > 0
        severity = self._determine_severity(max_drift)

        # Generate recommendations
        recommendations = self._generate_recommendations(degraded_metrics, drift_metrics, severity)

        report = DriftReport(
            drift_type='model',
            detected=detected,
            severity=severity,
            metrics=drift_metrics,
            details={
                'baseline_metrics': self.baseline_metrics,
                'current_metrics': current_metrics,
                'degraded_metrics': degraded_metrics,
                'threshold': threshold
            },
            timestamp=datetime.now(),
            recommendations=recommendations
        )

        logger.info(
            f"Model drift: detected={detected}, severity={severity}, "
            f"degraded_metrics={degraded_metrics}"
        )

        return report

    def _determine_severity(self, max_drift: float) -> str:
        """Determine drift severity based on maximum drift"""
        if max_drift < 0.05:
            return 'none'
        elif max_drift < 0.10:
            return 'low'
        elif max_drift < 0.20:
            return 'medium'
        elif max_drift < 0.35:
            return 'high'
        else:
            return 'critical'

    def _generate_recommendations(
        self,
        degraded_metrics: List[str],
        drift_metrics: Dict[str, float],
        severity: str
    ) -> List[str]:
        """Generate recommendations based on drift analysis"""
        recommendations = []

        if severity == 'none':
            recommendations.append("No significant performance drift detected.")
        elif severity == 'low':
            recommendations.append(f"Minor performance drift in: {', '.join(degraded_metrics)}")
            recommendations.append("Continue monitoring for sustained degradation.")
        elif severity in ['medium', 'high']:
            recommendations.extend([
                f"Significant performance drift detected in: {', '.join(degraded_metrics)}",
                "Investigate potential causes:",
                "  - Data distribution shift",
                "  - Data quality issues",
                "  - System or infrastructure changes",
                "Consider model retraining with recent data."
            ])
        elif severity == 'critical':
            recommendations.extend([
                f"CRITICAL performance degradation in: {', '.join(degraded_metrics)}",
                "Immediate action required!",
                "Recommendations:",
                "  1. Roll back to previous model version if available",
                "  2. Investigate root cause urgently",
                "  3. Retrain model with quality-checked recent data",
                "  4. Review monitoring and alerting configuration"
            ])

        return recommendations

    def update_baseline(self, new_baseline: Dict[str, float]) -> None:
        """Update baseline metrics"""
        self.baseline_metrics = new_baseline
        logger.info(f"Updated baseline metrics: {list(new_baseline.keys())}")


class DriftDetector:
    """
    Unified drift detector combining data and model drift detection

    Features:
    - Data distribution drift
    - Model performance drift
    - Unified reporting
    - Automated recommendations
    """

    def __init__(self, baseline_metrics: Optional[Dict[str, float]] = None):
        """
        Initialize drift detector

        Args:
            baseline_metrics: Baseline model performance metrics
        """
        self.data_analyzer = DataDriftAnalyzer()
        self.model_analyzer = ModelDriftAnalyzer(baseline_metrics)

    def detect_all_drift(
        self,
        reference_data: Optional[List[Any]] = None,
        current_data: Optional[List[Any]] = None,
        current_metrics: Optional[Dict[str, float]] = None,
        feature_key: Optional[str] = None
    ) -> Dict[str, DriftReport]:
        """
        Detect both data and model drift

        Args:
            reference_data: Baseline data
            current_data: Recent data
            current_metrics: Current model metrics
            feature_key: Key for feature extraction

        Returns:
            Dictionary with 'data' and 'model' drift reports
        """
        reports = {}

        # Data drift
        if reference_data and current_data:
            reports['data'] = self.data_analyzer.detect_drift(
                reference_data,
                current_data,
                feature_key
            )

        # Model drift
        if current_metrics:
            reports['model'] = self.model_analyzer.detect_drift(current_metrics)

        return reports

    def update_baseline(self, new_metrics: Dict[str, float]) -> None:
        """Update model baseline metrics"""
        self.model_analyzer.update_baseline(new_metrics)
