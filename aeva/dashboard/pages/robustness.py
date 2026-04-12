"""
Adversarial robustness page

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import numpy as np
import pandas as pd

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def render():
    """Render robustness page"""

    st.markdown('<p class="main-header">🛡️ 对抗鲁棒性测试</p>', unsafe_allow_html=True)
    st.markdown("### 评估模型对对抗攻击的鲁棒性")

    st.markdown("---")

    tabs = st.tabs(["⚔️ FGSM攻击", "💥 PGD攻击", "🎯 综合测试", "💻 代码示例"])

    with tabs[0]:
        render_fgsm_tab()

    with tabs[1]:
        render_pgd_tab()

    with tabs[2]:
        render_comprehensive_tab()

    with tabs[3]:
        render_code_tab()


def render_fgsm_tab():
    st.markdown("## ⚔️ FGSM (Fast Gradient Sign Method)")

    st.markdown("""
    FGSM是最简单快速的对抗攻击方法，通过梯度方向添加扰动。

    **特点**:
    - ⚡ 速度快（单步攻击）
    - 📊 效果适中
    - 🎯 适合快速测试
    """)

    if st.button("🚀 运行FGSM攻击", key="fgsm"):
        with st.spinner("正在生成对抗样本..."):
            try:
                from aeva.robustness import FGSMAttack
                from sklearn.datasets import load_breast_cancer
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.model_selection import train_test_split

                # Load and train
                data = load_breast_cancer()
                X_train, X_test, y_train, y_test = train_test_split(
                    data.data, data.target, test_size=0.2, random_state=42
                )
                model = RandomForestClassifier(n_estimators=30, random_state=42)
                model.fit(X_train, y_train)

                # FGSM attack
                fgsm = FGSMAttack(model, epsilon=0.1)
                result = fgsm.generate(X_test[0], y_test[0])

                st.success("✅ FGSM攻击完成!")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("原始预测", result.original_pred)
                    st.metric("对抗预测", result.adversarial_pred)
                with col2:
                    st.metric("攻击成功", "是" if result.success else "否")
                    st.metric("扰动大小", f"{result.perturbation:.4f}")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")


def render_pgd_tab():
    st.markdown("## 💥 PGD (Projected Gradient Descent)")

    st.markdown("""
    PGD是FGSM的迭代加强版，通过多步优化生成更强的对抗样本。

    **特点**:
    - 🎯 攻击能力强
    - 🔄 多步迭代
    - ⏱️ 计算较慢
    """)

    if st.button("🚀 运行PGD攻击", key="pgd"):
        st.info("PGD攻击演示（需要更多时间）")


def render_comprehensive_tab():
    st.markdown("## 🎯 综合鲁棒性测试")

    st.markdown("""
    使用多种攻击方法全面评估模型鲁棒性。

    **测试内容**:
    - ⚔️ FGSM攻击
    - 💥 PGD攻击
    - 🎭 BIM攻击
    - 📊 综合评分
    """)

    if st.button("🚀 运行综合测试", key="comprehensive"):
        with st.spinner("正在进行综合测试..."):
            try:
                from aeva.robustness import RobustnessEvaluator
                from sklearn.datasets import load_breast_cancer
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.model_selection import train_test_split

                data = load_breast_cancer()
                X_train, X_test, y_train, y_test = train_test_split(
                    data.data, data.target, test_size=0.2, random_state=42
                )
                model = RandomForestClassifier(n_estimators=30, random_state=42)
                model.fit(X_train, y_train)

                evaluator = RobustnessEvaluator(model)
                results = evaluator.evaluate(X_test[:20], y_test[:20])

                st.success("✅ 综合测试完成!")

                st.metric("鲁棒性评分", f"{results.get('robustness_score', 0):.1%}")

                if 'attack_results' in results:
                    df = pd.DataFrame(results['attack_results'])
                    st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")


def render_code_tab():
    st.markdown("## 💻 代码示例")

    st.code("""
from aeva.robustness import FGSMAttack, PGDAttack, RobustnessEvaluator

# FGSM攻击
fgsm = FGSMAttack(model, epsilon=0.1)
result = fgsm.generate(X_test[0], y_test[0])

# PGD攻击
pgd = PGDAttack(model, epsilon=0.1, max_iterations=10)
result = pgd.generate(X_test[0], y_test[0])

# 综合测试
evaluator = RobustnessEvaluator(model)
results = evaluator.evaluate(X_test, y_test)
""", language="python")
