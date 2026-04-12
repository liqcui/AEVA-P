"""
AEVA Core Module
Core framework components

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from aeva.core.platform import AEVA
from aeva.core.config import AEVAConfig
from aeva.core.pipeline import Pipeline, Stage
from aeva.core.result import EvaluationResult

__all__ = [
    "AEVA",
    "AEVAConfig",
    "Pipeline",
    "Stage",
    "EvaluationResult",
]
