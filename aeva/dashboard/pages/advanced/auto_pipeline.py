"""
Auto Pipeline page - Advanced feature

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def render():
    """Render auto pipeline page"""

    # Back button
    if st.button("← 返回主页", key="back_from_auto"):
        st.session_state.subpage = None
        st.rerun()

    st.markdown('<p class="main-header">🤖 自动化评估流水线</p>', unsafe_allow_html=True)
    st.markdown("### 工作流编排与任务调度")

    st.markdown("---")

    tabs = st.tabs(["🔄 流水线管理", "⚙️ 任务调度", "🚀 执行监控", "📊 分布式执行", "💻 代码示例"])

    with tabs[0]:
        render_pipeline_management()

    with tabs[1]:
        render_task_scheduling()

    with tabs[2]:
        render_execution_monitoring()

    with tabs[3]:
        render_distributed_execution()

    with tabs[4]:
        render_code_examples()


def render_pipeline_management():
    st.markdown("## 🔄 流水线管理")

    st.markdown("""
    创建和管理自动化评估流水线，支持复杂的工作流编排。

    **核心功能**:
    - 📋 可视化流水线配置
    - 🔗 任务依赖管理
    - 🔄 失败重试策略
    - 📊 流水线模板复用
    """)

    st.markdown("---")

    st.markdown("### 已注册的流水线")

    # Demo pipelines
    pipelines_data = [
        {
            "名称": "ml_eval_pipeline",
            "描述": "机器学习模型全流程评估",
            "任务数": 8,
            "状态": "活跃",
            "上次运行": "2小时前"
        },
        {
            "名称": "data_quality_check",
            "描述": "数据质量检查流水线",
            "任务数": 5,
            "状态": "活跃",
            "上次运行": "30分钟前"
        },
        {
            "名称": "model_benchmark",
            "描述": "模型基准测试流水线",
            "任务数": 6,
            "状态": "暂停",
            "上次运行": "1天前"
        }
    ]

    df = pd.DataFrame(pipelines_data)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    st.markdown("### 创建新的流水线")

    with st.form("create_pipeline"):
        pipeline_name = st.text_input("流水线名称", "my_eval_pipeline")
        pipeline_desc = st.text_area("描述", "自定义评估流水线")

        st.markdown("**选择评估任务**:")
        col1, col2 = st.columns(2)

        with col1:
            task_data_quality = st.checkbox("数据质量检查", value=True)
            task_train = st.checkbox("模型训练", value=True)
            task_eval = st.checkbox("模型评估", value=True)
            task_explainability = st.checkbox("可解释性分析", value=False)

        with col2:
            task_robustness = st.checkbox("鲁棒性测试", value=False)
            task_benchmark = st.checkbox("基准测试", value=False)
            task_report = st.checkbox("生成报告", value=True)
            task_notification = st.checkbox("发送通知", value=False)

        retry_policy = st.selectbox(
            "失败重试策略",
            ["不重试", "重试1次", "重试3次", "指数退避重试"]
        )

        submitted = st.form_submit_button("创建流水线")

        if submitted:
            selected_tasks = []
            if task_data_quality:
                selected_tasks.append("data_quality")
            if task_train:
                selected_tasks.append("train")
            if task_eval:
                selected_tasks.append("evaluate")
            if task_explainability:
                selected_tasks.append("explainability")
            if task_robustness:
                selected_tasks.append("robustness")
            if task_benchmark:
                selected_tasks.append("benchmark")
            if task_report:
                selected_tasks.append("report")
            if task_notification:
                selected_tasks.append("notification")

            st.success(f"✅ 流水线 '{pipeline_name}' 创建成功!")
            st.info(f"包含 {len(selected_tasks)} 个任务: {', '.join(selected_tasks)}")
            st.info(f"重试策略: {retry_policy}")


def render_task_scheduling():
    st.markdown("## ⚙️ 任务调度")

    st.markdown("""
    配置任务调度策略，支持定时触发和条件触发。
    """)

    if st.button("📅 配置调度演示", key="config_schedule"):
        with st.spinner("正在配置任务调度..."):
            try:
                from aeva.auto import AutomationManager, TaskScheduler

                st.success("✅ 调度配置完成!")

                # Demo scheduler info
                st.markdown("### 调度器配置")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("活跃调度", "5")

                with col2:
                    st.metric("待执行任务", "12")

                with col3:
                    st.metric("下次执行", "15分钟后")

                # Schedule table
                st.markdown("### 调度列表")

                schedule_data = {
                    "流水线": ["ml_eval_pipeline", "data_quality_check", "model_benchmark", "nightly_test", "weekly_report"],
                    "调度类型": ["Cron", "Cron", "事件触发", "Cron", "Cron"],
                    "调度规则": ["0 */2 * * *", "*/30 * * * *", "on_data_update", "0 2 * * *", "0 0 * * 0"],
                    "下次执行": ["14:00", "13:30", "数据更新时", "明天 02:00", "周日 00:00"],
                    "状态": ["启用", "启用", "启用", "启用", "暂停"]
                }

                df = pd.DataFrame(schedule_data)
                st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    st.markdown("---")

    st.markdown("### 新增调度规则")

    col1, col2 = st.columns(2)

    with col1:
        schedule_type = st.selectbox(
            "调度类型",
            ["Cron表达式", "固定间隔", "事件触发", "手动触发"]
        )

        if schedule_type == "Cron表达式":
            cron_expr = st.text_input("Cron表达式", "0 */6 * * *")
            st.caption("示例: 0 */6 * * * (每6小时运行一次)")
        elif schedule_type == "固定间隔":
            interval = st.number_input("间隔时间(分钟)", value=60, min_value=1)

    with col2:
        priority = st.selectbox("优先级", ["高", "中", "低"])
        max_concurrent = st.number_input("最大并发数", value=1, min_value=1, max_value=10)


def render_execution_monitoring():
    st.markdown("## 🚀 执行监控")

    st.markdown("""
    实时监控流水线执行状态，查看执行历史和性能统计。
    """)

    if st.button("📊 查看执行状态", key="view_execution"):
        with st.spinner("正在加载执行状态..."):
            st.success("✅ 执行状态加载完成!")

            # Current running tasks
            st.markdown("### 🔄 运行中的任务")

            running_data = {
                "流水线": ["ml_eval_pipeline", "data_quality_check"],
                "当前任务": ["模型训练", "数据清洗"],
                "进度": [65, 90],
                "开始时间": ["12:30", "13:10"],
                "预计完成": ["14:15", "13:25"]
            }

            df_running = pd.DataFrame(running_data)
            st.dataframe(df_running, use_container_width=True)

            # Progress bars
            for idx, row in df_running.iterrows():
                st.write(f"**{row['流水线']}** - {row['当前任务']}")
                st.progress(row['进度'] / 100)

            st.markdown("---")

            # Execution history
            st.markdown("### 📜 执行历史")

            history_data = {
                "流水线": ["model_benchmark", "ml_eval_pipeline", "nightly_test", "data_quality_check", "weekly_report"],
                "状态": ["✅ 成功", "✅ 成功", "❌ 失败", "✅ 成功", "✅ 成功"],
                "开始时间": ["11:00", "10:30", "02:00", "09:00", "00:00"],
                "结束时间": ["11:45", "12:15", "02:10", "09:25", "00:50"],
                "耗时": ["45分钟", "1小时45分钟", "10分钟", "25分钟", "50分钟"]
            }

            df_history = pd.DataFrame(history_data)
            st.dataframe(df_history, use_container_width=True)

            st.markdown("---")

            # Performance stats
            st.markdown("### 📈 性能统计 (近7天)")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("总执行次数", "124")

            with col2:
                st.metric("成功率", "95.2%", "2.1%")

            with col3:
                st.metric("平均耗时", "38分钟", "-5分钟")

            with col4:
                st.metric("失败次数", "6", "-2")

            # Execution trend chart
            st.markdown("### 执行趋势")

            dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
            trend_data = pd.DataFrame({
                "日期": dates.strftime('%m-%d'),
                "成功": [18, 15, 20, 17, 19, 16, 19],
                "失败": [2, 1, 0, 2, 1, 0, 0]
            })

            st.bar_chart(trend_data.set_index("日期"))


def render_distributed_execution():
    st.markdown("## 📊 分布式执行")

    st.markdown("""
    支持多节点分布式执行，提高大规模评估任务的效率。
    """)

    if st.button("🌐 查看集群状态", key="view_cluster"):
        with st.spinner("正在加载集群状态..."):
            st.success("✅ 集群状态加载完成!")

            # Cluster overview
            st.markdown("### 集群概览")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("节点总数", "8", "2")

            with col2:
                st.metric("在线节点", "7")

            with col3:
                st.metric("CPU使用率", "62%")

            with col4:
                st.metric("内存使用率", "48%")

            st.markdown("---")

            # Node details
            st.markdown("### 节点状态")

            nodes_data = {
                "节点": ["node-1", "node-2", "node-3", "node-4", "node-5", "node-6", "node-7", "node-8"],
                "状态": ["在线", "在线", "在线", "在线", "在线", "在线", "在线", "离线"],
                "CPU": ["45%", "78%", "32%", "90%", "55%", "23%", "67%", "-"],
                "内存": ["60%", "85%", "40%", "75%", "50%", "35%", "70%", "-"],
                "运行任务": [2, 3, 1, 4, 2, 0, 3, 0],
                "队列任务": [1, 2, 0, 1, 1, 0, 2, 0]
            }

            df_nodes = pd.DataFrame(nodes_data)
            st.dataframe(df_nodes, use_container_width=True)

            st.markdown("---")

            # Load balancing
            st.markdown("### 负载均衡策略")

            strategy = st.selectbox(
                "选择策略",
                ["轮询 (Round Robin)", "最少连接 (Least Connections)", "CPU优先", "内存优先", "自定义"]
            )

            if strategy:
                st.info(f"当前策略: {strategy}")

            st.markdown("---")

            # Task distribution
            st.markdown("### 任务分布")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**按节点分布**")
                node_tasks = {
                    "node-1": 2,
                    "node-2": 3,
                    "node-3": 1,
                    "node-4": 4,
                    "node-5": 2,
                    "node-6": 0,
                    "node-7": 3
                }
                st.bar_chart(node_tasks)

            with col2:
                st.markdown("**资源利用率**")
                resource_data = pd.DataFrame({
                    "资源": ["CPU", "内存", "磁盘", "网络"],
                    "利用率": [62, 48, 35, 28]
                })
                st.bar_chart(resource_data.set_index("资源"))


def render_code_examples():
    st.markdown("## 💻 代码示例")

    st.markdown("### 1. 创建自动化流水线")

    st.code("""
from aeva.auto import AutomationManager, PipelineExecutor

# 初始化管理器
manager = AutomationManager()

# 创建流水线
pipeline = PipelineExecutor(name="ml_eval_pipeline")

# 添加任务
pipeline.add_task(
    name="data_quality",
    function=check_data_quality,
    retry_on_failure=True,
    max_retries=3
)

pipeline.add_task(
    name="train_model",
    function=train_model,
    depends_on=["data_quality"]  # 依赖数据质量检查
)

pipeline.add_task(
    name="evaluate",
    function=evaluate_model,
    depends_on=["train_model"]
)

pipeline.add_task(
    name="generate_report",
    function=generate_report,
    depends_on=["evaluate"]
)

# 注册流水线
manager.register_pipeline(pipeline)
print(f"Pipeline '{pipeline.name}' registered with {len(pipeline.tasks)} tasks")
""", language="python")

    st.markdown("---")

    st.markdown("### 2. 配置任务调度")

    st.code("""
from aeva.auto import TaskScheduler

# 创建调度器
scheduler = TaskScheduler()

# Cron调度 - 每6小时运行一次
scheduler.add_cron_schedule(
    pipeline_name="ml_eval_pipeline",
    cron_expr="0 */6 * * *",
    timezone="Asia/Shanghai"
)

# 固定间隔调度 - 每30分钟运行一次
scheduler.add_interval_schedule(
    pipeline_name="data_quality_check",
    interval_minutes=30
)

# 事件触发调度 - 数据更新时运行
scheduler.add_event_trigger(
    pipeline_name="model_benchmark",
    event_type="data_update",
    condition=lambda event: event.data_size > 1000
)

# 启动调度器
scheduler.start()
print("Scheduler started with", len(scheduler.schedules), "schedules")
""", language="python")

    st.markdown("---")

    st.markdown("### 3. 监控流水线执行")

    st.code("""
from aeva.auto import PipelineMonitor

# 创建监控器
monitor = PipelineMonitor()

# 运行流水线
execution_id = manager.run_pipeline(
    pipeline_name="ml_eval_pipeline",
    inputs={"data_path": "data/train.csv"}
)

# 实时监控
while True:
    status = monitor.get_status(execution_id)

    print(f"Pipeline: {status.pipeline_name}")
    print(f"Status: {status.state}")
    print(f"Current Task: {status.current_task}")
    print(f"Progress: {status.progress}%")

    if status.is_completed:
        break

    time.sleep(5)

# 获取结果
result = monitor.get_result(execution_id)
print(f"Result: {result.success}")
print(f"Duration: {result.duration_seconds}s")
print(f"Output: {result.output}")
""", language="python")

    st.markdown("---")

    st.markdown("### 4. 分布式执行")

    st.code("""
from aeva.auto import DistributedExecutor

# 配置分布式执行器
executor = DistributedExecutor(
    nodes=[
        {"host": "node-1", "port": 8080},
        {"host": "node-2", "port": 8080},
        {"host": "node-3", "port": 8080}
    ],
    load_balancing="least_connections"
)

# 注册到管理器
manager.set_executor(executor)

# 分布式运行
execution_id = manager.run_pipeline(
    pipeline_name="ml_eval_pipeline",
    distributed=True,
    max_parallel_tasks=5
)

# 查看任务分布
distribution = executor.get_task_distribution(execution_id)
for node, tasks in distribution.items():
    print(f"{node}: {len(tasks)} tasks")

# 监控集群状态
cluster_status = executor.get_cluster_status()
print(f"Total nodes: {cluster_status.total_nodes}")
print(f"Online nodes: {cluster_status.online_nodes}")
print(f"CPU usage: {cluster_status.cpu_usage}%")
print(f"Memory usage: {cluster_status.memory_usage}%")
""", language="python")

    st.markdown("---")

    st.markdown("### 5. 失败处理与重试")

    st.code("""
from aeva.auto import RetryPolicy, FailureHandler

# 配置重试策略
retry_policy = RetryPolicy(
    max_retries=3,
    backoff_strategy="exponential",
    initial_delay=1,  # 初始延迟1秒
    max_delay=60      # 最大延迟60秒
)

# 配置失败处理
failure_handler = FailureHandler(
    on_task_failure=lambda task, error: send_alert(task, error),
    on_pipeline_failure=lambda pipeline, error: rollback(pipeline)
)

# 应用到流水线
pipeline.set_retry_policy(retry_policy)
pipeline.set_failure_handler(failure_handler)

# 运行流水线
try:
    result = manager.run_pipeline(
        pipeline_name="ml_eval_pipeline",
        timeout=3600  # 1小时超时
    )

    if result.success:
        print("Pipeline completed successfully")
    else:
        print(f"Pipeline failed: {result.error}")
        print(f"Failed task: {result.failed_task}")

except TimeoutError:
    print("Pipeline execution timeout")
""", language="python")

    st.markdown("---")

    st.info("""
    💡 **使用建议**:
    - 合理设置任务依赖关系，确保执行顺序正确
    - 使用重试策略处理临时性失败
    - 监控流水线执行状态，及时发现和处理问题
    - 在分布式环境中注意任务的数据依赖和状态同步
    - 定期清理历史执行记录，避免存储空间不足
    """)
