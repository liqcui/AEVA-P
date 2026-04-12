"""
Report Generation page - Comprehensive report generation and management

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import i18n
from aeva.dashboard.i18n import t, get_current_language


def render():
    """Render report generation page"""

    lang = get_current_language()

    st.markdown('<p class="main-header">📄 报告生成中心</p>' if lang == "zh" else '<p class="main-header">📄 Report Generation Center</p>', unsafe_allow_html=True)
    st.markdown("### 综合评估报告生成与管理" if lang == "zh" else "### Comprehensive Evaluation Report Generation & Management")

    st.markdown("---")

    if lang == "zh":
        tabs = st.tabs(["📊 生成报告", "📑 报告模板", "📚 历史报告", "⚙️ 配置", "💻 代码示例"])
    else:
        tabs = st.tabs(["📊 Generate Report", "📑 Report Templates", "📚 Report History", "⚙️ Configuration", "💻 Code Examples"])

    with tabs[0]:
        render_generate_report(lang)

    with tabs[1]:
        render_report_templates(lang)

    with tabs[2]:
        render_report_history(lang)

    with tabs[3]:
        render_configuration(lang)

    with tabs[4]:
        render_code_examples(lang)


def render_generate_report(lang):
    """Render report generation tab"""

    st.markdown("## 📊 生成综合评估报告" if lang == "zh" else "## 📊 Generate Comprehensive Evaluation Report")

    if lang == "zh":
        st.markdown("""
        创建包含多个评估维度的综合报告，支持多种导出格式。

        **报告类型**:
        - 📋 **完整评估报告**: 包含所有评估模块的结果
        - 🎯 **自定义报告**: 选择特定模块和指标
        - 📈 **对比报告**: 多模型/多版本对比分析
        - 🔍 **专项报告**: 单一维度深度分析
        """)
    else:
        st.markdown("""
        Create comprehensive reports with multiple evaluation dimensions and support various export formats.

        **Report Types**:
        - 📋 **Full Evaluation Report**: Include all evaluation modules
        - 🎯 **Custom Report**: Select specific modules and metrics
        - 📈 **Comparison Report**: Multi-model/version comparison
        - 🔍 **Specialized Report**: In-depth analysis of single dimension
        """)

    st.markdown("---")

    # Report configuration form
    with st.form("report_generation_form"):
        st.markdown("### 📝 " + ("报告配置" if lang == "zh" else "Report Configuration"))

        col1, col2 = st.columns(2)

        with col1:
            report_type = st.selectbox(
                "报告类型 / Report Type" if lang == "zh" else "Report Type",
                ["完整评估报告" if lang == "zh" else "Full Evaluation Report",
                 "自定义报告" if lang == "zh" else "Custom Report",
                 "对比报告" if lang == "zh" else "Comparison Report",
                 "专项报告" if lang == "zh" else "Specialized Report"]
            )

            report_name = st.text_input(
                "报告名称 / Report Name" if lang == "zh" else "Report Name",
                "Model_Evaluation_Report_" + datetime.now().strftime("%Y%m%d")
            )

            report_format = st.multiselect(
                "导出格式 / Export Format" if lang == "zh" else "Export Format",
                ["PDF", "HTML", "Markdown", "JSON", "Excel"],
                default=["HTML", "PDF"]
            )

        with col2:
            report_template = st.selectbox(
                "报告模板 / Report Template" if lang == "zh" else "Report Template",
                ["标准模板" if lang == "zh" else "Standard Template",
                 "企业模板" if lang == "zh" else "Enterprise Template",
                 "学术模板" if lang == "zh" else "Academic Template",
                 "监管模板" if lang == "zh" else "Regulatory Template",
                 "自定义模板" if lang == "zh" else "Custom Template"]
            )

            include_code = st.checkbox(
                "包含代码示例 / Include Code Examples" if lang == "zh" else "Include Code Examples",
                value=True
            )

            include_visualizations = st.checkbox(
                "包含可视化图表 / Include Visualizations" if lang == "zh" else "Include Visualizations",
                value=True
            )

        st.markdown("---")
        st.markdown("### 🎯 " + ("评估模块选择" if lang == "zh" else "Evaluation Modules Selection"))

        col1, col2, col3 = st.columns(3)

        with col1:
            if lang == "zh":
                module_explainability = st.checkbox("🔍 可解释性分析", value=True)
                module_robustness = st.checkbox("🛡️ 对抗鲁棒性", value=True)
                module_fairness = st.checkbox("⚖️ 公平性评估", value=True)
            else:
                module_explainability = st.checkbox("🔍 Explainability", value=True)
                module_robustness = st.checkbox("🛡️ Robustness", value=True)
                module_fairness = st.checkbox("⚖️ Fairness", value=True)

        with col2:
            if lang == "zh":
                module_data_quality = st.checkbox("📊 数据质量", value=True)
                module_performance = st.checkbox("📈 性能指标", value=True)
                module_benchmark = st.checkbox("🏆 基准测试", value=False)
            else:
                module_data_quality = st.checkbox("📊 Data Quality", value=True)
                module_performance = st.checkbox("📈 Performance", value=True)
                module_benchmark = st.checkbox("🏆 Benchmarking", value=False)

        with col3:
            if lang == "zh":
                module_model_card = st.checkbox("📝 模型卡片", value=True)
                module_quality_gates = st.checkbox("🛡️ 质量门禁", value=False)
                module_ab_testing = st.checkbox("🧪 A/B测试", value=False)
            else:
                module_model_card = st.checkbox("📝 Model Card", value=True)
                module_quality_gates = st.checkbox("🛡️ Quality Gates", value=False)
                module_ab_testing = st.checkbox("🧪 A/B Testing", value=False)

        st.markdown("---")
        st.markdown("### 📤 " + ("导出选项" if lang == "zh" else "Export Options"))

        col1, col2 = st.columns(2)

        with col1:
            auto_open = st.checkbox(
                "生成后自动打开 / Auto-open after generation" if lang == "zh" else "Auto-open after generation",
                value=True
            )

        with col2:
            send_email = st.checkbox(
                "发送到邮箱 / Send via email" if lang == "zh" else "Send via email",
                value=False
            )

        if send_email:
            email_address = st.text_input(
                "邮箱地址 / Email Address" if lang == "zh" else "Email Address",
                "user@example.com"
            )

        submitted = st.form_submit_button("🚀 " + ("生成报告" if lang == "zh" else "Generate Report"))

        if submitted:
            with st.spinner("正在生成报告..." if lang == "zh" else "Generating report..."):
                # Simulate report generation
                import time
                time.sleep(2)

                st.success("✅ " + ("报告生成成功！" if lang == "zh" else "Report generated successfully!"))

                # Count selected modules
                selected_modules = sum([
                    module_explainability, module_robustness, module_fairness,
                    module_data_quality, module_performance, module_benchmark,
                    module_model_card, module_quality_gates, module_ab_testing
                ])

                # Display report summary
                st.markdown("---")
                st.markdown("### 📋 " + ("报告摘要" if lang == "zh" else "Report Summary"))

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("模块数量" if lang == "zh" else "Modules", selected_modules)

                with col2:
                    st.metric("页数" if lang == "zh" else "Pages", selected_modules * 3 + 2)

                with col3:
                    st.metric("图表数" if lang == "zh" else "Charts", selected_modules * 2)

                with col4:
                    st.metric("导出格式" if lang == "zh" else "Formats", len(report_format))

                # Download links
                st.markdown("---")
                st.markdown("### 📥 " + ("下载报告" if lang == "zh" else "Download Report"))

                col1, col2, col3 = st.columns(3)

                with col1:
                    if "PDF" in report_format:
                        st.download_button(
                            "📄 下载 PDF" if lang == "zh" else "📄 Download PDF",
                            data="Sample PDF content",
                            file_name=f"{report_name}.pdf",
                            mime="application/pdf"
                        )

                with col2:
                    if "HTML" in report_format:
                        st.download_button(
                            "🌐 下载 HTML" if lang == "zh" else "🌐 Download HTML",
                            data="<html><body>Sample HTML Report</body></html>",
                            file_name=f"{report_name}.html",
                            mime="text/html"
                        )

                with col3:
                    if "Markdown" in report_format:
                        st.download_button(
                            "📝 下载 Markdown" if lang == "zh" else "📝 Download Markdown",
                            data="# Sample Markdown Report\n\n## Summary\n...",
                            file_name=f"{report_name}.md",
                            mime="text/markdown"
                        )


def render_report_templates(lang):
    """Render report templates tab"""

    st.markdown("## 📑 " + ("报告模板管理" if lang == "zh" else "Report Template Management"))

    if lang == "zh":
        st.markdown("""
        管理和自定义报告模板，支持创建、编辑和删除模板。
        """)
    else:
        st.markdown("""
        Manage and customize report templates, support creating, editing, and deleting templates.
        """)

    st.markdown("---")

    # Available templates
    st.markdown("### 📚 " + ("可用模板" if lang == "zh" else "Available Templates"))

    templates_data = {
        "模板名称" if lang == "zh" else "Template Name": [
            "标准模板" if lang == "zh" else "Standard Template",
            "企业模板" if lang == "zh" else "Enterprise Template",
            "学术模板" if lang == "zh" else "Academic Template",
            "监管模板" if lang == "zh" else "Regulatory Template"
        ],
        "描述" if lang == "zh" else "Description": [
            "通用评估报告模板" if lang == "zh" else "General evaluation report template",
            "企业级详细报告模板" if lang == "zh" else "Enterprise-level detailed report template",
            "学术论文风格模板" if lang == "zh" else "Academic paper style template",
            "符合监管要求的报告模板" if lang == "zh" else "Regulatory compliance report template"
        ],
        "包含模块" if lang == "zh" else "Included Modules": [
            "5个核心模块" if lang == "zh" else "5 core modules",
            "9个完整模块" if lang == "zh" else "9 full modules",
            "科研导向模块" if lang == "zh" else "Research-oriented modules",
            "合规必需模块" if lang == "zh" else "Compliance-required modules"
        ],
        "格式" if lang == "zh" else "Format": [
            "PDF, HTML",
            "PDF, HTML, Excel",
            "PDF, LaTeX",
            "PDF, HTML, JSON"
        ],
        "状态" if lang == "zh" else "Status": [
            "✅ 启用" if lang == "zh" else "✅ Enabled",
            "✅ 启用" if lang == "zh" else "✅ Enabled",
            "✅ 启用" if lang == "zh" else "✅ Enabled",
            "✅ 启用" if lang == "zh" else "✅ Enabled"
        ]
    }

    df_templates = pd.DataFrame(templates_data)
    st.dataframe(df_templates, use_container_width=True)

    st.markdown("---")

    # Template preview
    st.markdown("### 👁️ " + ("模板预览" if lang == "zh" else "Template Preview"))

    selected_template = st.selectbox(
        "选择模板预览" if lang == "zh" else "Select template to preview",
        ["标准模板" if lang == "zh" else "Standard Template",
         "企业模板" if lang == "zh" else "Enterprise Template",
         "学术模板" if lang == "zh" else "Academic Template",
         "监管模板" if lang == "zh" else "Regulatory Template"]
    )

    if lang == "zh":
        st.markdown("""
        ```markdown
        # 模型评估报告

        ## 1. 执行摘要
        - 模型名称: [模型名称]
        - 评估日期: [日期]
        - 总体评分: [评分]

        ## 2. 性能指标
        - Accuracy: [值]
        - Precision: [值]
        - Recall: [值]
        - F1 Score: [值]

        ## 3. 可解释性分析
        - SHAP值分析
        - 特征重要性排名
        - 决策路径可视化

        ## 4. 鲁棒性测试
        - 对抗样本测试结果
        - 扰动敏感度分析
        - 边界案例测试

        ## 5. 数据质量评估
        - 数据完整性检查
        - 数据分布分析
        - 异常值检测

        ## 6. 建议与结论
        - 主要发现
        - 改进建议
        - 部署建议
        ```
        """)
    else:
        st.markdown("""
        ```markdown
        # Model Evaluation Report

        ## 1. Executive Summary
        - Model Name: [Model Name]
        - Evaluation Date: [Date]
        - Overall Score: [Score]

        ## 2. Performance Metrics
        - Accuracy: [Value]
        - Precision: [Value]
        - Recall: [Value]
        - F1 Score: [Value]

        ## 3. Explainability Analysis
        - SHAP Value Analysis
        - Feature Importance Ranking
        - Decision Path Visualization

        ## 4. Robustness Testing
        - Adversarial Testing Results
        - Perturbation Sensitivity Analysis
        - Edge Case Testing

        ## 5. Data Quality Assessment
        - Data Integrity Check
        - Data Distribution Analysis
        - Outlier Detection

        ## 6. Recommendations & Conclusions
        - Key Findings
        - Improvement Suggestions
        - Deployment Recommendations
        ```
        """)

    st.markdown("---")

    # Create custom template
    st.markdown("### ➕ " + ("创建自定义模板" if lang == "zh" else "Create Custom Template"))

    with st.expander("展开创建表单" if lang == "zh" else "Expand to create"):
        template_name = st.text_input(
            "模板名称" if lang == "zh" else "Template Name",
            "My_Custom_Template"
        )
        template_desc = st.text_area(
            "模板描述" if lang == "zh" else "Template Description",
            "自定义报告模板" if lang == "zh" else "Custom report template"
        )

        if st.button("💾 " + ("保存模板" if lang == "zh" else "Save Template")):
            st.success("✅ " + ("模板保存成功！" if lang == "zh" else "Template saved successfully!"))


def render_report_history(lang):
    """Render report history tab"""

    st.markdown("## 📚 " + ("历史报告" if lang == "zh" else "Report History"))

    if lang == "zh":
        st.markdown("""
        查看和管理已生成的历史报告。
        """)
    else:
        st.markdown("""
        View and manage previously generated reports.
        """)

    st.markdown("---")

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("总报告数" if lang == "zh" else "Total Reports", "156")

    with col2:
        st.metric("本月生成" if lang == "zh" else "This Month", "24", "+8")

    with col3:
        st.metric("总大小" if lang == "zh" else "Total Size", "2.3 GB")

    with col4:
        st.metric("平均生成时间" if lang == "zh" else "Avg Time", "45s")

    st.markdown("---")

    # Recent reports
    st.markdown("### 📋 " + ("最近生成的报告" if lang == "zh" else "Recently Generated Reports"))

    history_data = {
        "报告名称" if lang == "zh" else "Report Name": [
            "Model_Evaluation_Report_20260413",
            "Comparison_Report_v2.3_vs_v2.4",
            "Robustness_Analysis_Report",
            "Full_Assessment_Q1_2026",
            "Custom_Report_Enterprise"
        ],
        "类型" if lang == "zh" else "Type": [
            "完整评估" if lang == "zh" else "Full Evaluation",
            "对比报告" if lang == "zh" else "Comparison",
            "专项报告" if lang == "zh" else "Specialized",
            "季度报告" if lang == "zh" else "Quarterly",
            "自定义" if lang == "zh" else "Custom"
        ],
        "生成时间" if lang == "zh" else "Generated": [
            "2小时前" if lang == "zh" else "2 hours ago",
            "1天前" if lang == "zh" else "1 day ago",
            "3天前" if lang == "zh" else "3 days ago",
            "1周前" if lang == "zh" else "1 week ago",
            "2周前" if lang == "zh" else "2 weeks ago"
        ],
        "格式" if lang == "zh" else "Format": [
            "PDF, HTML",
            "PDF, Excel",
            "HTML, Markdown",
            "PDF, HTML, JSON",
            "PDF"
        ],
        "大小" if lang == "zh" else "Size": [
            "15.2 MB",
            "8.7 MB",
            "4.3 MB",
            "28.5 MB",
            "6.1 MB"
        ],
        "状态" if lang == "zh" else "Status": [
            "✅ 可用" if lang == "zh" else "✅ Available",
            "✅ 可用" if lang == "zh" else "✅ Available",
            "✅ 可用" if lang == "zh" else "✅ Available",
            "✅ 可用" if lang == "zh" else "✅ Available",
            "✅ 可用" if lang == "zh" else "✅ Available"
        ]
    }

    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True)

    st.markdown("---")

    # Report actions
    st.markdown("### ⚡ " + ("操作" if lang == "zh" else "Actions"))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📥 " + ("下载选中" if lang == "zh" else "Download Selected")):
            st.info("下载功能演示" if lang == "zh" else "Download feature demo")

    with col2:
        if st.button("🗑️ " + ("删除选中" if lang == "zh" else "Delete Selected")):
            st.warning("删除功能演示" if lang == "zh" else "Delete feature demo")

    with col3:
        if st.button("🔄 " + ("重新生成" if lang == "zh" else "Regenerate")):
            st.info("重新生成功能演示" if lang == "zh" else "Regenerate feature demo")

    with col4:
        if st.button("📤 " + ("导出列表" if lang == "zh" else "Export List")):
            st.info("导出功能演示" if lang == "zh" else "Export feature demo")


def render_configuration(lang):
    """Render configuration tab"""

    st.markdown("## ⚙️ " + ("报告配置" if lang == "zh" else "Report Configuration"))

    if lang == "zh":
        st.markdown("""
        配置报告生成的默认设置和高级选项。
        """)
    else:
        st.markdown("""
        Configure default settings and advanced options for report generation.
        """)

    st.markdown("---")

    # Default settings
    st.markdown("### 🎛️ " + ("默认设置" if lang == "zh" else "Default Settings"))

    col1, col2 = st.columns(2)

    with col1:
        default_format = st.multiselect(
            "默认导出格式" if lang == "zh" else "Default Export Format",
            ["PDF", "HTML", "Markdown", "JSON", "Excel"],
            default=["PDF", "HTML"]
        )

        default_template = st.selectbox(
            "默认模板" if lang == "zh" else "Default Template",
            ["标准模板" if lang == "zh" else "Standard Template",
             "企业模板" if lang == "zh" else "Enterprise Template",
             "学术模板" if lang == "zh" else "Academic Template"]
        )

        auto_archive = st.checkbox(
            "自动归档旧报告" if lang == "zh" else "Auto-archive old reports",
            value=True
        )

    with col2:
        report_language = st.selectbox(
            "报告语言" if lang == "zh" else "Report Language",
            ["中文" if lang == "zh" else "Chinese",
             "English" if lang == "zh" else "English",
             "双语 / Bilingual" if lang == "zh" else "Bilingual"]
        )

        include_raw_data = st.checkbox(
            "包含原始数据" if lang == "zh" else "Include raw data",
            value=False
        )

        compress_output = st.checkbox(
            "压缩输出文件" if lang == "zh" else "Compress output files",
            value=True
        )

    st.markdown("---")

    # Advanced options
    st.markdown("### 🔧 " + ("高级选项" if lang == "zh" else "Advanced Options"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### " + ("性能设置" if lang == "zh" else "Performance Settings"))

        max_parallel = st.slider(
            "最大并行任务" if lang == "zh" else "Max parallel tasks",
            min_value=1,
            max_value=10,
            value=4
        )

        cache_results = st.checkbox(
            "缓存中间结果" if lang == "zh" else "Cache intermediate results",
            value=True
        )

    with col2:
        st.markdown("#### " + ("存储设置" if lang == "zh" else "Storage Settings"))

        retention_days = st.number_input(
            "报告保留天数" if lang == "zh" else "Report retention days",
            min_value=7,
            max_value=365,
            value=90
        )

        max_storage = st.number_input(
            "最大存储空间(GB)" if lang == "zh" else "Max storage (GB)",
            min_value=1,
            max_value=100,
            value=10
        )

    st.markdown("---")

    # Save configuration
    if st.button("💾 " + ("保存配置" if lang == "zh" else "Save Configuration")):
        st.success("✅ " + ("配置已保存" if lang == "zh" else "Configuration saved"))


def render_code_examples(lang):
    """Render code examples tab"""

    st.markdown("## 💻 " + ("代码示例" if lang == "zh" else "Code Examples"))

    if lang == "zh":
        st.markdown("### 1. 生成完整评估报告")
    else:
        st.markdown("### 1. Generate Full Evaluation Report")

    st.code("""
from aeva.reporting import ReportGenerator, ReportType, ExportFormat

# Initialize report generator
generator = ReportGenerator()

# Generate full evaluation report
report = generator.generate_report(
    report_type=ReportType.FULL_EVALUATION,
    model_name="my_classifier",
    model_version="1.0.0",
    include_modules=[
        "explainability",
        "robustness",
        "fairness",
        "data_quality",
        "performance"
    ],
    export_formats=[ExportFormat.PDF, ExportFormat.HTML]
)

# Save report
report.save("./reports/full_evaluation_report.pdf")
print(f"Report generated: {report.file_path}")
""", language="python")

    st.markdown("---")

    if lang == "zh":
        st.markdown("### 2. 生成对比报告")
    else:
        st.markdown("### 2. Generate Comparison Report")

    st.code("""
from aeva.reporting import ComparisonReportGenerator

# Initialize comparison report generator
comp_generator = ComparisonReportGenerator()

# Compare multiple models
report = comp_generator.compare_models(
    models=[
        {"name": "model_v1", "path": "models/v1.pkl"},
        {"name": "model_v2", "path": "models/v2.pkl"},
        {"name": "model_v3", "path": "models/v3.pkl"}
    ],
    metrics=["accuracy", "precision", "recall", "f1_score"],
    test_data="data/test.csv"
)

# Export report
report.export(
    format=ExportFormat.HTML,
    output_path="./reports/model_comparison.html",
    include_visualizations=True
)
""", language="python")

    st.markdown("---")

    if lang == "zh":
        st.markdown("### 3. 使用自定义模板")
    else:
        st.markdown("### 3. Use Custom Template")

    st.code("""
from aeva.reporting import ReportGenerator, ReportTemplate

# Load custom template
template = ReportTemplate.from_file("./templates/my_template.yaml")

# Generate report with custom template
generator = ReportGenerator(template=template)

report = generator.generate_report(
    report_type=ReportType.CUSTOM,
    data={
        "model_info": {...},
        "metrics": {...},
        "visualizations": [...]
    }
)

# Export to multiple formats
report.export_all(
    formats=[ExportFormat.PDF, ExportFormat.HTML, ExportFormat.MARKDOWN],
    output_dir="./reports/"
)
""", language="python")

    st.markdown("---")

    if lang == "zh":
        st.markdown("### 4. 批量报告生成")
    else:
        st.markdown("### 4. Batch Report Generation")

    st.code("""
from aeva.reporting import BatchReportGenerator
from pathlib import Path

# Initialize batch generator
batch_gen = BatchReportGenerator()

# Configure batch job
batch_job = batch_gen.create_job(
    models_dir="./models/",
    output_dir="./reports/batch/",
    report_type=ReportType.FULL_EVALUATION,
    export_formats=[ExportFormat.PDF, ExportFormat.HTML]
)

# Run batch generation
results = batch_gen.run(
    batch_job,
    max_parallel=4,
    on_progress=lambda p: print(f"Progress: {p}%")
)

# Summary
print(f"Generated {results.success_count} reports")
print(f"Failed: {results.failure_count}")
print(f"Total time: {results.elapsed_time}s")
""", language="python")

    st.markdown("---")

    if lang == "zh":
        st.markdown("### 5. 定时报告生成")
    else:
        st.markdown("### 5. Scheduled Report Generation")

    st.code("""
from aeva.reporting import ScheduledReportGenerator
from aeva.reporting.schedules import CronSchedule

# Initialize scheduled generator
scheduler = ScheduledReportGenerator()

# Schedule weekly report
scheduler.add_schedule(
    name="weekly_model_report",
    schedule=CronSchedule("0 9 * * 1"),  # Every Monday at 9 AM
    report_config={
        "type": ReportType.FULL_EVALUATION,
        "models": ["production_model"],
        "formats": [ExportFormat.PDF, ExportFormat.HTML]
    },
    email_to=["team@example.com"]
)

# Start scheduler
scheduler.start()
print("Report scheduler started")
""", language="python")

    st.markdown("---")

    if lang == "zh":
        st.info("""
        💡 **提示**:
        - 使用 `ReportGenerator` 生成单个报告
        - 使用 `BatchReportGenerator` 批量处理多个模型
        - 使用 `ScheduledReportGenerator` 设置定时任务
        - 支持自定义模板和多种导出格式
        - 可以通过邮件自动发送报告
        """)
    else:
        st.info("""
        💡 **Tips**:
        - Use `ReportGenerator` for single reports
        - Use `BatchReportGenerator` for batch processing
        - Use `ScheduledReportGenerator` for scheduled tasks
        - Support custom templates and multiple export formats
        - Reports can be automatically sent via email
        """)
