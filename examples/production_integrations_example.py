"""
Production-Grade Integrations Example

演示如何使用AEVA的生产级库集成:
1. ART (Adversarial Robustness Toolbox) - 对抗鲁棒性
2. Great Expectations - 数据质量
3. statsmodels - 高级统计检验

这些集成提供了更强大的功能，同时在库未安装时自动回退到基础实现。
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
import sys
sys.path.insert(0, '.')

print("=" * 70)
print("AEVA Production Integrations Demo")
print("=" * 70)

# 加载数据
print("\n📊 Loading data...")
data = load_breast_cancer()
X, y = data.data, data.target
feature_names = data.feature_names.tolist()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   ✓ Training: {len(X_train)}, Test: {len(X_test)}")

# 训练模型
print("\n🎯 Training model...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(f"   ✓ Model accuracy: {accuracy:.3f}")

# ==============================================================================
# 1. ART Integration - 对抗鲁棒性测试
# ==============================================================================

print("\n" + "=" * 70)
print("1. ART Integration - Advanced Robustness Testing")
print("=" * 70)

try:
    from aeva.integrations import ARTRobustnessTester

    print("\n🛡️  Initializing ART robustness tester...")

    # 标准化数据（对抗攻击推荐）
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 创建ART测试器
    art_tester = ARTRobustnessTester(
        model=model,
        input_shape=(X_train.shape[1],),
        nb_classes=2,
        clip_values=(X_test_scaled.min(), X_test_scaled.max())
    )

    if art_tester.is_available():
        print("   ✓ ART library detected - using production implementation")
    else:
        print("   ⚠️  ART not installed - using fallback implementation")

    # 测试1: FGSM攻击
    print("\n   Testing FGSM attack...")
    fgsm_result = art_tester.fgsm_attack(
        X_test_scaled[:20],
        y_test[:20],
        epsilon=0.1
    )
    print(f"   ✓ Success rate: {fgsm_result.success_rate:.2%}")
    print(f"   ✓ Avg perturbation: {fgsm_result.avg_perturbation:.6f}")

    # 测试2: PGD攻击（更强）
    print("\n   Testing PGD attack...")
    pgd_result = art_tester.pgd_attack(
        X_test_scaled[:20],
        y_test[:20],
        epsilon=0.1,
        max_iter=10
    )
    print(f"   ✓ Success rate: {pgd_result.success_rate:.2%}")
    print(f"   ✓ Avg perturbation: {pgd_result.avg_perturbation:.6f}")

    # 综合测试
    print("\n   Running comprehensive robustness test...")
    comprehensive_results = art_tester.comprehensive_test(
        X_test_scaled[:30],
        y_test[:30],
        attacks=['fgsm', 'pgd'],
        epsilon_values=[0.05, 0.1]
    )

    print(f"   ✓ Completed {len(comprehensive_results)} attack scenarios")

    # 生成报告
    report = art_tester.generate_robustness_report(comprehensive_results)
    print("\n" + "=" * 70)
    print("Robustness Report Preview:")
    print("=" * 70)
    print(report[:500] + "...\n")

    # 保存完整报告
    with open('/tmp/art_robustness_report.txt', 'w') as f:
        f.write(report)
    print(f"   ✓ Full report saved to /tmp/art_robustness_report.txt")

except Exception as e:
    print(f"\n   ✗ ART integration failed: {e}")
    print("   Install with: pip install adversarial-robustness-toolbox")

# ==============================================================================
# 2. Great Expectations Integration - 数据质量
# ==============================================================================

print("\n" + "=" * 70)
print("2. Great Expectations Integration - Data Quality")
print("=" * 70)

try:
    from aeva.integrations import GreatExpectationsProfiler

    print("\n📋 Initializing Great Expectations profiler...")

    # 创建DataFrame
    df = pd.DataFrame(X_train, columns=feature_names)

    # 创建profiler
    ge_profiler = GreatExpectationsProfiler()

    if ge_profiler.is_available():
        print("   ✓ Great Expectations library detected - using production implementation")
    else:
        print("   ⚠️  Great Expectations not installed - using fallback implementation")

    # 数据分析
    print("\n   Profiling dataset...")
    profile_results = ge_profiler.profile_dataframe(
        df,
        dataset_name="breast_cancer_training",
        profile_type="auto"
    )

    stats = profile_results.get('statistics', {})
    print(f"   ✓ Dataset profiled:")
    print(f"      Rows: {stats.get('row_count', 'N/A')}")
    print(f"      Columns: {stats.get('column_count', 'N/A')}")

    if 'quality_score' in stats:
        print(f"      Quality Score: {stats['quality_score']:.1f}/100")

    # 验证
    print("\n   Validating dataset...")
    validation_results = ge_profiler.validate(df, profile_results)

    val_stats = validation_results.get('statistics', {})
    print(f"   ✓ Validation complete:")
    print(f"      Success: {validation_results.get('success', False)}")

    if 'evaluated_expectations' in val_stats:
        print(f"      Evaluated: {val_stats['evaluated_expectations']}")
        print(f"      Successful: {val_stats['successful_expectations']}")
        print(f"      Success rate: {val_stats['success_percent']:.1f}%")

    # 生成文档
    print("\n   Generating data documentation...")
    docs = ge_profiler.generate_data_docs(profile_results, '/tmp/ge_data_quality.html')

    if docs.startswith('/'):
        print(f"   ✓ Documentation saved to {docs}")
    else:
        print(f"   ✓ Documentation generated ({len(docs)} characters)")
        with open('/tmp/ge_data_quality.html', 'w') as f:
            f.write(docs)
        print(f"   ✓ Saved to /tmp/ge_data_quality.html")

except Exception as e:
    print(f"\n   ✗ Great Expectations integration failed: {e}")
    print("   Install with: pip install great_expectations")

# ==============================================================================
# 3. statsmodels Integration - 高级统计检验
# ==============================================================================

print("\n" + "=" * 70)
print("3. statsmodels Integration - Advanced A/B Testing")
print("=" * 70)

try:
    from aeva.integrations import StatsModelsABTest

    print("\n📊 Initializing statsmodels A/B tester...")

    # 训练两个模型进行比较
    print("\n   Training two models for comparison...")
    model_a = RandomForestClassifier(n_estimators=30, random_state=42)
    model_b = GradientBoostingClassifier(n_estimators=30, random_state=42)

    model_a.fit(X_train, y_train)
    model_b.fit(X_train, y_train)

    scores_a = cross_val_score(model_a, X_test, y_test, cv=5)
    scores_b = cross_val_score(model_b, X_test, y_test, cv=5)

    print(f"   ✓ Model A (RF): {scores_a.mean():.4f} ± {scores_a.std():.4f}")
    print(f"   ✓ Model B (GB): {scores_b.mean():.4f} ± {scores_b.std():.4f}")

    # 创建测试器
    sm_tester = StatsModelsABTest(significance_level=0.05)

    if sm_tester.is_available():
        print("   ✓ statsmodels library detected - using production implementation")
    else:
        print("   ⚠️  statsmodels not installed - using scipy fallback")

    # 高级A/B测试
    print("\n   Running advanced A/B test...")
    result = sm_tester.advanced_ab_test(
        scores_a.tolist(),
        scores_b.tolist(),
        test_type='welch'
    )

    print(f"   ✓ Test completed:")
    print(f"      Effect size: {result.effect_size:.4f}")
    print(f"      P-value: {result.p_value:.6f}")
    print(f"      95% CI: ({result.confidence_interval[0]:.4f}, {result.confidence_interval[1]:.4f})")
    print(f"      Significant: {result.is_significant}")

    if result.power > 0:
        print(f"      Statistical power: {result.power:.2%}")

    if result.winner:
        print(f"      Winner: {result.winner}")

    # 贝叶斯A/B测试
    print("\n   Running Bayesian A/B test...")
    bayesian_result = sm_tester.bayesian_ab_test(
        scores_a.tolist(),
        scores_b.tolist()
    )

    if bayesian_result.get('available'):
        print(f"   ✓ Bayesian test completed:")
        print(f"      P(B > A): {bayesian_result['prob_b_better_than_a']:.2%}")
        print(f"      Recommendation: {bayesian_result['recommendation']}")
    else:
        print(f"   ⚠️  {bayesian_result.get('message', 'Not available')}")

    # 功效分析
    print("\n   Running power analysis...")
    power_result = sm_tester.power_analysis(
        effect_size=0.5,  # Medium effect
        alpha=0.05,
        power=0.8
    )

    print(f"   ✓ Power analysis completed:")
    print(f"      Required sample size (each group): {power_result['n1_required']}")
    print(f"      Total required: {power_result['total_required']}")

    # 生成报告
    print("\n" + "=" * 70)
    print("A/B Test Report Preview:")
    print("=" * 70)

    report = sm_tester.generate_report(result)
    print(report[:500] + "...\n")

    with open('/tmp/ab_test_report.txt', 'w') as f:
        f.write(report)
    print(f"   ✓ Full report saved to /tmp/ab_test_report.txt")

except Exception as e:
    print(f"\n   ✗ statsmodels integration failed: {e}")
    print("   Install with: pip install statsmodels")

# ==============================================================================
# 总结
# ==============================================================================

print("\n" + "=" * 70)
print("🎉 Production Integrations Demo Complete!")
print("=" * 70)

print("\n📝 Summary:")
print("   1. ART Integration - Advanced adversarial robustness testing")
print("   2. Great Expectations - Production data quality validation")
print("   3. statsmodels - Comprehensive statistical analysis")

print("\n💡 Installation:")
print("   pip install adversarial-robustness-toolbox  # For ART")
print("   pip install great_expectations              # For GE")
print("   pip install statsmodels                      # For statsmodels")

print("\n✨ All integrations include automatic fallback to basic implementations")
print("   if the production libraries are not installed.")

print("\n📄 Generated files:")
print("   - /tmp/art_robustness_report.txt")
print("   - /tmp/ge_data_quality.html")
print("   - /tmp/ab_test_report.txt")

print("\n" + "=" * 70)
