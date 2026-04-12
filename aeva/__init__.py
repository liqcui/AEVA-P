"""
AEVA - Algorithm Evaluation & Validation Agent
算法评测与验证智能体

Main package initialization
"""

__version__ = "0.1.0"
__author__ = "AEVA Development Team"
__description__ = "Algorithm Evaluation & Validation Agent"

from aeva.core.platform import AEVA
from aeva.core.config import AEVAConfig

__all__ = [
    "AEVA",
    "AEVAConfig",
    "__version__",
]
