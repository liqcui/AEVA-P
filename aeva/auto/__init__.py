"""
AEVA-Auto Module
Automation pipeline and workflow orchestration

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from aeva.auto.manager import AutomationManager
from aeva.auto.executor import PipelineExecutor
from aeva.auto.scheduler import TaskScheduler

__all__ = [
    "AutomationManager",
    "PipelineExecutor",
    "TaskScheduler",
]
