"""
AEVA Benchmark Suite Example

Demonstrates AEVA-Bench capabilities with standardized benchmarks
"""

from aeva import AEVA
from aeva.bench import BenchmarkSuite, Benchmark
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def create_evaluation_benchmark(X_test, y_test):
    """Create a benchmark with test data"""

    def evaluate_accuracy(algorithm, test_data):
        y_pred = algorithm.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def evaluate_precision(algorithm, test_data):
        y_pred = algorithm.predict(X_test)
        return precision_score(y_test, y_pred, average='weighted')

    def evaluate_recall(algorithm, test_data):
        y_pred = algorithm.predict(X_test)
        return recall_score(y_test, y_pred, average='weighted')

    def evaluate_f1(algorithm, test_data):
        y_pred = algorithm.predict(X_test)
        return f1_score(y_test, y_pred, average='weighted')

    return [
        Benchmark(name="accuracy", metric_type="accuracy", evaluate_fn=evaluate_accuracy),
        Benchmark(name="precision", metric_type="precision", evaluate_fn=evaluate_precision),
        Benchmark(name="recall", metric_type="recall", evaluate_fn=evaluate_recall),
        Benchmark(name="f1_score", metric_type="f1", evaluate_fn=evaluate_f1),
    ]


def main():
    print("=" * 60)
    print("AEVA-Bench: Benchmark Suite Example")
    print("=" * 60)
    print()

    # 1. Initialize AEVA
    print("1. Initializing AEVA...")
    aeva = AEVA(config_path="config/aeva.yaml")
    print("   ✓ AEVA initialized\n")

    # 2. Create dataset
    print("2. Creating dataset...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   ✓ Dataset ready\n")

    # 3. Create benchmark suite
    print("3. Creating benchmark suite...")
    suite = BenchmarkSuite(
        name="ml_comparison_suite",
        description="Comprehensive ML algorithm comparison"
    )

    # Add benchmarks
    for benchmark in create_evaluation_benchmark(X_test, y_test):
        suite.add_benchmark(benchmark)

    # Register suite
    aeva.bench.register_suite(suite)
    print(f"   ✓ Suite created with {len(suite)} benchmarks\n")

    # 4. Train multiple algorithms
    print("4. Training algorithms...")
    algorithms = {
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
    }

    for name, algo in algorithms.items():
        print(f"   Training {name}...")
        algo.fit(X_train, y_train)

    print("   ✓ All algorithms trained\n")

    # 5. Run benchmarks for each algorithm
    print("5. Running benchmark suite on all algorithms...")
    print()

    all_results = {}

    for algo_name, algo in algorithms.items():
        print(f"   Benchmarking {algo_name}...")
        results = suite.run(algorithm=algo, parallel=True)
        all_results[algo_name] = results

        # Display summary
        summary = results["summary"]
        avg_score = summary["average_metric"]
        print(f"     Average Score: {avg_score:.4f}")
        print()

    # 6. Compare results
    print("6. Benchmark Comparison:")
    print("=" * 80)
    print(f"{'Algorithm':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<12}")
    print("-" * 80)

    for algo_name, results in all_results.items():
        benchmarks = results["benchmarks"]
        metrics = {
            "Accuracy": benchmarks["accuracy"]["metric_value"],
            "Precision": benchmarks["precision"]["metric_value"],
            "Recall": benchmarks["recall"]["metric_value"],
            "F1": benchmarks["f1_score"]["metric_value"],
        }

        print(
            f"{algo_name:<20} "
            f"{metrics['Accuracy']:<12.4f} "
            f"{metrics['Precision']:<12.4f} "
            f"{metrics['Recall']:<12.4f} "
            f"{metrics['F1']:<12.4f}"
        )

    print("=" * 80)
    print()

    # 7. Find best algorithm
    print("7. Best Algorithm:")
    best_algo = max(
        all_results.items(),
        key=lambda x: x[1]["summary"]["average_metric"]
    )
    print(f"   Winner: {best_algo[0]}")
    print(f"   Average Score: {best_algo[1]['summary']['average_metric']:.4f}\n")

    # 8. Set as baseline
    print("8. Setting baseline...")
    baseline_metrics = {
        name: data["metric_value"]
        for name, data in best_algo[1]["benchmarks"].items()
    }
    aeva.bench.set_baseline(
        suite_name="ml_comparison_suite",
        metrics=baseline_metrics,
        version="v1.0"
    )
    print("   ✓ Baseline set\n")

    # 9. Shutdown
    print("9. Shutting down...")
    aeva.shutdown()
    print("   ✓ Complete\n")

    print("=" * 60)
    print("Benchmark Suite Example Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
