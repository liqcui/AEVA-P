"""
Feature Importance Analyzer

Provides multiple methods for analyzing feature importance including:
- Permutation importance
- Drop-column importance
- Model-specific importance (for tree-based models)
- SHAP-based importance

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import numpy as np
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class FeatureImportance:
    """
    Container for feature importance results

    Attributes:
        importance_scores: Dictionary mapping feature names to importance scores
        method: Method used to compute importance
        feature_names: Names of features
        rankings: Rank of each feature (1 = most important)
        metadata: Additional metadata
    """
    importance_scores: Dict[str, float]
    method: str
    feature_names: List[str]
    rankings: Optional[Dict[str, int]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Calculate rankings after initialization"""
        if self.rankings is None:
            self.rankings = self._calculate_rankings()

    def _calculate_rankings(self) -> Dict[str, int]:
        """Calculate feature rankings based on importance scores"""
        sorted_features = sorted(
            self.importance_scores.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        return {feature: rank + 1 for rank, (feature, _) in enumerate(sorted_features)}

    def get_top_features(self, n: int = 10) -> List[tuple]:
        """
        Get top N most important features

        Args:
            n: Number of top features

        Returns:
            List of (feature_name, importance_score, rank) tuples
        """
        sorted_features = sorted(
            self.importance_scores.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:n]

        return [
            (name, score, self.rankings[name])
            for name, score in sorted_features
        ]


class FeatureImportanceAnalyzer:
    """
    Analyze feature importance using multiple methods

    Supports:
    - Permutation importance (model-agnostic)
    - Drop-column importance (model-agnostic)
    - Model-specific importance (tree-based models)
    - SHAP-based importance

    Example:
        >>> analyzer = FeatureImportanceAnalyzer(model, X_test, y_test)
        >>> importance = analyzer.permutation_importance()
        >>> print(importance.get_top_features(5))
    """

    def __init__(
        self,
        model: Any,
        X: np.ndarray,
        y: np.ndarray,
        feature_names: Optional[List[str]] = None,
        scoring: Optional[Callable] = None
    ):
        """
        Initialize feature importance analyzer

        Args:
            model: Trained model
            X: Input features
            y: Target values
            feature_names: Names of features
            scoring: Scoring function (default: accuracy for classification, R² for regression)
        """
        self.model = model
        self.X = X
        self.y = y
        self.scoring = scoring

        # Setup feature names
        if feature_names is None:
            self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        else:
            self.feature_names = feature_names

        # Auto-detect scoring function if not provided
        if self.scoring is None:
            self.scoring = self._auto_detect_scoring()

    def _auto_detect_scoring(self) -> Callable:
        """Auto-detect appropriate scoring function"""
        from sklearn.metrics import accuracy_score, r2_score

        # Check if classification or regression
        if hasattr(self.model, 'predict_proba'):
            # Classification
            def scoring_fn(y_true, y_pred):
                return accuracy_score(y_true, y_pred)
        else:
            # Regression
            def scoring_fn(y_true, y_pred):
                return r2_score(y_true, y_pred)

        return scoring_fn

    def permutation_importance(
        self,
        n_repeats: int = 10,
        random_state: Optional[int] = None
    ) -> FeatureImportance:
        """
        Calculate permutation importance

        Measures importance by shuffling each feature and measuring
        the decrease in model performance.

        Args:
            n_repeats: Number of times to permute each feature
            random_state: Random seed

        Returns:
            Feature importance results
        """
        logger.info("Calculating permutation importance...")

        # Get baseline score
        y_pred = self.model.predict(self.X)
        baseline_score = self.scoring(self.y, y_pred)

        # Calculate importance for each feature
        importances = {}
        rng = np.random.RandomState(random_state)

        for i, feature_name in enumerate(self.feature_names):
            scores = []

            for _ in range(n_repeats):
                # Create copy of data
                X_permuted = self.X.copy()

                # Permute feature i
                X_permuted[:, i] = rng.permutation(X_permuted[:, i])

                # Get score with permuted feature
                y_pred_permuted = self.model.predict(X_permuted)
                permuted_score = self.scoring(self.y, y_pred_permuted)

                # Importance = decrease in score
                scores.append(baseline_score - permuted_score)

            # Average over repeats
            importances[feature_name] = np.mean(scores)

        return FeatureImportance(
            importance_scores=importances,
            method='permutation',
            feature_names=self.feature_names,
            metadata={
                'n_repeats': n_repeats,
                'baseline_score': baseline_score
            }
        )

    def drop_column_importance(self) -> FeatureImportance:
        """
        Calculate drop-column importance

        Measures importance by removing each feature and retraining
        the model (expensive but accurate).

        Returns:
            Feature importance results
        """
        logger.info("Calculating drop-column importance (may be slow)...")

        # Get baseline score
        y_pred = self.model.predict(self.X)
        baseline_score = self.scoring(self.y, y_pred)

        importances = {}

        for i, feature_name in enumerate(self.feature_names):
            # Create dataset without feature i
            X_dropped = np.delete(self.X, i, axis=1)

            # Clone and retrain model
            try:
                from sklearn.base import clone
                model_dropped = clone(self.model)
                model_dropped.fit(X_dropped, self.y)

                # Get score without feature
                y_pred_dropped = model_dropped.predict(X_dropped)
                dropped_score = self.scoring(self.y, y_pred_dropped)

                # Importance = decrease in score
                importances[feature_name] = baseline_score - dropped_score

            except Exception as e:
                logger.warning(f"Failed to compute drop-column importance for {feature_name}: {e}")
                importances[feature_name] = 0.0

        return FeatureImportance(
            importance_scores=importances,
            method='drop_column',
            feature_names=self.feature_names,
            metadata={'baseline_score': baseline_score}
        )

    def model_importance(self) -> Optional[FeatureImportance]:
        """
        Get model-specific feature importance (for tree-based models)

        Returns:
            Feature importance results, or None if not supported
        """
        if not hasattr(self.model, 'feature_importances_'):
            logger.warning("Model does not have feature_importances_ attribute")
            return None

        logger.info("Extracting model-specific feature importance...")

        importances = dict(zip(
            self.feature_names,
            self.model.feature_importances_
        ))

        return FeatureImportance(
            importance_scores=importances,
            method='model_specific',
            feature_names=self.feature_names
        )

    def shap_importance(
        self,
        background_data: Optional[np.ndarray] = None,
        max_samples: int = 100
    ) -> FeatureImportance:
        """
        Calculate SHAP-based feature importance

        Args:
            background_data: Background data for SHAP explainer
            max_samples: Maximum samples to use

        Returns:
            Feature importance results
        """
        try:
            from aeva.explainability.shap_explainer import SHAPExplainer
        except ImportError:
            logger.error("SHAP explainer not available")
            return None

        logger.info("Calculating SHAP-based importance...")

        # Use subset of X as background if not provided
        if background_data is None:
            if len(self.X) > max_samples:
                indices = np.random.choice(len(self.X), max_samples, replace=False)
                background_data = self.X[indices]
            else:
                background_data = self.X

        # Create SHAP explainer
        explainer = SHAPExplainer(
            model=self.model,
            background_data=background_data,
            feature_names=self.feature_names
        )

        # Get feature importance
        importance_dict = explainer.get_feature_importance(self.X[:max_samples])

        return FeatureImportance(
            importance_scores=importance_dict,
            method='shap',
            feature_names=self.feature_names,
            metadata={'max_samples': max_samples}
        )

    def compare_methods(
        self,
        methods: Optional[List[str]] = None
    ) -> Dict[str, FeatureImportance]:
        """
        Compare multiple importance calculation methods

        Args:
            methods: List of methods to compare
                   Options: 'permutation', 'model', 'shap'
                   Default: all available methods

        Returns:
            Dictionary mapping method names to importance results
        """
        if methods is None:
            methods = ['permutation', 'model', 'shap']

        results = {}

        for method in methods:
            if method == 'permutation':
                results['permutation'] = self.permutation_importance()
            elif method == 'model':
                importance = self.model_importance()
                if importance is not None:
                    results['model'] = importance
            elif method == 'shap':
                try:
                    results['shap'] = self.shap_importance()
                except Exception as e:
                    logger.warning(f"Failed to compute SHAP importance: {e}")
            else:
                logger.warning(f"Unknown method: {method}")

        return results

    def aggregate_importances(
        self,
        importances: Dict[str, FeatureImportance],
        method: str = 'mean'
    ) -> FeatureImportance:
        """
        Aggregate multiple importance results

        Args:
            importances: Dictionary of importance results
            method: Aggregation method ('mean', 'median', 'rank_average')

        Returns:
            Aggregated feature importance
        """
        # Collect scores for each feature
        feature_scores = defaultdict(list)

        for imp_result in importances.values():
            for feature, score in imp_result.importance_scores.items():
                feature_scores[feature].append(score)

        # Aggregate scores
        aggregated_scores = {}

        if method == 'mean':
            for feature, scores in feature_scores.items():
                aggregated_scores[feature] = np.mean(scores)

        elif method == 'median':
            for feature, scores in feature_scores.items():
                aggregated_scores[feature] = np.median(scores)

        elif method == 'rank_average':
            # Average of ranks across methods
            for feature in self.feature_names:
                ranks = [imp_result.rankings[feature] for imp_result in importances.values()]
                aggregated_scores[feature] = -np.mean(ranks)  # Negative for correct sorting

        else:
            raise ValueError(f"Unknown aggregation method: {method}")

        return FeatureImportance(
            importance_scores=aggregated_scores,
            method=f'aggregated_{method}',
            feature_names=self.feature_names,
            metadata={
                'methods_used': list(importances.keys()),
                'aggregation': method
            }
        )
