"""
AEVA-Bench Benchmark Suites

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


@dataclass
class Benchmark:
    """Individual benchmark test"""
    name: str
    description: str = ""
    metric_type: str = "custom"  # accuracy, precision, recall, f1, custom, etc.
    evaluate_fn: Optional[Callable] = None
    test_data: Any = None
    expected_output: Any = None

    def run(self, algorithm: Any, **kwargs) -> Dict[str, Any]:
        """
        Run the benchmark on an algorithm

        Args:
            algorithm: Algorithm to benchmark
            **kwargs: Additional parameters

        Returns:
            Dictionary with benchmark results
        """
        start_time = time.time()

        try:
            if self.evaluate_fn:
                # Use custom evaluation function
                result = self.evaluate_fn(algorithm, self.test_data, **kwargs)
            else:
                # Use default evaluation based on metric type
                result = self._default_evaluate(algorithm, **kwargs)

            duration = time.time() - start_time

            return {
                "success": True,
                "metric_value": result,
                "duration": duration,
                "error": None,
            }

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Benchmark {self.name} failed: {e}")

            return {
                "success": False,
                "metric_value": 0.0,
                "duration": duration,
                "error": str(e),
            }

    def _default_evaluate(self, algorithm: Any, **kwargs) -> float:
        """Default evaluation logic"""
        # This is a placeholder - should be overridden or use evaluate_fn
        if hasattr(algorithm, "score"):
            return algorithm.score(self.test_data, self.expected_output)
        elif hasattr(algorithm, "evaluate"):
            return algorithm.evaluate(self.test_data, self.expected_output)
        else:
            raise NotImplementedError(
                f"Algorithm must implement 'score' or 'evaluate' method, "
                f"or provide custom evaluate_fn"
            )


class BenchmarkSuite:
    """
    Collection of related benchmarks

    A suite groups multiple benchmarks together for comprehensive evaluation
    """

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.benchmarks: List[Benchmark] = []

    def add_benchmark(self, benchmark: Benchmark) -> "BenchmarkSuite":
        """
        Add a benchmark to the suite

        Args:
            benchmark: Benchmark to add

        Returns:
            Self for chaining
        """
        self.benchmarks.append(benchmark)
        logger.info(f"Added benchmark '{benchmark.name}' to suite '{self.name}'")
        return self

    def run(
        self,
        algorithm: Any,
        parallel: bool = True,
        max_workers: int = 4,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run all benchmarks in the suite

        Args:
            algorithm: Algorithm to benchmark
            parallel: Whether to run benchmarks in parallel
            max_workers: Maximum number of parallel workers
            **kwargs: Additional parameters passed to benchmarks

        Returns:
            Dictionary with all benchmark results
        """
        logger.info(f"Running benchmark suite: {self.name} ({len(self.benchmarks)} benchmarks)")

        results = {}
        start_time = time.time()

        if parallel and len(self.benchmarks) > 1:
            results = self._run_parallel(algorithm, max_workers, **kwargs)
        else:
            results = self._run_sequential(algorithm, **kwargs)

        total_duration = time.time() - start_time

        # Calculate summary statistics
        successful = sum(1 for r in results.values() if r["success"])
        failed = len(results) - successful
        avg_metric = sum(r["metric_value"] for r in results.values()) / len(results)

        return {
            "suite_name": self.name,
            "benchmarks": results,
            "summary": {
                "total": len(self.benchmarks),
                "successful": successful,
                "failed": failed,
                "average_metric": avg_metric,
                "total_duration": total_duration,
            }
        }

    def _run_sequential(self, algorithm: Any, **kwargs) -> Dict[str, Dict[str, Any]]:
        """Run benchmarks sequentially"""
        results = {}

        for benchmark in self.benchmarks:
            logger.info(f"Running benchmark: {benchmark.name}")
            results[benchmark.name] = benchmark.run(algorithm, **kwargs)

        return results

    def _run_parallel(
        self,
        algorithm: Any,
        max_workers: int,
        **kwargs
    ) -> Dict[str, Dict[str, Any]]:
        """Run benchmarks in parallel"""
        results = {}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all benchmarks
            future_to_benchmark = {
                executor.submit(benchmark.run, algorithm, **kwargs): benchmark
                for benchmark in self.benchmarks
            }

            # Collect results as they complete
            for future in as_completed(future_to_benchmark):
                benchmark = future_to_benchmark[future]
                try:
                    results[benchmark.name] = future.result()
                    logger.info(f"Completed benchmark: {benchmark.name}")
                except Exception as e:
                    logger.error(f"Benchmark {benchmark.name} raised exception: {e}")
                    results[benchmark.name] = {
                        "success": False,
                        "metric_value": 0.0,
                        "duration": 0.0,
                        "error": str(e),
                    }

        return results

    def to_dict(self) -> Dict[str, Any]:
        """Convert suite to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "benchmarks": [
                {
                    "name": b.name,
                    "description": b.description,
                    "metric_type": b.metric_type,
                }
                for b in self.benchmarks
            ],
        }

    def to_file(self, path: str) -> None:
        """Save suite definition to file"""
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BenchmarkSuite":
        """Create suite from dictionary"""
        suite = cls(name=data["name"], description=data.get("description", ""))

        for bench_data in data.get("benchmarks", []):
            benchmark = Benchmark(
                name=bench_data["name"],
                description=bench_data.get("description", ""),
                metric_type=bench_data.get("metric_type", "custom"),
            )
            suite.add_benchmark(benchmark)

        return suite

    @classmethod
    def from_file(cls, path: str) -> "BenchmarkSuite":
        """Load suite from file"""
        with open(path, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def load(cls, name: str) -> "BenchmarkSuite":
        """
        Load a predefined benchmark suite

        Args:
            name: Name of the suite to load

        Returns:
            BenchmarkSuite instance
        """
        # This would load from a registry or predefined suites
        # For now, create a basic suite
        if name == "standard_ml_bench":
            suite = cls(
                name="standard_ml_bench",
                description="Standard machine learning benchmarks"
            )
            suite.add_benchmark(Benchmark(
                name="accuracy",
                description="Model accuracy",
                metric_type="accuracy"
            ))
            return suite
        else:
            raise ValueError(f"Unknown benchmark suite: {name}")

    def __len__(self) -> int:
        """Return number of benchmarks"""
        return len(self.benchmarks)

    def __repr__(self) -> str:
        return f"BenchmarkSuite(name='{self.name}', benchmarks={len(self.benchmarks)})"
