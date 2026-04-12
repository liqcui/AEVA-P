"""
LIME (Local Interpretable Model-agnostic Explanations) Explainer

Provides LIME-based local explanations by fitting interpretable models
to approximate the behavior of complex models locally.

References:
- Ribeiro et al. (2016): "Why Should I Trust You?" Explaining the Predictions
  of Any Classifier"
- LIME documentation: https://lime-ml.readthedocs.io/

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class LIMEExplanation:
    """
    Container for LIME explanation results

    Attributes:
        feature_weights: Dictionary mapping features to their weights
        intercept: Intercept of the linear approximation
        score: R² score of the linear approximation
        local_pred: Prediction for the explained instance
        feature_names: Names of features
        feature_values: Actual feature values
        used_features: Features used in the explanation
        metadata: Additional metadata
    """
    feature_weights: Dict[str, float]
    intercept: float
    score: float
    local_pred: Optional[float] = None
    feature_names: Optional[List[str]] = None
    feature_values: Optional[np.ndarray] = None
    used_features: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_top_features(self, n: int = 10, absolute: bool = True) -> List[Tuple[str, float]]:
        """
        Get top N most important features

        Args:
            n: Number of top features
            absolute: Use absolute values for sorting

        Returns:
            List of (feature_name, weight) tuples
        """
        if absolute:
            sorted_features = sorted(
                self.feature_weights.items(),
                key=lambda x: abs(x[1]),
                reverse=True
            )
        else:
            sorted_features = sorted(
                self.feature_weights.items(),
                key=lambda x: x[1],
                reverse=True
            )

        return sorted_features[:n]


class LIMEExplainer:
    """
    LIME-based model explainer

    Provides local explanations by approximating the model with an interpretable
    linear model in the neighborhood of the instance being explained.

    Example:
        >>> explainer = LIMEExplainer(model.predict, X_train)
        >>> explanation = explainer.explain_instance(X_test[0])
        >>> print(explanation.get_top_features(5))
    """

    def __init__(
        self,
        predict_fn: Callable,
        training_data: np.ndarray,
        feature_names: Optional[List[str]] = None,
        categorical_features: Optional[List[int]] = None,
        mode: str = 'regression',
        kernel_width: Optional[float] = None,
        **lime_kwargs
    ):
        """
        Initialize LIME explainer

        Args:
            predict_fn: Prediction function (takes numpy array, returns predictions)
            training_data: Training data for generating perturbations
            feature_names: Names of features
            categorical_features: Indices of categorical features
            mode: 'regression' or 'classification'
            kernel_width: Width of the exponential kernel (auto if None)
            **lime_kwargs: Additional arguments for LIME explainer
        """
        self.predict_fn = predict_fn
        self.training_data = training_data
        self.categorical_features = categorical_features or []
        self.mode = mode
        self.lime_kwargs = lime_kwargs

        # Try to import lime
        try:
            from lime import lime_tabular
            self.lime = lime_tabular
        except ImportError:
            raise ImportError(
                "LIME package is required. Install it with: pip install lime"
            )

        # Setup feature names
        if feature_names is None:
            self.feature_names = [f"feature_{i}" for i in range(training_data.shape[1])]
        else:
            self.feature_names = feature_names

        # Calculate kernel width if not provided
        if kernel_width is None:
            # Use LIME default: sqrt(n_features) * 0.75
            kernel_width = np.sqrt(training_data.shape[1]) * 0.75

        self.kernel_width = kernel_width

        # Initialize LIME explainer
        self.explainer = self._create_explainer()

        logger.info(f"Initialized LIME explainer in {mode} mode")

    def _create_explainer(self) -> Any:
        """
        Create LIME tabular explainer

        Returns:
            LIME explainer instance
        """
        return self.lime.LimeTabularExplainer(
            training_data=self.training_data,
            feature_names=self.feature_names,
            categorical_features=self.categorical_features,
            mode=self.mode,
            kernel_width=self.kernel_width,
            **self.lime_kwargs
        )

    def explain_instance(
        self,
        instance: np.ndarray,
        num_features: int = 10,
        num_samples: int = 5000,
        labels: Optional[Tuple[int]] = None
    ) -> LIMEExplanation:
        """
        Explain a single instance using LIME

        Args:
            instance: Instance to explain (1D array)
            num_features: Number of features to include in explanation
            num_samples: Number of perturbed samples to generate
            labels: Labels to explain (for classification, None = all labels)

        Returns:
            LIME explanation
        """
        # Ensure instance is 1D
        if len(instance.shape) > 1:
            instance = instance.flatten()

        logger.info(f"Explaining instance with LIME ({num_samples} samples)...")

        # Generate explanation
        if self.mode == 'classification':
            explanation = self.explainer.explain_instance(
                data_row=instance,
                predict_fn=self.predict_fn,
                num_features=num_features,
                num_samples=num_samples,
                labels=labels
            )
        else:
            explanation = self.explainer.explain_instance(
                data_row=instance,
                predict_fn=self.predict_fn,
                num_features=num_features,
                num_samples=num_samples
            )

        # Extract explanation components
        if self.mode == 'classification' and labels is not None:
            # For specific label
            label = labels[0] if isinstance(labels, tuple) else labels
            feature_weights = dict(explanation.as_list(label=label))
            intercept = explanation.intercept[label]
            score = explanation.score[label] if hasattr(explanation, 'score') else None
            local_pred = explanation.predict_proba[label]
        else:
            # For regression or default classification
            feature_weights = dict(explanation.as_list())
            intercept = explanation.intercept[1] if isinstance(explanation.intercept, dict) else explanation.intercept
            score = explanation.score if hasattr(explanation, 'score') else None
            local_pred = explanation.predicted_value if hasattr(explanation, 'predicted_value') else None

        # Get used features
        used_features = list(feature_weights.keys())

        return LIMEExplanation(
            feature_weights=feature_weights,
            intercept=intercept,
            score=score,
            local_pred=local_pred,
            feature_names=self.feature_names,
            feature_values=instance,
            used_features=used_features,
            metadata={
                'num_samples': num_samples,
                'num_features': num_features,
                'mode': self.mode
            }
        )

    def explain_instance_with_distance(
        self,
        instance: np.ndarray,
        num_features: int = 10,
        num_samples: int = 5000,
        distance_metric: str = 'euclidean'
    ) -> Tuple[LIMEExplanation, np.ndarray]:
        """
        Explain instance and return distances to generated samples

        Args:
            instance: Instance to explain
            num_features: Number of features
            num_samples: Number of samples
            distance_metric: Distance metric ('euclidean', 'manhattan', 'cosine')

        Returns:
            Tuple of (explanation, distances array)
        """
        from scipy.spatial import distance

        # Get explanation
        explanation = self.explain_instance(
            instance, num_features, num_samples
        )

        # Calculate distances (simplified - would need access to LIME internals)
        # This is a placeholder for demonstration
        distances = np.zeros(num_samples)

        explanation.metadata['distance_metric'] = distance_metric

        return explanation, distances

    def compare_instances(
        self,
        instance1: np.ndarray,
        instance2: np.ndarray,
        num_features: int = 10
    ) -> Dict[str, Any]:
        """
        Compare explanations for two instances

        Args:
            instance1: First instance
            instance2: Second instance
            num_features: Number of features to compare

        Returns:
            Comparison results
        """
        # Explain both instances
        exp1 = self.explain_instance(instance1, num_features)
        exp2 = self.explain_instance(instance2, num_features)

        # Find common and different features
        features1 = set(exp1.feature_weights.keys())
        features2 = set(exp2.feature_weights.keys())

        common_features = features1.intersection(features2)
        unique_to_1 = features1 - features2
        unique_to_2 = features2 - features1

        # Compare weights for common features
        weight_differences = {}
        for feature in common_features:
            diff = exp1.feature_weights[feature] - exp2.feature_weights[feature]
            weight_differences[feature] = diff

        return {
            'explanation_1': exp1,
            'explanation_2': exp2,
            'common_features': list(common_features),
            'unique_to_1': list(unique_to_1),
            'unique_to_2': list(unique_to_2),
            'weight_differences': weight_differences,
            'prediction_difference': exp1.local_pred - exp2.local_pred if exp1.local_pred and exp2.local_pred else None
        }

    def get_counterfactual_direction(
        self,
        instance: np.ndarray,
        target_change: float,
        num_features: int = 5
    ) -> Dict[str, float]:
        """
        Get suggested feature changes to achieve target prediction change

        Args:
            instance: Instance to modify
            target_change: Desired change in prediction
            num_features: Number of features to modify

        Returns:
            Dictionary with suggested feature changes
        """
        # Get explanation
        explanation = self.explain_instance(instance, num_features)

        # Get top features by absolute weight
        top_features = explanation.get_top_features(num_features, absolute=True)

        # Calculate required changes
        suggestions = {}
        total_weight = sum(abs(weight) for _, weight in top_features)

        for feature, weight in top_features:
            if total_weight > 0:
                # Proportional change based on feature weight
                proportion = abs(weight) / total_weight
                suggested_change = (target_change * proportion) / weight
                suggestions[feature] = suggested_change
            else:
                suggestions[feature] = 0.0

        return suggestions
