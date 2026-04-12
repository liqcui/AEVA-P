"""
AEVA - Algorithm Evaluation & Validation Agent
算法评测与验证智能体

Main package initialization

Copyright (c) 2024-2026 AEVA Development Team
All rights reserved.

License: Dual License
- Personal/Academic Use: Free with attribution
- Commercial Use: Requires explicit permission

If you use this code, you must:
1. Notify the original author
2. Provide attribution in your project
3. Keep this watermark intact
4. For commercial use: Obtain written permission

Project: AEVA v2.0 - Enterprise ML Model Evaluation Platform
GitHub: https://github.com/liqcui/AEVA-P
Creation Date: 2024-01-15
Last Modified: 2026-04-12

Traceable Watermark ID: AEVA-2026-LQC-dc68e33
This unique identifier must remain in all derivatives.

Contact: liquan_cui@126.com
- Usage notifications
- Commercial license inquiries
- Questions and support
"""

__version__ = "2.0.0"
__author__ = "AEVA Development Team"
__copyright__ = "Copyright (c) 2024-2026 AEVA Development Team. All rights reserved."
__license__ = "Dual License: Free for Personal/Academic, Commercial Requires Permission"
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
