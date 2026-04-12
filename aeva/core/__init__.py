"""
AEVA Core Module
Core framework components
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
