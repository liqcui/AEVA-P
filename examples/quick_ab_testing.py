"""
Quick A/B Testing Test - Statistical Comparison Demo
快速验证A/B测试模块的核心功能
"""
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import sys
sys.path.insert(0, '.')

from aeva.ab_testing import ABTester, StatisticalTest

print("=" * 70)
print("AEVA A/B Testing Module - Quick Test")
print("=" * 70)

# Load data
print("\n1. Loading data...")
data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   ✓ Training: {len(X_train)}, Test: {len(X_test)}")

# Train two models (Variant A vs Variant B)
print("\n2. Training two models...")
try:
    # Variant A: Random Forest
    model_a = RandomForestClassifier(n_estimators=50, random_state=42)
    model_a.fit(X_train, y_train)
    scores_a = cross_val_score(model_a, X_test, y_test, cv=5)

    # Variant B: Gradient Boosting
    model_b = GradientBoostingClassifier(n_estimators=50, random_state=42)
    model_b.fit(X_train, y_train)
    scores_b = cross_val_score(model_b, X_test, y_test, cv=5)

    print(f"   ✓ Variant A (RF) mean score: {scores_a.mean():.3f}")
    print(f"   ✓ Variant B (GB) mean score: {scores_b.mean():.3f}")
except Exception as e:
    print(f"   ✗ Model training failed: {e}")
    scores_a = [0.96, 0.95, 0.97, 0.96, 0.95]
    scores_b = [0.97, 0.96, 0.98, 0.97, 0.96]

# Test ABTester
print("\n3. Testing A/B Tester...")
try:
    tester = ABTester(
        variant_a_name="Random Forest",
        variant_b_name="Gradient Boosting",
        significance_level=0.05
    )

    result = tester.compare(
        variant_a_scores=scores_a.tolist(),
        variant_b_scores=scores_b.tolist(),
        metric_name="accuracy"
    )

    print(f"   ✓ Test complete")
    print(f"   ✓ Variant A mean: {result.variant_a_mean:.4f}")
    print(f"   ✓ Variant B mean: {result.variant_b_mean:.4f}")
    print(f"   ✓ Difference: {result.difference:.4f}")
    print(f"   ✓ Improvement: {result.improvement_percentage:.2f}%")
    print(f"   ✓ P-value: {result.p_value:.4f}")
    print(f"   ✓ Significant: {result.is_significant}")
    print(f"   ✓ Winner: {result.winner if result.winner else 'No clear winner'}")
except Exception as e:
    print(f"   ✗ AB test failed: {e}")

# Test Statistical Tests
print("\n4. Testing Statistical Test Methods...")
try:
    stat_test = StatisticalTest()

    # T-test
    t_stat, t_pvalue = stat_test.t_test(scores_a.tolist(), scores_b.tolist())
    print(f"   ✓ T-test: statistic={t_stat:.4f}, p-value={t_pvalue:.4f}")

    # Mann-Whitney U test
    u_stat, u_pvalue = stat_test.mann_whitney_u(scores_a.tolist(), scores_b.tolist())
    print(f"   ✓ Mann-Whitney: statistic={u_stat:.4f}, p-value={u_pvalue:.4f}")

    # Effect size (Cohen's d)
    effect_size = stat_test.cohens_d(scores_a.tolist(), scores_b.tolist())
    print(f"   ✓ Cohen's d: {effect_size:.4f}")

    if abs(effect_size) < 0.2:
        magnitude = "small"
    elif abs(effect_size) < 0.5:
        magnitude = "medium"
    else:
        magnitude = "large"
    print(f"   ✓ Effect magnitude: {magnitude}")
except Exception as e:
    print(f"   ✗ Statistical tests failed: {e}")

# Test with classification predictions
print("\n5. Testing with classification results...")
try:
    # Get predictions
    pred_a = model_a.predict(X_test)
    pred_b = model_b.predict(X_test)

    # Chi-square test
    chi_stat, chi_pvalue = stat_test.chi_square_test(pred_a, pred_b)
    print(f"   ✓ Chi-square test: statistic={chi_stat:.4f}, p-value={chi_pvalue:.4f}")
except Exception as e:
    print(f"   ✗ Classification test failed: {e}")

# Test Report Generation
print("\n6. Testing Report Generation...")
try:
    report = tester.generate_report(result)
    print(f"   ✓ Report generated ({len(report)} characters)")

    # Save to file
    with open('/tmp/ab_test_report.txt', 'w') as f:
        f.write(report)
    print(f"   ✓ Saved to /tmp/ab_test_report.txt")
except Exception as e:
    print(f"   ✗ Report generation failed: {e}")

print("\n" + "=" * 70)
print("✅ A/B Testing Module Test Complete!")
print("=" * 70)
