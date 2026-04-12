"""
Fairness and Bias Metrics

Calculate various fairness metrics for ML models

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from collections import Counter

logger = logging.getLogger(__name__)


@dataclass
class BiasMetrics:
    """Container for bias metrics"""
    demographic_parity_difference: float
    equalized_odds_difference: float
    disparate_impact_ratio: float
    statistical_parity_difference: float
    equal_opportunity_difference: float
    predictive_parity_difference: float

    def to_dict(self) -> Dict[str, float]:
        return {
            'demographic_parity_difference': self.demographic_parity_difference,
            'equalized_odds_difference': self.equalized_odds_difference,
            'disparate_impact_ratio': self.disparate_impact_ratio,
            'statistical_parity_difference': self.statistical_parity_difference,
            'equal_opportunity_difference': self.equal_opportunity_difference,
            'predictive_parity_difference': self.predictive_parity_difference
        }


class FairnessMetrics:
    """
    Calculate fairness metrics for binary classification

    Supports multiple fairness definitions:
    - Demographic Parity (Statistical Parity)
    - Equalized Odds
    - Equal Opportunity
    - Predictive Parity
    - Disparate Impact
    """

    def __init__(self):
        """Initialize fairness metrics calculator"""
        pass

    def calculate_all_metrics(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        positive_label: int = 1,
        privileged_group: Optional[Any] = None
    ) -> BiasMetrics:
        """
        Calculate all fairness metrics

        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            sensitive_attribute: Protected attribute values (e.g., gender, race)
            positive_label: Label considered positive
            privileged_group: Value of privileged group (auto-detected if None)

        Returns:
            BiasMetrics object
        """
        logger.info(f"Calculating fairness metrics for {len(y_true)} samples")

        # Auto-detect privileged group if not provided
        if privileged_group is None:
            privileged_group = self._detect_privileged_group(
                y_true, y_pred, sensitive_attribute, positive_label
            )

        # Calculate individual metrics
        dpd = self.demographic_parity_difference(
            y_pred, sensitive_attribute, privileged_group, positive_label
        )

        eod = self.equalized_odds_difference(
            y_true, y_pred, sensitive_attribute, privileged_group, positive_label
        )

        dir = self.disparate_impact_ratio(
            y_pred, sensitive_attribute, privileged_group, positive_label
        )

        spd = self.statistical_parity_difference(
            y_pred, sensitive_attribute, privileged_group, positive_label
        )

        eopd = self.equal_opportunity_difference(
            y_true, y_pred, sensitive_attribute, privileged_group, positive_label
        )

        ppd = self.predictive_parity_difference(
            y_true, y_pred, sensitive_attribute, privileged_group, positive_label
        )

        metrics = BiasMetrics(
            demographic_parity_difference=dpd,
            equalized_odds_difference=eod,
            disparate_impact_ratio=dir,
            statistical_parity_difference=spd,
            equal_opportunity_difference=eopd,
            predictive_parity_difference=ppd
        )

        logger.info("Fairness metrics calculated successfully")

        return metrics

    def demographic_parity_difference(
        self,
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        positive_label: int = 1
    ) -> float:
        """
        Demographic Parity Difference (DPD)

        Measures difference in positive prediction rates between groups.
        Fair if close to 0.

        DPD = P(Y_pred=1 | Privileged) - P(Y_pred=1 | Unprivileged)
        """
        privileged_rate = self._positive_rate(
            y_pred, sensitive_attribute, privileged_group, positive_label
        )

        unprivileged_rate = self._positive_rate_unprivileged(
            y_pred, sensitive_attribute, privileged_group, positive_label
        )

        return privileged_rate - unprivileged_rate

    def statistical_parity_difference(
        self,
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        positive_label: int = 1
    ) -> float:
        """
        Statistical Parity Difference (same as Demographic Parity)
        """
        return self.demographic_parity_difference(
            y_pred, sensitive_attribute, privileged_group, positive_label
        )

    def disparate_impact_ratio(
        self,
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        positive_label: int = 1
    ) -> float:
        """
        Disparate Impact Ratio (DIR)

        Ratio of positive prediction rates between groups.
        Fair if close to 1. Legal threshold often 0.8 (80% rule).

        DIR = P(Y_pred=1 | Unprivileged) / P(Y_pred=1 | Privileged)
        """
        privileged_rate = self._positive_rate(
            y_pred, sensitive_attribute, privileged_group, positive_label
        )

        unprivileged_rate = self._positive_rate_unprivileged(
            y_pred, sensitive_attribute, privileged_group, positive_label
        )

        if privileged_rate == 0:
            return 0.0

        return unprivileged_rate / privileged_rate

    def equalized_odds_difference(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        positive_label: int = 1
    ) -> float:
        """
        Equalized Odds Difference (EOD)

        Average of TPR difference and FPR difference.
        Fair if close to 0.

        EOD = 0.5 * (|TPR_diff| + |FPR_diff|)
        """
        tpr_diff = self._tpr_difference(
            y_true, y_pred, sensitive_attribute, privileged_group, positive_label
        )

        fpr_diff = self._fpr_difference(
            y_true, y_pred, sensitive_attribute, privileged_group, positive_label
        )

        return 0.5 * (abs(tpr_diff) + abs(fpr_diff))

    def equal_opportunity_difference(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        positive_label: int = 1
    ) -> float:
        """
        Equal Opportunity Difference (EOPD)

        Difference in True Positive Rates between groups.
        Fair if close to 0.

        EOPD = TPR_privileged - TPR_unprivileged
        """
        return self._tpr_difference(
            y_true, y_pred, sensitive_attribute, privileged_group, positive_label
        )

    def predictive_parity_difference(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        positive_label: int = 1
    ) -> float:
        """
        Predictive Parity Difference (PPD)

        Difference in Positive Predictive Values (Precision) between groups.
        Fair if close to 0.

        PPD = PPV_privileged - PPV_unprivileged
        """
        ppv_privileged = self._ppv(
            y_true, y_pred, sensitive_attribute, privileged_group, True, positive_label
        )

        ppv_unprivileged = self._ppv(
            y_true, y_pred, sensitive_attribute, privileged_group, False, positive_label
        )

        return ppv_privileged - ppv_unprivileged

    # Helper methods

    def _detect_privileged_group(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        positive_label: int
    ) -> Any:
        """Auto-detect privileged group (group with higher positive rate)"""
        groups = set(sensitive_attribute)

        group_rates = {}
        for group in groups:
            rate = self._positive_rate(y_pred, sensitive_attribute, group, positive_label)
            group_rates[group] = rate

        privileged = max(group_rates.items(), key=lambda x: x[1])[0]

        logger.info(f"Auto-detected privileged group: {privileged}")

        return privileged

    def _positive_rate(
        self,
        y_pred: List[int],
        sensitive_attribute: List[Any],
        group_value: Any,
        positive_label: int
    ) -> float:
        """Calculate positive prediction rate for a group"""
        group_indices = [i for i, s in enumerate(sensitive_attribute) if s == group_value]

        if not group_indices:
            return 0.0

        group_predictions = [y_pred[i] for i in group_indices]
        positive_count = sum(1 for p in group_predictions if p == positive_label)

        return positive_count / len(group_predictions)

    def _positive_rate_unprivileged(
        self,
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        positive_label: int
    ) -> float:
        """Calculate average positive rate for unprivileged groups"""
        groups = set(sensitive_attribute)
        unprivileged_groups = groups - {privileged_group}

        if not unprivileged_groups:
            return 0.0

        rates = []
        for group in unprivileged_groups:
            rate = self._positive_rate(y_pred, sensitive_attribute, group, positive_label)
            rates.append(rate)

        return sum(rates) / len(rates) if rates else 0.0

    def _tpr_difference(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        positive_label: int
    ) -> float:
        """Calculate TPR difference between privileged and unprivileged"""
        tpr_privileged = self._tpr(
            y_true, y_pred, sensitive_attribute, privileged_group, True, positive_label
        )

        tpr_unprivileged = self._tpr(
            y_true, y_pred, sensitive_attribute, privileged_group, False, positive_label
        )

        return tpr_privileged - tpr_unprivileged

    def _fpr_difference(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        positive_label: int
    ) -> float:
        """Calculate FPR difference between privileged and unprivileged"""
        fpr_privileged = self._fpr(
            y_true, y_pred, sensitive_attribute, privileged_group, True, positive_label
        )

        fpr_unprivileged = self._fpr(
            y_true, y_pred, sensitive_attribute, privileged_group, False, positive_label
        )

        return fpr_privileged - fpr_unprivileged

    def _tpr(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        is_privileged: bool,
        positive_label: int
    ) -> float:
        """Calculate True Positive Rate for a group"""
        if is_privileged:
            indices = [i for i, s in enumerate(sensitive_attribute) if s == privileged_group]
        else:
            indices = [i for i, s in enumerate(sensitive_attribute) if s != privileged_group]

        if not indices:
            return 0.0

        # True positives: y_true=1 and y_pred=1
        tp = sum(1 for i in indices if y_true[i] == positive_label and y_pred[i] == positive_label)

        # Actual positives: y_true=1
        p = sum(1 for i in indices if y_true[i] == positive_label)

        return tp / p if p > 0 else 0.0

    def _fpr(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        is_privileged: bool,
        positive_label: int
    ) -> float:
        """Calculate False Positive Rate for a group"""
        if is_privileged:
            indices = [i for i, s in enumerate(sensitive_attribute) if s == privileged_group]
        else:
            indices = [i for i, s in enumerate(sensitive_attribute) if s != privileged_group]

        if not indices:
            return 0.0

        # False positives: y_true=0 and y_pred=1
        fp = sum(1 for i in indices if y_true[i] != positive_label and y_pred[i] == positive_label)

        # Actual negatives: y_true=0
        n = sum(1 for i in indices if y_true[i] != positive_label)

        return fp / n if n > 0 else 0.0

    def _ppv(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        privileged_group: Any,
        is_privileged: bool,
        positive_label: int
    ) -> float:
        """Calculate Positive Predictive Value (Precision) for a group"""
        if is_privileged:
            indices = [i for i, s in enumerate(sensitive_attribute) if s == privileged_group]
        else:
            indices = [i for i, s in enumerate(sensitive_attribute) if s != privileged_group]

        if not indices:
            return 0.0

        # True positives: y_true=1 and y_pred=1
        tp = sum(1 for i in indices if y_true[i] == positive_label and y_pred[i] == positive_label)

        # Predicted positives: y_pred=1
        pp = sum(1 for i in indices if y_pred[i] == positive_label)

        return tp / pp if pp > 0 else 0.0

    def calculate_group_metrics(
        self,
        y_true: List[int],
        y_pred: List[int],
        sensitive_attribute: List[Any],
        positive_label: int = 1
    ) -> Dict[Any, Dict[str, float]]:
        """
        Calculate performance metrics for each demographic group

        Returns:
            Dictionary mapping group values to metrics
        """
        groups = set(sensitive_attribute)
        group_metrics = {}

        for group in groups:
            indices = [i for i, s in enumerate(sensitive_attribute) if s == group]

            if not indices:
                continue

            # Calculate metrics for this group
            group_y_true = [y_true[i] for i in indices]
            group_y_pred = [y_pred[i] for i in indices]

            tp = sum(1 for yt, yp in zip(group_y_true, group_y_pred)
                    if yt == positive_label and yp == positive_label)
            fp = sum(1 for yt, yp in zip(group_y_true, group_y_pred)
                    if yt != positive_label and yp == positive_label)
            tn = sum(1 for yt, yp in zip(group_y_true, group_y_pred)
                    if yt != positive_label and yp != positive_label)
            fn = sum(1 for yt, yp in zip(group_y_true, group_y_pred)
                    if yt == positive_label and yp != positive_label)

            accuracy = (tp + tn) / len(indices) if len(indices) > 0 else 0.0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

            group_metrics[group] = {
                'size': len(indices),
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'tp': tp,
                'fp': fp,
                'tn': tn,
                'fn': fn
            }

        logger.info(f"Calculated metrics for {len(group_metrics)} demographic groups")

        return group_metrics
