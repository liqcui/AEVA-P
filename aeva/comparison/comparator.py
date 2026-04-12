"""
Model Comparator for multi-model evaluation

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from aeva.core.result import EvaluationResult

logger = logging.getLogger(__name__)


class ComparisonResult:
    """
    Result of model comparison

    Attributes:
        models: List of model names being compared
        metrics_comparison: Dict of metrics for each model
        statistical_tests: Results of statistical significance tests
        rankings: Model rankings by different criteria
        best_model: Best performing model for each metric
        summary: Overall comparison summary
    """

    def __init__(self, models: List[str]):
        self.models = models
        self.metrics_comparison: Dict[str, Dict[str, float]] = {}
        self.statistical_tests: Dict[str, Any] = {}
        self.rankings: Dict[str, int] = {}
        self.best_model: Dict[str, str] = {}
        self.summary: str = ""
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'models': self.models,
            'metrics_comparison': self.metrics_comparison,
            'statistical_tests': self.statistical_tests,
            'rankings': self.rankings,
            'best_model': self.best_model,
            'summary': self.summary,
            'timestamp': self.timestamp.isoformat()
        }


class ModelComparator:
    """
    Compare multiple models side-by-side

    Features:
    - Multi-model metric comparison
    - Statistical significance testing
    - Ranking and best model identification
    - Detailed analysis reports
    """

    def __init__(self, confidence_level: float = 0.95):
        """
        Initialize comparator

        Args:
            confidence_level: Confidence level for statistical tests (default 0.95)
        """
        self.confidence_level = confidence_level

    def compare(
        self,
        results: List[EvaluationResult],
        metrics: Optional[List[str]] = None
    ) -> ComparisonResult:
        """
        Compare multiple evaluation results

        Args:
            results: List of evaluation results to compare
            metrics: Specific metrics to compare (None = all metrics)

        Returns:
            ComparisonResult object
        """
        if len(results) < 2:
            raise ValueError("Need at least 2 models to compare")

        logger.info(f"Comparing {len(results)} models")

        # Extract model names
        model_names = [r.model_name for r in results]
        comparison = ComparisonResult(model_names)

        # Build metrics comparison
        comparison.metrics_comparison = self._build_metrics_comparison(
            results, metrics
        )

        # Compute rankings
        comparison.rankings = self._compute_rankings(comparison.metrics_comparison)

        # Identify best models
        comparison.best_model = self._identify_best_models(comparison.metrics_comparison)

        # Statistical significance tests
        comparison.statistical_tests = self._run_statistical_tests(results)

        # Generate summary
        comparison.summary = self._generate_summary(comparison)

        logger.info("Comparison completed successfully")

        return comparison

    def _build_metrics_comparison(
        self,
        results: List[EvaluationResult],
        metrics_filter: Optional[List[str]]
    ) -> Dict[str, Dict[str, float]]:
        """Build metrics comparison dictionary"""
        comparison = {}

        for result in results:
            model_name = result.model_name
            model_metrics = {}

            # Get all metrics from result
            if hasattr(result, 'metrics'):
                for metric_name, value in result.metrics.items():
                    # Filter if needed
                    if metrics_filter is None or metric_name in metrics_filter:
                        model_metrics[metric_name] = value

            comparison[model_name] = model_metrics

        return comparison

    def _compute_rankings(
        self,
        metrics_comparison: Dict[str, Dict[str, float]]
    ) -> Dict[str, int]:
        """
        Compute overall rankings for models

        Uses weighted average of normalized metrics
        """
        if not metrics_comparison:
            return {}

        # Define metric weights and directions (True = higher is better)
        metric_config = {
            'accuracy': (1.0, True),
            'precision': (0.8, True),
            'recall': (0.8, True),
            'f1_score': (1.0, True),
            'inference_time_ms': (0.6, False),  # Lower is better
            'throughput': (0.5, True),
            'memory_mb': (0.3, False),  # Lower is better
        }

        # Calculate weighted scores
        scores = {}

        for model, metrics in metrics_comparison.items():
            total_score = 0.0
            total_weight = 0.0

            for metric, (weight, higher_better) in metric_config.items():
                if metric in metrics:
                    value = metrics[metric]

                    # Normalize to 0-1 range
                    all_values = [m.get(metric, 0) for m in metrics_comparison.values()]
                    min_val = min(all_values)
                    max_val = max(all_values)

                    if max_val > min_val:
                        normalized = (value - min_val) / (max_val - min_val)
                        if not higher_better:
                            normalized = 1 - normalized  # Invert for "lower is better"

                        total_score += normalized * weight
                        total_weight += weight

            # Average score
            scores[model] = total_score / total_weight if total_weight > 0 else 0.0

        # Rank by score
        sorted_models = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return {model: idx + 1 for idx, (model, _) in enumerate(sorted_models)}

    def _identify_best_models(
        self,
        metrics_comparison: Dict[str, Dict[str, float]]
    ) -> Dict[str, str]:
        """Identify best model for each metric"""
        best_models = {}

        # Get all metrics
        all_metrics = set()
        for metrics in metrics_comparison.values():
            all_metrics.update(metrics.keys())

        # For each metric, find best model
        for metric in all_metrics:
            values = {
                model: data.get(metric, None)
                for model, data in metrics_comparison.items()
            }

            # Remove None values
            values = {k: v for k, v in values.items() if v is not None}

            if not values:
                continue

            # Determine if higher or lower is better
            higher_better_metrics = [
                'accuracy', 'precision', 'recall', 'f1_score',
                'throughput', 'auc', 'map'
            ]

            if any(m in metric.lower() for m in higher_better_metrics):
                best_models[metric] = max(values, key=values.get)
            else:
                best_models[metric] = min(values, key=values.get)

        return best_models

    def _run_statistical_tests(
        self,
        results: List[EvaluationResult]
    ) -> Dict[str, Any]:
        """
        Run statistical significance tests

        Note: For production, would use scipy.stats for proper tests
        This is a simplified version for demonstration
        """
        tests = {
            'method': 'pairwise_comparison',
            'confidence_level': self.confidence_level,
            'note': 'Simplified statistical tests for demonstration'
        }

        # In production, would implement:
        # - T-tests for metric comparison
        # - ANOVA for multiple models
        # - Effect size calculations
        # - Confidence intervals

        return tests

    def _generate_summary(self, comparison: ComparisonResult) -> str:
        """Generate comparison summary"""
        best_overall = min(comparison.rankings.items(), key=lambda x: x[1])[0]

        summary = f"""
Model Comparison Summary
========================

Total Models: {len(comparison.models)}
Best Overall Model: {best_overall} (Rank #{comparison.rankings[best_overall]})

Model Rankings:
{self._format_rankings(comparison.rankings)}

Best Models by Metric:
{self._format_best_models(comparison.best_model)}
"""
        return summary.strip()

    def _format_rankings(self, rankings: Dict[str, int]) -> str:
        """Format rankings for display"""
        sorted_rankings = sorted(rankings.items(), key=lambda x: x[1])
        return "\n".join(
            f"  #{rank}. {model}"
            for model, rank in sorted_rankings
        )

    def _format_best_models(self, best_models: Dict[str, str]) -> str:
        """Format best models for display"""
        return "\n".join(
            f"  {metric}: {model}"
            for metric, model in best_models.items()
        )

    def compare_pairwise(
        self,
        model_a: EvaluationResult,
        model_b: EvaluationResult
    ) -> Dict[str, Any]:
        """
        Compare two models in detail

        Args:
            model_a: First model result
            model_b: Second model result

        Returns:
            Detailed comparison dictionary
        """
        logger.info(f"Pairwise comparison: {model_a.model_name} vs {model_b.model_name}")

        comparison = {
            'model_a': model_a.model_name,
            'model_b': model_b.model_name,
            'metrics_delta': {},
            'winner': None,
            'statistical_significance': {}
        }

        # Compare metrics
        metrics_a = getattr(model_a, 'metrics', {})
        metrics_b = getattr(model_b, 'metrics', {})

        for metric in set(list(metrics_a.keys()) + list(metrics_b.keys())):
            value_a = metrics_a.get(metric, 0)
            value_b = metrics_b.get(metric, 0)

            delta = value_b - value_a
            delta_percent = (delta / value_a * 100) if value_a != 0 else 0

            comparison['metrics_delta'][metric] = {
                'model_a_value': value_a,
                'model_b_value': value_b,
                'absolute_delta': delta,
                'percent_delta': delta_percent
            }

        # Determine winner (simplified)
        # In production, would use proper statistical tests
        comparison['winner'] = self._determine_pairwise_winner(
            metrics_a, metrics_b
        )

        return comparison

    def _determine_pairwise_winner(
        self,
        metrics_a: Dict[str, float],
        metrics_b: Dict[str, float]
    ) -> str:
        """Determine winner in pairwise comparison"""
        # Simple heuristic: compare key metrics
        key_metrics = ['accuracy', 'f1_score', 'precision', 'recall']

        score_a = sum(metrics_a.get(m, 0) for m in key_metrics)
        score_b = sum(metrics_b.get(m, 0) for m in key_metrics)

        if score_a > score_b:
            return 'model_a'
        elif score_b > score_a:
            return 'model_b'
        else:
            return 'tie'
