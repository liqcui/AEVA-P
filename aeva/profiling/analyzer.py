"""
Bottleneck Analyzer for performance optimization

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Bottleneck:
    """Identified performance bottleneck"""
    type: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str
    impact: str
    recommendations: List[str]
    estimated_improvement: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'severity': self.severity,
            'description': self.description,
            'impact': self.impact,
            'recommendations': self.recommendations,
            'estimated_improvement': self.estimated_improvement
        }


class BottleneckAnalyzer:
    """
    Analyze performance bottlenecks and provide optimization recommendations

    Features:
    - Latency bottleneck detection
    - Resource bottleneck identification
    - Optimization recommendation generation
    - Impact estimation
    """

    def __init__(self):
        """Initialize analyzer"""
        pass

    def analyze(self, profiling_result) -> List[Bottleneck]:
        """
        Analyze profiling result for bottlenecks

        Args:
            profiling_result: ProfilingResult from PerformanceProfiler

        Returns:
            List of identified bottlenecks
        """
        logger.info(f"Analyzing bottlenecks for {profiling_result.model_name}")

        bottlenecks = []

        # Check latency issues
        bottlenecks.extend(self._check_latency_issues(profiling_result))

        # Check resource issues
        bottlenecks.extend(self._check_resource_issues(profiling_result))

        # Check throughput issues
        bottlenecks.extend(self._check_throughput_issues(profiling_result))

        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        bottlenecks.sort(key=lambda x: severity_order.get(x.severity, 999))

        logger.info(f"Found {len(bottlenecks)} bottlenecks")

        return bottlenecks

    def _check_latency_issues(self, result) -> List[Bottleneck]:
        """Check for latency-related bottlenecks"""
        bottlenecks = []

        # High average latency
        if result.avg_latency_ms > 1000:  # 1 second
            bottlenecks.append(Bottleneck(
                type='high_latency',
                severity='critical',
                description=f'Very high average latency: {result.avg_latency_ms:.1f}ms',
                impact='Poor user experience, low throughput',
                recommendations=[
                    'Profile model layers to identify slow operations',
                    'Consider model quantization (INT8/FP16)',
                    'Implement model pruning or distillation',
                    'Use GPU acceleration if on CPU',
                    'Optimize preprocessing pipeline'
                ],
                estimated_improvement='50-80% latency reduction'
            ))
        elif result.avg_latency_ms > 500:
            bottlenecks.append(Bottleneck(
                type='moderate_latency',
                severity='high',
                description=f'Moderate latency: {result.avg_latency_ms:.1f}ms',
                impact='Suboptimal response time',
                recommendations=[
                    'Enable mixed-precision inference (FP16)',
                    'Optimize batch size',
                    'Use TensorRT or ONNX Runtime',
                    'Review preprocessing overhead'
                ],
                estimated_improvement='30-50% latency reduction'
            ))

        # High latency variance
        if result.p99_latency_ms > result.avg_latency_ms * 2:
            bottlenecks.append(Bottleneck(
                type='latency_variance',
                severity='high',
                description=f'High latency variance: P99 {result.p99_latency_ms:.1f}ms vs avg {result.avg_latency_ms:.1f}ms',
                impact='Inconsistent user experience, tail latency issues',
                recommendations=[
                    'Investigate outliers and edge cases',
                    'Implement request queuing with timeouts',
                    'Use load balancing across instances',
                    'Monitor and handle cold start issues',
                    'Consider dynamic batching'
                ],
                estimated_improvement='40-60% P99 improvement'
            ))

        return bottlenecks

    def _check_resource_issues(self, result) -> List[Bottleneck]:
        """Check for resource-related bottlenecks"""
        bottlenecks = []

        # CPU bottleneck
        cpu_usage = result.cpu_usage.get('avg_percent', 0)
        if cpu_usage > 90:
            bottlenecks.append(Bottleneck(
                type='cpu_bottleneck',
                severity='critical',
                description=f'CPU near capacity: {cpu_usage:.1f}%',
                impact='Limited scalability, potential system instability',
                recommendations=[
                    'Migrate to GPU if not already using',
                    'Reduce model complexity',
                    'Implement model quantization',
                    'Scale horizontally with more instances',
                    'Use compiled inference engines (TorchScript, TensorRT)'
                ],
                estimated_improvement='2-5x throughput increase with GPU'
            ))
        elif cpu_usage > 70:
            bottlenecks.append(Bottleneck(
                type='high_cpu',
                severity='medium',
                description=f'High CPU usage: {cpu_usage:.1f}%',
                impact='Limited headroom for traffic spikes',
                recommendations=[
                    'Consider GPU acceleration',
                    'Optimize preprocessing',
                    'Use efficient model serving frameworks',
                    'Plan for horizontal scaling'
                ],
                estimated_improvement='30-100% capacity increase'
            ))

        # Memory bottleneck
        memory_mb = result.memory_usage.get('avg_mb', 0)
        if memory_mb > 12000:  # 12GB
            bottlenecks.append(Bottleneck(
                type='high_memory',
                severity='high',
                description=f'High memory usage: {memory_mb:.0f}MB',
                impact='Increased costs, limited scalability',
                recommendations=[
                    'Use model compression techniques',
                    'Implement gradient checkpointing',
                    'Use mixed-precision inference',
                    'Reduce batch size if applicable',
                    'Consider model sharding for very large models'
                ],
                estimated_improvement='30-50% memory reduction'
            ))

        # GPU bottleneck
        if result.gpu_usage:
            gpu_util = result.gpu_usage.get('avg_utilization', 0)
            if gpu_util > 95:
                bottlenecks.append(Bottleneck(
                    type='gpu_saturation',
                    severity='critical',
                    description=f'GPU near capacity: {gpu_util:.1f}%',
                    impact='Cannot handle additional load',
                    recommendations=[
                        'Reduce batch size to lower GPU utilization',
                        'Scale to multi-GPU setup',
                        'Implement request queuing',
                        'Use model parallelism for large models',
                        'Consider load balancing across GPU instances'
                    ],
                    estimated_improvement='2-4x capacity with multi-GPU'
                ))
            elif gpu_util < 30:
                bottlenecks.append(Bottleneck(
                    type='gpu_underutilization',
                    severity='low',
                    description=f'GPU underutilized: {gpu_util:.1f}%',
                    impact='Wasted GPU resources, higher cost per request',
                    recommendations=[
                        'Increase batch size to better utilize GPU',
                        'Process multiple requests in parallel',
                        'Consider using smaller/cheaper GPU',
                        'Consolidate workloads from multiple models'
                    ],
                    estimated_improvement='50-200% better GPU utilization'
                ))

        return bottlenecks

    def _check_throughput_issues(self, result) -> List[Bottleneck]:
        """Check for throughput-related bottlenecks"""
        bottlenecks = []

        # Low throughput
        if result.throughput_qps < 1:
            bottlenecks.append(Bottleneck(
                type='very_low_throughput',
                severity='critical',
                description=f'Very low throughput: {result.throughput_qps:.2f} QPS',
                impact='Cannot serve production traffic effectively',
                recommendations=[
                    'Implement batch inference',
                    'Use GPU acceleration',
                    'Optimize model architecture',
                    'Enable async processing',
                    'Consider model distillation'
                ],
                estimated_improvement='10-100x throughput increase'
            ))
        elif result.throughput_qps < 10:
            bottlenecks.append(Bottleneck(
                type='low_throughput',
                severity='high',
                description=f'Low throughput: {result.throughput_qps:.2f} QPS',
                impact='Limited serving capacity',
                recommendations=[
                    'Implement dynamic batching',
                    'Optimize preprocessing pipeline',
                    'Use faster inference runtime (TensorRT, ONNX)',
                    'Consider multi-threaded serving',
                    'Profile and optimize hot paths'
                ],
                estimated_improvement='3-10x throughput increase'
            ))

        return bottlenecks

    def generate_report(self, bottlenecks: List[Bottleneck]) -> str:
        """
        Generate human-readable bottleneck analysis report

        Args:
            bottlenecks: List of bottlenecks

        Returns:
            Formatted report string
        """
        if not bottlenecks:
            return "No significant bottlenecks detected. Performance is optimal."

        report = "Performance Bottleneck Analysis Report\n"
        report += "=" * 60 + "\n\n"

        # Group by severity
        by_severity = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }

        for bottleneck in bottlenecks:
            by_severity[bottleneck.severity].append(bottleneck)

        for severity in ['critical', 'high', 'medium', 'low']:
            items = by_severity[severity]
            if items:
                report += f"\n{severity.upper()} Priority ({len(items)} issue{'s' if len(items) > 1 else ''})\n"
                report += "-" * 60 + "\n"

                for idx, bottleneck in enumerate(items, 1):
                    report += f"\n{idx}. {bottleneck.type.replace('_', ' ').title()}\n"
                    report += f"   Description: {bottleneck.description}\n"
                    report += f"   Impact: {bottleneck.impact}\n"
                    report += f"   Expected Improvement: {bottleneck.estimated_improvement}\n"
                    report += f"   Recommendations:\n"
                    for rec in bottleneck.recommendations:
                        report += f"   - {rec}\n"

        return report
