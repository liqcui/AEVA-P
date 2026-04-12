"""
AEVA Continuous Evaluation Module

Provides continuous monitoring, drift detection, and automated evaluation capabilities.
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
