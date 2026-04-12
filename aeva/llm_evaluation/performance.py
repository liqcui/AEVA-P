"""
LLM Performance Evaluation Module

Measures LLM-specific performance metrics:
- TTFT (Time To First Token)
- TPOT (Time Per Output Token)
- Token consumption statistics
- Streaming performance
- Latency percentiles

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Watermark: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import time
import statistics
import logging

logger = logging.getLogger(__name__)


@dataclass
class TokenMetrics:
    """Token consumption and generation metrics"""
    input_tokens: int
    output_tokens: int
    total_tokens: int
    tokens_per_second: float
    cost_estimate: float = 0.0
    model_name: str = ""


@dataclass
class LatencyMetrics:
    """Detailed latency metrics"""
    ttft_ms: float  # Time To First Token
    tpot_ms: float  # Time Per Output Token
    total_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    streaming_latency_ms: List[float] = field(default_factory=list)


@dataclass
class LLMPerformanceResult:
    """Complete LLM performance evaluation result"""
    token_metrics: TokenMetrics
    latency_metrics: LatencyMetrics
    throughput_qps: float
    resource_usage: Dict[str, float]
    performance_score: float
    bottlenecks: List[str]


class LLMPerformanceProfiler:
    """
    Comprehensive LLM performance profiler

    Measures:
    - Token-level latency (TTFT, TPOT)
    - Throughput (QPS, TPS)
    - Resource consumption
    - Cost estimation
    """

    def __init__(
        self,
        model_name: str = "unknown",
        pricing: Optional[Dict[str, float]] = None
    ):
        """
        Initialize LLM performance profiler

        Args:
            model_name: Name of the LLM model
            pricing: Token pricing (input_price, output_price per 1K tokens)
        """
        self.model_name = model_name
        self.pricing = pricing or {
            'input_price_per_1k': 0.003,  # Default GPT-4 pricing
            'output_price_per_1k': 0.015
        }

        # Metrics storage
        self.latency_samples: List[float] = []
        self.token_counts: List[TokenMetrics] = []
        self.ttft_samples: List[float] = []
        self.tpot_samples: List[float] = []

    def profile_generation(
        self,
        generate_func: callable,
        input_text: str,
        **kwargs
    ) -> LLMPerformanceResult:
        """
        Profile a single LLM generation

        Args:
            generate_func: Function that generates output
            input_text: Input prompt
            **kwargs: Additional arguments for generate_func

        Returns:
            LLMPerformanceResult with performance metrics
        """
        # Estimate input tokens (rough approximation)
        input_tokens = len(input_text.split()) * 1.3  # ~1.3 tokens per word

        # Measure generation
        start_time = time.perf_counter()
        ttft = None
        token_times = []

        # Call generation function
        output = generate_func(input_text, **kwargs)

        total_time = (time.perf_counter() - start_time) * 1000  # milliseconds

        # Estimate output tokens
        output_tokens = len(output.split()) * 1.3 if isinstance(output, str) else 0
        total_tokens = input_tokens + output_tokens

        # Calculate TTFT and TPOT (simplified for non-streaming)
        ttft_ms = total_time * 0.1  # Assume 10% for first token
        tpot_ms = (total_time - ttft_ms) / max(output_tokens, 1)

        # Token metrics
        token_metrics = self._calculate_token_metrics(
            int(input_tokens),
            int(output_tokens),
            total_time
        )

        # Latency metrics
        latency_metrics = LatencyMetrics(
            ttft_ms=ttft_ms,
            tpot_ms=tpot_ms,
            total_latency_ms=total_time,
            p50_latency_ms=total_time,  # Single sample
            p95_latency_ms=total_time,
            p99_latency_ms=total_time,
            streaming_latency_ms=[total_time]
        )

        # Throughput (for single request)
        throughput_qps = 1000 / total_time if total_time > 0 else 0

        # Resource usage (simplified)
        resource_usage = {
            'memory_mb': 0.0,  # Would need actual monitoring
            'gpu_utilization': 0.0,
            'cpu_utilization': 0.0
        }

        # Performance score
        performance_score = self._calculate_performance_score(
            token_metrics, latency_metrics
        )

        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(
            token_metrics, latency_metrics
        )

        # Store samples
        self.latency_samples.append(total_time)
        self.ttft_samples.append(ttft_ms)
        self.tpot_samples.append(tpot_ms)
        self.token_counts.append(token_metrics)

        return LLMPerformanceResult(
            token_metrics=token_metrics,
            latency_metrics=latency_metrics,
            throughput_qps=throughput_qps,
            resource_usage=resource_usage,
            performance_score=performance_score,
            bottlenecks=bottlenecks
        )

    def profile_streaming(
        self,
        stream_func: callable,
        input_text: str,
        **kwargs
    ) -> LLMPerformanceResult:
        """
        Profile streaming generation

        Args:
            stream_func: Function that returns streaming generator
            input_text: Input prompt
            **kwargs: Additional arguments

        Returns:
            LLMPerformanceResult with streaming metrics
        """
        input_tokens = len(input_text.split()) * 1.3

        start_time = time.perf_counter()
        ttft = None
        token_times = []
        output_chunks = []

        # Process stream
        try:
            for chunk in stream_func(input_text, **kwargs):
                current_time = (time.perf_counter() - start_time) * 1000

                if ttft is None:
                    ttft = current_time

                token_times.append(current_time)
                output_chunks.append(chunk)

        except Exception as e:
            logger.error(f"Streaming error: {e}")

        total_time = (time.perf_counter() - start_time) * 1000

        # Calculate metrics
        output_text = ''.join(output_chunks) if output_chunks else ""
        output_tokens = len(output_text.split()) * 1.3

        # TTFT and TPOT
        ttft_ms = ttft or total_time
        tpot_ms = (total_time - ttft_ms) / max(output_tokens, 1)

        # Token metrics
        token_metrics = self._calculate_token_metrics(
            int(input_tokens),
            int(output_tokens),
            total_time
        )

        # Latency metrics with percentiles
        latency_metrics = self._calculate_latency_percentiles(
            ttft_ms, tpot_ms, total_time, token_times
        )

        throughput_qps = 1000 / total_time if total_time > 0 else 0
        resource_usage = {'memory_mb': 0.0}
        performance_score = self._calculate_performance_score(
            token_metrics, latency_metrics
        )
        bottlenecks = self._identify_bottlenecks(
            token_metrics, latency_metrics
        )

        return LLMPerformanceResult(
            token_metrics=token_metrics,
            latency_metrics=latency_metrics,
            throughput_qps=throughput_qps,
            resource_usage=resource_usage,
            performance_score=performance_score,
            bottlenecks=bottlenecks
        )

    def profile_batch(
        self,
        generate_func: callable,
        inputs: List[str],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Profile batch generation

        Args:
            generate_func: Generation function
            inputs: List of input prompts
            **kwargs: Additional arguments

        Returns:
            Aggregated performance metrics
        """
        results = []

        for input_text in inputs:
            result = self.profile_generation(generate_func, input_text, **kwargs)
            results.append(result)

        # Aggregate metrics
        return self._aggregate_results(results)

    def _calculate_token_metrics(
        self,
        input_tokens: int,
        output_tokens: int,
        total_time_ms: float
    ) -> TokenMetrics:
        """Calculate token consumption metrics"""
        total_tokens = input_tokens + output_tokens

        # Tokens per second
        tokens_per_second = (output_tokens / total_time_ms * 1000) if total_time_ms > 0 else 0

        # Cost estimation
        input_cost = (input_tokens / 1000) * self.pricing.get('input_price_per_1k', 0)
        output_cost = (output_tokens / 1000) * self.pricing.get('output_price_per_1k', 0)
        total_cost = input_cost + output_cost

        return TokenMetrics(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            tokens_per_second=tokens_per_second,
            cost_estimate=total_cost,
            model_name=self.model_name
        )

    def _calculate_latency_percentiles(
        self,
        ttft: float,
        tpot: float,
        total: float,
        samples: List[float]
    ) -> LatencyMetrics:
        """Calculate latency percentiles"""
        if len(samples) < 2:
            return LatencyMetrics(
                ttft_ms=ttft,
                tpot_ms=tpot,
                total_latency_ms=total,
                p50_latency_ms=total,
                p95_latency_ms=total,
                p99_latency_ms=total,
                streaming_latency_ms=samples
            )

        sorted_samples = sorted(samples)
        p50 = sorted_samples[int(len(sorted_samples) * 0.5)]
        p95 = sorted_samples[int(len(sorted_samples) * 0.95)]
        p99 = sorted_samples[int(len(sorted_samples) * 0.99)]

        return LatencyMetrics(
            ttft_ms=ttft,
            tpot_ms=tpot,
            total_latency_ms=total,
            p50_latency_ms=p50,
            p95_latency_ms=p95,
            p99_latency_ms=p99,
            streaming_latency_ms=samples
        )

    def _calculate_performance_score(
        self,
        token_metrics: TokenMetrics,
        latency_metrics: LatencyMetrics
    ) -> float:
        """Calculate overall performance score (0-100)"""
        # Scoring based on latency and throughput
        # Lower latency = better score
        # Higher tokens/sec = better score

        latency_score = 100 * max(0, 1 - (latency_metrics.total_latency_ms / 10000))
        throughput_score = min(100, token_metrics.tokens_per_second * 2)

        overall = (latency_score + throughput_score) / 2
        return round(overall, 2)

    def _identify_bottlenecks(
        self,
        token_metrics: TokenMetrics,
        latency_metrics: LatencyMetrics
    ) -> List[str]:
        """Identify performance bottlenecks"""
        bottlenecks = []

        # High TTFT
        if latency_metrics.ttft_ms > 1000:
            bottlenecks.append(
                f"High TTFT: {latency_metrics.ttft_ms:.0f}ms (target: <1000ms)"
            )

        # High TPOT
        if latency_metrics.tpot_ms > 100:
            bottlenecks.append(
                f"High TPOT: {latency_metrics.tpot_ms:.0f}ms (target: <100ms)"
            )

        # Low throughput
        if token_metrics.tokens_per_second < 10:
            bottlenecks.append(
                f"Low throughput: {token_metrics.tokens_per_second:.1f} tokens/sec"
            )

        # High cost
        if token_metrics.cost_estimate > 1.0:
            bottlenecks.append(
                f"High cost: ${token_metrics.cost_estimate:.3f} per request"
            )

        return bottlenecks

    def _aggregate_results(
        self,
        results: List[LLMPerformanceResult]
    ) -> Dict[str, Any]:
        """Aggregate batch results"""
        if not results:
            return {}

        # Calculate aggregate statistics
        ttfts = [r.latency_metrics.ttft_ms for r in results]
        tpots = [r.latency_metrics.tpot_ms for r in results]
        totals = [r.latency_metrics.total_latency_ms for r in results]
        costs = [r.token_metrics.cost_estimate for r in results]

        return {
            'batch_size': len(results),
            'avg_ttft_ms': statistics.mean(ttfts),
            'avg_tpot_ms': statistics.mean(tpots),
            'avg_latency_ms': statistics.mean(totals),
            'p50_latency_ms': statistics.median(totals),
            'p95_latency_ms': sorted(totals)[int(len(totals) * 0.95)],
            'p99_latency_ms': sorted(totals)[int(len(totals) * 0.99)],
            'total_cost': sum(costs),
            'avg_cost': statistics.mean(costs),
            'total_tokens': sum(r.token_metrics.total_tokens for r in results),
            'avg_tokens_per_sec': statistics.mean([r.token_metrics.tokens_per_second for r in results])
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all profiling sessions"""
        if not self.latency_samples:
            return {'message': 'No profiling data available'}

        return {
            'total_requests': len(self.latency_samples),
            'avg_latency_ms': statistics.mean(self.latency_samples),
            'avg_ttft_ms': statistics.mean(self.ttft_samples),
            'avg_tpot_ms': statistics.mean(self.tpot_samples),
            'p50_latency_ms': statistics.median(self.latency_samples),
            'p95_latency_ms': sorted(self.latency_samples)[int(len(self.latency_samples) * 0.95)],
            'p99_latency_ms': sorted(self.latency_samples)[int(len(self.latency_samples) * 0.99)],
            'total_cost': sum(tm.cost_estimate for tm in self.token_counts),
            'total_tokens': sum(tm.total_tokens for tm in self.token_counts)
        }
