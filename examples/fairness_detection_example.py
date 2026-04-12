"""
Example: Fairness and Bias Detection

Demonstrates how to use the fairness module for:
- Bias detection across demographic groups
- Fairness metrics calculation
- Intersectional bias analysis
- Mitigation recommendations
- Fairness report generation
"""

import random
from aeva.fairness import (
    FairnessMetrics,
    BiasDetector,
    FairnessAnalyzer,
    FairnessReportGenerator,
    BiasMitigation,
    FairnessOptimizer
)


def create_mock_predictions_with_bias(
    n_samples: int = 1000,
    bias_strength: float = 0.3
):
    """
    Create mock predictions with demographic bias

    Args:
        n_samples: Number of samples
        bias_strength: Strength of bias (0-1)
    """
    data = []

    for i in range(n_samples):
        # Demographic attributes
        gender = random.choice(['male', 'female'])
        race = random.choice(['group_a', 'group_b', 'group_c'])
        age_group = random.choice(['young', 'middle', 'senior'])

        # Ground truth (unbiased)
        y_true = random.choice([0, 1])

        # Biased prediction (favors male + group_a)
        if gender == 'male' and race == 'group_a':
            # Privileged group: higher probability of positive prediction
            if y_true == 1:
                prob = random.uniform(0.7, 0.99)
            else:
                prob = random.uniform(0.3, 0.7)  # Still biased towards positive
        else:
            # Unprivileged groups: lower probability
            if y_true == 1:
                prob = random.uniform(0.4, 0.8)
            else:
                prob = random.uniform(0.1, 0.5)

        # Apply bias strength
        if bias_strength > 0 and gender != 'male':
            prob = prob * (1 - bias_strength * 0.5)

        y_pred = 1 if prob > 0.5 else 0

        data.append({
            'id': i,
            'gender': gender,
            'race': race,
            'age_group': age_group,
            'y_true': y_true,
            'y_pred': y_pred,
            'y_prob': prob
        })

    return data


def example_basic_fairness_metrics():
    """Example 1: Calculate basic fairness metrics"""
    print("=" * 70)
    print("Example 1: Basic Fairness Metrics")
    print("=" * 70)

    # Create biased predictions
    data = create_mock_predictions_with_bias(n_samples=1000, bias_strength=0.4)

    y_true = [d['y_true'] for d in data]
    y_pred = [d['y_pred'] for d in data]
    gender = [d['gender'] for d in data]

    # Calculate fairness metrics
    calculator = FairnessMetrics()

    metrics = calculator.calculate_all_metrics(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_attribute=gender,
        positive_label=1
    )

    print("\n📊 Fairness Metrics (Gender):")
    print(f"  Demographic Parity Difference: {metrics.demographic_parity_difference:.4f}")
    print(f"  Disparate Impact Ratio: {metrics.disparate_impact_ratio:.4f}")
    print(f"  Equalized Odds Difference: {metrics.equalized_odds_difference:.4f}")
    print(f"  Equal Opportunity Difference: {metrics.equal_opportunity_difference:.4f}")
    print(f"  Predictive Parity Difference: {metrics.predictive_parity_difference:.4f}")

    # Calculate group-specific metrics
    print("\n👥 Performance by Group:")
    group_metrics = calculator.calculate_group_metrics(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_attribute=gender,
        positive_label=1
    )

    for group, group_stats in group_metrics.items():
        print(f"\n  {group}:")
        print(f"    Size: {group_stats['size']}")
        print(f"    Accuracy: {group_stats['accuracy']:.4f}")
        print(f"    Precision: {group_stats['precision']:.4f}")
        print(f"    Recall: {group_stats['recall']:.4f}")
        print(f"    F1: {group_stats['f1']:.4f}")

    return data, metrics


def example_bias_detection():
    """Example 2: Comprehensive bias detection"""
    print("\n" + "=" * 70)
    print("Example 2: Comprehensive Bias Detection")
    print("=" * 70)

    # Create biased data
    data = create_mock_predictions_with_bias(n_samples=1000, bias_strength=0.5)

    y_true = [d['y_true'] for d in data]
    y_pred = [d['y_pred'] for d in data]
    gender = [d['gender'] for d in data]

    # Detect bias
    detector = BiasDetector(strict_mode=False)

    result = detector.detect_bias(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_attribute=gender,
        positive_label=1,
        attribute_name="Gender"
    )

    print(f"\n🔍 Bias Detection Result:")
    print(f"  Biased: {result.biased}")
    print(f"  Severity: {result.severity.upper()}")
    print(f"  Privileged Group: {result.privileged_group}")
    print(f"  Unprivileged Groups: {', '.join(str(g) for g in result.unprivileged_groups)}")

    # Show violations
    if result.violations:
        print(f"\n⚠️ Violations Detected ({len(result.violations)}):")
        for v in result.violations:
            print(f"\n  {v['metric']}:")
            print(f"    {v['description']}")
            print(f"    Value: {v['value']:.4f}")
            print(f"    Threshold: {v['threshold']}")

    # Show recommendations
    print(f"\n💡 Recommendations:")
    for rec in result.recommendations[:8]:
        if rec.strip():
            print(f"  {rec}")

    return result


def example_multi_attribute_analysis():
    """Example 3: Multi-attribute fairness analysis"""
    print("\n" + "=" * 70)
    print("Example 3: Multi-Attribute Fairness Analysis")
    print("=" * 70)

    # Create biased data
    data = create_mock_predictions_with_bias(n_samples=1000, bias_strength=0.4)

    y_true = [d['y_true'] for d in data]
    y_pred = [d['y_pred'] for d in data]

    sensitive_attributes = {
        'gender': [d['gender'] for d in data],
        'race': [d['race'] for d in data],
        'age_group': [d['age_group'] for d in data]
    }

    # Analyze fairness across all attributes
    analyzer = FairnessAnalyzer(strict_mode=False)

    results = analyzer.analyze_fairness(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_attributes=sensitive_attributes,
        positive_label=1
    )

    print("\n📊 Fairness Analysis Across Attributes:")

    for attr_name, result in results.items():
        status_symbol = "⚠️" if result.biased else "✓"
        print(f"\n{status_symbol} {attr_name.upper()}:")
        print(f"  Biased: {result.biased}")
        print(f"  Severity: {result.severity}")
        print(f"  Violations: {len(result.violations)}")

        if result.violations:
            for v in result.violations[:2]:
                print(f"    - {v['description']}")

    return results


def example_intersectional_bias():
    """Example 4: Intersectional bias detection"""
    print("\n" + "=" * 70)
    print("Example 4: Intersectional Bias Detection")
    print("=" * 70)

    # Create biased data
    data = create_mock_predictions_with_bias(n_samples=1000, bias_strength=0.5)

    y_true = [d['y_true'] for d in data]
    y_pred = [d['y_pred'] for d in data]
    gender = [d['gender'] for d in data]
    race = [d['race'] for d in data]

    # Detect intersectional bias (Gender × Race)
    analyzer = FairnessAnalyzer(strict_mode=False)

    result = analyzer.detect_intersectional_bias(
        y_true=y_true,
        y_pred=y_pred,
        attribute1=gender,
        attribute2=race,
        attribute1_name="Gender",
        attribute2_name="Race",
        positive_label=1
    )

    print(f"\n🔍 Intersectional Bias (Gender × Race):")
    print(f"  Biased: {result.biased}")
    print(f"  Severity: {result.severity}")
    print(f"  Privileged Group: {result.privileged_group}")

    print(f"\n👥 Performance by Intersectional Groups:")
    # Show top and bottom performing groups
    sorted_groups = sorted(
        result.group_metrics.items(),
        key=lambda x: x[1]['accuracy'],
        reverse=True
    )

    print("\n  Top 3 Groups:")
    for group, metrics in sorted_groups[:3]:
        print(f"    {group}: Accuracy={metrics['accuracy']:.4f}, Size={metrics['size']}")

    print("\n  Bottom 3 Groups:")
    for group, metrics in sorted_groups[-3:]:
        print(f"    {group}: Accuracy={metrics['accuracy']:.4f}, Size={metrics['size']}")

    # Performance comparison
    print("\n📊 Group Performance Comparison:")
    comparison = analyzer.compare_group_performance(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_attribute=gender,
        positive_label=1
    )

    print(f"  Best Performing: {comparison['best_performing_group']}")
    print(f"  Worst Performing: {comparison['worst_performing_group']}")
    print(f"  Performance Gap: {comparison['performance_gap']:.4f}")

    return result


def example_fairness_report():
    """Example 5: Generate fairness report"""
    print("\n" + "=" * 70)
    print("Example 5: Fairness Report Generation")
    print("=" * 70)

    # Create biased data
    data = create_mock_predictions_with_bias(n_samples=1000, bias_strength=0.4)

    y_true = [d['y_true'] for d in data]
    y_pred = [d['y_pred'] for d in data]

    sensitive_attributes = {
        'gender': [d['gender'] for d in data],
        'race': [d['race'] for d in data]
    }

    # Analyze fairness
    analyzer = FairnessAnalyzer(strict_mode=False)

    results = analyzer.analyze_fairness(
        y_true=y_true,
        y_pred=y_pred,
        sensitive_attributes=sensitive_attributes,
        positive_label=1
    )

    # Generate report
    report_generator = FairnessReportGenerator()

    report = report_generator.generate_report(
        model_name="credit_scoring_model",
        attribute_results=results
    )

    print(f"\n📄 Fairness Report Generated:")
    print(f"  Model: {report.model_name}")
    print(f"  Overall Biased: {report.overall_biased}")
    print(f"  Overall Severity: {report.overall_severity}")

    print(f"\n📊 Summary:")
    print(f"  Attributes Analyzed: {report.summary['total_attributes_analyzed']}")
    print(f"  Biased Attributes: {report.summary['biased_attributes']}")
    print(f"  Fair Attributes: {report.summary['fair_attributes']}")

    # Generate text report
    print("\n" + "=" * 70)
    print("TEXT REPORT:")
    print("=" * 70)
    text_report = report_generator.generate_text_report(report)
    print(text_report[:1500])  # Show first 1500 characters
    print("\n... (truncated)")

    # Save HTML report
    html_report = report_generator.generate_html_report(report)
    with open("/tmp/fairness_report.html", "w") as f:
        f.write(html_report)
    print(f"\n✓ HTML report saved to: /tmp/fairness_report.html")

    return report


def example_bias_mitigation():
    """Example 6: Bias mitigation strategies"""
    print("\n" + "=" * 70)
    print("Example 6: Bias Mitigation Strategies")
    print("=" * 70)

    # Create biased data
    data = create_mock_predictions_with_bias(n_samples=1000, bias_strength=0.4)

    X = [{'feature1': d['id'], 'feature2': random.random()} for d in data]
    y = [d['y_true'] for d in data]
    gender = [d['gender'] for d in data]
    y_prob = [d['y_prob'] for d in data]

    mitigation = BiasMitigation()

    # 1. Sample reweighting
    print("\n1️⃣ Sample Reweighting (Pre-processing):")
    weights = mitigation.reweight_samples(
        X=X,
        y=y,
        sensitive_attribute=gender,
        positive_label=1
    )

    print(f"  ✓ Calculated sample weights")
    print(f"    Weight range: [{min(weights):.2f}, {max(weights):.2f}]")
    print(f"    Average weight: {sum(weights)/len(weights):.2f}")

    # 2. Resampling
    print("\n2️⃣ Resampling (Pre-processing):")
    X_resampled, y_resampled, gender_resampled = mitigation.resample_for_balance(
        X=X,
        y=y,
        sensitive_attribute=gender,
        strategy='oversample',
        random_seed=42
    )

    print(f"  ✓ Resampled dataset")
    print(f"    Original size: {len(X)}")
    print(f"    Resampled size: {len(X_resampled)}")

    from collections import Counter
    print(f"    Original distribution: {Counter(gender)}")
    print(f"    Resampled distribution: {Counter(gender_resampled)}")

    # 3. Threshold adjustment
    print("\n3️⃣ Threshold Adjustment (Post-processing):")
    thresholds = mitigation.adjust_thresholds(
        y_prob=y_prob,
        sensitive_attribute=gender,
        target_metric='demographic_parity'
    )

    print(f"  ✓ Calculated optimal thresholds per group:")
    for group, threshold in thresholds.items():
        print(f"    {group}: {threshold:.3f}")

    # 4. Mitigation plan
    print("\n4️⃣ Comprehensive Mitigation Plan:")

    # Detect violations first
    detector = BiasDetector()
    result = detector.detect_bias(
        y_true=[d['y_true'] for d in data],
        y_pred=[d['y_pred'] for d in data],
        sensitive_attribute=gender
    )

    plan = mitigation.generate_mitigation_plan(
        violations=result.violations,
        group_metrics=result.group_metrics
    )

    print(f"  Priority: {plan['priority'].upper()}")
    print(f"  Timeline: {plan['timeline']}")
    print(f"  Estimated Effort: {plan['estimated_effort']}")

    print(f"\n  Pre-processing Techniques:")
    for tech in plan['techniques']['pre_processing']:
        print(f"    • {tech}")

    print(f"\n  In-processing Techniques:")
    for tech in plan['techniques']['in_processing'][:3]:
        print(f"    • {tech}")

    print(f"\n  Post-processing Techniques:")
    for tech in plan['techniques']['post_processing'][:3]:
        print(f"    • {tech}")

    return plan


def example_fairness_optimization():
    """Example 7: Fairness optimization"""
    print("\n" + "=" * 70)
    print("Example 7: Fairness-Accuracy Trade-off Optimization")
    print("=" * 70)

    # Create biased data
    data = create_mock_predictions_with_bias(n_samples=1000, bias_strength=0.3)

    y_true = [d['y_true'] for d in data]
    y_prob = [d['y_prob'] for d in data]
    gender = [d['gender'] for d in data]

    optimizer = FairnessOptimizer()

    # 1. Optimize threshold
    print("\n🎯 Optimizing Decision Threshold:")
    result = optimizer.optimize_threshold(
        y_true=y_true,
        y_prob=y_prob,
        sensitive_attribute=gender,
        fairness_metric='demographic_parity',
        accuracy_threshold=0.75
    )

    print(f"  Optimal Threshold: {result['threshold']:.3f}")
    print(f"  Accuracy: {result['accuracy']:.4f}")
    print(f"  Fairness Disparity: {result['fairness_disparity']:.4f}")
    print(f"  Combined Score: {result['score']:.4f}")

    # 2. Trade-off analysis
    print("\n⚖️ Accuracy-Fairness Trade-off Analysis:")
    tradeoff = optimizer.analyze_tradeoffs(
        y_true=y_true,
        y_prob=y_prob,
        sensitive_attribute=gender
    )

    print(f"\n  Best Accuracy Point:")
    ba = tradeoff['best_accuracy']
    print(f"    Threshold: {ba['threshold']:.3f}")
    print(f"    Accuracy: {ba['accuracy']:.4f}")
    print(f"    Fairness Disparity: {ba['fairness_disparity']:.4f}")

    print(f"\n  Best Fairness Point:")
    bf = tradeoff['best_fairness']
    print(f"    Threshold: {bf['threshold']:.3f}")
    print(f"    Accuracy: {bf['accuracy']:.4f}")
    print(f"    Fairness Disparity: {bf['fairness_disparity']:.4f}")

    print(f"\n  Balanced Point:")
    bb = tradeoff['balanced']
    print(f"    Threshold: {bb['threshold']:.3f}")
    print(f"    Accuracy: {bb['accuracy']:.4f}")
    print(f"    Fairness Disparity: {bb['fairness_disparity']:.4f}")

    return tradeoff


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("AEVA Fairness and Bias Detection Examples")
    print("=" * 70)

    # Run examples
    data, metrics = example_basic_fairness_metrics()
    result = example_bias_detection()
    multi_results = example_multi_attribute_analysis()
    intersect_result = example_intersectional_bias()
    report = example_fairness_report()
    mitigation_plan = example_bias_mitigation()
    tradeoff = example_fairness_optimization()

    print("\n" + "=" * 70)
    print("All Examples Completed!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Fairness metrics (6 metrics)")
    print("  ✓ Bias detection with severity levels")
    print("  ✓ Multi-attribute analysis")
    print("  ✓ Intersectional bias detection")
    print("  ✓ Fairness report generation (text & HTML)")
    print("  ✓ Bias mitigation strategies")
    print("  ✓ Fairness-accuracy trade-off optimization")


if __name__ == '__main__':
    main()
