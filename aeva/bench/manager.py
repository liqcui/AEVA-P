"""
AEVA-Bench Manager
Manages benchmark suites and execution

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
import json

from aeva.core.config import BenchConfig
from aeva.bench.suite import BenchmarkSuite

logger = logging.getLogger(__name__)


class BenchmarkManager:
    """
    Manages benchmark suites and their execution

    Responsibilities:
    - Load and manage benchmark datasets
    - Execute standardized benchmarks
    - Track baseline performance
    - Compare algorithm versions
    """

    def __init__(self, config: BenchConfig):
        self.config = config
        self.benchmark_dir = Path(config.benchmark_dir)
        self.suites: Dict[str, BenchmarkSuite] = {}
        self.baselines: Dict[str, Dict[str, float]] = {}

        self._initialize()

    def _initialize(self) -> None:
        """Initialize benchmark manager"""
        # Create benchmark directory if it doesn't exist
        self.benchmark_dir.mkdir(parents=True, exist_ok=True)

        # Load any existing benchmark suites
        self._load_suites()

        logger.info(f"BenchmarkManager initialized with {len(self.suites)} suites")

    def _load_suites(self) -> None:
        """Load benchmark suites from directory"""
        if not self.benchmark_dir.exists():
            return

        for suite_file in self.benchmark_dir.glob("*.json"):
            try:
                suite = BenchmarkSuite.from_file(str(suite_file))
                self.suites[suite.name] = suite
                logger.info(f"Loaded benchmark suite: {suite.name}")
            except Exception as e:
                logger.error(f"Failed to load suite {suite_file}: {e}")

    def register_suite(self, suite: BenchmarkSuite) -> None:
        """Register a benchmark suite"""
        self.suites[suite.name] = suite
        logger.info(f"Registered benchmark suite: {suite.name}")

        # Save suite to disk if caching enabled
        if self.config.cache_enabled:
            self._save_suite(suite)

    def _save_suite(self, suite: BenchmarkSuite) -> None:
        """Save benchmark suite to disk"""
        suite_file = self.benchmark_dir / f"{suite.name}.json"
        suite.to_file(str(suite_file))
        logger.debug(f"Saved benchmark suite to {suite_file}")

    def get_suite(self, name: str) -> Optional[BenchmarkSuite]:
        """Get a benchmark suite by name"""
        return self.suites.get(name)

    def list_suites(self) -> List[str]:
        """List all available benchmark suites"""
        return list(self.suites.keys())

    def run_suite(
        self,
        suite_name: str,
        algorithm: Any,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run a benchmark suite on an algorithm

        Args:
            suite_name: Name of the suite to run
            algorithm: Algorithm to benchmark
            **kwargs: Additional parameters

        Returns:
            Dictionary of benchmark results
        """
        suite = self.get_suite(suite_name)
        if suite is None:
            raise ValueError(f"Benchmark suite '{suite_name}' not found")

        logger.info(f"Running benchmark suite: {suite_name}")

        results = suite.run(
            algorithm=algorithm,
            parallel=self.config.parallel_execution,
            max_workers=self.config.max_workers,
            **kwargs
        )

        return results

    def set_baseline(
        self,
        suite_name: str,
        metrics: Dict[str, float],
        version: str = "baseline"
    ) -> None:
        """
        Set baseline metrics for a benchmark suite

        Args:
            suite_name: Name of the suite
            metrics: Dictionary of metric values
            version: Version identifier for the baseline
        """
        key = f"{suite_name}:{version}"
        self.baselines[key] = metrics
        logger.info(f"Set baseline for {suite_name} (version: {version})")

    def compare_to_baseline(
        self,
        suite_name: str,
        current_metrics: Dict[str, float],
        version: str = "baseline"
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare current metrics to baseline

        Args:
            suite_name: Name of the suite
            current_metrics: Current metric values
            version: Baseline version to compare against

        Returns:
            Dictionary with comparison results
        """
        key = f"{suite_name}:{version}"
        baseline = self.baselines.get(key)

        if baseline is None:
            logger.warning(f"No baseline found for {suite_name}:{version}")
            return {}

        comparison = {}
        for metric_name, current_value in current_metrics.items():
            if metric_name in baseline:
                baseline_value = baseline[metric_name]
                diff = current_value - baseline_value
                percent_change = (diff / baseline_value * 100) if baseline_value != 0 else 0

                comparison[metric_name] = {
                    "current": current_value,
                    "baseline": baseline_value,
                    "diff": diff,
                    "percent_change": percent_change,
                    "improved": diff > 0,
                }

        return comparison

    def get_status(self) -> Dict[str, Any]:
        """Get benchmark manager status"""
        return {
            "suites_count": len(self.suites),
            "baselines_count": len(self.baselines),
            "benchmark_dir": str(self.benchmark_dir),
            "cache_enabled": self.config.cache_enabled,
            "parallel_execution": self.config.parallel_execution,
            "max_workers": self.config.max_workers,
        }

    def create_standard_ml_suite(self) -> BenchmarkSuite:
        """Create a standard ML benchmark suite"""
        from aeva.bench.suite import Benchmark

        suite = BenchmarkSuite(
            name="standard_ml_bench",
            description="Standard machine learning benchmarks"
        )

        # Add standard ML benchmarks
        suite.add_benchmark(
            Benchmark(
                name="accuracy",
                description="Classification accuracy",
                metric_type="accuracy"
            )
        )

        suite.add_benchmark(
            Benchmark(
                name="precision",
                description="Precision score",
                metric_type="precision"
            )
        )

        suite.add_benchmark(
            Benchmark(
                name="recall",
                description="Recall score",
                metric_type="recall"
            )
        )

        suite.add_benchmark(
            Benchmark(
                name="f1_score",
                description="F1 score",
                metric_type="f1"
            )
        )

        self.register_suite(suite)
        return suite
