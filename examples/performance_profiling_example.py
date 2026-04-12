"""
Example: Performance Profiling and Optimization

Demonstrates how to use the profiling module to analyze and optimize model performance.
"""

import time
import random
from aeva.profiling import PerformanceProfiler, BottleneckAnalyzer, CostAnalyzer


# Mock model for demonstration
class MockModel:
    """Mock ML model for demonstration"""

    def __init__(self, latency_ms: float = 100, variance: float = 0.2):
        self.latency_ms = latency_ms
        self.variance = variance

    def predict(self, input_data):
        """Simulate model inference"""
        # Simulate processing time with variance
        base_latency = self.latency_ms / 1000
        actual_latency = base_latency * (1 + random.uniform(-self.variance, self.variance))
        time.sleep(actual_latency)

        # Return mock prediction
        return {'prediction': random.choice(['positive', 'negative', 'neutral'])}


def create_mock_data(num_samples: int = 100):
    """Create mock input data"""
    return [
        {'text': f'Sample input {i}', 'id': i}
        for i in range(num_samples)
    ]


def example_basic_profiling():
    """Example 1: Basic performance profiling"""
    print("=" * 70)
    print("Example 1: Basic Performance Profiling")
    print("=" * 70)

    # Create mock model and data
    model = MockModel(latency_ms=50, variance=0.3)
    data = create_mock_data(num_samples=100)

    # Create profiler
    profiler = PerformanceProfiler(
        warmup_samples=10,
        profile_samples=50,
        enable_resource_monitoring=True
    )

    # Profile the model
    result = profiler.profile(
        model_fn=model.predict,
        input_data=data,
        model_name="mock_sentiment_model"
    )

    # Print results
    print(f"\nModel: {result.model_name}")
    print(f"Total Samples: {result.total_samples}")
    print(f"Total Time: {result.total_time:.2f}s")
    print(f"\nLatency Metrics:")
    print(f"  Average: {result.avg_latency_ms:.2f}ms")
    print(f"  P50: {result.p50_latency_ms:.2f}ms")
    print(f"  P95: {result.p95_latency_ms:.2f}ms")
    print(f"  P99: {result.p99_latency_ms:.2f}ms")
    print(f"  Min: {result.min_latency_ms:.2f}ms")
    print(f"  Max: {result.max_latency_ms:.2f}ms")
    print(f"\nThroughput: {result.throughput_qps:.2f} QPS")

    if result.cpu_usage:
        print(f"\nCPU Usage:")
        print(f"  Average: {result.cpu_usage['avg_percent']:.1f}%")
        print(f"  Max: {result.cpu_usage['max_percent']:.1f}%")

    if result.memory_usage:
        print(f"\nMemory Usage:")
        print(f"  Average: {result.memory_usage['avg_mb']:.1f}MB")
        print(f"  Max: {result.memory_usage['max_mb']:.1f}MB")

    if result.bottlenecks:
        print(f"\nIdentified Bottlenecks ({len(result.bottlenecks)}):")
        for bottleneck in result.bottlenecks:
            print(f"  - [{bottleneck['severity']}] {bottleneck['type']}: {bottleneck['description']}")
            print(f"    Recommendation: {bottleneck['recommendation']}")

    return result


def example_batch_size_optimization():
    """Example 2: Batch size optimization"""
    print("\n" + "=" * 70)
    print("Example 2: Batch Size Optimization")
    print("=" * 70)

    # Create model and data
    model = MockModel(latency_ms=30, variance=0.2)
    data = create_mock_data(num_samples=200)

    # Mock batch inference function
    def batch_predict(batch):
        """Process a batch of inputs"""
        # Simulate batch processing (slightly faster than sequential)
        batch_size = len(batch)
        time.sleep((model.latency_ms / 1000) * batch_size * 0.8)  # 20% efficiency gain
        return [model.predict(item) for item in batch]

    # Test different batch sizes
    profiler = PerformanceProfiler(
        warmup_samples=5,
        profile_samples=30
    )

    batch_sizes = [1, 4, 8, 16, 32]
    results = profiler.profile_batch_sizes(
        model_fn=batch_predict,
        input_data=data,
        batch_sizes=batch_sizes,
        model_name="mock_model"
    )

    # Compare results
    print("\nBatch Size Performance Comparison:")
    print(f"{'Batch Size':<12} {'Avg Latency (ms)':<18} {'Throughput (QPS)':<18} {'Efficiency':<12}")
    print("-" * 70)

    baseline_throughput = results[1].throughput_qps

    for batch_size in batch_sizes:
        result = results[batch_size]
        efficiency = (result.throughput_qps / baseline_throughput) * 100
        print(f"{batch_size:<12} {result.avg_latency_ms:<18.2f} {result.throughput_qps:<18.2f} {efficiency:<12.1f}%")

    # Find optimal
    optimal_batch = max(results.items(), key=lambda x: x[1].throughput_qps)
    print(f"\n✓ Optimal batch size: {optimal_batch[0]} (Throughput: {optimal_batch[1].throughput_qps:.2f} QPS)")

    return results


def example_bottleneck_analysis():
    """Example 3: Bottleneck analysis and recommendations"""
    print("\n" + "=" * 70)
    print("Example 3: Bottleneck Analysis")
    print("=" * 70)

    # Create a slow model to trigger bottlenecks
    slow_model = MockModel(latency_ms=500, variance=0.5)
    data = create_mock_data(num_samples=50)

    # Profile
    profiler = PerformanceProfiler(
        warmup_samples=5,
        profile_samples=30
    )

    result = profiler.profile(
        model_fn=slow_model.predict,
        input_data=data,
        model_name="slow_model"
    )

    # Analyze bottlenecks
    analyzer = BottleneckAnalyzer()
    bottlenecks = analyzer.analyze(result)

    # Generate report
    report = analyzer.generate_report(bottlenecks)
    print(report)

    return bottlenecks


def example_cost_analysis():
    """Example 4: Cost analysis and optimization"""
    print("\n" + "=" * 70)
    print("Example 4: Cost Analysis")
    print("=" * 70)

    # Profile a model
    model = MockModel(latency_ms=100, variance=0.2)
    data = create_mock_data(num_samples=50)

    profiler = PerformanceProfiler(warmup_samples=5, profile_samples=30)
    profiling_result = profiler.profile(
        model_fn=model.predict,
        input_data=data,
        model_name="production_model"
    )

    # Initialize cost analyzer
    cost_analyzer = CostAnalyzer()

    # Estimate cost for different scenarios
    print("\n1. Monthly Cost Estimate (10,000 requests/day):")
    print("-" * 70)

    monthly_estimate = cost_analyzer.estimate_with_profiling(
        profiling_result=profiling_result,
        requests_per_day=10000,
        gpu_type='T4',
        days=30
    )

    print(f"Total Cost: ${monthly_estimate.total_cost_usd:.2f}")
    print(f"Cost per 1K requests: ${monthly_estimate.cost_per_1k_requests:.4f}")
    print(f"Cost per hour: ${monthly_estimate.cost_per_hour:.4f}")
    print(f"\nBreakdown:")
    for key, value in monthly_estimate.breakdown.items():
        print(f"  {key}: ${value:.2f}" if isinstance(value, (int, float)) else f"  {key}: {value}")

    # Compare deployment options
    print("\n2. Deployment Options Comparison:")
    print("-" * 70)

    options = cost_analyzer.compare_deployment_options(
        profiling_result=profiling_result,
        requests_per_day=10000,
        days=30
    )

    print(f"{'GPU Type':<10} {'Total Cost':<15} {'Cost/1K Req':<15} {'Cost/Hour':<15}")
    print("-" * 70)

    for gpu_type, estimate in options.items():
        print(f"{gpu_type:<10} ${estimate.total_cost_usd:<14.2f} ${estimate.cost_per_1k_requests:<14.4f} ${estimate.cost_per_hour:<14.4f}")

    # Cost optimization recommendations
    print("\n3. Cost Optimization (Budget: $500/month):")
    print("-" * 70)

    optimization = cost_analyzer.optimize_cost(
        profiling_result=profiling_result,
        requests_per_day=10000,
        budget_usd=500,
        days=30
    )

    print(f"Current Estimate: ${optimization['current_estimate']['total_cost_usd']:.2f}")
    print(f"Budget: ${optimization['budget_usd']:.2f}")
    print(f"Within Budget: {'✓ Yes' if optimization['within_budget'] else '✗ No'}")

    if optimization['recommendations']:
        print(f"\nRecommendations ({len(optimization['recommendations'])}):")
        for idx, rec in enumerate(optimization['recommendations'], 1):
            print(f"\n{idx}. [{rec['severity'].upper()}] {rec['type']}")
            print(f"   {rec['message']}")
            print(f"   Suggestions:")
            for suggestion in rec['suggestions']:
                print(f"   - {suggestion}")

    return optimization


def example_comprehensive_analysis():
    """Example 5: Comprehensive performance analysis"""
    print("\n" + "=" * 70)
    print("Example 5: Comprehensive Performance Analysis")
    print("=" * 70)

    # Create realistic model
    model = MockModel(latency_ms=150, variance=0.3)
    data = create_mock_data(num_samples=100)

    # 1. Profile
    print("\nStep 1: Profiling model performance...")
    profiler = PerformanceProfiler(
        warmup_samples=10,
        profile_samples=50,
        enable_resource_monitoring=True
    )

    result = profiler.profile(
        model_fn=model.predict,
        input_data=data,
        model_name="bert_sentiment_classifier"
    )

    print(f"✓ Profiling complete")
    print(f"  Average latency: {result.avg_latency_ms:.2f}ms")
    print(f"  Throughput: {result.throughput_qps:.2f} QPS")

    # 2. Analyze bottlenecks
    print("\nStep 2: Analyzing bottlenecks...")
    analyzer = BottleneckAnalyzer()
    bottlenecks = analyzer.analyze(result)

    print(f"✓ Found {len(bottlenecks)} bottleneck(s)")
    for bottleneck in bottlenecks[:3]:  # Show top 3
        print(f"  - [{bottleneck.severity}] {bottleneck.type}: {bottleneck.description}")

    # 3. Cost analysis
    print("\nStep 3: Analyzing costs...")
    cost_analyzer = CostAnalyzer()
    cost_estimate = cost_analyzer.estimate_with_profiling(
        profiling_result=result,
        requests_per_day=5000,
        gpu_type='T4',
        days=30
    )

    print(f"✓ Cost estimate: ${cost_estimate.total_cost_usd:.2f}/month")
    print(f"  Cost per 1K requests: ${cost_estimate.cost_per_1k_requests:.4f}")

    # 4. Generate summary
    print("\n" + "=" * 70)
    print("Performance Analysis Summary")
    print("=" * 70)

    print(f"\nModel: {result.model_name}")
    print(f"Samples Tested: {result.total_samples}")

    print(f"\n📊 Performance Metrics:")
    print(f"  Latency (avg): {result.avg_latency_ms:.2f}ms")
    print(f"  Latency (P99): {result.p99_latency_ms:.2f}ms")
    print(f"  Throughput: {result.throughput_qps:.2f} QPS")

    print(f"\n💰 Cost Estimate (5K req/day for 30 days):")
    print(f"  Total: ${cost_estimate.total_cost_usd:.2f}")
    print(f"  Per 1K requests: ${cost_estimate.cost_per_1k_requests:.4f}")

    print(f"\n🔍 Bottlenecks ({len(bottlenecks)} found):")
    for bottleneck in bottlenecks[:3]:
        print(f"  {bottleneck.severity.upper()}: {bottleneck.description}")
        print(f"    → {bottleneck.estimated_improvement}")

    print("\n" + "=" * 70)


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("AEVA Performance Profiling Examples")
    print("=" * 70)

    # Run examples
    example_basic_profiling()
    example_batch_size_optimization()
    example_bottleneck_analysis()
    example_cost_analysis()
    example_comprehensive_analysis()

    print("\n" + "=" * 70)
    print("All Examples Completed!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Performance profiling (latency, throughput)")
    print("  ✓ Resource monitoring (CPU, memory, GPU)")
    print("  ✓ Batch size optimization")
    print("  ✓ Bottleneck identification")
    print("  ✓ Cost analysis and optimization")
    print("  ✓ Comprehensive performance analysis")


if __name__ == '__main__':
    main()
