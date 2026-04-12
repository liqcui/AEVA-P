"""
AEVA Continuous Evaluation Module

Provides continuous monitoring, drift detection, and automated evaluation capabilities.

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from aeva.continuous.monitor import ContinuousMonitor, MetricMonitor
from aeva.continuous.drift import DriftDetector, DataDriftAnalyzer, ModelDriftAnalyzer
from aeva.continuous.scheduler import EvaluationScheduler, ScheduledTask
from aeva.continuous.alerting import AlertManager, Alert, AlertRule

__all__ = [
    'ContinuousMonitor',
    'MetricMonitor',
    'DriftDetector',
    'DataDriftAnalyzer',
    'ModelDriftAnalyzer',
    'EvaluationScheduler',
    'ScheduledTask',
    'AlertManager',
    'Alert',
    'AlertRule',
]
