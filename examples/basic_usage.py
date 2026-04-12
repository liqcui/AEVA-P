"""
AEVA Basic Usage Example

This example demonstrates basic AEVA platform usage for algorithm evaluation
"""

from aeva import AEVA
from aeva.core.pipeline import Pipeline, FunctionStage, StageType
from aeva.guard import ThresholdGate
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def main():
    print("=" * 60)
    print("AEVA Platform - Basic Usage Example")
    print("=" * 60)
    print()

    # 1. Initialize AEVA Platform
    print("1. Initializing AEVA Platform...")
    aeva = AEVA(config_path="config/aeva.yaml")
    print("   ✓ AEVA initialized\n")

    # 2. Create sample dataset
    print("2. Creating sample dataset...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   ✓ Dataset created: {len(X_train)} train, {len(X_test)} test\n")

    # 3. Create and train algorithm
    print("3. Training RandomForest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("   ✓ Model trained\n")

    # 4. Create evaluation pipeline
    print("4. Creating evaluation pipeline...")
    pipeline = aeva.create_pipeline(name="rf_evaluation")

    # Add evaluation stage
    def evaluate_model(context):
        algorithm = context["algorithm"]
        X_test = context["X_test"]
        y_test = context["y_test"]

        # Make predictions
        y_pred = algorithm.predict(X_test)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)

        return {
            "metrics": {
                "accuracy": accuracy,
                "test_size": len(y_test)
            }
        }

    pipeline.add_function(
        name="model_evaluation",
        function=evaluate_model,
        stage_type=StageType.BENCHMARK
    )

    print("   ✓ Pipeline created with 1 stage\n")

    # 5. Add quality gate
    print("5. Adding quality gate...")
    gate = ThresholdGate(
        name="accuracy_gate",
        threshold=0.80,
        metric_name="accuracy",
        is_blocking=True
    )
    aeva.guard.add_gate(gate)
    print("   ✓ Quality gate added (threshold: 0.80)\n")

    # 6. Run evaluation
    print("6. Running evaluation pipeline...")
    result = aeva.run(
        pipeline=pipeline,
        algorithm=model,
        X_test=X_test,
        y_test=y_test
    )
    print("   ✓ Evaluation complete\n")

    # 7. Display results
    print("7. Evaluation Results:")
    print("-" * 60)
    print(result.summary())
    print("-" * 60)
    print()

    # 8. Check gate result
    if result.gate_result:
        if result.gate_result.passed:
            print("✓ Quality Gate: PASSED")
        else:
            print("✗ Quality Gate: FAILED")
            if result.gate_result.blocked:
                print("⚠ Deployment BLOCKED")
    print()

    # 9. Shutdown
    print("9. Shutting down AEVA...")
    aeva.shutdown()
    print("   ✓ Shutdown complete\n")

    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
