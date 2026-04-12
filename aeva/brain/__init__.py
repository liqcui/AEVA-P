"""
AEVA-Brain Module
Intelligent analysis and diagnosis using LLM

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from aeva.brain.manager import BrainManager
from aeva.brain.analyzer import ResultAnalyzer
from aeva.brain.llm import LLMProvider, ClaudeProvider

__all__ = [
    "BrainManager",
    "ResultAnalyzer",
    "LLMProvider",
    "ClaudeProvider",
]
