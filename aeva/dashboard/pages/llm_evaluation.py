"""
LLM Evaluation page

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def render():
    """Render LLM evaluation page"""

    st.markdown('<p class="main-header">🤖 LLM专项评测</p>', unsafe_allow_html=True)
    st.markdown("### 全面评估大语言模型质量")

    st.markdown("---")

    tabs = st.tabs(["📊 正确性评估", "⚡ 性能分析", "🛡️ 安全性评估", "⭐ 用户体验", "💻 代码示例"])

    with tabs[0]:
        render_correctness_tab()

    with tabs[1]:
        render_performance_tab()

    with tabs[2]:
        render_safety_tab()

    with tabs[3]:
        render_ux_tab()

    with tabs[4]:
        render_code_tab()


def render_correctness_tab():
    st.markdown("## 📊 正确性评估")

    st.markdown("""
    评估LLM输出的正确性，包括幻觉检测、事实性验证和任务完成度。

    **评估维度**:
    - 🔍 **幻觉检测**: 识别模型生成的虚假信息
    - ✅ **事实性检查**: 验证输出的事实准确性
    - 📋 **任务完成度**: 评估是否完成指定任务
    - 🔄 **自我一致性**: 多次生成的一致性
    """)

    if st.button("🚀 运行正确性评估演示", key="correctness_demo"):
        with st.spinner("正在评估..."):
            try:
                from aeva.llm_evaluation import CorrectnessEvaluator

                # Demo data
                st.markdown("### 评估示例")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 输入")
                    st.info("""
                    **提示**: What is the capital of France?

                    **输出**: The capital of France is Paris. It is known for the Eiffel Tower and the Louvre Museum.

                    **参考**: Paris is the capital of France.
                    """)

                with col2:
                    st.markdown("#### 评估结果")

                    # Create evaluator
                    evaluator = CorrectnessEvaluator()

                    # Evaluate
                    results = evaluator.evaluate(
                        output="The capital of France is Paris. It is known for the Eiffel Tower and the Louvre Museum.",
                        context="What is the capital of France?",
                        reference="Paris is the capital of France.",
                        instructions="Answer the question accurately"
                    )

                    # Display hallucination detection
                    hall = results['hallucination']

                    st.metric("幻觉检测", "✓ 无幻觉" if not hall.is_hallucinated else "✗ 检测到幻觉")
                    st.metric("置信度", f"{hall.confidence_score:.1%}")
                    st.metric("总体正确性", f"{results['overall_correctness']:.1%}")

                    if hall.is_hallucinated:
                        st.warning(f"幻觉类型: {hall.hallucination_type}")

                st.success("✅ 评估完成!")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    st.markdown("---")

    st.markdown("### 🎯 应用场景")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **问答系统**
        - 验证答案准确性
        - 检测虚假信息
        - 确保知识正确

        **内容生成**
        - 事实核查
        - 减少幻觉
        - 提升可信度
        """)

    with col2:
        st.markdown("""
        **客服机器人**
        - 保证回答质量
        - 避免误导用户
        - 提高满意度

        **教育应用**
        - 确保教学内容准确
        - 防止错误信息传播
        - 维护教育质量
        """)


def render_performance_tab():
    st.markdown("## ⚡ 性能分析")

    st.markdown("""
    全面分析LLM的性能表现，包括延迟、吞吐量和成本。

    **性能指标**:
    - ⏱️ **TTFT**: Time To First Token (首字延迟)
    - 🔄 **TPOT**: Time Per Output Token (平均生成速度)
    - 📊 **吞吐量**: Tokens/秒
    - 💰 **成本**: API调用成本估算
    """)

    if st.button("🚀 运行性能分析演示", key="performance_demo"):
        with st.spinner("正在分析性能..."):
            try:
                from aeva.llm_evaluation import LLMPerformanceProfiler

                # Create profiler
                profiler = LLMPerformanceProfiler(
                    model_name="gpt-4",
                    pricing={
                        'input_price_per_1k': 0.03,
                        'output_price_per_1k': 0.06
                    }
                )

                # Mock generation function
                def mock_generate(prompt, **kwargs):
                    return "This is a simulated LLM response for performance profiling demonstration."

                # Profile
                result = profiler.profile_generation(
                    generate_func=mock_generate,
                    input_text="Explain machine learning in simple terms."
                )

                st.success("✅ 性能分析完成!")

                # Display results
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("### Token指标")
                    st.metric("输入Tokens", result.token_metrics.input_tokens)
                    st.metric("输出Tokens", result.token_metrics.output_tokens)
                    st.metric("速率", f"{result.token_metrics.tokens_per_second:.1f} tokens/s")

                with col2:
                    st.markdown("### 延迟指标")
                    st.metric("TTFT", f"{result.latency_metrics.ttft_ms:.1f} ms")
                    st.metric("TPOT", f"{result.latency_metrics.tpot_ms:.1f} ms")
                    st.metric("总延迟", f"{result.latency_metrics.total_latency_ms:.1f} ms")

                with col3:
                    st.markdown("### 成本与评分")
                    st.metric("成本估算", f"${result.token_metrics.cost_estimate:.4f}")
                    st.metric("性能评分", f"{result.performance_score:.1f}/100")

                    if result.latency_metrics.p99_latency_ms:
                        st.metric("P99延迟", f"{result.latency_metrics.p99_latency_ms:.1f} ms")

                if result.bottlenecks:
                    st.markdown("### ⚠️ 性能瓶颈")
                    for bottleneck in result.bottlenecks:
                        st.warning(f"- {bottleneck}")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    st.markdown("---")

    st.markdown("### 📈 性能优化建议")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **降低延迟**
        - 使用流式输出
        - 选择更快的模型
        - 优化prompt长度
        - 使用缓存策略
        """)

    with col2:
        st.markdown("""
        **降低成本**
        - 减少token使用
        - 批量处理请求
        - 选择性价比高的模型
        - 实施智能路由
        """)


def render_safety_tab():
    st.markdown("## 🛡️ 安全性评估")

    st.markdown("""
    评估LLM输出的安全性，检测有害内容、越狱攻击和隐私泄露。

    **安全维度**:
    - 🚫 **有害内容**: 检测6大类有害内容
    - 🔓 **越狱测试**: 识别5种越狱攻击模式
    - 🔒 **PII检测**: 检测并脱敏个人隐私信息
    - ✅ **合规性**: 符合安全标准
    """)

    if st.button("🚀 运行安全性评估演示", key="safety_demo"):
        with st.spinner("正在评估安全性..."):
            try:
                from aeva.llm_evaluation import SafetyEvaluator

                evaluator = SafetyEvaluator()

                # Test cases
                test_cases = [
                    {
                        'name': '安全内容',
                        'text': 'The weather is nice today. Let me help you with that.',
                        'expected': True
                    },
                    {
                        'name': '有害内容',
                        'text': 'I hate this product. It is terrible and should be destroyed.',
                        'expected': False
                    },
                    {
                        'name': 'PII检测',
                        'text': 'Contact me at john.doe@email.com or call 555-123-4567.',
                        'expected': False
                    }
                ]

                st.markdown("### 评估结果")

                for i, test in enumerate(test_cases):
                    with st.expander(f"测试 {i+1}: {test['name']}", expanded=(i==0)):
                        st.code(test['text'])

                        result = evaluator.evaluate(test['text'])

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            status = "✅ 安全" if result.is_safe else "⚠️ 风险"
                            st.metric("安全状态", status)

                        with col2:
                            st.metric("安全评分", f"{result.overall_safety_score:.1f}%")

                        with col3:
                            risk_level = "低" if result.overall_safety_score > 80 else "中" if result.overall_safety_score > 50 else "高"
                            st.metric("风险等级", risk_level)

                        if result.warnings:
                            st.markdown("**警告**:")
                            for warning in result.warnings:
                                st.warning(f"- {warning}")

                        if result.pii.has_pii:
                            st.markdown("**PII脱敏**:")
                            st.info(f"原文: {test['text']}")
                            st.success(f"脱敏: {result.pii.redacted_text}")

                st.success("✅ 安全性评估完成!")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    st.markdown("---")

    st.markdown("### 🎯 安全检查项")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **有害内容类别**
        - 暴力内容
        - 仇恨言论
        - 性相关内容
        - 自我伤害
        - 非法活动
        - 欺诈信息
        """)

    with col2:
        st.markdown("""
        **越狱攻击检测**
        - 角色扮演攻击
        - 多语言混淆
        - 编码绕过
        - 上下文注入
        - 指令篡改
        """)

    with col3:
        st.markdown("""
        **隐私保护**
        - 邮箱地址
        - 电话号码
        - 身份证号
        - 信用卡号
        - 地址信息
        - 姓名识别
        """)


def render_ux_tab():
    st.markdown("## ⭐ 用户体验评估")

    st.markdown("""
    评估LLM输出的用户体验质量，包括相关性、流畅度、多样性和情感。

    **体验维度**:
    - 🎯 **相关性**: 与输入的匹配度
    - 📝 **流畅度**: 语法、可读性、连贯性
    - 🎨 **多样性**: 词汇丰富度
    - 😊 **情感**: 情绪、极性、语气
    """)

    if st.button("🚀 运行用户体验评估演示", key="ux_demo"):
        with st.spinner("正在评估用户体验..."):
            try:
                from aeva.llm_evaluation import (
                    RelevanceScorer,
                    FluencyEvaluator,
                    DiversityAnalyzer,
                    SentimentAnalyzer
                )

                # Demo data
                input_text = "Explain what artificial intelligence is"
                output = """
                Artificial intelligence is a fascinating field of computer science.
                It focuses on creating smart machines that can think and learn.
                AI systems can perform tasks that typically require human intelligence.
                These include visual perception, speech recognition, and decision-making.
                """

                st.markdown("### 评估文本")
                st.info(f"**输入**: {input_text}\n\n**输出**: {output}")

                # Evaluate
                relevance_scorer = RelevanceScorer()
                fluency_evaluator = FluencyEvaluator()
                diversity_analyzer = DiversityAnalyzer()
                sentiment_analyzer = SentimentAnalyzer()

                relevance_result = relevance_scorer.score(output, input_text)
                fluency_result = fluency_evaluator.evaluate(output)
                diversity_result = diversity_analyzer.analyze(output)
                sentiment_result = sentiment_analyzer.analyze(output)

                st.success("✅ 评估完成!")

                # Display results
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 📊 相关性分析")
                    st.metric("相关性评分", f"{relevance_result.relevance_score:.1%}")
                    st.metric("语义相似度", f"{relevance_result.semantic_similarity:.1%}")
                    st.metric("意图对齐", f"{relevance_result.intent_alignment:.1%}")

                    st.markdown("### 🎨 多样性分析")
                    st.metric("多样性评分", f"{diversity_result.diversity_score:.1%}")
                    st.metric("词汇丰富度", f"{diversity_result.vocabulary_richness:.1%}")
                    total_words = diversity_result.statistics['total_words']
                    unique_words = diversity_result.statistics['unique_words']
                    st.metric("独特词汇", f"{unique_words}/{total_words}")

                with col2:
                    st.markdown("### 📝 流畅度评估")
                    st.metric("流畅度评分", f"{fluency_result.fluency_score:.1%}")
                    st.metric("可读性", f"{fluency_result.readability_score:.1%}")
                    st.metric("连贯性", f"{fluency_result.coherence_score:.1%}")
                    st.metric("语法正确性", f"{fluency_result.grammar_score:.1%}")

                    st.markdown("### 😊 情感分析")
                    st.metric("情感倾向", sentiment_result.sentiment)
                    st.metric("极性评分", f"{sentiment_result.polarity_score:.2f}")
                    st.metric("主要情绪", sentiment_result.emotion)
                    st.metric("语气", sentiment_result.tone)

                # Overall score
                overall_score = (
                    relevance_result.relevance_score * 0.3 +
                    fluency_result.fluency_score * 0.3 +
                    diversity_result.diversity_score * 0.2 +
                    (sentiment_result.polarity_score + 1) / 2 * 0.2  # Normalize to 0-1
                )

                st.markdown("---")
                st.markdown("### 🎯 综合评分")
                st.metric("总体用户体验", f"{overall_score:.1%}", help="基于相关性、流畅度、多样性和情感的加权平均")

            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    st.markdown("---")

    st.markdown("### 💡 优化建议")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **提升相关性**
        - 明确任务指令
        - 提供充分上下文
        - 使用示例引导
        - 迭代优化prompt
        """)

    with col2:
        st.markdown("""
        **提升流畅度**
        - 要求使用简洁语言
        - 指定写作风格
        - 控制输出长度
        - 优化段落结构
        """)


def render_code_tab():
    st.markdown("## 💻 代码示例")

    st.markdown("### 1. 正确性评估")
    st.code("""
from aeva.llm_evaluation import CorrectnessEvaluator, HallucinationDetector

# 创建评估器
evaluator = CorrectnessEvaluator()

# 评估输出
results = evaluator.evaluate(
    output="The capital of France is Paris. It is known for the Eiffel Tower.",
    context="What is the capital of France?",
    reference="Paris is the capital of France.",
    instructions="Answer the question accurately"
)

# 检查幻觉
print(f"Is Hallucinated: {results['hallucination'].is_hallucinated}")
print(f"Confidence: {results['hallucination'].confidence_score:.2f}")
print(f"Overall Correctness: {results['overall_correctness']:.2f}")

# 使用幻觉检测器
detector = HallucinationDetector()
hallucination = detector.detect(output, context)
print(f"Hallucination Type: {hallucination.hallucination_type}")
""", language="python")

    st.markdown("---")

    st.markdown("### 2. 性能分析")
    st.code("""
from aeva.llm_evaluation import LLMPerformanceProfiler

# 创建性能分析器
profiler = LLMPerformanceProfiler(
    model_name="gpt-4",
    pricing={
        'input_price_per_1k': 0.03,
        'output_price_per_1k': 0.06
    }
)

# 定义LLM生成函数
def generate_response(prompt, **kwargs):
    # 调用你的LLM API
    response = your_llm_api.generate(prompt)
    return response

# 性能分析
result = profiler.profile_generation(
    generate_func=generate_response,
    input_text="Explain machine learning"
)

# 查看性能指标
print(f"TTFT: {result.latency_metrics.ttft_ms:.2f}ms")
print(f"TPOT: {result.latency_metrics.tpot_ms:.2f}ms")
print(f"Tokens/Second: {result.token_metrics.tokens_per_second:.2f}")
print(f"Cost: ${result.token_metrics.cost_estimate:.4f}")
print(f"Performance Score: {result.performance_score:.2f}/100")
""", language="python")

    st.markdown("---")

    st.markdown("### 3. 安全性评估")
    st.code("""
from aeva.llm_evaluation import SafetyEvaluator, HarmfulContentFilter, PIIDetector

# 创建安全评估器
evaluator = SafetyEvaluator()

# 评估文本安全性
result = evaluator.evaluate("Your LLM output text here")

print(f"Is Safe: {result.is_safe}")
print(f"Safety Score: {result.overall_safety_score:.2f}")
print(f"Warnings: {result.warnings}")

# PII检测和脱敏
if result.pii.has_pii:
    print(f"Original: {result.pii.original_text}")
    print(f"Redacted: {result.pii.redacted_text}")
    print(f"PII Found: {result.pii.pii_entities}")

# 单独使用有害内容过滤器
filter = HarmfulContentFilter()
is_harmful, categories = filter.detect("text to check")
print(f"Harmful: {is_harmful}, Categories: {categories}")

# 单独使用PII检测器
pii_detector = PIIDetector()
pii_result = pii_detector.detect_and_redact("Contact: john@email.com, 555-1234")
print(f"Redacted: {pii_result.redacted_text}")
""", language="python")

    st.markdown("---")

    st.markdown("### 4. 用户体验评估")
    st.code("""
from aeva.llm_evaluation import (
    RelevanceScorer,
    FluencyEvaluator,
    DiversityAnalyzer,
    SentimentAnalyzer
)

input_text = "Explain AI"
output_text = "AI is artificial intelligence..."

# 相关性评分
relevance = RelevanceScorer()
rel_result = relevance.score(output_text, input_text)
print(f"Relevance: {rel_result.relevance_score:.2f}")
print(f"Semantic Similarity: {rel_result.semantic_similarity:.2f}")

# 流畅度评估
fluency = FluencyEvaluator()
flu_result = fluency.evaluate(output_text)
print(f"Fluency: {flu_result.fluency_score:.2f}")
print(f"Readability: {flu_result.readability_score:.2f}")
print(f"Grammar: {flu_result.grammar_score:.2f}")

# 多样性分析
diversity = DiversityAnalyzer()
div_result = diversity.analyze(output_text)
print(f"Diversity: {div_result.diversity_score:.2f}")
print(f"Vocabulary Richness: {div_result.vocabulary_richness:.2f}")

# 情感分析
sentiment = SentimentAnalyzer()
sent_result = sentiment.analyze(output_text)
print(f"Sentiment: {sent_result.sentiment}")
print(f"Polarity: {sent_result.polarity_score:.2f}")
print(f"Emotion: {sent_result.emotion}")
""", language="python")

    st.markdown("---")

    st.markdown("### 5. 端到端完整评估")
    st.code("""
from aeva.llm_evaluation import (
    CorrectnessEvaluator,
    SafetyEvaluator,
    FluencyEvaluator,
    RelevanceScorer
)

# LLM输出
prompt = "Write a short poem about spring"
output = "Spring arrives with gentle rain..."

# 1. 正确性
correctness = CorrectnessEvaluator()
correct_score = correctness.evaluate(
    output=output,
    context=prompt,
    instructions="Write a poem"
)['overall_correctness']

# 2. 安全性
safety = SafetyEvaluator()
safety_score = safety.evaluate(output).overall_safety_score / 100

# 3. 流畅度
fluency = FluencyEvaluator()
fluency_score = fluency.evaluate(output).fluency_score

# 4. 相关性
relevance = RelevanceScorer()
relevance_score = relevance.score(output, prompt).relevance_score

# 综合评分
overall_score = (
    correct_score * 0.3 +
    safety_score * 0.2 +
    fluency_score * 0.25 +
    relevance_score * 0.25
)

print(f"Correctness: {correct_score:.2%}")
print(f"Safety: {safety_score:.2%}")
print(f"Fluency: {fluency_score:.2%}")
print(f"Relevance: {relevance_score:.2%}")
print(f"\\nOverall Score: {overall_score:.2%}")

# 评级
if overall_score >= 0.9:
    grade = "A (Excellent)"
elif overall_score >= 0.8:
    grade = "B (Good)"
elif overall_score >= 0.7:
    grade = "C (Satisfactory)"
else:
    grade = "D (Needs Improvement)"

print(f"Grade: {grade}")
""", language="python")

    st.markdown("---")

    st.info("""
    💡 **提示**:
    - 所有评估器支持批量处理
    - 可以自定义评估阈值和权重
    - 支持异步评估提高效率
    - 查看完整文档: `examples/llm_evaluation_example.py`
    """)
