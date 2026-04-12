"""
Alerting System for Continuous Monitoring

Send alerts when thresholds are breached or anomalies detected
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertChannel(Enum):
    """Alert delivery channels"""
    LOG = "log"
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"


@dataclass
class Alert:
    """Alert message"""
    alert_id: str
    title: str
    message: str
    severity: AlertSeverity
    source: str  # Component that generated the alert
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'alert_id': self.alert_id,
            'title': self.title,
            'message': self.message,
            'severity': self.severity.value,
            'source': self.source,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata,
            'acknowledged': self.acknowledged,
            'acknowledged_by': self.acknowledged_by,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None
        }


@dataclass
class AlertRule:
    """Alert rule configuration"""
    rule_id: str
    name: str
    condition: Callable[[Any], bool]  # Function that returns True if alert should fire
    severity: AlertSeverity
    channels: List[AlertChannel]
    cooldown_seconds: int = 300  # Minimum time between alerts
    enabled: bool = True
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0

    def should_trigger(self, data: Any) -> bool:
        """Check if rule should trigger an alert"""
        if not self.enabled:
            return False

        # Check cooldown
        if self.last_triggered:
            elapsed = (datetime.now() - self.last_triggered).total_seconds()
            if elapsed < self.cooldown_seconds:
                return False

        # Evaluate condition
        try:
            return self.condition(data)
        except Exception as e:
            logger.error(f"Error evaluating alert rule {self.rule_id}: {e}")
            return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            'rule_id': self.rule_id,
            'name': self.name,
            'severity': self.severity.value,
            'channels': [c.value for c in self.channels],
            'cooldown_seconds': self.cooldown_seconds,
            'enabled': self.enabled,
            'last_triggered': self.last_triggered.isoformat() if self.last_triggered else None,
            'trigger_count': self.trigger_count
        }


class AlertManager:
    """
    Manage alerts and notifications

    Features:
    - Rule-based alerting
    - Multiple delivery channels
    - Alert history
    - Acknowledgment tracking
    - Cooldown periods
    """

    def __init__(self):
        """Initialize alert manager"""
        self.rules: Dict[str, AlertRule] = {}
        self.alerts: List[Alert] = []
        self.handlers: Dict[AlertChannel, Callable] = {
            AlertChannel.LOG: self._log_handler
        }

        logger.info("Alert manager initialized")

    def add_rule(self, rule: AlertRule) -> None:
        """
        Add an alert rule

        Args:
            rule: AlertRule to add
        """
        self.rules[rule.rule_id] = rule
        logger.info(f"Added alert rule: {rule.name} (severity: {rule.severity.value})")

    def remove_rule(self, rule_id: str) -> None:
        """Remove an alert rule"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            logger.info(f"Removed alert rule: {rule_id}")

    def enable_rule(self, rule_id: str) -> None:
        """Enable an alert rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = True
            logger.info(f"Enabled alert rule: {rule_id}")

    def disable_rule(self, rule_id: str) -> None:
        """Disable an alert rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
            logger.info(f"Disabled alert rule: {rule_id}")

    def register_handler(self, channel: AlertChannel, handler: Callable) -> None:
        """
        Register a custom alert handler

        Args:
            channel: Alert channel
            handler: Callable that takes Alert as parameter
        """
        self.handlers[channel] = handler
        logger.info(f"Registered handler for channel: {channel.value}")

    def evaluate_rules(self, data: Any, source: str = "unknown") -> List[Alert]:
        """
        Evaluate all rules against data

        Args:
            data: Data to evaluate
            source: Source component

        Returns:
            List of triggered alerts
        """
        triggered_alerts = []

        for rule in self.rules.values():
            if rule.should_trigger(data):
                alert = self._create_alert(rule, data, source)
                triggered_alerts.append(alert)

                # Update rule state
                rule.last_triggered = datetime.now()
                rule.trigger_count += 1

                # Send alert
                self._send_alert(alert, rule.channels)

        return triggered_alerts

    def _create_alert(self, rule: AlertRule, data: Any, source: str) -> Alert:
        """Create an alert from a rule"""
        alert_id = f"{rule.rule_id}_{int(datetime.now().timestamp())}"

        alert = Alert(
            alert_id=alert_id,
            title=rule.name,
            message=f"Alert triggered: {rule.name}",
            severity=rule.severity,
            source=source,
            timestamp=datetime.now(),
            metadata={'data': data}
        )

        self.alerts.append(alert)

        logger.info(f"Alert created: {alert.title} ({alert.severity.value})")

        return alert

    def create_manual_alert(
        self,
        title: str,
        message: str,
        severity: AlertSeverity,
        source: str,
        channels: Optional[List[AlertChannel]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Alert:
        """
        Create and send a manual alert

        Args:
            title: Alert title
            message: Alert message
            severity: Severity level
            source: Source component
            channels: Delivery channels
            metadata: Additional metadata

        Returns:
            Alert
        """
        alert_id = f"manual_{int(datetime.now().timestamp())}"

        alert = Alert(
            alert_id=alert_id,
            title=title,
            message=message,
            severity=severity,
            source=source,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )

        self.alerts.append(alert)

        # Send to specified channels or default to log
        channels = channels or [AlertChannel.LOG]
        self._send_alert(alert, channels)

        logger.info(f"Manual alert created: {title}")

        return alert

    def _send_alert(self, alert: Alert, channels: List[AlertChannel]) -> None:
        """Send alert to specified channels"""
        for channel in channels:
            handler = self.handlers.get(channel)

            if handler:
                try:
                    handler(alert)
                except Exception as e:
                    logger.error(f"Error sending alert to {channel.value}: {e}", exc_info=True)
            else:
                logger.warning(f"No handler registered for channel: {channel.value}")

    def _log_handler(self, alert: Alert) -> None:
        """Default log handler"""
        severity_map = {
            AlertSeverity.INFO: logger.info,
            AlertSeverity.WARNING: logger.warning,
            AlertSeverity.ERROR: logger.error,
            AlertSeverity.CRITICAL: logger.critical
        }

        log_func = severity_map.get(alert.severity, logger.info)
        log_func(f"[ALERT] {alert.title}: {alert.message}")

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> None:
        """
        Acknowledge an alert

        Args:
            alert_id: Alert ID
            acknowledged_by: Who acknowledged it
        """
        for alert in self.alerts:
            if alert.alert_id == alert_id and not alert.acknowledged:
                alert.acknowledged = True
                alert.acknowledged_by = acknowledged_by
                alert.acknowledged_at = datetime.now()

                logger.info(f"Alert acknowledged: {alert_id} by {acknowledged_by}")
                break

    def get_active_alerts(self, severity: Optional[AlertSeverity] = None) -> List[Alert]:
        """
        Get active (unacknowledged) alerts

        Args:
            severity: Optional severity filter

        Returns:
            List of active alerts
        """
        active = [a for a in self.alerts if not a.acknowledged]

        if severity:
            active = [a for a in active if a.severity == severity]

        return active

    def get_alert_history(
        self,
        limit: Optional[int] = None,
        severity: Optional[AlertSeverity] = None
    ) -> List[Alert]:
        """
        Get alert history

        Args:
            limit: Maximum number of alerts
            severity: Optional severity filter

        Returns:
            List of alerts
        """
        alerts = self.alerts

        if severity:
            alerts = [a for a in alerts if a.severity == severity]

        # Sort by timestamp descending
        alerts = sorted(alerts, key=lambda a: a.timestamp, reverse=True)

        if limit:
            alerts = alerts[:limit]

        return alerts

    def get_stats(self) -> Dict[str, Any]:
        """Get alerting statistics"""
        total_alerts = len(self.alerts)
        active_alerts = len(self.get_active_alerts())

        severity_counts = {}
        for severity in AlertSeverity:
            count = sum(1 for a in self.alerts if a.severity == severity)
            severity_counts[severity.value] = count

        return {
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'acknowledged_alerts': total_alerts - active_alerts,
            'severity_counts': severity_counts,
            'total_rules': len(self.rules),
            'enabled_rules': sum(1 for r in self.rules.values() if r.enabled)
        }

    def clear_old_alerts(self, days: int = 30) -> int:
        """
        Clear alerts older than specified days

        Args:
            days: Number of days to keep

        Returns:
            Number of alerts removed
        """
        cutoff = datetime.now() - timedelta(days=days)
        original_count = len(self.alerts)

        self.alerts = [a for a in self.alerts if a.timestamp > cutoff]

        removed = original_count - len(self.alerts)

        if removed > 0:
            logger.info(f"Cleared {removed} old alerts (older than {days} days)")

        return removed


# Pre-defined alert rule helpers

def create_threshold_rule(
    rule_id: str,
    name: str,
    metric_key: str,
    threshold: float,
    operator: str,  # '>', '<', '>=', '<=', '==', '!='
    severity: AlertSeverity = AlertSeverity.WARNING,
    channels: Optional[List[AlertChannel]] = None
) -> AlertRule:
    """
    Create a threshold-based alert rule

    Args:
        rule_id: Unique rule ID
        name: Rule name
        metric_key: Key to extract from data
        threshold: Threshold value
        operator: Comparison operator
        severity: Alert severity
        channels: Delivery channels

    Returns:
        AlertRule
    """
    def condition(data):
        if isinstance(data, dict) and metric_key in data:
            value = data[metric_key]

            if operator == '>':
                return value > threshold
            elif operator == '<':
                return value < threshold
            elif operator == '>=':
                return value >= threshold
            elif operator == '<=':
                return value <= threshold
            elif operator == '==':
                return value == threshold
            elif operator == '!=':
                return value != threshold

        return False

    return AlertRule(
        rule_id=rule_id,
        name=name,
        condition=condition,
        severity=severity,
        channels=channels or [AlertChannel.LOG]
    )


def create_drift_rule(
    rule_id: str,
    name: str,
    severity: AlertSeverity = AlertSeverity.ERROR,
    channels: Optional[List[AlertChannel]] = None
) -> AlertRule:
    """
    Create a drift detection alert rule

    Args:
        rule_id: Unique rule ID
        name: Rule name
        severity: Alert severity
        channels: Delivery channels

    Returns:
        AlertRule
    """
    def condition(data):
        # Expecting DriftReport or similar
        if isinstance(data, dict):
            return data.get('detected', False) and data.get('severity') in ['high', 'critical']
        return False

    return AlertRule(
        rule_id=rule_id,
        name=name,
        condition=condition,
        severity=severity,
        channels=channels or [AlertChannel.LOG]
    )


from datetime import timedelta
