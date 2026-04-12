"""
Continuous Monitoring for ML Models

Real-time monitoring of model performance metrics

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import statistics

logger = logging.getLogger(__name__)


@dataclass
class MetricSnapshot:
    """Snapshot of metrics at a point in time"""
    timestamp: datetime
    metrics: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'metrics': self.metrics,
            'metadata': self.metadata
        }


@dataclass
class MonitoringReport:
    """Monitoring report summary"""
    monitor_name: str
    start_time: datetime
    end_time: datetime
    total_snapshots: int
    metrics_summary: Dict[str, Dict[str, float]]  # metric_name -> {avg, min, max, latest}
    anomalies: List[Dict[str, Any]]
    trends: Dict[str, str]  # metric_name -> trend (improving, degrading, stable)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'monitor_name': self.monitor_name,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'total_snapshots': self.total_snapshots,
            'metrics_summary': self.metrics_summary,
            'anomalies': self.anomalies,
            'trends': self.trends
        }


class MetricMonitor:
    """
    Monitor individual metric over time

    Features:
    - Rolling window statistics
    - Anomaly detection
    - Trend analysis
    - Threshold alerts
    """

    def __init__(
        self,
        metric_name: str,
        window_size: int = 100,
        alert_threshold: Optional[float] = None,
        alert_direction: str = 'below'  # 'below', 'above', 'both'
    ):
        """
        Initialize metric monitor

        Args:
            metric_name: Name of the metric
            window_size: Number of recent values to keep
            alert_threshold: Threshold for alerts
            alert_direction: Direction for threshold ('below', 'above', 'both')
        """
        self.metric_name = metric_name
        self.window_size = window_size
        self.alert_threshold = alert_threshold
        self.alert_direction = alert_direction

        self.values = deque(maxlen=window_size)
        self.timestamps = deque(maxlen=window_size)
        self.anomalies: List[Dict[str, Any]] = []

    def record(self, value: float, timestamp: Optional[datetime] = None) -> None:
        """Record a new metric value"""
        if timestamp is None:
            timestamp = datetime.now()

        self.values.append(value)
        self.timestamps.append(timestamp)

        # Check for anomaly
        if self.alert_threshold is not None:
            self._check_threshold(value, timestamp)

    def _check_threshold(self, value: float, timestamp: datetime) -> None:
        """Check if value violates threshold"""
        alert = False

        if self.alert_direction == 'below' and value < self.alert_threshold:
            alert = True
        elif self.alert_direction == 'above' and value > self.alert_threshold:
            alert = True
        elif self.alert_direction == 'both':
            if isinstance(self.alert_threshold, tuple):
                low, high = self.alert_threshold
                if value < low or value > high:
                    alert = True

        if alert:
            self.anomalies.append({
                'timestamp': timestamp.isoformat(),
                'value': value,
                'threshold': self.alert_threshold,
                'direction': self.alert_direction
            })

            logger.warning(
                f"Metric {self.metric_name} threshold alert: "
                f"value={value:.4f}, threshold={self.alert_threshold}"
            )

    def get_statistics(self) -> Dict[str, float]:
        """Get statistics for current window"""
        if not self.values:
            return {}

        values_list = list(self.values)

        return {
            'count': len(values_list),
            'mean': statistics.mean(values_list),
            'median': statistics.median(values_list),
            'stdev': statistics.stdev(values_list) if len(values_list) > 1 else 0.0,
            'min': min(values_list),
            'max': max(values_list),
            'latest': values_list[-1]
        }

    def get_trend(self) -> str:
        """
        Analyze trend in recent values

        Returns:
            'improving', 'degrading', or 'stable'
        """
        if len(self.values) < 10:
            return 'insufficient_data'

        values_list = list(self.values)

        # Compare first half vs second half
        midpoint = len(values_list) // 2
        first_half_avg = statistics.mean(values_list[:midpoint])
        second_half_avg = statistics.mean(values_list[midpoint:])

        change_pct = ((second_half_avg - first_half_avg) / first_half_avg) * 100

        # Threshold for significance
        if abs(change_pct) < 5:  # Less than 5% change
            return 'stable'
        elif change_pct > 0:
            return 'improving'  # Assuming higher is better
        else:
            return 'degrading'

    def detect_anomalies(self, std_threshold: float = 3.0) -> List[Dict[str, Any]]:
        """
        Detect statistical anomalies using z-score

        Args:
            std_threshold: Number of standard deviations for anomaly

        Returns:
            List of anomaly dictionaries
        """
        if len(self.values) < 10:
            return []

        values_list = list(self.values)
        timestamps_list = list(self.timestamps)

        mean = statistics.mean(values_list)
        stdev = statistics.stdev(values_list)

        if stdev == 0:
            return []

        statistical_anomalies = []

        for i, (value, timestamp) in enumerate(zip(values_list, timestamps_list)):
            z_score = abs((value - mean) / stdev)

            if z_score > std_threshold:
                statistical_anomalies.append({
                    'index': i,
                    'timestamp': timestamp.isoformat(),
                    'value': value,
                    'z_score': z_score,
                    'mean': mean,
                    'stdev': stdev
                })

        return statistical_anomalies


class ContinuousMonitor:
    """
    Continuous monitoring system for ML models

    Features:
    - Multi-metric tracking
    - Real-time statistics
    - Anomaly detection
    - Trend analysis
    - Reporting
    """

    def __init__(
        self,
        model_name: str,
        metrics: List[str],
        window_size: int = 100,
        alert_rules: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        """
        Initialize continuous monitor

        Args:
            model_name: Name of the model being monitored
            metrics: List of metric names to track
            window_size: Rolling window size
            alert_rules: Alert configuration per metric
        """
        self.model_name = model_name
        self.window_size = window_size
        self.start_time = datetime.now()

        # Create monitors for each metric
        self.monitors: Dict[str, MetricMonitor] = {}

        for metric in metrics:
            alert_config = alert_rules.get(metric, {}) if alert_rules else {}

            self.monitors[metric] = MetricMonitor(
                metric_name=metric,
                window_size=window_size,
                alert_threshold=alert_config.get('threshold'),
                alert_direction=alert_config.get('direction', 'below')
            )

        self.snapshots: List[MetricSnapshot] = []

        logger.info(f"Initialized continuous monitor for {model_name} with {len(metrics)} metrics")

    def record_metrics(
        self,
        metrics: Dict[str, float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record metrics snapshot

        Args:
            metrics: Dictionary of metric values
            metadata: Optional metadata for this snapshot
        """
        timestamp = datetime.now()

        # Record each metric
        for metric_name, value in metrics.items():
            if metric_name in self.monitors:
                self.monitors[metric_name].record(value, timestamp)

        # Create snapshot
        snapshot = MetricSnapshot(
            timestamp=timestamp,
            metrics=metrics,
            metadata=metadata or {}
        )

        self.snapshots.append(snapshot)

        logger.debug(f"Recorded metrics: {metrics}")

    def get_current_statistics(self) -> Dict[str, Dict[str, float]]:
        """Get current statistics for all metrics"""
        return {
            metric_name: monitor.get_statistics()
            for metric_name, monitor in self.monitors.items()
        }

    def get_trends(self) -> Dict[str, str]:
        """Get trends for all metrics"""
        return {
            metric_name: monitor.get_trend()
            for metric_name, monitor in self.monitors.items()
        }

    def get_anomalies(self, std_threshold: float = 3.0) -> Dict[str, List[Dict[str, Any]]]:
        """Get anomalies for all metrics"""
        return {
            metric_name: monitor.detect_anomalies(std_threshold)
            for metric_name, monitor in self.monitors.items()
        }

    def get_threshold_alerts(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get threshold-based alerts for all metrics"""
        return {
            metric_name: monitor.anomalies
            for metric_name, monitor in self.monitors.items()
            if monitor.anomalies
        }

    def generate_report(self) -> MonitoringReport:
        """
        Generate comprehensive monitoring report

        Returns:
            MonitoringReport with summary and analysis
        """
        end_time = datetime.now()

        # Collect statistics
        metrics_summary = {}
        for metric_name, monitor in self.monitors.items():
            stats = monitor.get_statistics()
            if stats:
                metrics_summary[metric_name] = stats

        # Collect all anomalies
        all_anomalies = []

        # Threshold alerts
        threshold_alerts = self.get_threshold_alerts()
        for metric_name, alerts in threshold_alerts.items():
            for alert in alerts:
                all_anomalies.append({
                    'type': 'threshold',
                    'metric': metric_name,
                    **alert
                })

        # Statistical anomalies
        statistical_anomalies = self.get_anomalies()
        for metric_name, anomalies in statistical_anomalies.items():
            for anomaly in anomalies:
                all_anomalies.append({
                    'type': 'statistical',
                    'metric': metric_name,
                    **anomaly
                })

        # Get trends
        trends = self.get_trends()

        report = MonitoringReport(
            monitor_name=self.model_name,
            start_time=self.start_time,
            end_time=end_time,
            total_snapshots=len(self.snapshots),
            metrics_summary=metrics_summary,
            anomalies=all_anomalies,
            trends=trends
        )

        logger.info(
            f"Generated report: {len(self.snapshots)} snapshots, "
            f"{len(all_anomalies)} anomalies, {len(metrics_summary)} metrics"
        )

        return report

    def reset(self) -> None:
        """Reset all monitors and snapshots"""
        for monitor in self.monitors.values():
            monitor.values.clear()
            monitor.timestamps.clear()
            monitor.anomalies.clear()

        self.snapshots.clear()
        self.start_time = datetime.now()

        logger.info("Monitor reset")

    def simulate_monitoring(
        self,
        model_fn: Callable,
        data_stream,
        interval_seconds: float = 1.0,
        max_iterations: Optional[int] = None
    ) -> None:
        """
        Simulate continuous monitoring with a model function

        Args:
            model_fn: Model prediction function
            data_stream: Iterator of input data
            interval_seconds: Time between evaluations
            max_iterations: Maximum iterations (None = unlimited)
        """
        logger.info(f"Starting monitoring simulation (interval: {interval_seconds}s)")

        iteration = 0

        for data_point in data_stream:
            if max_iterations and iteration >= max_iterations:
                break

            # Run model
            prediction = model_fn(data_point)

            # Extract metrics (assuming prediction contains metrics)
            if isinstance(prediction, dict) and 'metrics' in prediction:
                self.record_metrics(prediction['metrics'])

            # Wait
            time.sleep(interval_seconds)

            iteration += 1

        logger.info(f"Monitoring simulation completed ({iteration} iterations)")
