"""
Robustness Visualizations

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""
import logging
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Dict, Any, Tuple, Union
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

# Set default style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class VisualizationType(Enum):
    """Types of robustness visualizations"""
    ADVERSARIAL_EXAMPLES = "adversarial_examples"
    PERTURBATION = "perturbation"
    ROBUSTNESS_CURVE = "robustness_curve"
    ATTACK_SUCCESS = "attack_success"
    DEFENSE_EFFECTIVENESS = "defense_effectiveness"
    ROC_CURVE = "roc_curve"
    HEATMAP = "heatmap"
    CONFIDENCE_DISTRIBUTION = "confidence_distribution"


@dataclass
class VisualizationConfig:
    """Configuration for visualizations"""
    figsize: Tuple[int, int] = (12, 8)
    dpi: int = 150
    style: str = "seaborn-v0_8-darkgrid"
    colormap: str = "viridis"
    save_format: str = "png"
    title_fontsize: int = 14
    label_fontsize: int = 12
    show_grid: bool = True


class RobustnessVisualizer:
    """Advanced visualizations for robustness analysis"""

    def __init__(self, config: Optional[VisualizationConfig] = None):
        """Initialize visualizer

        Args:
            config: Visualization configuration
        """
        self.config = config or VisualizationConfig()

    def plot_adversarial_examples(
        self,
        original: np.ndarray,
        adversarial: np.ndarray,
        labels: Optional[List[str]] = None,
        predictions: Optional[Tuple[str, str]] = None,
        save_path: Optional[str] = None
    ) -> Figure:
        """Plot original vs adversarial examples

        Args:
            original: Original input samples
            adversarial: Adversarial samples
            labels: True labels for samples
            predictions: Tuple of (original_pred, adversarial_pred)
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        num_samples = min(len(original), 5)  # Show up to 5 examples
        fig, axes = plt.subplots(num_samples, 3, figsize=(12, 3 * num_samples))

        if num_samples == 1:
            axes = axes.reshape(1, -1)

        for idx in range(num_samples):
            # Original image
            self._plot_single_image(
                axes[idx, 0],
                original[idx],
                f"Original\n{labels[idx] if labels else ''}"
            )

            # Adversarial image
            pred_text = f"\n{predictions[1]}" if predictions else ""
            self._plot_single_image(
                axes[idx, 1],
                adversarial[idx],
                f"Adversarial{pred_text}"
            )

            # Difference (perturbation)
            diff = np.abs(adversarial[idx] - original[idx])
            self._plot_single_image(
                axes[idx, 2],
                diff,
                "Perturbation",
                cmap='hot'
            )

        plt.suptitle("Adversarial Examples Comparison", fontsize=16, fontweight='bold')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            logger.info(f"Adversarial examples plot saved to {save_path}")

        return fig

    def plot_perturbation(
        self,
        perturbation: np.ndarray,
        original: Optional[np.ndarray] = None,
        save_path: Optional[str] = None
    ) -> Figure:
        """Plot perturbation analysis

        Args:
            perturbation: Perturbation array
            original: Original input for context
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        if original is not None:
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        else:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Perturbation heatmap
        if len(perturbation.shape) == 2:
            im = ax1.imshow(perturbation, cmap='hot', interpolation='nearest')
        elif len(perturbation.shape) == 3:
            # For color images, show magnitude
            pert_magnitude = np.linalg.norm(perturbation, axis=-1)
            im = ax1.imshow(pert_magnitude, cmap='hot', interpolation='nearest')
        else:
            # Flatten for 1D visualization
            im = ax1.plot(perturbation.flatten())

        ax1.set_title("Perturbation Heatmap", fontsize=self.config.title_fontsize)
        plt.colorbar(im, ax=ax1)

        # Perturbation distribution
        ax2.hist(perturbation.flatten(), bins=50, alpha=0.7, color='steelblue', edgecolor='black')
        ax2.set_xlabel("Perturbation Value", fontsize=self.config.label_fontsize)
        ax2.set_ylabel("Frequency", fontsize=self.config.label_fontsize)
        ax2.set_title("Perturbation Distribution", fontsize=self.config.title_fontsize)
        ax2.grid(alpha=0.3)

        # Original image if provided
        if original is not None:
            self._plot_single_image(ax3, original, "Original Input")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            logger.info(f"Perturbation plot saved to {save_path}")

        return fig

    def plot_robustness_curve(
        self,
        epsilons: Union[List[float], np.ndarray],
        accuracies: Union[List[float], np.ndarray],
        baseline_accuracy: Optional[float] = None,
        labels: Optional[List[str]] = None,
        save_path: Optional[str] = None
    ) -> Figure:
        """Plot robustness curve (accuracy vs perturbation strength)

        Args:
            epsilons: Perturbation strengths
            accuracies: Corresponding accuracies (can be 2D for multiple models)
            baseline_accuracy: Clean accuracy baseline
            labels: Labels for multiple curves
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.config.figsize)

        # Handle multiple curves
        if isinstance(accuracies[0], (list, np.ndarray)):
            for idx, acc in enumerate(accuracies):
                label = labels[idx] if labels and idx < len(labels) else f"Model {idx+1}"
                ax.plot(epsilons, acc, marker='o', linewidth=2, label=label, alpha=0.8)
        else:
            ax.plot(epsilons, accuracies, marker='o', linewidth=2, label='Model', alpha=0.8)

        # Baseline accuracy
        if baseline_accuracy:
            ax.axhline(y=baseline_accuracy, color='red', linestyle='--',
                      linewidth=2, label=f'Baseline ({baseline_accuracy:.2%})', alpha=0.7)

        ax.set_xlabel("Epsilon (Perturbation Strength)", fontsize=self.config.label_fontsize)
        ax.set_ylabel("Accuracy", fontsize=self.config.label_fontsize)
        ax.set_title("Robustness Curve", fontsize=self.config.title_fontsize, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(alpha=0.3)
        ax.set_ylim(0, 1)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            logger.info(f"Robustness curve saved to {save_path}")

        return fig

    def plot_attack_success_rates(
        self,
        attack_names: List[str],
        success_rates: List[float],
        threshold: float = 0.5,
        save_path: Optional[str] = None
    ) -> Figure:
        """Plot attack success rates comparison

        Args:
            attack_names: Names of attack methods
            success_rates: Success rates for each attack
            threshold: Acceptable success rate threshold
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.config.figsize)

        colors = ['#dc3545' if rate > threshold else '#28a745' for rate in success_rates]
        bars = ax.barh(attack_names, success_rates, color=colors, alpha=0.7, edgecolor='black')

        # Add threshold line
        ax.axvline(x=threshold, color='orange', linestyle='--',
                  linewidth=2, label=f'Threshold ({threshold:.0%})', alpha=0.8)

        # Add value labels
        for idx, (bar, rate) in enumerate(zip(bars, success_rates)):
            ax.text(rate + 0.02, idx, f'{rate:.1%}',
                   va='center', fontsize=10, fontweight='bold')

        ax.set_xlabel("Success Rate", fontsize=self.config.label_fontsize)
        ax.set_title("Attack Success Rates", fontsize=self.config.title_fontsize, fontweight='bold')
        ax.legend(loc='best')
        ax.set_xlim(0, 1)
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            logger.info(f"Attack success plot saved to {save_path}")

        return fig

    def plot_defense_effectiveness(
        self,
        defense_names: List[str],
        effectiveness: List[float],
        performance_impact: Optional[List[float]] = None,
        save_path: Optional[str] = None
    ) -> Figure:
        """Plot defense mechanism effectiveness

        Args:
            defense_names: Names of defense mechanisms
            effectiveness: Effectiveness scores
            performance_impact: Optional performance impact scores
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        if performance_impact:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        else:
            fig, ax1 = plt.subplots(figsize=(10, 6))

        # Effectiveness plot
        bars = ax1.bar(defense_names, effectiveness, color='#667eea', alpha=0.7, edgecolor='black')
        ax1.set_ylabel("Effectiveness", fontsize=self.config.label_fontsize)
        ax1.set_title("Defense Effectiveness", fontsize=self.config.title_fontsize, fontweight='bold')
        ax1.set_ylim(0, 1)
        ax1.grid(axis='y', alpha=0.3)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1%}', ha='center', va='bottom', fontsize=10)

        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Performance impact plot
        if performance_impact:
            bars2 = ax2.bar(defense_names, performance_impact, color='#fd7e14', alpha=0.7, edgecolor='black')
            ax2.set_ylabel("Performance Impact", fontsize=self.config.label_fontsize)
            ax2.set_title("Performance Impact", fontsize=self.config.title_fontsize, fontweight='bold')
            ax2.set_ylim(0, 1)
            ax2.grid(axis='y', alpha=0.3)

            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1%}', ha='center', va='bottom', fontsize=10)

            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            logger.info(f"Defense effectiveness plot saved to {save_path}")

        return fig

    def plot_roc_curve(
        self,
        fpr: np.ndarray,
        tpr: np.ndarray,
        auc_score: Optional[float] = None,
        multiple_curves: Optional[Dict[str, Tuple[np.ndarray, np.ndarray, float]]] = None,
        save_path: Optional[str] = None
    ) -> Figure:
        """Plot ROC curve for adversarial detection

        Args:
            fpr: False positive rates
            tpr: True positive rates
            auc_score: Area under curve score
            multiple_curves: Dict of {name: (fpr, tpr, auc)} for comparison
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.config.figsize)

        if multiple_curves:
            for name, (fpr_vals, tpr_vals, auc_val) in multiple_curves.items():
                ax.plot(fpr_vals, tpr_vals, linewidth=2,
                       label=f'{name} (AUC = {auc_val:.3f})', alpha=0.8)
        else:
            label = f'ROC Curve (AUC = {auc_score:.3f})' if auc_score else 'ROC Curve'
            ax.plot(fpr, tpr, linewidth=2, label=label, alpha=0.8)

        # Diagonal reference line
        ax.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Random Classifier', alpha=0.5)

        ax.set_xlabel("False Positive Rate", fontsize=self.config.label_fontsize)
        ax.set_ylabel("True Positive Rate", fontsize=self.config.label_fontsize)
        ax.set_title("ROC Curve - Adversarial Detection", fontsize=self.config.title_fontsize, fontweight='bold')
        ax.legend(loc='lower right', fontsize=10)
        ax.grid(alpha=0.3)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            logger.info(f"ROC curve saved to {save_path}")

        return fig

    def plot_confidence_distribution(
        self,
        clean_confidences: np.ndarray,
        adversarial_confidences: np.ndarray,
        save_path: Optional[str] = None
    ) -> Figure:
        """Plot confidence score distributions for clean vs adversarial examples

        Args:
            clean_confidences: Confidence scores for clean examples
            adversarial_confidences: Confidence scores for adversarial examples
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Overlapping histograms
        ax1.hist(clean_confidences, bins=30, alpha=0.6, label='Clean', color='#28a745', edgecolor='black')
        ax1.hist(adversarial_confidences, bins=30, alpha=0.6, label='Adversarial', color='#dc3545', edgecolor='black')
        ax1.set_xlabel("Confidence Score", fontsize=self.config.label_fontsize)
        ax1.set_ylabel("Frequency", fontsize=self.config.label_fontsize)
        ax1.set_title("Confidence Distribution Comparison", fontsize=self.config.title_fontsize, fontweight='bold')
        ax1.legend(loc='best')
        ax1.grid(alpha=0.3)

        # Box plots
        data_to_plot = [clean_confidences, adversarial_confidences]
        bp = ax2.boxplot(data_to_plot, labels=['Clean', 'Adversarial'],
                         patch_artist=True, showmeans=True)

        colors = ['#28a745', '#dc3545']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)

        ax2.set_ylabel("Confidence Score", fontsize=self.config.label_fontsize)
        ax2.set_title("Confidence Score Box Plot", fontsize=self.config.title_fontsize, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            logger.info(f"Confidence distribution plot saved to {save_path}")

        return fig

    def plot_perturbation_heatmap(
        self,
        perturbations: np.ndarray,
        sample_names: Optional[List[str]] = None,
        feature_names: Optional[List[str]] = None,
        save_path: Optional[str] = None
    ) -> Figure:
        """Plot heatmap of perturbations across samples and features

        Args:
            perturbations: 2D array of perturbation values
            sample_names: Names for samples (rows)
            feature_names: Names for features (columns)
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        # Create heatmap
        im = ax.imshow(perturbations, cmap='RdYlGn_r', aspect='auto', interpolation='nearest')

        # Set ticks and labels
        if sample_names:
            ax.set_yticks(np.arange(len(sample_names)))
            ax.set_yticklabels(sample_names)
        if feature_names:
            ax.set_xticks(np.arange(len(feature_names)))
            ax.set_xticklabels(feature_names, rotation=45, ha='right')

        ax.set_title("Perturbation Heatmap", fontsize=self.config.title_fontsize, fontweight='bold')
        ax.set_xlabel("Features", fontsize=self.config.label_fontsize)
        ax.set_ylabel("Samples", fontsize=self.config.label_fontsize)

        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Perturbation Magnitude', fontsize=self.config.label_fontsize)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            logger.info(f"Perturbation heatmap saved to {save_path}")

        return fig

    def plot_epsilon_sensitivity(
        self,
        epsilons: np.ndarray,
        metrics: Dict[str, np.ndarray],
        save_path: Optional[str] = None
    ) -> Figure:
        """Plot sensitivity to epsilon parameter

        Args:
            epsilons: Array of epsilon values
            metrics: Dictionary of metric_name -> values arrays
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.config.figsize)

        for metric_name, values in metrics.items():
            ax.plot(epsilons, values, marker='o', linewidth=2,
                   label=metric_name, alpha=0.8)

        ax.set_xlabel("Epsilon (Perturbation Budget)", fontsize=self.config.label_fontsize)
        ax.set_ylabel("Metric Value", fontsize=self.config.label_fontsize)
        ax.set_title("Epsilon Sensitivity Analysis", fontsize=self.config.title_fontsize, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
            logger.info(f"Epsilon sensitivity plot saved to {save_path}")

        return fig

    def _plot_single_image(
        self,
        ax: Axes,
        image: np.ndarray,
        title: str,
        cmap: Optional[str] = None
    ):
        """Helper to plot a single image

        Args:
            ax: Matplotlib axis
            image: Image array
            title: Title for the image
            cmap: Colormap to use
        """
        if len(image.shape) == 3 and image.shape[-1] in [1, 3, 4]:
            # Color or grayscale image
            if image.shape[-1] == 1:
                ax.imshow(image.squeeze(), cmap=cmap or 'gray')
            else:
                # Ensure values are in [0, 1] range
                img_normalized = np.clip(image, 0, 1)
                ax.imshow(img_normalized, cmap=cmap)
        elif len(image.shape) == 2:
            # 2D grayscale
            ax.imshow(image, cmap=cmap or 'gray')
        else:
            # Flatten and show as 1D
            ax.plot(image.flatten())

        ax.set_title(title, fontsize=10)
        ax.axis('off')


# Standalone convenience functions
def plot_adversarial_examples(
    original: np.ndarray,
    adversarial: np.ndarray,
    save_path: Optional[str] = None,
    **kwargs
) -> Figure:
    """Convenience function to plot adversarial examples

    Args:
        original: Original samples
        adversarial: Adversarial samples
        save_path: Path to save figure
        **kwargs: Additional arguments for RobustnessVisualizer

    Returns:
        Matplotlib figure
    """
    visualizer = RobustnessVisualizer()
    return visualizer.plot_adversarial_examples(original, adversarial, save_path=save_path, **kwargs)


def plot_perturbation(
    perturbation: np.ndarray,
    save_path: Optional[str] = None,
    **kwargs
) -> Figure:
    """Convenience function to plot perturbation

    Args:
        perturbation: Perturbation array
        save_path: Path to save figure
        **kwargs: Additional arguments for RobustnessVisualizer

    Returns:
        Matplotlib figure
    """
    visualizer = RobustnessVisualizer()
    return visualizer.plot_perturbation(perturbation, save_path=save_path, **kwargs)


def plot_robustness_curve(
    epsilons: Union[List[float], np.ndarray],
    accuracies: Union[List[float], np.ndarray],
    save_path: Optional[str] = None,
    **kwargs
) -> Figure:
    """Convenience function to plot robustness curve

    Args:
        epsilons: Perturbation strengths
        accuracies: Corresponding accuracies
        save_path: Path to save figure
        **kwargs: Additional arguments for RobustnessVisualizer

    Returns:
        Matplotlib figure
    """
    visualizer = RobustnessVisualizer()
    return visualizer.plot_robustness_curve(epsilons, accuracies, save_path=save_path, **kwargs)
