"""
AEVA-Bench Metric Calculators

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Any, List, Dict
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    mean_squared_error,
    mean_absolute_error,
)


class MetricCalculator:
    """
    Unified metric calculation interface

    Provides standardized metrics for various tasks:
    - Classification metrics
    - Regression metrics
    - Ranking metrics
    - Custom metrics
    """

    @staticmethod
    def accuracy(y_true: Any, y_pred: Any, **kwargs) -> float:
        """Calculate accuracy"""
        return float(accuracy_score(y_true, y_pred, **kwargs))

    @staticmethod
    def precision(y_true: Any, y_pred: Any, **kwargs) -> float:
        """Calculate precision"""
        return float(precision_score(y_true, y_pred, average='weighted', **kwargs))

    @staticmethod
    def recall(y_true: Any, y_pred: Any, **kwargs) -> float:
        """Calculate recall"""
        return float(recall_score(y_true, y_pred, average='weighted', **kwargs))

    @staticmethod
    def f1(y_true: Any, y_pred: Any, **kwargs) -> float:
        """Calculate F1 score"""
        return float(f1_score(y_true, y_pred, average='weighted', **kwargs))

    @staticmethod
    def roc_auc(y_true: Any, y_score: Any, **kwargs) -> float:
        """Calculate ROC AUC score"""
        try:
            return float(roc_auc_score(y_true, y_score, **kwargs))
        except ValueError:
            # Handle binary classification case
            return float(roc_auc_score(y_true, y_score, average='weighted', multi_class='ovr', **kwargs))

    @staticmethod
    def mse(y_true: Any, y_pred: Any, **kwargs) -> float:
        """Calculate Mean Squared Error"""
        return float(mean_squared_error(y_true, y_pred, **kwargs))

    @staticmethod
    def rmse(y_true: Any, y_pred: Any, **kwargs) -> float:
        """Calculate Root Mean Squared Error"""
        return float(np.sqrt(mean_squared_error(y_true, y_pred, **kwargs)))

    @staticmethod
    def mae(y_true: Any, y_pred: Any, **kwargs) -> float:
        """Calculate Mean Absolute Error"""
        return float(mean_absolute_error(y_true, y_pred, **kwargs))

    @staticmethod
    def r2_score(y_true: Any, y_pred: Any, **kwargs) -> float:
        """Calculate R² score"""
        from sklearn.metrics import r2_score as sklearn_r2
        return float(sklearn_r2(y_true, y_pred, **kwargs))

    @staticmethod
    def confusion_matrix(y_true: Any, y_pred: Any, **kwargs) -> np.ndarray:
        """Calculate confusion matrix"""
        from sklearn.metrics import confusion_matrix as sklearn_cm
        return sklearn_cm(y_true, y_pred, **kwargs)

    @staticmethod
    def calculate_all_classification(y_true: Any, y_pred: Any, y_score: Any = None) -> Dict[str, float]:
        """
        Calculate all common classification metrics

        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_score: Prediction scores (for ROC AUC)

        Returns:
            Dictionary of metric values
        """
        metrics = {
            "accuracy": MetricCalculator.accuracy(y_true, y_pred),
            "precision": MetricCalculator.precision(y_true, y_pred),
            "recall": MetricCalculator.recall(y_true, y_pred),
            "f1_score": MetricCalculator.f1(y_true, y_pred),
        }

        if y_score is not None:
            try:
                metrics["roc_auc"] = MetricCalculator.roc_auc(y_true, y_score)
            except Exception:
                pass

        return metrics

    @staticmethod
    def calculate_all_regression(y_true: Any, y_pred: Any) -> Dict[str, float]:
        """
        Calculate all common regression metrics

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            Dictionary of metric values
        """
        return {
            "mse": MetricCalculator.mse(y_true, y_pred),
            "rmse": MetricCalculator.rmse(y_true, y_pred),
            "mae": MetricCalculator.mae(y_true, y_pred),
            "r2_score": MetricCalculator.r2_score(y_true, y_pred),
        }
