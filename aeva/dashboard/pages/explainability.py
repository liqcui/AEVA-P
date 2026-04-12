"""
Explainability analysis page

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def render():
    """Render explainability page"""

    st.markdown('<p class="main-header">🔍 可解释性分析</p>', unsafe_allow_html=True)
    st.markdown("### 使用SHAP, LIME, 特征重要性解释模型决策")

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SHAP分析", "🔬 LIME解释", "📈 特征重要性", "💡 示例代码"])

    with tab1:
        render_shap_tab()

    with tab2:
        render_lime_tab()

    with tab3:
        render_feature_importance_tab()

    with tab4:
        render_code_examples()


def render_shap_tab():
    """Render SHAP analysis tab"""

    st.markdown("## 📊 SHAP (SHapley Additive exPlanations)")

    st.markdown("""
    SHAP基于博弈论的Shapley值，提供模型决策的公平、一致的解释。

    **优势**:
    - ✅ 理论基础坚实（Shapley值）
    - ✅ 全局和局部解释
    - ✅ 支持所有模型类型
    - ✅ 丰富的可视化
    """)

    if st.button("🚀 运行SHAP演示", key="shap_demo"):
        with st.spinner("正在计算SHAP值..."):
            try:
                from aeva.explainability import SHAPExplainer
                from sklearn.datasets import load_breast_cancer
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.model_selection import train_test_split

                # Load data
                data = load_breast_cancer()
                X_train, X_test, y_train, y_test = train_test_split(
                    data.data, data.target, test_size=0.2, random_state=42
                )

                # Train model
                model = RandomForestClassifier(n_estimators=30, random_state=42, max_depth=5)
                model.fit(X_train, y_train)

                # SHAP analysis
                explainer = SHAPExplainer(
                    model=model,
                    background_data=X_train[:50],
                    feature_names=data.feature_names.tolist()
                )

                # Explain instance
                instance_idx = 0
                explanation = explainer.explain_instance(X_test[instance_idx])

                # Display results
                st.success("✅ SHAP分析完成!")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 预测结果")
                    pred = model.predict_proba(X_test[instance_idx:instance_idx+1])[0]
                    st.metric("恶性概率", f"{pred[0]:.1%}")
                    st.metric("良性概率", f"{pred[1]:.1%}")

                with col2:
                    st.markdown("### Top 5 特征")
                    top_features = explanation.get_top_features(5)
                    df = pd.DataFrame(top_features, columns=["特征", "SHAP值"])
                    st.dataframe(df, use_container_width=True)

                # Feature values
                st.markdown("### 特征值")
                feature_df = pd.DataFrame({
                    '特征': data.feature_names[:10],
                    '值': X_test[instance_idx][:10]
                })
                st.dataframe(feature_df, use_container_width=True)

                st.info("""
                💡 **解读**: SHAP值表示每个特征对模型预测的贡献。
                正值推动预测向一个方向，负值推动向另一个方向。
                """)

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")

    st.markdown("---")

    st.markdown("""
    ### 🎯 使用场景

    - **医疗诊断**: 解释疾病预测，理解关键症状
    - **金融风控**: 解释信用评分，满足合规要求
    - **推荐系统**: 解释推荐理由，提高用户信任
    - **自动驾驶**: 解释决策过程，确保安全
    """)


def render_lime_tab():
    """Render LIME tab"""

    st.markdown("## 🔬 LIME (Local Interpretable Model-agnostic Explanations)")

    st.markdown("""
    LIME通过局部线性近似解释复杂模型的预测。

    **优势**:
    - ✅ 模型无关
    - ✅ 局部可解释
    - ✅ 直观易懂
    - ✅ 快速计算
    """)

    if st.button("🚀 运行LIME演示", key="lime_demo"):
        with st.spinner("正在计算LIME解释..."):
            try:
                from aeva.explainability import LIMEExplainer
                from sklearn.datasets import load_breast_cancer
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.model_selection import train_test_split

                # Load data
                data = load_breast_cancer()
                X_train, X_test, y_train, y_test = train_test_split(
                    data.data, data.target, test_size=0.2, random_state=42
                )

                # Train model
                model = RandomForestClassifier(n_estimators=30, random_state=42, max_depth=5)
                model.fit(X_train, y_train)

                # LIME analysis
                explainer = LIMEExplainer(
                    model=model,
                    training_data=X_train,
                    feature_names=data.feature_names.tolist()
                )

                # Explain instance
                instance_idx = 0
                explanation = explainer.explain_instance(X_test[instance_idx])

                # Display results
                st.success("✅ LIME分析完成!")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 预测结果")
                    pred = model.predict_proba(X_test[instance_idx:instance_idx+1])[0]
                    st.metric("恶性概率", f"{pred[0]:.1%}")
                    st.metric("良性概率", f"{pred[1]:.1%}")

                with col2:
                    st.markdown("### Top 5 特征")
                    top_features = explanation.get_top_features(5)
                    df = pd.DataFrame(top_features, columns=["特征", "权重"])
                    st.dataframe(df, use_container_width=True)

                st.info("""
                💡 **解读**: LIME权重表示特征对预测的影响。
                通过在实例周围采样，LIME构建局部线性模型来解释预测。
                """)

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")

    st.markdown("---")

    st.markdown("""
    ### 🎯 LIME vs SHAP

    | 特性 | LIME | SHAP |
    |------|------|------|
    | 理论基础 | 局部近似 | Shapley值 |
    | 全局解释 | ❌ | ✅ |
    | 局部解释 | ✅ | ✅ |
    | 计算速度 | 快 | 慢 |
    | 一致性 | 低 | 高 |
    | 适用场景 | 快速原型 | 生产部署 |
    """)


def render_feature_importance_tab():
    """Render feature importance tab"""

    st.markdown("## 📈 特征重要性分析")

    st.markdown("""
    分析模型中每个特征的重要性，帮助理解哪些特征对预测最关键。

    **方法**:
    - 📊 **模型内置重要性**: RandomForest, XGBoost等
    - 🔀 **排列重要性**: 打乱特征值，观察性能下降
    - 📉 **Drop重要性**: 删除特征，观察性能变化
    """)

    if st.button("🚀 运行特征重要性分析", key="fi_demo"):
        with st.spinner("正在计算特征重要性..."):
            try:
                from aeva.explainability import FeatureImportanceAnalyzer
                from sklearn.datasets import load_breast_cancer
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.model_selection import train_test_split

                # Load data
                data = load_breast_cancer()
                X_train, X_test, y_train, y_test = train_test_split(
                    data.data, data.target, test_size=0.2, random_state=42
                )

                # Train model
                model = RandomForestClassifier(n_estimators=30, random_state=42, max_depth=5)
                model.fit(X_train, y_train)

                # Feature importance analysis
                analyzer = FeatureImportanceAnalyzer(
                    model=model,
                    feature_names=data.feature_names.tolist()
                )

                # Get importance
                importance = analyzer.get_feature_importance()

                # Display results
                st.success("✅ 特征重要性分析完成!")

                # Top 10 features
                st.markdown("### Top 10 重要特征")
                df = pd.DataFrame(
                    list(importance.items())[:10],
                    columns=["特征", "重要性"]
                )
                df = df.sort_values("重要性", ascending=False)

                # Bar chart
                st.bar_chart(df.set_index("特征"))

                # Table
                st.dataframe(df, use_container_width=True)

                st.info("""
                💡 **解读**: 特征重要性值越高，该特征对模型预测的贡献越大。
                可以用于特征选择，降维，和模型简化。
                """)

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")


def render_code_examples():
    """Render code examples tab"""

    st.markdown("## 💡 代码示例")

    st.markdown("### SHAP分析")

    st.code("""
from aeva.explainability import SHAPExplainer

# 创建解释器
explainer = SHAPExplainer(
    model=model,
    background_data=X_train[:100],
    feature_names=feature_names
)

# 解释单个实例
explanation = explainer.explain_instance(X_test[0])

# 获取top特征
top_features = explanation.get_top_features(10)
print(top_features)

# 可视化
explainer.visualize(X_test[0], save_path="shap_plot.png")
""", language="python")

    st.markdown("---")

    st.markdown("### LIME分析")

    st.code("""
from aeva.explainability import LIMEExplainer

# 创建解释器
explainer = LIMEExplainer(
    model=model,
    training_data=X_train,
    feature_names=feature_names
)

# 解释单个实例
explanation = explainer.explain_instance(X_test[0])

# 获取解释
top_features = explanation.get_top_features(10)
print(top_features)
""", language="python")

    st.markdown("---")

    st.markdown("### 特征重要性")

    st.code("""
from aeva.explainability import FeatureImportanceAnalyzer

# 创建分析器
analyzer = FeatureImportanceAnalyzer(
    model=model,
    feature_names=feature_names
)

# 获取重要性
importance = analyzer.get_feature_importance()

# 生成报告
report = analyzer.generate_importance_report()
print(report)
""", language="python")
