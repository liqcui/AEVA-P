"""
AEVA LLM Evaluation Module

Comprehensive evaluation suite for Large Language Models including:
- Correctness evaluation (accuracy, hallucination detection)
- Performance evaluation (TTFT, TPOT, latency)
- Safety evaluation (harmful content, jailbreak testing)
- User experience evaluation (relevance, fluency)

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission
GitHub: https://github.com/liqcui/AEVA-P
Watermark: AEVA-2026-LQC-dc68e33
"""

from aeva.llm_evaluation.correctness import (
    CorrectnessEvaluator,
    HallucinationDetector,
    FactualityChecker,
    TaskCompletionScorer
)

from aeva.llm_evaluation.performance import (
    LLMPerformanceProfiler,
    TokenMetrics,
    LatencyMetrics
)

from aeva.llm_evaluation.safety import (
    SafetyEvaluator,
    HarmfulContentFilter,
    JailbreakTester,
    PIIDetector
)

from aeva.llm_evaluation.user_experience import (
    RelevanceScorer,
    FluencyEvaluator,
    DiversityAnalyzer,
    SentimentAnalyzer
)

__all__ = [
    # Correctness
    'CorrectnessEvaluator',
    'HallucinationDetector',
    'FactualityChecker',
    'TaskCompletionScorer',

    # Performance
    'LLMPerformanceProfiler',
    'TokenMetrics',
    'LatencyMetrics',

    # Safety
    'SafetyEvaluator',
    'HarmfulContentFilter',
    'JailbreakTester',
    'PIIDetector',

    # User Experience
    'RelevanceScorer',
    'FluencyEvaluator',
    'DiversityAnalyzer',
    'SentimentAnalyzer',
]

__version__ = '1.0.0'
