"""
Tests for AEVA-Bench module
"""

import pytest
from aeva.core.config import BenchConfig
from aeva.bench import BenchmarkManager, BenchmarkSuite, Benchmark


class DummyAlgorithm:
    """Dummy algorithm for testing"""

    def score(self, X, y):
        return 0.85


def test_benchmark_manager_initialization():
    """Test BenchmarkManager initialization"""
    config = BenchConfig(benchmark_dir="./test_benchmarks")
    manager = BenchmarkManager(config)

    assert manager is not None
    assert manager.config == config


def test_benchmark_suite_creation():
    """Test BenchmarkSuite creation"""
    suite = BenchmarkSuite(
        name="test_suite",
        description="Test benchmark suite"
    )

    assert suite.name == "test_suite"
    assert len(suite.benchmarks) == 0

    # Add benchmark
    benchmark = Benchmark(
        name="test_benchmark",
        metric_type="accuracy"
    )
    suite.add_benchmark(benchmark)

    assert len(suite.benchmarks) == 1


def test_benchmark_execution():
    """Test benchmark execution"""

    def custom_evaluate(algorithm, test_data):
        return 0.92

    benchmark = Benchmark(
        name="custom_bench",
        metric_type="custom",
        evaluate_fn=custom_evaluate
    )

    algo = DummyAlgorithm()
    result = benchmark.run(algo)

    assert result["success"] is True
    assert result["metric_value"] == 0.92


def test_suite_execution():
    """Test suite execution"""
    suite = BenchmarkSuite(name="test_suite")

    # Add multiple benchmarks
    for i in range(3):
        def eval_fn(algo, data, index=i):
            return 0.80 + (index * 0.05)

        benchmark = Benchmark(
            name=f"bench_{i}",
            evaluate_fn=eval_fn
        )
        suite.add_benchmark(benchmark)

    algo = DummyAlgorithm()
    results = suite.run(algo, parallel=False)

    assert results["summary"]["total"] == 3
    assert results["summary"]["successful"] >= 0


def test_baseline_management():
    """Test baseline setting and comparison"""
    config = BenchConfig()
    manager = BenchmarkManager(config)

    # Set baseline
    baseline_metrics = {
        "accuracy": 0.90,
        "precision": 0.85
    }
    manager.set_baseline("test_suite", baseline_metrics)

    # Compare to baseline
    current_metrics = {
        "accuracy": 0.92,
        "precision": 0.83
    }
    comparison = manager.compare_to_baseline("test_suite", current_metrics)

    assert "accuracy" in comparison
    assert comparison["accuracy"]["improved"] is True
    assert "precision" in comparison
    assert comparison["precision"]["improved"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
