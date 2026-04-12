"""
Explanation Visualizations

Provides visualization functions for model explanations including:
- SHAP summary plots, waterfall plots, force plots
- LIME explanation plots
- Feature importance plots
- Comparison visualizations

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from typing import Any, List, Optional, Union
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def plot_shap_summary(
    shap_values: np.ndarray,
    features: np.ndarray,
    feature_names: List[str],
    max_display: int = 20,
    plot_type: str = 'dot',
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create SHAP summary plot

    Args:
        shap_values: SHAP values matrix
        features: Feature values matrix
        feature_names: Names of features
        max_display: Maximum features to display
        plot_type: 'dot', 'bar', or 'violin'
        save_path: Path to save plot

    Returns:
        Matplotlib figure
    """
    try:
        import shap
        shap.summary_plot(
            shap_values,
            features,
            feature_names=feature_names,
            max_display=max_display,
            plot_type=plot_type,
            show=False
        )

        fig = plt.gcf()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=150)
            logger.info(f"SHAP summary plot saved to {save_path}")

        return fig

    except ImportError:
        logger.error("SHAP package required for SHAP visualizations")
        return None


def plot_shap_waterfall(
    shap_explanation: Any,
    max_display: int = 20,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create SHAP waterfall plot for single instance

    Args:
        shap_explanation: SHAP explanation object
        max_display: Maximum features to display
        save_path: Path to save plot

    Returns:
        Matplotlib figure
    """
    try:
        import shap
        shap.plots.waterfall(shap_explanation, max_display=max_display, show=False)

        fig = plt.gcf()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=150)

        return fig

    except ImportError:
        logger.error("SHAP package required")
        return None


def plot_lime_explanation(
    lime_explanation: 'LIMEExplanation',
    num_features: int = 10,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create bar plot for LIME explanation

    Args:
        lime_explanation: LIME explanation object
        num_features: Number of features to display
        save_path: Path to save plot

    Returns:
        Matplotlib figure
    """
    # Get top features
    top_features = lime_explanation.get_top_features(num_features, absolute=False)

    # Separate positive and negative
    features = [f[0] for f in top_features]
    weights = [f[1] for f in top_features]

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['green' if w > 0 else 'red' for w in weights]
    y_pos = np.arange(len(features))

    ax.barh(y_pos, weights, color=colors, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(features)
    ax.set_xlabel('Feature Weight')
    ax.set_title(f'LIME Explanation (R²={lime_explanation.score:.3f})')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=150)

    return fig


def plot_feature_importance(
    feature_importance: 'FeatureImportance',
    top_n: int = 20,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create bar plot for feature importance

    Args:
        feature_importance: FeatureImportance object
        top_n: Number of top features to display
        save_path: Path to save plot

    Returns:
        Matplotlib figure
    """
    # Get top features
    top_features = feature_importance.get_top_features(top_n)

    features = [f[0] for f in top_features]
    scores = [f[1] for f in top_features]

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))

    y_pos = np.arange(len(features))
    ax.barh(y_pos, scores, color='steelblue', alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(features)
    ax.set_xlabel('Importance Score')
    ax.set_title(f'Feature Importance ({feature_importance.method})')
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=150)

    return fig


class ExplanationVisualizer:
    """
    Unified visualization interface for all explanation types
    """

    @staticmethod
    def visualize_shap(
        explanation: 'SHAPExplanation',
        plot_type: str = 'waterfall',
        **kwargs
    ) -> plt.Figure:
        """Visualize SHAP explanation"""
        if plot_type == 'waterfall':
            return plot_shap_waterfall(explanation, **kwargs)
        elif plot_type == 'summary':
            return plot_shap_summary(
                explanation.shap_values,
                explanation.data,
                explanation.feature_names,
                **kwargs
            )
        else:
            raise ValueError(f"Unknown plot type: {plot_type}")

    @staticmethod
    def visualize_lime(
        explanation: 'LIMEExplanation',
        **kwargs
    ) -> plt.Figure:
        """Visualize LIME explanation"""
        return plot_lime_explanation(explanation, **kwargs)

    @staticmethod
    def visualize_importance(
        importance: 'FeatureImportance',
        **kwargs
    ) -> plt.Figure:
        """Visualize feature importance"""
        return plot_feature_importance(importance, **kwargs)
