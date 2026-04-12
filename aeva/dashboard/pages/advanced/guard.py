"""
Guard (Quality Gates) page - Advanced feature

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import i18n
from aeva.dashboard.i18n import t, get_current_language


def render():
    """Render guard (quality gates) page"""

    # Back button
    if st.button(t("back_to_home"), key="back_from_guard"):
        st.session_state.subpage = None
        st.rerun()

    st.markdown(f'<p class="main-header">{t("guard_title")}</p>', unsafe_allow_html=True)
    st.markdown(f"### {t('guard_subtitle')}")

    st.markdown("---")

    tabs = st.tabs([
        t("guard_tab_management"),
        t("guard_tab_rules"),
        t("guard_tab_monitoring"),
        t("guard_tab_statistics"),
        t("guard_tab_code")
    ])

    with tabs[0]:
        render_gate_management()

    with tabs[1]:
        render_rule_configuration()

    with tabs[2]:
        render_execution_monitoring()

    with tabs[3]:
        render_statistics_report()

    with tabs[4]:
        render_code_examples()


def render_gate_management():
    st.markdown("## 🎯 质量门禁管理")

    st.markdown("""
    配置和管理质量门禁，确保只有符合标准的模型才能发布。

    **核心功能**:
    - 🎯 阈值门禁 - 设置性能指标阈值
    - 📊 多指标门禁 - 组合多个评估指标
    - ⚡ 性能门禁 - 限制延迟和资源消耗
    - 🔧 自定义门禁 - 自定义验证逻辑
    """)

    st.markdown("---")

    st.markdown("### 已注册的质量门禁")

    # Demo gates
    gates_data = [
        {
            "名称": "accuracy_gate",
            "类型": "阈值门禁",
            "指标": "accuracy",
            "阈值": "≥ 0.85",
            "阻断": "是",
            "状态": "启用"
        },
        {
            "名称": "comprehensive_gate",
            "类型": "多指标门禁",
            "指标": "accuracy, precision, recall",
            "阈值": "≥ 0.80",
            "阻断": "是",
            "状态": "启用"
        },
        {
            "名称": "performance_gate",
            "类型": "性能门禁",
            "指标": "duration, memory",
            "阈值": "< 5s, < 1GB",
            "阻断": "否",
            "状态": "启用"
        },
        {
            "名称": "fairness_gate",
            "类型": "自定义门禁",
            "指标": "demographic_parity",
            "阈值": "自定义",
            "阻断": "是",
            "状态": "暂停"
        }
    ]

    df = pd.DataFrame(gates_data)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    st.markdown("### 创建新的质量门禁")

    gate_type = st.selectbox(
        "选择门禁类型",
        ["阈值门禁 (ThresholdGate)", "多指标门禁 (MultiMetricGate)",
         "性能门禁 (PerformanceGate)", "自定义门禁 (CustomGate)"]
    )

    if gate_type == "阈值门禁 (ThresholdGate)":
        with st.form("create_threshold_gate"):
            gate_name = st.text_input("门禁名称", "my_threshold_gate")
            metric_name = st.selectbox("选择指标", ["accuracy", "precision", "recall", "f1_score", "auc_roc"])
            threshold = st.slider("阈值", 0.0, 1.0, 0.85, 0.01)
            is_blocking = st.checkbox("阻断发布（未通过时）", value=True)

            submitted = st.form_submit_button("创建门禁")

            if submitted:
                st.success(f"✅ 质量门禁 '{gate_name}' 创建成功!")
                st.info(f"指标: {metric_name} ≥ {threshold}, 阻断: {'是' if is_blocking else '否'}")

    elif gate_type == "多指标门禁 (MultiMetricGate)":
        with st.form("create_multi_gate"):
            gate_name = st.text_input("门禁名称", "my_multi_gate")

            st.markdown("**配置指标阈值**:")
            col1, col2 = st.columns(2)

            with col1:
                acc_enabled = st.checkbox("Accuracy", value=True)
                acc_threshold = st.slider("Accuracy阈值", 0.0, 1.0, 0.85, 0.01, disabled=not acc_enabled)

                prec_enabled = st.checkbox("Precision", value=True)
                prec_threshold = st.slider("Precision阈值", 0.0, 1.0, 0.80, 0.01, disabled=not prec_enabled)

            with col2:
                rec_enabled = st.checkbox("Recall", value=True)
                rec_threshold = st.slider("Recall阈值", 0.0, 1.0, 0.80, 0.01, disabled=not rec_enabled)

                f1_enabled = st.checkbox("F1 Score", value=False)
                f1_threshold = st.slider("F1阈值", 0.0, 1.0, 0.80, 0.01, disabled=not f1_enabled)

            is_blocking = st.checkbox("阻断发布（未通过时）", value=True)

            submitted = st.form_submit_button("创建门禁")

            if submitted:
                metrics = []
                if acc_enabled:
                    metrics.append(f"accuracy≥{acc_threshold}")
                if prec_enabled:
                    metrics.append(f"precision≥{prec_threshold}")
                if rec_enabled:
                    metrics.append(f"recall≥{rec_threshold}")
                if f1_enabled:
                    metrics.append(f"f1_score≥{f1_threshold}")

                st.success(f"✅ 质量门禁 '{gate_name}' 创建成功!")
                st.info(f"指标: {', '.join(metrics)}, 阻断: {'是' if is_blocking else '否'}")

    elif gate_type == "性能门禁 (PerformanceGate)":
        with st.form("create_performance_gate"):
            gate_name = st.text_input("门禁名称", "my_performance_gate")

            col1, col2 = st.columns(2)

            with col1:
                enable_duration = st.checkbox("限制执行时间", value=True)
                max_duration = st.number_input("最大执行时间(秒)", value=5.0, min_value=0.1, disabled=not enable_duration)

            with col2:
                enable_memory = st.checkbox("限制内存使用", value=True)
                max_memory = st.number_input("最大内存(MB)", value=1024, min_value=1, disabled=not enable_memory)

            is_blocking = st.checkbox("阻断发布（未通过时）", value=False)

            submitted = st.form_submit_button("创建门禁")

            if submitted:
                limits = []
                if enable_duration:
                    limits.append(f"时间<{max_duration}s")
                if enable_memory:
                    limits.append(f"内存<{max_memory}MB")

                st.success(f"✅ 质量门禁 '{gate_name}' 创建成功!")
                st.info(f"限制: {', '.join(limits)}, 阻断: {'是' if is_blocking else '否'}")


def render_rule_configuration():
    st.markdown("## 📊 门禁规则配置")

    st.markdown("""
    配置质量门禁的触发规则和验证策略。
    """)

    if st.button("⚙️ 查看规则配置", key="view_rules"):
        with st.spinner("正在加载规则配置..."):
            st.success("✅ 规则配置加载完成!")

            # Rules overview
            st.markdown("### 触发规则")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 自动触发场景")
                st.markdown("""
                - ✅ 模型训练完成后
                - ✅ 模型评估完成后
                - ✅ 准备发布前
                - ⚠️ 定期检查（每日）
                - ❌ 手动触发
                """)

            with col2:
                st.markdown("#### 验证策略")
                st.markdown("""
                - **严格模式**: 所有门禁必须通过
                - **宽松模式**: 只要非阻断门禁失败
                - **投票模式**: 多数门禁通过即可
                - **加权模式**: 根据权重计算总分
                """)

            st.markdown("---")

            # Gate priority
            st.markdown("### 门禁优先级")

            priority_data = {
                "优先级": ["1 (最高)", "2", "3", "4 (最低)"],
                "门禁名称": ["accuracy_gate", "comprehensive_gate", "fairness_gate", "performance_gate"],
                "权重": [40, 30, 20, 10],
                "执行顺序": ["第一", "第二", "第三", "第四"]
            }

            df_priority = pd.DataFrame(priority_data)
            st.dataframe(df_priority, use_container_width=True)

            st.markdown("---")

            # Failure handling
            st.markdown("### 失败处理策略")

            failure_strategy = st.selectbox(
                "选择失败处理策略",
                ["立即阻断", "记录警告并继续", "发送通知", "自动重试", "人工审核"]
            )

            if failure_strategy == "自动重试":
                max_retries = st.number_input("最大重试次数", value=3, min_value=1, max_value=10)
                retry_delay = st.number_input("重试间隔(秒)", value=60, min_value=1)

            if failure_strategy:
                st.info(f"当前策略: {failure_strategy}")

            st.markdown("---")

            # Notifications
            st.markdown("### 通知配置")

            col1, col2 = st.columns(2)

            with col1:
                notify_on_pass = st.checkbox("通过时通知", value=False)
                notify_on_fail = st.checkbox("失败时通知", value=True)

            with col2:
                notification_channels = st.multiselect(
                    "通知渠道",
                    ["Email", "Slack", "钉钉", "企业微信", "Webhook"],
                    default=["Email"]
                )


def render_execution_monitoring():
    st.markdown("## 🚦 门禁执行监控")

    st.markdown("""
    实时监控质量门禁的执行状态和历史记录。
    """)

    if st.button("📊 查看执行状态", key="view_execution"):
        with st.spinner("正在加载执行状态..."):
            st.success("✅ 执行状态加载完成!")

            # Current execution
            st.markdown("### 🔄 当前执行")

            current_data = {
                "模型": ["classifier_v2.4.pkl"],
                "门禁": ["comprehensive_gate"],
                "状态": ["执行中"],
                "进度": ["75%"],
                "已用时": ["2.3s"]
            }

            df_current = pd.DataFrame(current_data)
            st.dataframe(df_current, use_container_width=True)

            st.progress(0.75, text="正在验证 Recall 指标...")

            st.markdown("---")

            # Recent executions
            st.markdown("### 📜 最近执行记录")

            history_data = {
                "模型": [
                    "classifier_v2.3.pkl",
                    "llm_model_gpt4.pkl",
                    "bert_sentiment.pkl",
                    "detector_v1.0.pkl",
                    "recommender_v3.pkl"
                ],
                "执行时间": [
                    "2分钟前",
                    "15分钟前",
                    "1小时前",
                    "3小时前",
                    "5小时前"
                ],
                "门禁总数": [4, 4, 4, 4, 4],
                "通过": [4, 3, 2, 1, 4],
                "失败": [0, 1, 2, 3, 0],
                "结果": ["✅ 全部通过", "⚠️ 部分失败", "⚠️ 部分失败", "❌ 阻断发布", "✅ 全部通过"]
            }

            df_history = pd.DataFrame(history_data)
            st.dataframe(df_history, use_container_width=True)

            st.markdown("---")

            # Detailed view
            st.markdown("### 🔍 详细执行信息")

            with st.expander("classifier_v2.3.pkl - 详细信息", expanded=True):
                st.markdown("**执行时间**: 2分钟前 | **总耗时**: 3.2秒")

                gate_results = {
                    "门禁": ["accuracy_gate", "comprehensive_gate", "performance_gate", "fairness_gate"],
                    "类型": ["阈值门禁", "多指标门禁", "性能门禁", "自定义门禁"],
                    "结果": ["✅ 通过", "✅ 通过", "✅ 通过", "✅ 通过"],
                    "评分": ["0.92 ≥ 0.85", "0.88 ≥ 0.80", "2.1s < 5s", "0.95 ≥ 0.90"],
                    "耗时": ["0.8s", "1.2s", "0.5s", "0.7s"]
                }

                df_gates = pd.DataFrame(gate_results)
                st.dataframe(df_gates, use_container_width=True)

            with st.expander("llm_model_gpt4.pkl - 详细信息"):
                st.markdown("**执行时间**: 15分钟前 | **总耗时**: 4.5秒")

                gate_results_2 = {
                    "门禁": ["accuracy_gate", "comprehensive_gate", "performance_gate", "fairness_gate"],
                    "类型": ["阈值门禁", "多指标门禁", "性能门禁", "自定义门禁"],
                    "结果": ["✅ 通过", "✅ 通过", "⚠️ 警告", "✅ 通过"],
                    "评分": ["0.89 ≥ 0.85", "0.85 ≥ 0.80", "3.8s < 5s", "0.92 ≥ 0.90"],
                    "耗时": ["1.0s", "1.5s", "0.5s", "1.5s"]
                }

                df_gates_2 = pd.DataFrame(gate_results_2)
                st.dataframe(df_gates_2, use_container_width=True)


def render_statistics_report():
    st.markdown("## 📈 统计报告")

    st.markdown("""
    查看质量门禁的统计数据和趋势分析。
    """)

    if st.button("📊 生成统计报告", key="gen_report"):
        with st.spinner("正在生成统计报告..."):
            st.success("✅ 统计报告生成完成!")

            # Overview metrics
            st.markdown("### 📊 总体统计 (近7天)")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("总执行次数", "156", "12")

            with col2:
                st.metric("通过率", "87.2%", "2.3%")

            with col3:
                st.metric("阻断次数", "8", "-3")

            with col4:
                st.metric("平均耗时", "3.1s", "-0.4s")

            st.markdown("---")

            # Gate performance
            st.markdown("### 🎯 门禁性能统计")

            gate_stats = {
                "门禁名称": ["accuracy_gate", "comprehensive_gate", "performance_gate", "fairness_gate"],
                "执行次数": [156, 156, 156, 98],
                "通过次数": [142, 136, 148, 85],
                "通过率": ["91.0%", "87.2%", "94.9%", "86.7%"],
                "平均耗时": ["0.8s", "1.3s", "0.5s", "0.9s"],
                "阻断次数": [8, 12, 0, 5]
            }

            df_gate_stats = pd.DataFrame(gate_stats)
            st.dataframe(
                df_gate_stats.style.background_gradient(subset=["通过率"], cmap="RdYlGn"),
                use_container_width=True
            )

            st.markdown("---")

            # Trend analysis
            st.markdown("### 📈 通过率趋势")

            trend_data = pd.DataFrame({
                "日期": ["04-07", "04-08", "04-09", "04-10", "04-11", "04-12", "04-13"],
                "通过率": [82, 84, 85, 88, 86, 89, 87]
            })

            st.line_chart(trend_data.set_index("日期"))

            st.markdown("---")

            # Common failures
            st.markdown("### ⚠️ 常见失败原因")

            failure_data = {
                "原因": [
                    "Accuracy低于阈值",
                    "Precision不达标",
                    "多指标综合评分不足",
                    "公平性检查失败",
                    "性能超时"
                ],
                "发生次数": [12, 8, 10, 5, 3],
                "占比": ["31.6%", "21.1%", "26.3%", "13.2%", "7.9%"]
            }

            df_failures = pd.DataFrame(failure_data)
            st.dataframe(df_failures, use_container_width=True)

            st.markdown("---")

            # Recommendations
            st.markdown("### 💡 优化建议")

            st.info("""
            **基于统计数据的建议**:
            1. **Accuracy门禁** - 失败率9%，建议检查训练数据质量和模型调优
            2. **Comprehensive门禁** - 失败率12.8%，建议调整部分指标阈值（当前可能过严）
            3. **Performance门禁** - 通过率最高(94.9%)，配置合理
            4. **Fairness门禁** - 执行次数较少，建议增加覆盖范围

            **总体建议**:
            - 整体通过率87.2%处于良好水平
            - 可考虑对通过率>95%的门禁适当提高阈值
            - 建议定期审查门禁配置，确保与业务目标一致
            """)


def render_code_examples():
    st.markdown("## 💻 代码示例")

    st.markdown("### 1. 创建阈值门禁")

    st.code("""
from aeva.guard import GuardManager, ThresholdGate

# 创建管理器
guard_manager = GuardManager()

# 创建阈值门禁
accuracy_gate = ThresholdGate(
    name="accuracy_gate",
    threshold=0.85,
    metric_name="accuracy",
    is_blocking=True  # 未通过时阻断发布
)

# 注册门禁
guard_manager.register_gate(accuracy_gate)

# 执行门禁检查
result = guard_manager.check_gates(evaluation_result)

print(f"通过: {result.passed}")
print(f"阻断: {result.blocked}")
if not result.passed:
    print(f"失败原因: {result.reason}")
""", language="python")

    st.markdown("---")

    st.markdown("### 2. 创建多指标门禁")

    st.code("""
from aeva.guard import MultiMetricGate

# 创建多指标门禁
comprehensive_gate = MultiMetricGate(
    name="comprehensive_gate",
    metric_thresholds={
        "accuracy": 0.85,
        "precision": 0.80,
        "recall": 0.80,
        "f1_score": 0.82
    },
    is_blocking=True
)

# 注册并执行
guard_manager.register_gate(comprehensive_gate)
result = guard_manager.check_gates(evaluation_result)

# 查看详细结果
for gate_name, gate_result in result.gate_results.items():
    print(f"{gate_name}: {gate_result.passed}")
    if not gate_result.passed:
        print(f"  原因: {gate_result.reason}")
        print(f"  评分: {gate_result.score:.4f}")
        print(f"  阈值: {gate_result.threshold:.4f}")
""", language="python")

    st.markdown("---")

    st.markdown("### 3. 创建性能门禁")

    st.code("""
from aeva.guard import PerformanceGate

# 创建性能门禁
performance_gate = PerformanceGate(
    name="performance_gate",
    max_duration=5.0,     # 最大执行时间5秒
    max_memory=1024,      # 最大内存1GB
    is_blocking=False     # 仅警告，不阻断
)

guard_manager.register_gate(performance_gate)

# 执行评估（会自动记录性能指标）
evaluation_result = evaluator.evaluate(model, test_data)

# 检查性能门禁
result = guard_manager.check_gates(evaluation_result)

if not result.passed:
    print("⚠️ 性能警告:")
    print(result.reason)
""", language="python")

    st.markdown("---")

    st.markdown("### 4. 创建自定义门禁")

    st.code("""
from aeva.guard import CustomGate
from aeva.core.result import GateResult

# 定义自定义验证函数
def check_fairness(result):
    \"\"\"检查模型公平性\"\"\"
    # 从metadata中获取公平性指标
    demographic_parity = result.metadata.get("demographic_parity", 0)

    # 自定义验证逻辑
    passed = demographic_parity >= 0.90

    return GateResult(
        passed=passed,
        threshold=0.90,
        score=demographic_parity,
        blocked=False,  # 在CustomGate初始化时设置
        reason=None if passed else f"人口统计平等性 ({demographic_parity:.4f}) 低于阈值 (0.90)"
    )

# 创建自定义门禁
fairness_gate = CustomGate(
    name="fairness_gate",
    evaluate_fn=check_fairness,
    is_blocking=True
)

guard_manager.register_gate(fairness_gate)
result = guard_manager.check_gates(evaluation_result)
""", language="python")

    st.markdown("---")

    st.markdown("### 5. 完整示例：模型发布流程")

    st.code("""
from aeva.guard import GuardManager, ThresholdGate, MultiMetricGate, PerformanceGate
from aeva.core import ModelEvaluator

# 1. 初始化
guard_manager = GuardManager()
evaluator = ModelEvaluator()

# 2. 配置质量门禁
gates = [
    ThresholdGate("accuracy_gate", 0.85, "accuracy", is_blocking=True),
    MultiMetricGate(
        "comprehensive_gate",
        {"precision": 0.80, "recall": 0.80, "f1_score": 0.82},
        is_blocking=True
    ),
    PerformanceGate("performance_gate", max_duration=5.0, is_blocking=False)
]

for gate in gates:
    guard_manager.register_gate(gate)

# 3. 评估模型
evaluation_result = evaluator.evaluate(model, test_data)

# 4. 执行质量门禁检查
gate_check_result = guard_manager.check_gates(evaluation_result)

# 5. 决定是否发布
if gate_check_result.passed:
    print("✅ 所有质量门禁通过，允许发布")
    deploy_model(model)
elif gate_check_result.blocked:
    print("❌ 质量门禁阻断发布")
    print(f"阻断原因: {gate_check_result.reason}")
    notify_team(gate_check_result)
else:
    print("⚠️ 部分门禁失败，但未阻断")
    print(f"警告: {gate_check_result.reason}")
    # 可以选择继续发布或人工审核
    if manual_review_approved():
        deploy_model(model)

# 6. 记录结果
log_gate_results(gate_check_result)
""", language="python")

    st.markdown("---")

    st.info("""
    💡 **使用建议**:
    - 为关键质量指标设置阻断门禁，确保底线
    - 为次要指标设置非阻断门禁，作为参考
    - 定期审查门禁配置，根据实际情况调整阈值
    - 记录所有门禁执行结果，用于趋势分析
    - 为门禁失败设置合理的通知和处理流程
    - 在CI/CD流程中集成质量门禁，实现自动化
    """)
