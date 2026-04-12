"""
Benchmark Suite page - Advanced feature

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def render():
    """Render benchmark suite page"""

    # Back button
    if st.button("← 返回主页", key="back_from_benchmark"):
        st.session_state.subpage = None
        st.rerun()

    st.markdown('<p class="main-header">🏆 基准测试套件</p>', unsafe_allow_html=True)
    st.markdown("### 标准化评估与多模型对比")

    st.markdown("---")

    tabs = st.tabs(["📊 基准套件", "🎯 运行测试", "📈 结果对比", "💻 代码示例"])

    with tabs[0]:
        render_suite_management()

    with tabs[1]:
        render_run_benchmark()

    with tabs[2]:
        render_results_comparison()

    with tabs[3]:
        render_code_examples()


def render_suite_management():
    st.markdown("## 📊 基准测试套件管理")

    st.markdown("""
    管理和配置标准化基准测试套件，支持多个评估指标和测试场景。

    **核心功能**:
    - 📋 创建自定义基准套件
    - 🔧 配置评估指标
    - 📁 管理测试数据集
    - 🔄 复用标准套件
    """)

    st.markdown("---")

    st.markdown("### 已注册的基准套件")

    # Demo benchmark suites
    suites_data = [
        {
            "名称": "ml_comparison_suite",
            "描述": "机器学习算法综合对比",
            "指标数": 4,
            "状态": "活跃"
        },
        {
            "名称": "classification_benchmark",
            "描述": "分类任务标准测试",
            "指标数": 6,
            "状态": "活跃"
        },
        {
            "名称": "regression_benchmark",
            "描述": "回归任务标准测试",
            "指标数": 5,
            "状态": "活跃"
        }
    ]

    df = pd.DataFrame(suites_data)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    st.markdown("### 创建新的基准套件")

    with st.form("create_suite"):
        suite_name = st.text_input("套件名称", "my_benchmark_suite")
        suite_desc = st.text_area("描述", "自定义基准测试套件")

        st.markdown("**选择评估指标**:")
        col1, col2 = st.columns(2)

        with col1:
            metric_accuracy = st.checkbox("Accuracy (准确率)", value=True)
            metric_precision = st.checkbox("Precision (精确率)", value=True)
            metric_recall = st.checkbox("Recall (召回率)", value=True)

        with col2:
            metric_f1 = st.checkbox("F1 Score", value=True)
            metric_auc = st.checkbox("AUC-ROC", value=False)
            metric_mse = st.checkbox("MSE (均方误差)", value=False)

        submitted = st.form_submit_button("创建基准套件")

        if submitted:
            selected_metrics = []
            if metric_accuracy:
                selected_metrics.append("accuracy")
            if metric_precision:
                selected_metrics.append("precision")
            if metric_recall:
                selected_metrics.append("recall")
            if metric_f1:
                selected_metrics.append("f1_score")
            if metric_auc:
                selected_metrics.append("auc_roc")
            if metric_mse:
                selected_metrics.append("mse")

            st.success(f"✅ 基准套件 '{suite_name}' 创建成功!")
            st.info(f"包含 {len(selected_metrics)} 个评估指标: {', '.join(selected_metrics)}")


def render_run_benchmark():
    st.markdown("## 🎯 运行基准测试")

    st.markdown("""
    运行标准化基准测试，评估多个模型的性能表现。
    """)

    if st.button("🚀 运行基准测试演示", key="run_benchmark"):
        with st.spinner("正在运行基准测试..."):
            try:
                from aeva.bench import BenchmarkSuite, Benchmark, BenchmarkManager

                st.success("✅ 基准测试完成!")

                # Demo results
                st.markdown("### 测试结果")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("测试模型数", "3")

                with col2:
                    st.metric("评估指标数", "4")

                with col3:
                    st.metric("总测试次数", "12")

                # Results table
                st.markdown("### 详细结果")

                results_data = {
                    "模型": ["RandomForest", "GradientBoosting", "LogisticRegression"],
                    "Accuracy": [0.92, 0.89, 0.85],
                    "Precision": [0.91, 0.88, 0.84],
                    "Recall": [0.93, 0.90, 0.86],
                    "F1 Score": [0.92, 0.89, 0.85]
                }

                df = pd.DataFrame(results_data)
                st.dataframe(
                    df.style.highlight_max(axis=0, subset=["Accuracy", "Precision", "Recall", "F1 Score"]),
                    use_container_width=True
                )

                # Best model
                best_model_idx = df["Accuracy"].idxmax()
                best_model = df.iloc[best_model_idx]["模型"]
                st.success(f"🏆 最佳模型: **{best_model}** (Accuracy: {df.iloc[best_model_idx]['Accuracy']:.2%})")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    st.markdown("---")

    st.markdown("### 配置测试参数")

    col1, col2 = st.columns(2)

    with col1:
        test_size = st.slider("测试集比例", 0.1, 0.5, 0.2, 0.05)
        random_state = st.number_input("随机种子", value=42, min_value=0)

    with col2:
        cv_folds = st.number_input("交叉验证折数", value=5, min_value=2, max_value=10)
        scoring = st.selectbox("评分方式", ["accuracy", "f1", "roc_auc", "precision", "recall"])


def render_results_comparison():
    st.markdown("## 📈 基准测试结果对比")

    st.markdown("""
    对比多个模型在标准基准测试上的表现，生成排名和可视化报告。
    """)

    if st.button("📊 生成对比报告", key="gen_comparison"):
        with st.spinner("正在生成对比报告..."):
            st.success("✅ 对比报告生成完成!")

            # Performance comparison
            st.markdown("### 性能对比")

            models = ["RandomForest", "GradientBoosting", "LogisticRegression", "SVM", "NeuralNet"]
            metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]

            # Generate demo data
            np.random.seed(42)
            data = {}
            data["模型"] = models
            for metric in metrics:
                data[metric] = np.random.uniform(0.75, 0.95, len(models))

            df = pd.DataFrame(data)

            # Bar chart
            st.bar_chart(df.set_index("模型")[metrics])

            st.markdown("---")

            # Ranking table
            st.markdown("### 综合排名")

            # Calculate overall score
            df["综合得分"] = df[metrics].mean(axis=1)
            df_sorted = df.sort_values("综合得分", ascending=False).reset_index(drop=True)
            df_sorted.index = df_sorted.index + 1
            df_sorted.index.name = "排名"

            st.dataframe(
                df_sorted.style.background_gradient(subset=["综合得分"], cmap="RdYlGn"),
                use_container_width=True
            )

            # Top 3
            st.markdown("### 🏆 Top 3 模型")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### 🥇 第一名")
                top1 = df_sorted.iloc[0]
                st.metric(top1["模型"], f"{top1['综合得分']:.2%}")

            with col2:
                st.markdown("#### 🥈 第二名")
                top2 = df_sorted.iloc[1]
                st.metric(top2["模型"], f"{top2['综合得分']:.2%}")

            with col3:
                st.markdown("#### 🥉 第三名")
                top3 = df_sorted.iloc[2]
                st.metric(top3["模型"], f"{top3['综合得分']:.2%}")


def render_code_examples():
    st.markdown("## 💻 代码示例")

    st.markdown("### 1. 创建基准测试套件")

    st.code("""
from aeva.bench import BenchmarkSuite, Benchmark

# 创建基准测试套件
suite = BenchmarkSuite(
    name="ml_comparison_suite",
    description="机器学习算法综合对比"
)

# 定义评估函数
def evaluate_accuracy(algorithm, test_data):
    X_test, y_test = test_data
    y_pred = algorithm.predict(X_test)
    return accuracy_score(y_test, y_pred)

# 添加基准测试
benchmark = Benchmark(
    name="accuracy",
    metric_type="accuracy",
    evaluate_fn=evaluate_accuracy
)

suite.add_benchmark(benchmark)
print(f"Suite created with {len(suite)} benchmarks")
""", language="python")

    st.markdown("---")

    st.markdown("### 2. 运行基准测试")

    st.code("""
from aeva.bench import BenchmarkManager
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# 初始化管理器
manager = BenchmarkManager()

# 注册基准套件
manager.register_suite(suite)

# 准备模型
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100),
    'GradientBoosting': GradientBoostingClassifier(n_estimators=100)
}

# 训练模型
for name, model in models.items():
    model.fit(X_train, y_train)

# 运行基准测试
results = manager.run_suite(
    suite_name="ml_comparison_suite",
    algorithms=models,
    test_data=(X_test, y_test)
)

# 查看结果
for model_name, scores in results.items():
    print(f"{model_name}:")
    for metric, score in scores.items():
        print(f"  {metric}: {score:.4f}")
""", language="python")

    st.markdown("---")

    st.markdown("### 3. 生成对比报告")

    st.code("""
# 获取所有结果
all_results = manager.get_all_results()

# 生成排名
ranking = manager.get_ranking(
    suite_name="ml_comparison_suite",
    metric="accuracy"
)

print("模型排名 (按Accuracy):")
for rank, (model_name, score) in enumerate(ranking, 1):
    print(f"{rank}. {model_name}: {score:.4f}")

# 导出报告
manager.export_report(
    suite_name="ml_comparison_suite",
    output_path="benchmark_report.json"
)
""", language="python")

    st.markdown("---")

    st.info("""
    💡 **使用建议**:
    - 使用标准基准测试确保评估的一致性
    - 定期运行基准测试跟踪模型性能
    - 对比多个模型选择最佳方案
    - 将结果用于模型选型和优化决策
    """)
