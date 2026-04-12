"""
Adversarial Defense Examples

Demonstrates comprehensive defense mechanisms against adversarial attacks.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aeva.robustness.defenses import (
    AdversarialTraining,
    InputTransformation,
    GradientMasking,
    EnsembleDefense,
    AdversarialDetection,
    DefenseEvaluator
)


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


class SimpleClassifier:
    """Simple classifier for demonstration"""

    def __init__(self):
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        """Train classifier"""
        # Simple linear classifier
        from sklearn.linear_model import LogisticRegression
        self.model = LogisticRegression(max_iter=100)
        self.model.fit(X, y)

    def partial_fit(self, X, y):
        """Partial fit for adversarial training"""
        self.fit(X, y)

    def predict(self, X):
        """Predict labels"""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predict probabilities"""
        return self.model.predict_proba(X)


def generate_adversarial_examples(X, y, epsilon=0.1):
    """
    Generate simple adversarial examples using FGSM-like approach.

    Args:
        X: Input data
        y: Labels
        epsilon: Perturbation magnitude

    Returns:
        Adversarial examples
    """
    # Random perturbation (simulating gradient-based attack)
    perturbation = np.random.randn(*X.shape) * epsilon
    X_adv = X + perturbation

    # Clip to valid range
    X_adv = np.clip(X_adv, 0, 1)
    return X_adv


def example_adversarial_training():
    """Example 1: Adversarial Training Defense"""
    print_section("Example 1: Adversarial Training Defense")

    # Generate synthetic data
    np.random.seed(42)
    n_samples = 500
    n_features = 20

    X_train = np.random.randn(n_samples, n_features) * 0.5 + 0.5
    X_train = np.clip(X_train, 0, 1)
    y_train = (X_train.sum(axis=1) > n_features * 0.5).astype(int)

    X_test = np.random.randn(200, n_features) * 0.5 + 0.5
    X_test = np.clip(X_test, 0, 1)
    y_test = (X_test.sum(axis=1) > n_features * 0.5).astype(int)

    # Generate adversarial test examples
    X_adv = generate_adversarial_examples(X_test, y_test, epsilon=0.15)

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Features: {n_features}")

    # Train model with adversarial training
    model = SimpleClassifier()

    defense = AdversarialTraining(
        attack_fn=lambda X, y: generate_adversarial_examples(X, y, epsilon=0.1),
        mix_ratio=0.5,
        epochs=5
    )

    print("\nTraining model with adversarial examples...")
    defense.fit(model, X_train, y_train)

    # Evaluate
    result = defense.evaluate(model, X_test, y_test, X_adv)
    print("\n" + str(result))


def example_input_transformation():
    """Example 2: Input Transformation Defense"""
    print_section("Example 2: Input Transformation Defense")

    # Generate data
    np.random.seed(42)
    X_train = np.random.rand(400, 28, 28) * 0.8 + 0.1
    y_train = (X_train.mean(axis=(1, 2)) > 0.5).astype(int)

    X_test = np.random.rand(100, 28, 28) * 0.8 + 0.1
    y_test = (X_test.mean(axis=(1, 2)) > 0.5).astype(int)

    # Flatten for classifier
    X_train_flat = X_train.reshape(len(X_train), -1)
    X_test_flat = X_test.reshape(len(X_test), -1)

    # Train model
    model = SimpleClassifier()
    model.fit(X_train_flat, y_train)

    # Generate adversarial examples
    X_adv = generate_adversarial_examples(X_test, y_test, epsilon=0.2)
    X_adv_flat = X_adv.reshape(len(X_adv), -1)

    print(f"Image shape: {X_test.shape}")
    print(f"Training samples: {len(X_train)}")

    # Test different transformations
    transformations = [
        ("Median Filter", "median_filter", 3),
        ("Quantization (4-bit)", "quantization", 4),
        ("Gaussian Blur", "gaussian_blur", 3)
    ]

    print("\nTesting transformations:")
    for name, trans_type, param in transformations:
        print(f"\n{name}:")

        if trans_type == "quantization":
            defense = InputTransformation(
                transformation_type=trans_type,
                quantization_bits=param
            )
        else:
            defense = InputTransformation(
                transformation_type=trans_type,
                kernel_size=param
            )

        defense.fit(model, X_train, y_train)

        # Transform test data
        X_test_trans = defense.apply(X_test)
        X_adv_trans = defense.apply(X_adv)

        # Evaluate
        result = defense.evaluate(
            model,
            X_test_flat,
            y_test,
            X_adv_flat,
            predict_fn=lambda X: model.predict(X)
        )

        print(f"  Defended Accuracy: {result.defended_accuracy:.2%}")
        print(f"  Defense Effectiveness: {result.defense_effectiveness:.2%}")
        print(f"  Overhead: {result.overhead_ms:.2f}ms")


def example_ensemble_defense():
    """Example 3: Ensemble Defense"""
    print_section("Example 3: Ensemble Defense")

    # Generate data
    np.random.seed(42)
    X_train = np.random.randn(600, 15) * 0.5 + 0.5
    X_train = np.clip(X_train, 0, 1)
    y_train = (X_train.sum(axis=1) > 7.5).astype(int)

    X_test = np.random.randn(150, 15) * 0.5 + 0.5
    X_test = np.clip(X_test, 0, 1)
    y_test = (X_test.sum(axis=1) > 7.5).astype(int)

    X_adv = generate_adversarial_examples(X_test, y_test, epsilon=0.2)

    print(f"Training samples: {len(X_train)}")
    print(f"Ensemble size: 5 models")

    # Create ensemble of models
    models = [SimpleClassifier() for _ in range(5)]

    defense = EnsembleDefense(
        models=models,
        aggregation="majority_vote"
    )

    print("\nTraining ensemble...")
    defense.fit(None, X_train, y_train)

    # Evaluate
    result = defense.evaluate(None, X_test, y_test, X_adv)
    print("\n" + str(result))


def example_adversarial_detection():
    """Example 4: Adversarial Detection"""
    print_section("Example 4: Adversarial Detection")

    # Generate data
    np.random.seed(42)
    X_train = np.random.randn(500, 20) * 0.3 + 0.5
    X_train = np.clip(X_train, 0, 1)
    y_train = (X_train.sum(axis=1) > 10).astype(int)

    X_test = np.random.randn(200, 20) * 0.3 + 0.5
    X_test = np.clip(X_test, 0, 1)
    y_test = (X_test.sum(axis=1) > 10).astype(int)

    # Generate adversarial examples with larger perturbation
    X_adv = generate_adversarial_examples(X_test, y_test, epsilon=0.3)

    # Train model
    model = SimpleClassifier()
    model.fit(X_train, y_train)

    print(f"Training samples: {len(X_train)}")
    print(f"Clean test samples: {len(X_test)}")
    print(f"Adversarial test samples: {len(X_adv)}")

    # Test different detection methods
    methods = [
        ("Statistical", "statistical", 0.9),
        ("Confidence", "confidence", 0.7),
        ("Feature", "feature", 0.9)
    ]

    print("\nTesting detection methods:")
    for name, method, threshold in methods:
        print(f"\n{name} Detection (threshold={threshold}):")

        defense = AdversarialDetection(
            detection_method=method,
            threshold=threshold
        )

        defense.fit(model, X_train, y_train)

        # Detect adversarial examples
        detected_clean = defense.detect(X_test, model)
        detected_adv = defense.detect(X_adv, model)

        fpr = detected_clean.mean()
        tpr = detected_adv.mean()

        print(f"  False Positive Rate: {fpr:.2%}")
        print(f"  True Positive Rate: {tpr:.2%}")
        print(f"  Detection Accuracy: {(1 - fpr + tpr) / 2:.2%}")


def example_defense_comparison():
    """Example 5: Comprehensive Defense Comparison"""
    print_section("Example 5: Comprehensive Defense Comparison")

    # Generate data
    np.random.seed(42)
    X_train = np.random.randn(600, 20) * 0.4 + 0.5
    X_train = np.clip(X_train, 0, 1)
    y_train = (X_train.sum(axis=1) > 10).astype(int)

    X_test = np.random.randn(200, 20) * 0.4 + 0.5
    X_test = np.clip(X_test, 0, 1)
    y_test = (X_test.sum(axis=1) > 10).astype(int)

    X_adv = generate_adversarial_examples(X_test, y_test, epsilon=0.2)

    # Train model
    model = SimpleClassifier()
    model.fit(X_train, y_train)

    print(f"Dataset: {len(X_train)} train, {len(X_test)} test")
    print(f"Features: {X_train.shape[1]}")

    # Create defenses
    defenses = [
        InputTransformation(transformation_type="median_filter", kernel_size=3),
        InputTransformation(transformation_type="quantization", quantization_bits=6),
        GradientMasking(noise_scale=0.05),
        AdversarialDetection(detection_method="statistical", threshold=0.85)
    ]

    # Initialize evaluator
    evaluator = DefenseEvaluator()

    print("\nEvaluating defenses...")

    # Fit and evaluate each defense
    for defense in defenses:
        defense.fit(model, X_train, y_train)
        evaluator.evaluate_defense(defense, model, X_test, y_test, X_adv)

    # Generate report
    print("\n" + evaluator.generate_report())

    # Best defense
    best_name, best_result = evaluator.get_best_defense("effectiveness")
    print(f"\nRecommended Defense: {best_name.replace('_', ' ').title()}")


def main():
    """Run all defense examples"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "AEVA Adversarial Defense Examples" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")

    examples = [
        ("Adversarial Training", example_adversarial_training),
        ("Input Transformation", example_input_transformation),
        ("Ensemble Defense", example_ensemble_defense),
        ("Adversarial Detection", example_adversarial_detection),
        ("Defense Comparison", example_defense_comparison)
    ]

    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
