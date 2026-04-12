"""
Performance Profiler for model inference

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import time
import logging
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from datetime import datetime
import statistics

logger = logging.getLogger(__name__)


@dataclass
class ProfilingResult:
    """Result of performance profiling"""
    model_name: str
    total_samples: int
    total_time: float

    # Latency metrics
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float

    # Throughput
    throughput_qps: float

    # Resource usage
    cpu_usage: Dict[str, float] = field(default_factory=dict)
    memory_usage: Dict[str, float] = field(default_factory=dict)
    gpu_usage: Dict[str, float] = field(default_factory=dict)

    # Bottlenecks
    bottlenecks: List[Dict[str, Any]] = field(default_factory=list)

    # Cost
    estimated_cost: Optional[float] = None

    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'model_name': self.model_name,
            'total_samples': self.total_samples,
            'total_time': self.total_time,
            'latency': {
                'avg_ms': self.avg_latency_ms,
                'p50_ms': self.p50_latency_ms,
                'p95_ms': self.p95_latency_ms,
                'p99_ms': self.p99_latency_ms,
                'min_ms': self.min_latency_ms,
                'max_ms': self.max_latency_ms
            },
            'throughput_qps': self.throughput_qps,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'gpu_usage': self.gpu_usage,
            'bottlenecks': self.bottlenecks,
            'estimated_cost': self.estimated_cost,
            'timestamp': self.timestamp.isoformat()
        }


class PerformanceProfiler:
    """
    Profile model inference performance

    Features:
    - Latency measurement (P50, P95, P99)
    - Throughput calculation
    - Resource monitoring (CPU, GPU, Memory)
    - Bottleneck identification
    - Cost estimation
    """

    def __init__(
        self,
        warmup_samples: int = 10,
        profile_samples: int = 100,
        enable_resource_monitoring: bool = True
    ):
        """
        Initialize profiler

        Args:
            warmup_samples: Number of warmup samples to run
            profile_samples: Number of samples to profile
            enable_resource_monitoring: Enable resource monitoring
        """
        self.warmup_samples = warmup_samples
        self.profile_samples = profile_samples
        self.enable_resource_monitoring = enable_resource_monitoring

        # Measurements
        self.latencies: List[float] = []
        self.cpu_measurements: List[float] = []
        self.memory_measurements: List[float] = []
        self.gpu_measurements: List[Dict[str, float]] = []

    def profile(
        self,
        model_fn: Callable,
        input_data: List[Any],
        model_name: str = "unknown"
    ) -> ProfilingResult:
        """
        Profile model performance

        Args:
            model_fn: Model inference function
            input_data: Input data for inference
            model_name: Model name

        Returns:
            ProfilingResult object
        """
        logger.info(f"Starting performance profiling for {model_name}")

        # Reset measurements
        self.latencies = []
        self.cpu_measurements = []
        self.memory_measurements = []
        self.gpu_measurements = []

        # Warmup phase
        logger.info(f"Warmup: {self.warmup_samples} samples")
        self._run_warmup(model_fn, input_data)

        # Profile phase
        logger.info(f"Profiling: {self.profile_samples} samples")
        total_start = time.time()
        self._run_profiling(model_fn, input_data)
        total_time = time.time() - total_start

        # Calculate metrics
        result = self._calculate_metrics(
            model_name=model_name,
            total_time=total_time,
            total_samples=len(self.latencies)
        )

        logger.info(f"Profiling completed: {result.avg_latency_ms:.2f}ms avg, {result.throughput_qps:.2f} QPS")

        return result

    def _run_warmup(self, model_fn: Callable, input_data: List[Any]) -> None:
        """Run warmup phase"""
        num_samples = min(self.warmup_samples, len(input_data))

        for i in range(num_samples):
            sample = input_data[i % len(input_data)]
            try:
                _ = model_fn(sample)
            except Exception as e:
                logger.warning(f"Warmup sample {i} failed: {e}")

    def _run_profiling(self, model_fn: Callable, input_data: List[Any]) -> None:
        """Run profiling phase"""
        from aeva.profiling.monitor import ResourceMonitor

        monitor = None
        if self.enable_resource_monitoring:
            monitor = ResourceMonitor()
            monitor.start()

        num_samples = min(self.profile_samples, len(input_data))

        for i in range(num_samples):
            sample = input_data[i % len(input_data)]

            # Measure latency
            start = time.time()
            try:
                _ = model_fn(sample)
                latency_ms = (time.time() - start) * 1000
                self.latencies.append(latency_ms)
            except Exception as e:
                logger.warning(f"Profile sample {i} failed: {e}")
                continue

            # Collect resource metrics
            if monitor and i % 10 == 0:  # Sample every 10 iterations
                snapshot = monitor.get_snapshot()
                if snapshot:
                    self.cpu_measurements.append(snapshot.get('cpu_percent', 0))
                    self.memory_measurements.append(snapshot.get('memory_mb', 0))
                    if snapshot.get('gpu_stats'):
                        self.gpu_measurements.append(snapshot['gpu_stats'])

        if monitor:
            monitor.stop()

    def _calculate_metrics(
        self,
        model_name: str,
        total_time: float,
        total_samples: int
    ) -> ProfilingResult:
        """Calculate performance metrics"""

        # Latency percentiles
        sorted_latencies = sorted(self.latencies)

        def percentile(data: List[float], p: float) -> float:
            if not data:
                return 0.0
            k = (len(data) - 1) * p
            f = int(k)
            c = int(k) + 1
            if c >= len(data):
                return data[-1]
            return data[f] + (k - f) * (data[c] - data[f])

        avg_latency = statistics.mean(self.latencies) if self.latencies else 0.0
        p50 = percentile(sorted_latencies, 0.50)
        p95 = percentile(sorted_latencies, 0.95)
        p99 = percentile(sorted_latencies, 0.99)
        min_latency = min(self.latencies) if self.latencies else 0.0
        max_latency = max(self.latencies) if self.latencies else 0.0

        # Throughput
        throughput = total_samples / total_time if total_time > 0 else 0.0

        # Resource usage
        cpu_usage = {
            'avg_percent': statistics.mean(self.cpu_measurements) if self.cpu_measurements else 0.0,
            'max_percent': max(self.cpu_measurements) if self.cpu_measurements else 0.0
        }

        memory_usage = {
            'avg_mb': statistics.mean(self.memory_measurements) if self.memory_measurements else 0.0,
            'max_mb': max(self.memory_measurements) if self.memory_measurements else 0.0
        }

        gpu_usage = {}
        if self.gpu_measurements:
            gpu_usage = {
                'avg_utilization': statistics.mean([g.get('utilization', 0) for g in self.gpu_measurements]),
                'avg_memory_mb': statistics.mean([g.get('memory_used_mb', 0) for g in self.gpu_measurements]),
                'max_memory_mb': max([g.get('memory_used_mb', 0) for g in self.gpu_measurements])
            }

        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(
            avg_latency=avg_latency,
            p99=p99,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            gpu_usage=gpu_usage
        )

        return ProfilingResult(
            model_name=model_name,
            total_samples=total_samples,
            total_time=total_time,
            avg_latency_ms=avg_latency,
            p50_latency_ms=p50,
            p95_latency_ms=p95,
            p99_latency_ms=p99,
            min_latency_ms=min_latency,
            max_latency_ms=max_latency,
            throughput_qps=throughput,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            gpu_usage=gpu_usage,
            bottlenecks=bottlenecks
        )

    def _identify_bottlenecks(
        self,
        avg_latency: float,
        p99: float,
        cpu_usage: Dict[str, float],
        memory_usage: Dict[str, float],
        gpu_usage: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks"""
        bottlenecks = []

        # High latency variance
        if p99 > avg_latency * 2:
            bottlenecks.append({
                'type': 'latency_variance',
                'severity': 'high',
                'description': f'High latency variance: P99 ({p99:.1f}ms) is {p99/avg_latency:.1f}x avg ({avg_latency:.1f}ms)',
                'recommendation': 'Consider batch size optimization or request queuing'
            })

        # High CPU usage
        if cpu_usage.get('avg_percent', 0) > 80:
            bottlenecks.append({
                'type': 'cpu_bottleneck',
                'severity': 'high',
                'description': f'High CPU usage: {cpu_usage["avg_percent"]:.1f}%',
                'recommendation': 'Consider model optimization, quantization, or GPU acceleration'
            })

        # High memory usage
        if memory_usage.get('avg_mb', 0) > 8000:  # 8GB threshold
            bottlenecks.append({
                'type': 'memory_bottleneck',
                'severity': 'medium',
                'description': f'High memory usage: {memory_usage["avg_mb"]:.0f}MB',
                'recommendation': 'Consider model compression or memory-efficient inference'
            })

        # GPU bottleneck
        if gpu_usage and gpu_usage.get('avg_utilization', 0) > 90:
            bottlenecks.append({
                'type': 'gpu_bottleneck',
                'severity': 'high',
                'description': f'GPU near capacity: {gpu_usage["avg_utilization"]:.1f}% utilization',
                'recommendation': 'Consider batch size reduction or multi-GPU inference'
            })

        return bottlenecks

    def profile_batch_sizes(
        self,
        model_fn: Callable,
        input_data: List[Any],
        batch_sizes: List[int],
        model_name: str = "unknown"
    ) -> Dict[int, ProfilingResult]:
        """
        Profile different batch sizes

        Args:
            model_fn: Model inference function (should accept batch)
            input_data: Input data
            batch_sizes: List of batch sizes to test
            model_name: Model name

        Returns:
            Dictionary mapping batch_size -> ProfilingResult
        """
        results = {}

        for batch_size in batch_sizes:
            logger.info(f"Profiling batch size: {batch_size}")

            # Create batched data
            batched_data = []
            for i in range(0, len(input_data), batch_size):
                batch = input_data[i:i+batch_size]
                batched_data.append(batch)

            # Profile
            result = self.profile(
                model_fn=model_fn,
                input_data=batched_data,
                model_name=f"{model_name}_batch{batch_size}"
            )

            results[batch_size] = result

        # Find optimal batch size
        optimal = self._find_optimal_batch_size(results)
        logger.info(f"Optimal batch size: {optimal}")

        return results

    def _find_optimal_batch_size(
        self,
        results: Dict[int, ProfilingResult]
    ) -> int:
        """Find optimal batch size based on throughput and latency"""
        if not results:
            return 1

        # Score based on throughput (70%) and latency (30%)
        scores = {}

        max_throughput = max(r.throughput_qps for r in results.values())
        min_latency = min(r.avg_latency_ms for r in results.values())

        for batch_size, result in results.items():
            throughput_score = result.throughput_qps / max_throughput
            latency_score = min_latency / result.avg_latency_ms

            scores[batch_size] = 0.7 * throughput_score + 0.3 * latency_score

        return max(scores, key=scores.get)
