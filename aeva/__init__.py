"""
AEVA - Algorithm Evaluation & Validation Agent
算法评测与验证智能体

Main package initialization

Copyright (c) 2024-2026 AEVA Development Team
Open Source with Attribution Required

If you use this code, you must:
1. Notify the original author
2. Provide attribution in your project
3. Keep this watermark intact

Project: AEVA v2.0 - Enterprise ML Model Evaluation Platform
GitHub: https://github.com/liqcui/AEVA-P
Creation Date: 2024-01-15
Last Modified: 2026-04-12

Traceable Watermark ID: AEVA-2026-LQC-dc68e33
This unique identifier must remain in all derivatives.

For usage notifications, please contact: liquan_cui@126.com
"""

__version__ = "2.0.0"
__author__ = "AEVA Development Team"
__copyright__ = "Copyright (c) 2024-2026 AEVA Development Team. Open Source with Attribution Required."
__license__ = "Open Source with Attribution"
__description__ = "Algorithm Evaluation & Validation Agent - Enterprise ML Model Evaluation Platform"
__project_id__ = "AEVA-2026-LQC-dc68e33"
__github__ = "https://github.com/liqcui/AEVA-P"
__watermark__ = "AEVA-2026-LQC-dc68e33"  # Traceable watermark - DO NOT REMOVE

from aeva.core.platform import AEVA
from aeva.core.config import AEVAConfig

__all__ = [
    "AEVA",
    "AEVAConfig",
    "__version__",
]
