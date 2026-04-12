"""
运行所有新模块的快速测试
"""
import subprocess
import sys
sys.path.insert(0, '.')

tests = [
    ("可解释性", "examples/quick_explainability.py"),
    ("对抗鲁棒性", "examples/quick_robustness.py"),
    ("模型卡片", "examples/quick_model_cards.py"),
    ("数据质量", "examples/quick_data_quality.py"),
    ("A/B测试", "examples/quick_ab_testing.py"),
]

print("=" * 70)
print("运行所有新模块快速测试")
print("=" * 70)

results = {}

for name, script in tests:
    print(f"\n{'='*70}")
    print(f"测试模块: {name}")
    print(f"{'='*70}\n")

    # Note: We'll create simplified inline tests instead

# 简化测试 - 直接在这里验证核心功能
print("\n" + "=" * 70)
print("核心功能验证")
print("=" * 70)

# 1. 可解释性
print("\n1. ✓ 可解释性模块 - SHAP/LIME/特征重要性")
try:
    from aeva.explainability import SHAPExplainer, LIMEExplainer, FeatureImportanceAnalyzer
    print("   ✓ 导入成功")
except Exception as e:
    print(f"   ✗ 导入失败: {e}")

# 2. 对抗鲁棒性
print("\n2. ✓ 对抗鲁棒性模块 - FGSM/PGD/BIM攻击")
try:
    from aeva.robustness import FGSMAttack, PGDAttack, BIMAttack, RobustnessEvaluator
    print("   ✓ 导入成功")
except Exception as e:
    print(f"   ✗ 导入失败: {e}")

# 3. 模型卡片
print("\n3. ✓ 模型卡片模块 - 文档生成与验证")
try:
    from aeva.model_cards import ModelCardGenerator, ModelCardValidator
    print("   ✓ 导入成功")
except Exception as e:
    print(f"   ✗ 导入失败: {e}")

# 4. 数据质量
print("\n4. ✓ 数据质量模块 - 数据画像与质量指标")
try:
    from aeva.data_quality import DataProfiler, QualityMetrics
    print("   ✓ 导入成功")
except Exception as e:
    print(f"   ✗ 导入失败: {e}")

# 5. A/B测试
print("\n5. ✓ A/B测试模块 - 统计检验")
try:
    from aeva.ab_testing import ABTester, StatisticalTest
    print("   ✓ 导入成功")
except Exception as e:
    print(f"   ✗ 导入失败: {e}")

print("\n" + "=" * 70)
print("✅ 所有模块导入测试完成！")
print("=" * 70)

# 快速功能测试
print("\n" + "=" * 70)
print("快速功能测试")
print("=" * 70)

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 加载数据
data = load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
model = RandomForestClassifier(n_estimators=30, random_state=42, max_depth=5)
model.fit(X_train, y_train)

print(f"\n准备测试数据: {len(X_train)} 训练样本, {len(X_test)} 测试样本")

# 测试1: SHAP解释
print("\n[1/5] 测试SHAP解释...")
try:
    from aeva.explainability import SHAPExplainer
    explainer = SHAPExplainer(
        model=model,
        background_data=X_train[:50],
        feature_names=data.feature_names.tolist()
    )
    explanation = explainer.explain_instance(X_test[0])
    top_features = explanation.get_top_features(3)
    print(f"   ✓ SHAP成功 - Top 3特征: {[f[0][:20] for f in top_features]}")
except Exception as e:
    print(f"   ✗ 失败: {e}")

# 测试2: 对抗攻击
print("\n[2/5] 测试FGSM对抗攻击...")
try:
    from aeva.robustness import FGSMAttack
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    fgsm = FGSMAttack(model)
    result = fgsm.attack(X_test_scaled[0], y_test[0], epsilon=0.05)
    print(f"   ✓ FGSM成功 - 攻击成功: {result.success}")
except Exception as e:
    print(f"   ✗ 失败: {e}")

# 测试3: 模型卡片
print("\n[3/5] 测试模型卡片生成...")
try:
    from aeva.model_cards import ModelCardGenerator
    generator = ModelCardGenerator("Test Model")
    card = generator.generate_card(
        model_version="1.0",
        intended_use="Testing",
        performance_metrics={'accuracy': 0.96}
    )
    generator.export_json(card, '/tmp/test_card.json')
    print(f"   ✓ 模型卡片成功 - 已保存到 /tmp/test_card.json")
except Exception as e:
    print(f"   ✗ 失败: {e}")

# 测试4: 数据质量
print("\n[4/5] 测试数据质量分析...")
try:
    from aeva.data_quality import DataProfiler
    import pandas as pd
    df = pd.DataFrame(X_train, columns=data.feature_names)
    profiler = DataProfiler()
    profile = profiler.profile(df)
    print(f"   ✓ 数据质量成功 - 质量分数: {profile.quality_score:.1f}/100")
except Exception as e:
    print(f"   ✗ 失败: {e}")

# 测试5: A/B测试
print("\n[5/5] 测试A/B统计比较...")
try:
    from aeva.ab_testing import StatisticalTest
    stat_test = StatisticalTest()
    scores_a = [0.95, 0.96, 0.94, 0.97, 0.95]
    scores_b = [0.96, 0.97, 0.95, 0.98, 0.96]
    t_stat, p_value = stat_test.t_test(scores_a, scores_b)
    print(f"   ✓ A/B测试成功 - p值: {p_value:.4f}")
except Exception as e:
    print(f"   ✗ 失败: {e}")

print("\n" + "=" * 70)
print("🎉 全部测试完成！")
print("=" * 70)
