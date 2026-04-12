"""
AEVA Knowledge Base and Few-shot Learning Module

Provides knowledge base management, few-shot learning, and prompt engineering capabilities.

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from aeva.knowledge.base import KnowledgeBase, KnowledgeEntry
from aeva.knowledge.retriever import KnowledgeRetriever, SemanticRetriever
from aeva.knowledge.fewshot import FewShotLearner, FewShotSelector
from aeva.knowledge.prompts import PromptTemplate, PromptBuilder, PromptOptimizer

__all__ = [
    'KnowledgeBase',
    'KnowledgeEntry',
    'KnowledgeRetriever',
    'SemanticRetriever',
    'FewShotLearner',
    'FewShotSelector',
    'PromptTemplate',
    'PromptBuilder',
    'PromptOptimizer',
]
