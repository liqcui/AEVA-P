"""
AEVA Advanced Example - Brain Analysis

This example demonstrates AEVA-Brain's intelligent analysis capabilities
using Claude LLM for root cause analysis and recommendations.
"""

import os
from aeva import AEVA, AEVAConfig
from aeva.core.pipeline import Pipeline, FunctionStage, StageType
from aeva.guard import ThresholdGate
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def main():
    print("=" * 60)
    print("AEVA Platform - Brain Analysis Example")
    print("=" * 60)
    print()

    # Check for API key
    api_key = os.getenv("AEVA_BRAIN_API_KEY")
    if not api_key:
        print("⚠ Warning: AEVA_BRAIN_API_KEY not set")
        print("Set your Claude API key to enable intelligent analysis:")
        print("  export AEVA_BRAIN_API_KEY='your_api_key_here'")
        print()
        print("Continuing without Brain analysis...\n")

    # 1. Initialize AEVA with Brain enabled
    print("1. Initializing AEVA with Brain module...")
    config = AEVAConfig.from_env()
    aeva = AEVA(config=config)
    print("   ✓ AEVA initialized with Brain\n")

    # 2. Create dataset with intentional imbalance
    print("2. Creating imbalanced dataset...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=10,
        n_redundant=5,
        n_classes=2,
        weights=[0.9, 0.1],  # Imbalanced classes
        flip_y=0.1,  # Add noise
        random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   ✓ Imbalanced dataset created")
    print(f"     Class distribution: {sum(y_test == 0)} / {sum(y_test == 1)}\n")

    # 3. Train a deliberately suboptimal model
    print("3. Training suboptimal model...")
    model = RandomForestClassifier(
        n_estimators=10,  # Too few trees
        max_depth=3,      # Too shallow
        random_state=42
    )
    model.fit(X_train, y_train)
    print("   ✓ Model trained (intentionally limited)\n")

    # 4. Create comprehensive evaluation pipeline
    print("4. Creating evaluation pipeline...")
    pipeline = aeva.create_pipeline(name="comprehensive_evaluation")

    def comprehensive_evaluation(context):
        algorithm = context["algorithm"]
        X_test = context["X_test"]
        y_test = context["y_test"]

        y_pred = algorithm.predict(X_test)

        # Calculate multiple metrics
        return {
            "metrics": {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, average='weighted'),
                "recall": recall_score(y_test, y_pred, average='weighted'),
                "f1_score": f1_score(y_test, y_pred, average='weighted'),
            }
        }

    pipeline.add_function(
        name="comprehensive_metrics",
        function=comprehensive_evaluation,
        stage_type=StageType.BENCHMARK
    )
    print("   ✓ Pipeline created\n")

    # 5. Add strict quality gates
    print("5. Adding quality gates...")
    aeva.guard.add_gate(ThresholdGate(
        name="accuracy_gate",
        threshold=0.90,  # High threshold
        metric_name="accuracy",
        is_blocking=False
    ))
    aeva.guard.add_gate(ThresholdGate(
        name="f1_gate",
        threshold=0.85,  # High threshold
        metric_name="f1_score",
        is_blocking=False
    ))
    print("   ✓ Quality gates added (high thresholds)\n")

    # 6. Run evaluation
    print("6. Running evaluation...")
    result = aeva.run(
        pipeline=pipeline,
        algorithm=model,
        X_test=X_test,
        y_test=y_test
    )
    print("   ✓ Evaluation complete\n")

    # 7. Display basic results
    print("7. Basic Results:")
    print("-" * 60)
    for name, metric in result.metrics.items():
        status = "✓" if metric.passed else "✗"
        print(f"  {status} {name}: {metric.value:.4f}")
    print("-" * 60)
    print()

    # 8. Display Brain analysis
    if result.analysis and api_key:
        print("8. AEVA-Brain Intelligent Analysis:")
        print("=" * 60)
        print(f"\nSummary: {result.analysis.summary}")
        print(f"Severity: {result.analysis.severity.upper()}")
        print(f"Confidence: {result.analysis.confidence:.1%}")

        if result.analysis.root_causes:
            print("\nRoot Causes Identified:")
            for i, cause in enumerate(result.analysis.root_causes, 1):
                print(f"  {i}. {cause}")

        if result.analysis.recommendations:
            print("\nRecommendations:")
            for i, rec in enumerate(result.analysis.recommendations, 1):
                print(f"  {i}. {rec}")

        print("=" * 60)
        print()
    elif not api_key:
        print("8. Brain analysis skipped (no API key)\n")
    else:
        print("8. No analysis available\n")

    # 9. Shutdown
    print("9. Shutting down...")
    aeva.shutdown()
    print("   ✓ Complete\n")

    print("=" * 60)
    print("Advanced Brain Analysis Example Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
