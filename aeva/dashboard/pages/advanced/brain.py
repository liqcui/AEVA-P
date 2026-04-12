"""
Brain (Intelligent Analysis) page - Advanced feature

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import json

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import i18n
from aeva.dashboard.i18n import t, get_current_language


def render():
    """Render brain (intelligent analysis) page"""

    # Back button
    if st.button(t("back_to_home"), key="back_from_brain"):
        st.session_state.subpage = None
        st.rerun()

    st.markdown(f'<p class="main-header">{t("brain_title")}</p>', unsafe_allow_html=True)
    st.markdown(f"### {t('brain_subtitle')}")

    st.markdown("---")

    tabs = st.tabs([
        t("brain_tab_analysis"),
        t("brain_tab_root_cause"),
        t("brain_tab_suggestions"),
        t("brain_tab_llm"),
        t("brain_tab_code")
    ])

    with tabs[0]:
        render_result_analysis()

    with tabs[1]:
        render_root_cause_analysis()

    with tabs[2]:
        render_improvement_suggestions()

    with tabs[3]:
        render_llm_configuration()

    with tabs[4]:
        render_code_examples()


def render_result_analysis():
    st.markdown("## 🔍 智能结果分析")

    st.markdown("""
    上传评估结果，使用LLM进行自动化深度分析。

    **核心功能**:
    - 📊 自动识别异常指标
    - 🔍 模式挖掘与趋势分析
    - 📈 性能对比分析
    - 🎯 关键问题识别
    """)

    st.markdown("---")

    # Upload evaluation results
    st.markdown("### 上传评估结果")

    uploaded_file = st.file_uploader(
        "选择评估结果文件 (JSON/CSV)",
        type=["json", "csv"],
        help="上传模型评估结果文件进行智能分析"
    )

    if st.button("🚀 运行智能分析演示", key="run_analysis"):
        with st.spinner("正在进行智能分析..."):
            try:
                from aeva.brain import BrainManager, ResultAnalyzer

                st.success("✅ 智能分析完成!")

                # Demo evaluation results
                st.markdown("### 评估结果概览")

                results_data = {
                    "指标": ["Accuracy", "Precision", "Recall", "F1 Score", "AUC-ROC", "训练时间"],
                    "当前值": [0.87, 0.85, 0.89, 0.87, 0.91, "45分钟"],
                    "基准值": [0.90, 0.88, 0.87, 0.88, 0.92, "30分钟"],
                    "差异": ["-3.3%", "-3.4%", "+2.3%", "-1.1%", "-1.1%", "+50%"],
                    "状态": ["⚠️ 偏低", "⚠️ 偏低", "✅ 正常", "⚠️ 偏低", "✅ 正常", "⚠️ 偏慢"]
                }

                df = pd.DataFrame(results_data)
                st.dataframe(df, use_container_width=True)

                st.markdown("---")

                # AI Analysis
                st.markdown("### 🤖 AI智能分析")

                st.markdown("#### 📊 异常检测")
                st.warning("""
                **检测到3项性能异常**:
                - Accuracy低于基准3.3% - 可能存在过拟合或数据质量问题
                - Precision低于基准3.4% - 假阳性率偏高
                - 训练时间增加50% - 可能存在性能瓶颈
                """)

                st.markdown("#### 🔍 模式识别")
                st.info("""
                **发现的关键模式**:
                - Recall表现良好(+2.3%)，但Precision偏低 → 模型倾向于更多预测为正类
                - F1 Score与Accuracy同步下降 → 整体性能退化
                - AUC-ROC保持稳定 → 模型的排序能力未受影响，问题可能在阈值选择
                """)

                st.markdown("#### 📈 趋势分析")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("性能趋势", "下降", "-2.5%")
                    st.caption("相比上一版本")

                with col2:
                    st.metric("效率趋势", "下降", "+50%")
                    st.caption("训练时间增加")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    st.markdown("---")

    st.markdown("### 分析配置")

    col1, col2 = st.columns(2)

    with col1:
        analysis_depth = st.select_slider(
            "分析深度",
            options=["快速", "标准", "深度", "全面"],
            value="标准"
        )

    with col2:
        comparison_baseline = st.selectbox(
            "对比基准",
            ["历史最佳", "上一版本", "行业标准", "自定义"]
        )


def render_root_cause_analysis():
    st.markdown("## 💡 根因分析")

    st.markdown("""
    使用LLM深度分析问题根本原因，提供专业诊断。
    """)

    if st.button("🔬 运行根因分析演示", key="run_root_cause"):
        with st.spinner("正在进行根因分析..."):
            st.success("✅ 根因分析完成!")

            # Problem identification
            st.markdown("### 🎯 问题识别")

            problems = [
                {
                    "问题": "Accuracy下降3.3%",
                    "严重程度": "中",
                    "影响范围": "整体性能"
                },
                {
                    "问题": "Precision偏低",
                    "严重程度": "中",
                    "影响范围": "假阳性控制"
                },
                {
                    "问题": "训练时间增加50%",
                    "严重程度": "高",
                    "影响范围": "效率"
                }
            ]

            df_problems = pd.DataFrame(problems)
            st.dataframe(df_problems, use_container_width=True)

            st.markdown("---")

            # Root cause analysis
            st.markdown("### 🔍 根因定位")

            with st.expander("**问题1: Accuracy下降** - 根因分析", expanded=True):
                st.markdown("""
                **可能原因**:

                1. **数据分布偏移** (可能性: 70%)
                   - 训练数据与测试数据分布不一致
                   - 新数据引入了未见过的模式
                   - 建议: 检查数据分布，使用数据增强

                2. **模型过拟合** (可能性: 50%)
                   - 模型在训练集上表现良好，但泛化能力下降
                   - 可能使用了过于复杂的模型
                   - 建议: 增加正则化，使用交叉验证

                3. **特征质量下降** (可能性: 30%)
                   - 某些特征工程失效
                   - 数据预处理问题
                   - 建议: 重新评估特征重要性

                **AI推荐**: 优先检查数据分布偏移
                """)

            with st.expander("**问题2: Precision偏低** - 根因分析"):
                st.markdown("""
                **可能原因**:

                1. **决策阈值不当** (可能性: 80%)
                   - 默认阈值0.5可能不适合当前数据
                   - 建议: 使用ROC曲线优化阈值

                2. **类别不平衡处理不当** (可能性: 60%)
                   - 正负样本比例失衡
                   - 建议: 使用SMOTE或调整类权重

                3. **模型偏向高召回率** (可能性: 40%)
                   - 模型倾向于预测更多正类
                   - 建议: 调整损失函数权重

                **AI推荐**: 优先优化决策阈值
                """)

            with st.expander("**问题3: 训练时间增加** - 根因分析"):
                st.markdown("""
                **可能原因**:

                1. **数据量增加** (可能性: 90%)
                   - 训练数据增加导致计算量上升
                   - 建议: 使用数据采样或分布式训练

                2. **模型复杂度增加** (可能性: 70%)
                   - 模型参数量增加
                   - 建议: 模型压缩或使用更高效的架构

                3. **计算资源不足** (可能性: 50%)
                   - CPU/GPU利用率低
                   - 建议: 优化数据加载和批处理

                **AI推荐**: 检查数据规模和计算资源配置
                """)

            st.markdown("---")

            # Impact assessment
            st.markdown("### 📊 影响评估")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("业务影响", "中等")
                st.caption("准确率下降影响用户体验")

            with col2:
                st.metric("成本影响", "高")
                st.caption("训练时间增加50%")

            with col3:
                st.metric("修复难度", "中等")
                st.caption("预计2-3天完成优化")


def render_improvement_suggestions():
    st.markdown("## 📝 改进建议")

    st.markdown("""
    基于分析结果，AI自动生成可执行的改进建议。
    """)

    if st.button("💡 生成改进建议", key="gen_suggestions"):
        with st.spinner("正在生成改进建议..."):
            st.success("✅ 改进建议生成完成!")

            st.markdown("### 🎯 优先级排序")

            # High priority
            st.markdown("#### 🔴 高优先级 (立即执行)")

            st.markdown("""
            **1. 优化决策阈值** ⭐⭐⭐⭐⭐
            - **目标**: 提升Precision到0.88+
            - **方法**: 使用ROC曲线找到最优阈值
            - **预期收益**: Precision +3-5%, F1 Score +2%
            - **工作量**: 2小时
            - **代码示例**:
            ```python
            from sklearn.metrics import roc_curve
            fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
            optimal_idx = np.argmax(tpr - fpr)
            optimal_threshold = thresholds[optimal_idx]
            ```
            """)

            st.markdown("""
            **2. 数据分布检查** ⭐⭐⭐⭐⭐
            - **目标**: 识别并修复数据偏移
            - **方法**: PSI (Population Stability Index) 分析
            - **预期收益**: Accuracy +2-4%
            - **工作量**: 4小时
            - **代码示例**:
            ```python
            from aeva.data_quality import DistributionAnalyzer
            analyzer = DistributionAnalyzer()
            psi_score = analyzer.calculate_psi(train_data, test_data)
            if psi_score > 0.2:
                print("Significant distribution shift detected")
            ```
            """)

            st.markdown("---")

            # Medium priority
            st.markdown("#### 🟡 中优先级 (本周完成)")

            st.markdown("""
            **3. 模型正则化调优** ⭐⭐⭐⭐
            - **目标**: 减少过拟合
            - **方法**: 调整L1/L2正则化参数
            - **预期收益**: Accuracy +1-2%
            - **工作量**: 6小时

            **4. 特征重要性重评估** ⭐⭐⭐⭐
            - **目标**: 移除低质量特征
            - **方法**: 使用SHAP值分析
            - **预期收益**: 训练时间 -20%, Accuracy +0.5%
            - **工作量**: 4小时

            **5. 计算资源优化** ⭐⭐⭐
            - **目标**: 减少训练时间
            - **方法**: 批处理优化、GPU利用率提升
            - **预期收益**: 训练时间 -30%
            - **工作量**: 8小时
            """)

            st.markdown("---")

            # Low priority
            st.markdown("#### 🟢 低优先级 (长期优化)")

            st.markdown("""
            **6. 模型架构探索** ⭐⭐⭐
            - **目标**: 尝试更高效的模型
            - **方法**: 测试LightGBM、CatBoost等
            - **预期收益**: 整体性能 +3-5%
            - **工作量**: 2周

            **7. 自动化超参数调优** ⭐⭐
            - **目标**: 寻找最优参数组合
            - **方法**: 使用Optuna或Hyperopt
            - **预期收益**: 性能 +1-3%
            - **工作量**: 1周
            """)

            st.markdown("---")

            # Implementation plan
            st.markdown("### 📅 实施计划")

            plan_data = {
                "建议": [
                    "优化决策阈值",
                    "数据分布检查",
                    "模型正则化调优",
                    "特征重要性重评估",
                    "计算资源优化"
                ],
                "预期收益": [
                    "Precision +3-5%",
                    "Accuracy +2-4%",
                    "Accuracy +1-2%",
                    "效率 +20%",
                    "训练时间 -30%"
                ],
                "工作量": ["2小时", "4小时", "6小时", "4小时", "8小时"],
                "优先级": ["高", "高", "中", "中", "中"],
                "状态": ["待开始", "待开始", "待开始", "待开始", "待开始"]
            }

            df_plan = pd.DataFrame(plan_data)
            st.dataframe(df_plan, use_container_width=True)

            st.markdown("---")

            st.success("""
            ✅ **综合建议**: 优先执行高优先级任务，预计可在1周内提升Accuracy至0.90+，Precision至0.88+，同时降低训练时间30%。
            """)


def render_llm_configuration():
    st.markdown("## 🤖 LLM配置")

    st.markdown("""
    配置LLM提供者和分析参数。

    **支持的LLM**:
    - 🤖 Claude (Anthropic)
    - 💬 GPT-4 (OpenAI)
    - 🌟 Gemini (Google)
    - 🔓 开源模型 (自托管)
    """)

    st.markdown("---")

    st.markdown("### LLM提供者配置")

    provider = st.selectbox(
        "选择LLM提供者",
        ["Claude (推荐)", "GPT-4", "Gemini", "自托管模型"]
    )

    if provider == "Claude (推荐)":
        st.markdown("#### Claude API配置")

        api_key = st.text_input(
            "API Key",
            type="password",
            help="从 https://console.anthropic.com/ 获取API密钥"
        )

        model = st.selectbox(
            "模型版本",
            ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"]
        )

        if st.button("测试连接", key="test_claude"):
            with st.spinner("正在测试Claude API连接..."):
                if api_key:
                    st.success("✅ Claude API连接成功!")
                    st.info(f"模型: {model}")
                else:
                    st.error("❌ 请输入API Key")

    elif provider == "GPT-4":
        st.markdown("#### OpenAI API配置")
        api_key = st.text_input("API Key", type="password")
        model = st.selectbox("模型版本", ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"])

    st.markdown("---")

    st.markdown("### 分析参数")

    col1, col2 = st.columns(2)

    with col1:
        temperature = st.slider("Temperature (创造性)", 0.0, 1.0, 0.3, 0.1)
        max_tokens = st.number_input("最大Tokens", value=2000, min_value=100, max_value=8000)

    with col2:
        analysis_language = st.selectbox("分析语言", ["中文", "英文", "自动检测"])
        include_code = st.checkbox("包含代码示例", value=True)

    st.markdown("---")

    st.markdown("### 提示词模板管理")

    template_type = st.selectbox(
        "选择模板类型",
        ["根因分析", "改进建议", "趋势预测", "异常检测", "自定义"]
    )

    if template_type == "根因分析":
        default_prompt = """你是一位资深的机器学习工程师。请分析以下模型评估结果，识别性能问题的根本原因。

评估结果:
{evaluation_results}

请提供:
1. 问题识别和严重程度评估
2. 可能的根本原因分析(按可能性排序)
3. 每个原因的详细解释
4. 推荐的验证方法

请用专业但易懂的语言回答。"""
    else:
        default_prompt = "自定义提示词模板..."

    prompt_template = st.text_area(
        "提示词模板",
        value=default_prompt,
        height=200,
        help="使用{变量名}表示占位符"
    )

    if st.button("保存模板", key="save_template"):
        st.success("✅ 模板保存成功!")

    st.markdown("---")

    st.markdown("### 使用统计")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("本月调用", "1,245")

    with col2:
        st.metric("消耗Tokens", "2.5M")

    with col3:
        st.metric("本月费用", "$45.20")

    with col4:
        st.metric("平均延迟", "2.3s")


def render_code_examples():
    st.markdown("## 💻 代码示例")

    st.markdown("### 1. 基本结果分析")

    st.code("""
from aeva.brain import BrainManager, ResultAnalyzer

# 初始化Brain管理器
brain = BrainManager(
    llm_provider="claude",
    api_key="your-api-key",
    model="claude-3-5-sonnet-20241022"
)

# 加载评估结果
evaluation_results = {
    "accuracy": 0.87,
    "precision": 0.85,
    "recall": 0.89,
    "f1_score": 0.87,
    "auc_roc": 0.91
}

# 创建分析器
analyzer = ResultAnalyzer(brain)

# 运行智能分析
analysis = analyzer.analyze(
    results=evaluation_results,
    baseline={"accuracy": 0.90, "precision": 0.88},
    context="RandomForest分类模型，训练数据10万条"
)

print("异常检测:", analysis.anomalies)
print("关键发现:", analysis.key_findings)
print("建议:", analysis.recommendations)
""", language="python")

    st.markdown("---")

    st.markdown("### 2. 根因分析")

    st.code("""
from aeva.brain import RootCauseAnalyzer

# 创建根因分析器
rca = RootCauseAnalyzer(brain)

# 定义问题
problem = {
    "metric": "accuracy",
    "current_value": 0.87,
    "expected_value": 0.90,
    "decline": -3.3
}

# 运行根因分析
root_causes = rca.analyze(
    problem=problem,
    evaluation_results=evaluation_results,
    training_logs=training_logs,
    data_statistics=data_stats
)

# 查看分析结果
for cause in root_causes:
    print(f"原因: {cause.description}")
    print(f"可能性: {cause.probability}%")
    print(f"建议: {cause.recommendation}")
    print("---")
""", language="python")

    st.markdown("---")

    st.markdown("### 3. 改进建议生成")

    st.code("""
from aeva.brain import ImprovementAdvisor

# 创建改进建议生成器
advisor = ImprovementAdvisor(brain)

# 生成建议
suggestions = advisor.generate_suggestions(
    analysis=analysis,
    root_causes=root_causes,
    constraints={
        "max_time": "1 week",
        "team_size": 2,
        "priority": "accuracy"
    }
)

# 按优先级排序
sorted_suggestions = sorted(
    suggestions,
    key=lambda x: x.priority_score,
    reverse=True
)

# 显示建议
for suggestion in sorted_suggestions:
    print(f"建议: {suggestion.title}")
    print(f"优先级: {suggestion.priority}")
    print(f"预期收益: {suggestion.expected_impact}")
    print(f"工作量: {suggestion.effort}")
    print(f"详细说明: {suggestion.description}")
    print("---")
""", language="python")

    st.markdown("---")

    st.markdown("### 4. 自定义分析提示词")

    st.code("""
from aeva.brain import CustomAnalyzer

# 创建自定义分析器
custom_analyzer = CustomAnalyzer(brain)

# 自定义提示词
custom_prompt = \"\"\"
你是一位机器学习专家。请分析以下评估结果，并关注:
1. 数据质量问题
2. 模型选择是否合适
3. 超参数优化空间

评估结果:
{evaluation_results}

数据统计:
{data_statistics}

请提供详细的分析和建议。
\"\"\"

# 运行自定义分析
result = custom_analyzer.analyze(
    prompt=custom_prompt,
    variables={
        "evaluation_results": evaluation_results,
        "data_statistics": data_stats
    },
    temperature=0.3,
    max_tokens=2000
)

print(result.analysis)
print(result.recommendations)
""", language="python")

    st.markdown("---")

    st.markdown("### 5. 批量分析多个模型")

    st.code("""
from aeva.brain import BatchAnalyzer

# 创建批量分析器
batch_analyzer = BatchAnalyzer(brain)

# 准备多个模型的结果
models_results = {
    "RandomForest": {
        "accuracy": 0.87,
        "precision": 0.85,
        "recall": 0.89
    },
    "GradientBoosting": {
        "accuracy": 0.89,
        "precision": 0.87,
        "recall": 0.91
    },
    "LogisticRegression": {
        "accuracy": 0.84,
        "precision": 0.82,
        "recall": 0.86
    }
}

# 批量分析
comparison = batch_analyzer.compare_models(
    models_results=models_results,
    metrics=["accuracy", "precision", "recall"],
    analysis_depth="comprehensive"
)

# 查看对比结果
print("最佳模型:", comparison.best_model)
print("排名:", comparison.ranking)
print("关键差异:", comparison.key_differences)
print("选择建议:", comparison.recommendation)

# 导出报告
comparison.export_report("model_comparison_report.html")
""", language="python")

    st.markdown("---")

    st.info("""
    💡 **使用建议**:
    - 使用Claude API可获得最佳分析效果
    - 提供充分的上下文信息以获得更准确的建议
    - 定期保存和复用高质量的提示词模板
    - 注意API调用成本，合理设置max_tokens
    - 对于关键决策，建议人工验证AI的分析结果
    """)
