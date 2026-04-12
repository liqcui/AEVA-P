"""
Bias Mitigation Strategies

Provide bias mitigation recommendations and techniques

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
import random
from typing import Dict, Any, List, Optional, Tuple
from collections import Counter

logger = logging.getLogger(__name__)


class BiasMitigation:
    """
    Bias mitigation techniques for ML models

    Provides:
    - Pre-processing mitigation (data-level)
    - In-processing mitigation (training-level)
    - Post-processing mitigation (prediction-level)
    """

    def __init__(self):
        """Initialize bias mitigation"""
        pass

    def reweight_samples(
        self,
        X: List[Any],
        y: List[int],
        sensitive_attribute: List[Any],
        positive_label: int = 1
    ) -> List[float]:
        """
        Calculate sample weights to achieve demographic parity

        Pre-processing technique: reweight training samples

        Args:
            X: Features
            y: Labels
            sensitive_attribute: Protected attribute values
            positive_label: Positive class label

        Returns:
            List of sample weights
        """
        logger.info("Calculating reweighting for demographic parity")

        # Calculate group statistics
        groups = set(sensitive_attribute)
        group_stats = {}

        total_positive = sum(1 for label in y if label == positive_label)
        total_samples = len(y)

        for group in groups:
            group_indices = [i for i, s in enumerate(sensitive_attribute) if s == group]
            group_size = len(group_indices)
            group_positive = sum(1 for i in group_indices if y[i] == positive_label)

            group_stats[group] = {
                'size': group_size,
                'positive': group_positive,
                'negative': group_size - group_positive
            }

        # Calculate weights for each sample
        weights = []

        for i in range(len(y)):
            group = sensitive_attribute[i]
            label = y[i]

            # Calculate expected proportion
            expected_positive = total_positive / total_samples
            expected_negative = 1 - expected_positive

            # Calculate group proportions
            group_size = group_stats[group]['size']

            if label == positive_label:
                # Positive sample
                actual_proportion = group_stats[group]['positive'] / group_size
                weight = expected_positive / actual_proportion if actual_proportion > 0 else 1.0
            else:
                # Negative sample
                actual_proportion = group_stats[group]['negative'] / group_size
                weight = expected_negative / actual_proportion if actual_proportion > 0 else 1.0

            weights.append(weight)

        logger.info(f"Reweighting complete: weight range [{min(weights):.2f}, {max(weights):.2f}]")

        return weights

    def resample_for_balance(
        self,
        X: List[Any],
        y: List[int],
        sensitive_attribute: List[Any],
        strategy: str = 'oversample',
        random_seed: int = 42
    ) -> Tuple[List[Any], List[int], List[Any]]:
        """
        Resample dataset to balance sensitive attribute distribution

        Pre-processing technique: modify dataset

        Args:
            X: Features
            y: Labels
            sensitive_attribute: Protected attribute values
            strategy: 'oversample' or 'undersample'
            random_seed: Random seed for reproducibility

        Returns:
            Resampled (X, y, sensitive_attribute)
        """
        random.seed(random_seed)

        logger.info(f"Resampling dataset using {strategy} strategy")

        # Group samples
        groups = {}
        for i in range(len(X)):
            group = sensitive_attribute[i]
            if group not in groups:
                groups[group] = []
            groups[group].append(i)

        # Determine target size
        if strategy == 'oversample':
            target_size = max(len(indices) for indices in groups.values())
        elif strategy == 'undersample':
            target_size = min(len(indices) for indices in groups.values())
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        # Resample each group
        resampled_indices = []

        for group, indices in groups.items():
            if len(indices) < target_size:
                # Oversample
                additional = random.choices(indices, k=target_size - len(indices))
                resampled_indices.extend(indices + additional)
            elif len(indices) > target_size:
                # Undersample
                sampled = random.sample(indices, k=target_size)
                resampled_indices.extend(sampled)
            else:
                resampled_indices.extend(indices)

        # Shuffle
        random.shuffle(resampled_indices)

        # Create resampled dataset
        X_resampled = [X[i] for i in resampled_indices]
        y_resampled = [y[i] for i in resampled_indices]
        sensitive_resampled = [sensitive_attribute[i] for i in resampled_indices]

        logger.info(f"Resampling complete: {len(X)} → {len(X_resampled)} samples")

        return X_resampled, y_resampled, sensitive_resampled

    def adjust_thresholds(
        self,
        y_prob: List[float],
        sensitive_attribute: List[Any],
        target_metric: str = 'demographic_parity',
        num_thresholds: int = 100
    ) -> Dict[Any, float]:
        """
        Calculate optimal decision thresholds per group

        Post-processing technique: adjust thresholds after prediction

        Args:
            y_prob: Predicted probabilities
            sensitive_attribute: Protected attribute values
            target_metric: Fairness metric to optimize
            num_thresholds: Number of thresholds to try

        Returns:
            Dictionary mapping groups to optimal thresholds
        """
        logger.info(f"Calculating optimal thresholds for {target_metric}")

        groups = set(sensitive_attribute)

        # For simplicity, use same threshold for all groups initially
        # In practice, use grid search to optimize per-group thresholds

        # Calculate overall positive rate
        thresholds = [i / num_thresholds for i in range(num_thresholds + 1)]

        group_thresholds = {}

        if target_metric == 'demographic_parity':
            # Find thresholds that equalize positive prediction rates

            # Calculate target positive rate (overall)
            target_rate = 0.5  # Can be calculated from data

            for group in groups:
                group_indices = [i for i, s in enumerate(sensitive_attribute) if s == group]
                group_probs = [y_prob[i] for i in group_indices]

                # Find threshold closest to target rate
                best_threshold = 0.5
                best_diff = float('inf')

                for threshold in thresholds:
                    positive_count = sum(1 for p in group_probs if p >= threshold)
                    rate = positive_count / len(group_probs) if group_probs else 0

                    diff = abs(rate - target_rate)
                    if diff < best_diff:
                        best_diff = diff
                        best_threshold = threshold

                group_thresholds[group] = best_threshold

        else:
            # Default: same threshold for all
            for group in groups:
                group_thresholds[group] = 0.5

        logger.info(f"Threshold adjustment complete: {group_thresholds}")

        return group_thresholds

    def generate_mitigation_plan(
        self,
        violations: List[Dict[str, Any]],
        group_metrics: Dict[Any, Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive bias mitigation plan

        Args:
            violations: List of fairness violations
            group_metrics: Performance metrics per group

        Returns:
            Mitigation plan
        """
        logger.info("Generating bias mitigation plan")

        plan = {
            'priority': self._determine_priority(violations),
            'techniques': {
                'pre_processing': [],
                'in_processing': [],
                'post_processing': []
            },
            'timeline': 'immediate' if len(violations) > 3 else 'short_term',
            'estimated_effort': self._estimate_effort(violations)
        }

        # Recommend pre-processing techniques
        if any(v['metric'] == 'demographic_parity_difference' for v in violations):
            plan['techniques']['pre_processing'].extend([
                'Reweight training samples to balance demographic distribution',
                'Oversample underrepresented groups',
                'Collect more data from underrepresented groups'
            ])

        # Recommend in-processing techniques
        if len(violations) >= 2:
            plan['techniques']['in_processing'].extend([
                'Use fairness-constrained optimization',
                'Apply adversarial debiasing during training',
                'Incorporate fairness regularization in loss function'
            ])

        # Recommend post-processing techniques
        if any(v['metric'] == 'equalized_odds_difference' for v in violations):
            plan['techniques']['post_processing'].extend([
                'Calibrate predictions per demographic group',
                'Adjust decision thresholds per group',
                'Apply equalized odds post-processing'
            ])

        return plan

    def _determine_priority(self, violations: List[Dict[str, Any]]) -> str:
        """Determine mitigation priority"""
        if len(violations) >= 4:
            return 'critical'
        elif len(violations) >= 2:
            return 'high'
        elif len(violations) >= 1:
            return 'medium'
        else:
            return 'low'

    def _estimate_effort(self, violations: List[Dict[str, Any]]) -> str:
        """Estimate implementation effort"""
        if len(violations) >= 3:
            return 'high (2-4 weeks)'
        elif len(violations) >= 1:
            return 'medium (1-2 weeks)'
        else:
            return 'low (< 1 week)'


class FairnessOptimizer:
    """
    Optimize model for fairness

    Features:
    - Multi-objective optimization (accuracy + fairness)
    - Fairness-aware hyperparameter tuning
    - Trade-off analysis
    """

    def __init__(self):
        """Initialize fairness optimizer"""
        self.mitigation = BiasMitigation()

    def optimize_threshold(
        self,
        y_true: List[int],
        y_prob: List[float],
        sensitive_attribute: List[Any],
        fairness_metric: str = 'demographic_parity',
        accuracy_threshold: float = 0.80
    ) -> Dict[str, Any]:
        """
        Find optimal threshold balancing accuracy and fairness

        Args:
            y_true: Ground truth labels
            y_prob: Predicted probabilities
            sensitive_attribute: Protected attribute values
            fairness_metric: Target fairness metric
            accuracy_threshold: Minimum acceptable accuracy

        Returns:
            Optimization result
        """
        logger.info(f"Optimizing threshold for {fairness_metric}")

        # Try different thresholds
        thresholds = [i / 100 for i in range(1, 100)]

        results = []

        for threshold in thresholds:
            # Convert probabilities to predictions
            y_pred = [1 if p >= threshold else 0 for p in y_prob]

            # Calculate accuracy
            correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
            accuracy = correct / len(y_true)

            # Skip if below accuracy threshold
            if accuracy < accuracy_threshold:
                continue

            # Calculate fairness metric (simplified)
            # In practice, use FairnessMetrics class
            groups = set(sensitive_attribute)
            group_rates = {}

            for group in groups:
                group_indices = [i for i, s in enumerate(sensitive_attribute) if s == group]
                group_preds = [y_pred[i] for i in group_indices]
                positive_rate = sum(group_preds) / len(group_preds) if group_preds else 0
                group_rates[group] = positive_rate

            # Calculate fairness disparity
            if len(group_rates) > 1:
                rates = list(group_rates.values())
                fairness_disparity = max(rates) - min(rates)
            else:
                fairness_disparity = 0.0

            results.append({
                'threshold': threshold,
                'accuracy': accuracy,
                'fairness_disparity': fairness_disparity,
                'score': accuracy - fairness_disparity  # Simple combined score
            })

        # Find best threshold
        if results:
            best = max(results, key=lambda x: x['score'])
        else:
            best = {'threshold': 0.5, 'accuracy': 0.0, 'fairness_disparity': 0.0, 'score': 0.0}

        logger.info(
            f"Optimal threshold: {best['threshold']:.2f} "
            f"(accuracy: {best['accuracy']:.3f}, disparity: {best['fairness_disparity']:.3f})"
        )

        return best

    def analyze_tradeoffs(
        self,
        y_true: List[int],
        y_prob: List[float],
        sensitive_attribute: List[Any]
    ) -> Dict[str, Any]:
        """
        Analyze accuracy-fairness trade-offs

        Args:
            y_true: Ground truth labels
            y_prob: Predicted probabilities
            sensitive_attribute: Protected attribute values

        Returns:
            Trade-off analysis
        """
        logger.info("Analyzing accuracy-fairness trade-offs")

        thresholds = [i / 20 for i in range(1, 20)]  # 0.05 to 0.95

        tradeoff_points = []

        for threshold in thresholds:
            y_pred = [1 if p >= threshold else 0 for p in y_prob]

            # Accuracy
            accuracy = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp) / len(y_true)

            # Fairness disparity
            groups = set(sensitive_attribute)
            group_rates = {}

            for group in groups:
                group_indices = [i for i, s in enumerate(sensitive_attribute) if s == group]
                group_preds = [y_pred[i] for i in group_indices]
                positive_rate = sum(group_preds) / len(group_preds) if group_preds else 0
                group_rates[group] = positive_rate

            if len(group_rates) > 1:
                rates = list(group_rates.values())
                fairness_disparity = max(rates) - min(rates)
            else:
                fairness_disparity = 0.0

            tradeoff_points.append({
                'threshold': threshold,
                'accuracy': accuracy,
                'fairness_disparity': fairness_disparity
            })

        return {
            'tradeoff_points': tradeoff_points,
            'best_accuracy': max(tradeoff_points, key=lambda x: x['accuracy']),
            'best_fairness': min(tradeoff_points, key=lambda x: x['fairness_disparity']),
            'balanced': min(tradeoff_points, key=lambda x: abs(x['accuracy'] - (1 - x['fairness_disparity'])))
        }
