"""
AEVA-Auto Module
Automation pipeline and workflow orchestration
"""

from aeva.auto.manager import AutomationManager
from aeva.auto.executor import PipelineExecutor
from aeva.auto.scheduler import TaskScheduler

__all__ = [
    "AutomationManager",
    "PipelineExecutor",
    "TaskScheduler",
]
