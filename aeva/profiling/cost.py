"""
Cost Analyzer for model inference

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CostEstimate:
    """Cost estimation result"""
    total_cost_usd: float
    cost_per_1k_requests: float
    cost_per_hour: float
    breakdown: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_cost_usd': self.total_cost_usd,
            'cost_per_1k_requests': self.cost_per_1k_requests,
            'cost_per_hour': self.cost_per_hour,
            'breakdown': self.breakdown
        }


class CostAnalyzer:
    """
    Analyze and estimate inference costs

    Features:
    - Compute cost estimation
    - Storage cost estimation
    - Network cost estimation
    - Cost optimization recommendations
    """

    # Default pricing (can be customized)
    DEFAULT_PRICING = {
        'gpu': {
            'A100': 2.50,  # USD per hour
            'V100': 1.50,
            'T4': 0.35,
            'CPU': 0.10
        },
        'memory_gb_hour': 0.01,  # USD per GB-hour
        'storage_gb_month': 0.02,  # USD per GB-month
        'network_gb': 0.12  # USD per GB transferred
    }

    def __init__(self, pricing: Optional[Dict[str, Any]] = None):
        """
        Initialize cost analyzer

        Args:
            pricing: Custom pricing configuration
        """
        self.pricing = pricing or self.DEFAULT_PRICING

    def estimate_inference_cost(
        self,
        requests_per_day: int,
        avg_latency_ms: float,
        gpu_type: str = 'T4',
        memory_gb: float = 8.0,
        days: int = 30
    ) -> CostEstimate:
        """
        Estimate inference cost

        Args:
            requests_per_day: Number of requests per day
            avg_latency_ms: Average latency in milliseconds
            gpu_type: GPU type (A100, V100, T4, CPU)
            memory_gb: Memory usage in GB
            days: Number of days

        Returns:
            CostEstimate object
        """
        logger.info(f"Estimating cost for {requests_per_day} requests/day on {gpu_type}")

        # Calculate total requests
        total_requests = requests_per_day * days

        # Calculate GPU hours needed
        # Assuming sequential processing (can be optimized with batching)
        total_inference_time_hours = (total_requests * avg_latency_ms / 1000) / 3600

        # GPU cost
        gpu_price_per_hour = self.pricing['gpu'].get(gpu_type, self.pricing['gpu']['CPU'])
        gpu_cost = total_inference_time_hours * gpu_price_per_hour

        # Memory cost
        memory_cost = memory_gb * (days * 24) * self.pricing['memory_gb_hour']

        # Total cost
        total_cost = gpu_cost + memory_cost

        # Cost per 1k requests
        cost_per_1k = (total_cost / total_requests) * 1000 if total_requests > 0 else 0

        # Cost per hour
        cost_per_hour = total_cost / (days * 24)

        breakdown = {
            'compute_cost': gpu_cost,
            'memory_cost': memory_cost,
            'total_inference_hours': total_inference_time_hours
        }

        logger.info(f"Estimated cost: ${total_cost:.2f} for {days} days")

        return CostEstimate(
            total_cost_usd=total_cost,
            cost_per_1k_requests=cost_per_1k,
            cost_per_hour=cost_per_hour,
            breakdown=breakdown
        )

    def estimate_with_profiling(
        self,
        profiling_result,
        requests_per_day: int,
        gpu_type: str = 'T4',
        days: int = 30
    ) -> CostEstimate:
        """
        Estimate cost using profiling results

        Args:
            profiling_result: ProfilingResult from PerformanceProfiler
            requests_per_day: Requests per day
            gpu_type: GPU type
            days: Number of days

        Returns:
            CostEstimate object
        """
        avg_latency_ms = profiling_result.avg_latency_ms
        memory_gb = profiling_result.memory_usage.get('avg_mb', 1000) / 1024

        return self.estimate_inference_cost(
            requests_per_day=requests_per_day,
            avg_latency_ms=avg_latency_ms,
            gpu_type=gpu_type,
            memory_gb=memory_gb,
            days=days
        )

    def compare_deployment_options(
        self,
        profiling_result,
        requests_per_day: int,
        days: int = 30
    ) -> Dict[str, CostEstimate]:
        """
        Compare costs across different deployment options

        Args:
            profiling_result: ProfilingResult
            requests_per_day: Requests per day
            days: Number of days

        Returns:
            Dictionary mapping deployment option to CostEstimate
        """
        options = {}

        for gpu_type in ['A100', 'V100', 'T4', 'CPU']:
            estimate = self.estimate_with_profiling(
                profiling_result=profiling_result,
                requests_per_day=requests_per_day,
                gpu_type=gpu_type,
                days=days
            )
            options[gpu_type] = estimate

        # Find cheapest option
        cheapest = min(options.items(), key=lambda x: x[1].total_cost_usd)
        logger.info(f"Cheapest option: {cheapest[0]} at ${cheapest[1].total_cost_usd:.2f}")

        return options

    def optimize_cost(
        self,
        profiling_result,
        requests_per_day: int,
        budget_usd: float,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Provide cost optimization recommendations

        Args:
            profiling_result: ProfilingResult
            requests_per_day: Requests per day
            budget_usd: Budget in USD
            days: Number of days

        Returns:
            Optimization recommendations
        """
        # Get current cost estimate
        current_estimate = self.estimate_with_profiling(
            profiling_result=profiling_result,
            requests_per_day=requests_per_day,
            gpu_type='T4',  # Default
            days=days
        )

        recommendations = []

        # Check if over budget
        if current_estimate.total_cost_usd > budget_usd:
            overage = current_estimate.total_cost_usd - budget_usd
            recommendations.append({
                'type': 'budget_exceeded',
                'severity': 'high',
                'message': f'Estimated cost ${current_estimate.total_cost_usd:.2f} exceeds budget ${budget_usd:.2f} by ${overage:.2f}',
                'suggestions': [
                    'Consider model quantization to reduce latency',
                    'Implement request batching to improve throughput',
                    'Use cheaper GPU instances (e.g., T4 instead of A100)',
                    'Implement caching for repeated requests'
                ]
            })

        # Batching recommendation
        if profiling_result.throughput_qps < 10:
            recommendations.append({
                'type': 'low_throughput',
                'severity': 'medium',
                'message': f'Low throughput ({profiling_result.throughput_qps:.1f} QPS) increases cost',
                'suggestions': [
                    'Implement batch inference to improve throughput',
                    'Consider GPU acceleration',
                    'Optimize model architecture'
                ]
            })

        # Memory optimization
        memory_mb = profiling_result.memory_usage.get('avg_mb', 0)
        if memory_mb > 4000:  # 4GB threshold
            recommendations.append({
                'type': 'high_memory',
                'severity': 'medium',
                'message': f'High memory usage ({memory_mb:.0f}MB) increases costs',
                'suggestions': [
                    'Consider model compression techniques',
                    'Use mixed-precision inference (FP16)',
                    'Implement model pruning'
                ]
            })

        return {
            'current_estimate': current_estimate.to_dict(),
            'budget_usd': budget_usd,
            'within_budget': current_estimate.total_cost_usd <= budget_usd,
            'recommendations': recommendations
        }
