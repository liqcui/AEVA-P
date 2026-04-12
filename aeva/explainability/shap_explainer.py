"""
SHAP (SHapley Additive exPlanations) Explainer

Provides SHAP-based model explanations using game theory concepts.
Supports multiple explainer types for different model architectures.

References:
- Lundberg & Lee (2017): "A Unified Approach to Interpreting Model Predictions"
- SHAP documentation: https://shap.readthedocs.io/

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)


class SHAPExplainerType(Enum):
    """SHAP explainer types for different model architectures"""
    TREE = "tree"              # TreeExplainer for tree-based models
    LINEAR = "linear"          # LinearExplainer for linear models
    KERNEL = "kernel"          # KernelExplainer (model-agnostic, slower)
    DEEP = "deep"              # DeepExplainer for neural networks
    GRADIENT = "gradient"      # GradientExplainer for neural networks
    SAMPLING = "sampling"      # SamplingExplainer (model-agnostic)
    PARTITION = "partition"    # PartitionExplainer (model-agnostic)


@dataclass
class SHAPExplanation:
    """
    Container for SHAP explanation results

    Attributes:
        shap_values: SHAP values for each feature
        base_value: Expected value (average model output)
        feature_names: Names of features
        feature_values: Actual feature values for the instance
        data: Original data matrix
        interaction_values: SHAP interaction values (if computed)
        expected_value: Expected model output
        model_output: Actual model output
        metadata: Additional metadata
    """
    shap_values: np.ndarray
    base_value: Union[float, np.ndarray]
    feature_names: List[str]
    feature_values: Optional[np.ndarray] = None
    data: Optional[np.ndarray] = None
    interaction_values: Optional[np.ndarray] = None
    expected_value: Optional[float] = None
    model_output: Optional[Union[float, np.ndarray]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_top_features(self, n: int = 10, absolute: bool = True) -> List[tuple]:
        """
        Get top N most important features

        Args:
            n: Number of top features to return
            absolute: If True, use absolute SHAP values

        Returns:
            List of (feature_name, shap_value) tuples
        """
        if len(self.shap_values.shape) > 1:
            # Multi-output model, use mean across samples (axis=0)
            values = np.mean(np.abs(self.shap_values) if absolute else self.shap_values, axis=0)
        else:
            values = np.abs(self.shap_values) if absolute else self.shap_values

        # Ensure values is 1D
        if len(values.shape) > 1:
            values = values.flatten()

        # Get indices of top features
        top_indices = np.argsort(values)[-n:][::-1]

        return [(self.feature_names[int(i)], float(values[int(i)])) for i in top_indices]


class SHAPExplainer:
    """
    SHAP-based model explainer

    Provides both local (single instance) and global (entire dataset) explanations
    using SHAP values.

    Example:
        >>> explainer = SHAPExplainer(model, X_train)
        >>> explanation = explainer.explain_instance(X_test[0])
        >>> print(explanation.get_top_features(5))
    """

    def __init__(
        self,
        model: Any,
        background_data: Optional[np.ndarray] = None,
        explainer_type: Optional[SHAPExplainerType] = None,
        feature_names: Optional[List[str]] = None,
        **explainer_kwargs
    ):
        """
        Initialize SHAP explainer

        Args:
            model: Trained model to explain
            background_data: Background dataset for computing expectations
            explainer_type: Type of SHAP explainer (auto-detected if None)
            feature_names: Names of features
            **explainer_kwargs: Additional arguments for SHAP explainer
        """
        self.model = model
        self.background_data = background_data
        self.feature_names = feature_names
        self.explainer_type = explainer_type
        self.explainer_kwargs = explainer_kwargs

        # Try to import shap
        try:
            import shap
            self.shap = shap
        except ImportError:
            raise ImportError(
                "SHAP package is required. Install it with: pip install shap"
            )

        # Auto-detect feature names if not provided
        if self.feature_names is None and background_data is not None:
            self.feature_names = [f"feature_{i}" for i in range(background_data.shape[1])]

        # Initialize SHAP explainer
        self.explainer = self._create_explainer()

        logger.info(f"Initialized SHAP explainer: {self.explainer_type}")

    def _create_explainer(self) -> Any:
        """
        Create appropriate SHAP explainer based on model type

        Returns:
            SHAP explainer instance
        """
        # Auto-detect explainer type if not specified
        if self.explainer_type is None:
            self.explainer_type = self._auto_detect_explainer_type()

        # Create explainer based on type
        if self.explainer_type == SHAPExplainerType.TREE:
            return self.shap.TreeExplainer(self.model, **self.explainer_kwargs)

        elif self.explainer_type == SHAPExplainerType.LINEAR:
            return self.shap.LinearExplainer(self.model, self.background_data, **self.explainer_kwargs)

        elif self.explainer_type == SHAPExplainerType.KERNEL:
            return self.shap.KernelExplainer(self.model.predict, self.background_data, **self.explainer_kwargs)

        elif self.explainer_type == SHAPExplainerType.DEEP:
            return self.shap.DeepExplainer(self.model, self.background_data, **self.explainer_kwargs)

        elif self.explainer_type == SHAPExplainerType.GRADIENT:
            return self.shap.GradientExplainer(self.model, self.background_data, **self.explainer_kwargs)

        elif self.explainer_type == SHAPExplainerType.SAMPLING:
            return self.shap.SamplingExplainer(self.model.predict, self.background_data, **self.explainer_kwargs)

        elif self.explainer_type == SHAPExplainerType.PARTITION:
            return self.shap.PartitionExplainer(self.model.predict, self.background_data, **self.explainer_kwargs)

        else:
            raise ValueError(f"Unsupported explainer type: {self.explainer_type}")

    def _auto_detect_explainer_type(self) -> SHAPExplainerType:
        """
        Auto-detect appropriate SHAP explainer type based on model

        Returns:
            Detected explainer type
        """
        model_class = self.model.__class__.__name__

        # Tree-based models
        tree_models = [
            'RandomForestClassifier', 'RandomForestRegressor',
            'GradientBoostingClassifier', 'GradientBoostingRegressor',
            'XGBClassifier', 'XGBRegressor',
            'LGBMClassifier', 'LGBMRegressor',
            'CatBoostClassifier', 'CatBoostRegressor',
            'DecisionTreeClassifier', 'DecisionTreeRegressor'
        ]

        if model_class in tree_models:
            logger.info(f"Auto-detected tree-based model: {model_class}")
            return SHAPExplainerType.TREE

        # Linear models
        linear_models = [
            'LinearRegression', 'LogisticRegression',
            'Ridge', 'Lasso', 'ElasticNet'
        ]

        if model_class in linear_models:
            logger.info(f"Auto-detected linear model: {model_class}")
            return SHAPExplainerType.LINEAR

        # Default to Kernel explainer (model-agnostic but slower)
        logger.info(f"Using KernelExplainer for model: {model_class}")
        return SHAPExplainerType.KERNEL

    def explain_instance(
        self,
        instance: np.ndarray,
        check_additivity: bool = False
    ) -> SHAPExplanation:
        """
        Explain a single instance using SHAP values

        Args:
            instance: Single instance to explain (1D or 2D array)
            check_additivity: Whether to check SHAP additivity property

        Returns:
            SHAP explanation for the instance
        """
        # Ensure instance is 2D
        if len(instance.shape) == 1:
            instance = instance.reshape(1, -1)

        # Compute SHAP values
        try:
            shap_values = self.explainer.shap_values(instance, check_additivity=check_additivity)
        except TypeError:
            # Some explainers don't support check_additivity
            shap_values = self.explainer.shap_values(instance)

        # Get base value (expected value)
        if hasattr(self.explainer, 'expected_value'):
            base_value = self.explainer.expected_value
        else:
            base_value = 0.0

        # Handle multi-class classification
        if isinstance(shap_values, list):
            # For multi-class, take first class for simplicity
            # In practice, you might want to explain specific class
            shap_values = shap_values[0]

        # Ensure shap_values is 1D for single instance
        if len(shap_values.shape) > 1 and shap_values.shape[0] == 1:
            shap_values = shap_values[0]

        # Get model output
        try:
            if hasattr(self.model, 'predict_proba'):
                model_output = self.model.predict_proba(instance)[0]
            else:
                model_output = self.model.predict(instance)[0]
        except:
            model_output = None

        return SHAPExplanation(
            shap_values=shap_values,
            base_value=base_value,
            feature_names=self.feature_names,
            feature_values=instance[0],
            expected_value=base_value if isinstance(base_value, float) else base_value[0],
            model_output=model_output
        )

    def explain_global(
        self,
        X: np.ndarray,
        max_samples: Optional[int] = None
    ) -> SHAPExplanation:
        """
        Explain global feature importance across dataset

        Args:
            X: Dataset to explain (2D array)
            max_samples: Maximum number of samples to use (for efficiency)

        Returns:
            Global SHAP explanation
        """
        # Limit samples for efficiency
        if max_samples is not None and len(X) > max_samples:
            indices = np.random.choice(len(X), max_samples, replace=False)
            X = X[indices]

        logger.info(f"Computing global SHAP values for {len(X)} samples...")

        # Compute SHAP values
        try:
            shap_values = self.explainer.shap_values(X)
        except Exception as e:
            logger.error(f"Failed to compute SHAP values: {e}")
            raise

        # Get base value
        if hasattr(self.explainer, 'expected_value'):
            base_value = self.explainer.expected_value
        else:
            base_value = 0.0

        # Handle multi-class classification
        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        return SHAPExplanation(
            shap_values=shap_values,
            base_value=base_value,
            feature_names=self.feature_names,
            feature_values=None,
            data=X,
            metadata={'n_samples': len(X)}
        )

    def compute_interaction_values(
        self,
        instance: np.ndarray
    ) -> SHAPExplanation:
        """
        Compute SHAP interaction values (feature interactions)

        Args:
            instance: Single instance to explain

        Returns:
            SHAP explanation with interaction values
        """
        # Ensure instance is 2D
        if len(instance.shape) == 1:
            instance = instance.reshape(1, -1)

        # Check if explainer supports interaction values
        if not hasattr(self.explainer, 'shap_interaction_values'):
            raise ValueError(
                f"Explainer type {self.explainer_type} does not support interaction values. "
                "Use TreeExplainer for tree-based models."
            )

        logger.info("Computing SHAP interaction values...")

        # Compute interaction values
        interaction_values = self.explainer.shap_interaction_values(instance)

        # Compute main effects (diagonal of interaction matrix)
        if isinstance(interaction_values, list):
            interaction_values = interaction_values[0]

        main_effects = np.diag(interaction_values[0])

        # Get base value
        if hasattr(self.explainer, 'expected_value'):
            base_value = self.explainer.expected_value
        else:
            base_value = 0.0

        return SHAPExplanation(
            shap_values=main_effects,
            base_value=base_value,
            feature_names=self.feature_names,
            feature_values=instance[0],
            interaction_values=interaction_values,
            metadata={'has_interactions': True}
        )

    def get_feature_importance(
        self,
        X: np.ndarray,
        method: str = 'mean_abs'
    ) -> Dict[str, float]:
        """
        Get global feature importance using SHAP values

        Args:
            X: Dataset to compute importance on
            method: Method to aggregate SHAP values
                   'mean_abs': Mean of absolute SHAP values (default)
                   'mean': Mean of SHAP values (can cancel out)

        Returns:
            Dictionary mapping feature names to importance scores
        """
        # Compute SHAP values
        explanation = self.explain_global(X)

        # Aggregate SHAP values
        if method == 'mean_abs':
            importance = np.mean(np.abs(explanation.shap_values), axis=0)
        elif method == 'mean':
            importance = np.mean(explanation.shap_values, axis=0)
        else:
            raise ValueError(f"Unknown aggregation method: {method}")

        # Create importance dictionary
        importance_dict = {
            name: float(score)
            for name, score in zip(self.feature_names, importance)
        }

        # Sort by importance
        return dict(sorted(importance_dict.items(), key=lambda x: abs(x[1]), reverse=True))
