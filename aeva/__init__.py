"""
AEVA - Algorithm Evaluation & Validation Agent
算法评测与验证智能体

Main package initialization

Copyright (c) 2024-2026 Liquan Cui
All rights reserved.

This software is the proprietary work of Liquan Cui.
Unauthorized copying, modification, distribution, or use of this software,
via any medium, is strictly prohibited without explicit permission.

Project: AEVA v2.0 - Enterprise ML Model Evaluation Platform
Author: Liquan Cui
GitHub: https://github.com/liqcui/AEVA-P
Creation Date: 2024-01-15
Last Modified: 2026-04-12
Unique ID: AEVA-2026-LQC-dc68e33

For licensing inquiries, please contact: liqcui@redhat.com
"""

__version__ = "2.0.0"
__author__ = "Liquan Cui"
__copyright__ = "Copyright (c) 2024-2026 Liquan Cui. All rights reserved."
__license__ = "Proprietary"
__description__ = "Algorithm Evaluation & Validation Agent - Enterprise ML Model Evaluation Platform"
__project_id__ = "AEVA-2026-LQC-dc68e33"
__github__ = "https://github.com/liqcui/AEVA-P"

from aeva.core.platform import AEVA
from aeva.core.config import AEVAConfig

__all__ = [
    "AEVA",
    "AEVAConfig",
    "__version__",
]
