"""
Example: Continuous Evaluation and Monitoring

Demonstrates how to use the continuous evaluation module for:
- Real-time performance monitoring
- Drift detection (data and model)
- Automated scheduling
- Alert management
"""

import random
import time
from datetime import datetime, timedelta
from aeva.continuous import (
    ContinuousMonitor,
    DriftDetector,
    DataDriftAnalyzer,
    ModelDriftAnalyzer,
    EvaluationScheduler,
    AlertManager,
    AlertRule,
    AlertSeverity,
    AlertChannel,
    create_threshold_rule,
    create_drift_rule,
    minutes,
    hours
)


def create_mock_predictions(n_samples: int = 100, accuracy: float = 0.85):
    """Create mock predictions with specified accuracy"""
    predictions = []

    for i in range(n_samples):
        # Simulate correct/incorrect predictions
        is_correct = random.random() < accuracy

        predictions.append({
            'id': i,
            'prediction': random.choice(['positive', 'negative', 'neutral']),
            'ground_truth': random.choice(['positive', 'negative', 'neutral']),
            'correct': is_correct,
            'confidence': random.uniform(0.6, 0.99)
        })

    return predictions


def calculate_metrics(predictions):
    """Calculate metrics from predictions"""
    correct = sum(1 for p in predictions if p['correct'])
    total = len(predictions)

    avg_confidence = sum(p['confidence'] for p in predictions) / total if total > 0 else 0

    return {
        'accuracy': correct / total if total > 0 else 0,
        'avg_confidence': avg_confidence,
        'total_predictions': total
    }


def example_continuous_monitoring():
    """Example 1: Continuous performance monitoring"""
    print("=" * 70)
    print("Example 1: Continuous Performance Monitoring")
    print("=" * 70)

    # Create monitor
    monitor = ContinuousMonitor(
        model_name="sentiment_classifier",
        metrics=['accuracy', 'avg_confidence'],
        window_size=50,
        alert_rules={
            'accuracy': {'threshold': 0.80, 'direction': 'below'},
            'avg_confidence': {'threshold': 0.70, 'direction': 'below'}
        }
    )

    print(f"\n✓ Monitor created for: {monitor.model_name}")
    print(f"  Tracking: {list(monitor.monitors.keys())}")

    # Simulate monitoring over time
    print("\nSimulating 20 evaluation rounds...")

    for round_num in range(20):
        # Simulate gradual degradation
        base_accuracy = 0.90 - (round_num * 0.015)  # Gradually decrease

        # Generate predictions
        predictions = create_mock_predictions(n_samples=50, accuracy=base_accuracy)
        metrics = calculate_metrics(predictions)

        # Record metrics
        monitor.record_metrics(metrics, metadata={'round': round_num})

        if round_num % 5 == 0:
            print(f"  Round {round_num}: accuracy={metrics['accuracy']:.3f}, confidence={metrics['avg_confidence']:.3f}")

    # Get statistics
    print("\n📊 Current Statistics:")
    stats = monitor.get_current_statistics()

    for metric_name, metric_stats in stats.items():
        print(f"\n  {metric_name}:")
        print(f"    Mean: {metric_stats['mean']:.4f}")
        print(f"    Median: {metric_stats['median']:.4f}")
        print(f"    Std Dev: {metric_stats['stdev']:.4f}")
        print(f"    Min: {metric_stats['min']:.4f}")
        print(f"    Max: {metric_stats['max']:.4f}")
        print(f"    Latest: {metric_stats['latest']:.4f}")

    # Get trends
    print("\n📈 Trends:")
    trends = monitor.get_trends()
    for metric_name, trend in trends.items():
        print(f"  {metric_name}: {trend}")

    # Check for anomalies
    print("\n🔍 Anomalies Detected:")
    threshold_alerts = monitor.get_threshold_alerts()

    for metric_name, alerts in threshold_alerts.items():
        if alerts:
            print(f"  {metric_name}: {len(alerts)} threshold violations")
            for alert in alerts[:3]:  # Show first 3
                print(f"    - Value {alert['value']:.4f} violated threshold {alert['threshold']}")

    # Generate report
    print("\n📋 Monitoring Report:")
    report = monitor.generate_report()

    print(f"  Monitor: {report.monitor_name}")
    print(f"  Period: {report.start_time.strftime('%H:%M:%S')} - {report.end_time.strftime('%H:%M:%S')}")
    print(f"  Total Snapshots: {report.total_snapshots}")
    print(f"  Total Anomalies: {len(report.anomalies)}")

    return monitor


def example_data_drift_detection():
    """Example 2: Data drift detection"""
    print("\n" + "=" * 70)
    print("Example 2: Data Drift Detection")
    print("=" * 70)

    # Create reference (training) data
    reference_data = []
    for i in range(1000):
        # Original distribution: mostly positive sentiment
        label = random.choices(
            ['positive', 'negative', 'neutral'],
            weights=[0.6, 0.2, 0.2],
            k=1
        )[0]

        reference_data.append({
            'id': i,
            'label': label,
            'score': random.gauss(0.7, 0.2)  # Mean 0.7, std 0.2
        })

    # Create current (production) data with drift
    current_data = []
    for i in range(1000):
        # Drifted distribution: more negative sentiment
        label = random.choices(
            ['positive', 'negative', 'neutral'],
            weights=[0.3, 0.5, 0.2],  # Shifted distribution
            k=1
        )[0]

        current_data.append({
            'id': i + 1000,
            'label': label,
            'score': random.gauss(0.5, 0.25)  # Shifted mean and higher variance
        })

    # Detect drift
    analyzer = DataDriftAnalyzer()

    print("\n1. Label Distribution Drift:")
    label_drift = analyzer.detect_drift(
        reference_data=reference_data,
        current_data=current_data,
        feature_key='label',
        threshold=0.2
    )

    print(f"  Detected: {label_drift.detected}")
    print(f"  Severity: {label_drift.severity}")
    print(f"  PSI: {label_drift.metrics['psi']:.4f}")
    print(f"  KL Divergence: {label_drift.metrics['kl_divergence']:.4f}")

    print("\n  Recommendations:")
    for rec in label_drift.recommendations:
        print(f"    - {rec}")

    print("\n2. Score Distribution Drift:")
    score_drift = analyzer.detect_drift(
        reference_data=[d['score'] for d in reference_data],
        current_data=[d['score'] for d in current_data],
        threshold=0.2
    )

    print(f"  Detected: {score_drift.detected}")
    print(f"  Severity: {score_drift.severity}")
    print(f"  PSI: {score_drift.metrics['psi']:.4f}")

    return label_drift, score_drift


def example_model_drift_detection():
    """Example 3: Model performance drift detection"""
    print("\n" + "=" * 70)
    print("Example 3: Model Performance Drift Detection")
    print("=" * 70)

    # Baseline metrics (training/validation)
    baseline_metrics = {
        'accuracy': 0.92,
        'precision': 0.90,
        'recall': 0.89,
        'f1': 0.895
    }

    print(f"\n📊 Baseline Metrics:")
    for metric, value in baseline_metrics.items():
        print(f"  {metric}: {value:.3f}")

    # Create analyzer
    analyzer = ModelDriftAnalyzer(baseline_metrics)

    # Simulate degrading performance over time
    print("\n⏱️ Monitoring performance over 5 time periods...")

    for period in range(1, 6):
        # Gradually degrade performance
        degradation = period * 0.05  # 5% per period

        current_metrics = {
            'accuracy': baseline_metrics['accuracy'] - degradation,
            'precision': baseline_metrics['precision'] - degradation * 0.8,
            'recall': baseline_metrics['recall'] - degradation * 1.2,
            'f1': baseline_metrics['f1'] - degradation
        }

        print(f"\n  Period {period}:")
        print(f"    Accuracy: {current_metrics['accuracy']:.3f}")

        # Detect drift
        drift_report = analyzer.detect_drift(
            current_metrics=current_metrics,
            threshold=0.05,
            metric_direction={
                'accuracy': 'higher',
                'precision': 'higher',
                'recall': 'higher',
                'f1': 'higher'
            }
        )

        print(f"    Drift Detected: {drift_report.detected}")
        print(f"    Severity: {drift_report.severity}")

        if drift_report.details.get('degraded_metrics'):
            degraded = drift_report.details['degraded_metrics']
            print(f"    Degraded Metrics: {', '.join(degraded)}")

        if period == 3:  # Show recommendations at period 3
            print(f"\n    Recommendations:")
            for rec in drift_report.recommendations[:3]:
                print(f"      - {rec}")

    return analyzer


def example_evaluation_scheduler():
    """Example 4: Automated evaluation scheduling"""
    print("\n" + "=" * 70)
    print("Example 4: Automated Evaluation Scheduling")
    print("=" * 70)

    # Create scheduler
    scheduler = EvaluationScheduler()

    # Define evaluation tasks
    def hourly_evaluation():
        """Hourly model evaluation"""
        print(f"  [{ datetime.now().strftime('%H:%M:%S')}] Running hourly evaluation...")
        predictions = create_mock_predictions(n_samples=100)
        metrics = calculate_metrics(predictions)
        print(f"  Accuracy: {metrics['accuracy']:.3f}")
        return metrics

    def daily_drift_check():
        """Daily drift detection"""
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] Running daily drift check...")
        print(f"  Drift status: OK")
        return {'drift_detected': False}

    def weekly_report():
        """Weekly performance report"""
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] Generating weekly report...")
        print(f"  Report generated successfully")
        return {'report_generated': True}

    # Schedule tasks
    print("\n📅 Scheduling Tasks:")

    # Note: Using short intervals for demo purposes
    scheduler.schedule_interval_task(
        task_id="hourly_eval",
        name="Hourly Model Evaluation",
        function=hourly_evaluation,
        interval_seconds=5,  # Demo: 5 seconds (in production: hours(1))
        metadata={'description': 'Regular model evaluation'}
    )
    print("  ✓ Scheduled: Hourly evaluation (every 5s for demo)")

    scheduler.schedule_interval_task(
        task_id="drift_check",
        name="Daily Drift Check",
        function=daily_drift_check,
        interval_seconds=10,  # Demo: 10 seconds (in production: days(1))
        metadata={'description': 'Daily drift detection'}
    )
    print("  ✓ Scheduled: Daily drift check (every 10s for demo)")

    scheduler.schedule_once(
        task_id="weekly_report",
        name="Weekly Performance Report",
        function=weekly_report,
        scheduled_time=datetime.now() + timedelta(seconds=8),  # Demo: 8 seconds from now
        metadata={'description': 'Weekly summary report'}
    )
    print("  ✓ Scheduled: Weekly report (8s from now)")

    # Start scheduler
    print("\n▶️ Starting scheduler...")
    scheduler.start(check_interval=1.0)

    # List tasks
    print("\n📋 Scheduled Tasks:")
    for task_info in scheduler.list_tasks():
        print(f"  - {task_info['name']}")
        print(f"    Status: {'Enabled' if task_info['enabled'] else 'Disabled'}")
        print(f"    Interval: {task_info.get('interval_seconds', 'N/A')}s")
        print(f"    Run Count: {task_info['run_count']}")

    # Run for 15 seconds
    print("\n⏳ Running scheduler for 15 seconds...")
    print("=" * 70)
    time.sleep(15)
    print("=" * 70)

    # Stop scheduler
    print("\n⏹️ Stopping scheduler...")
    scheduler.stop()

    # Get stats
    stats = scheduler.get_stats()
    print(f"\n📊 Scheduler Statistics:")
    print(f"  Total Tasks: {stats['total_tasks']}")
    print(f"  Enabled Tasks: {stats['enabled_tasks']}")
    print(f"  Total Runs: {stats['total_runs']}")

    return scheduler


def example_alert_management():
    """Example 5: Alert management"""
    print("\n" + "=" * 70)
    print("Example 5: Alert Management")
    print("=" * 70)

    # Create alert manager
    alert_manager = AlertManager()

    # Define alert rules
    print("\n📋 Defining Alert Rules:")

    # Accuracy threshold rule
    accuracy_rule = create_threshold_rule(
        rule_id="accuracy_low",
        name="Low Accuracy Alert",
        metric_key="accuracy",
        threshold=0.85,
        operator='<',
        severity=AlertSeverity.WARNING,
        channels=[AlertChannel.LOG]
    )
    alert_manager.add_rule(accuracy_rule)
    print("  ✓ Added: Low accuracy threshold rule (<0.85)")

    # Critical accuracy rule
    critical_rule = create_threshold_rule(
        rule_id="accuracy_critical",
        name="Critical Accuracy Drop",
        metric_key="accuracy",
        threshold=0.75,
        operator='<',
        severity=AlertSeverity.CRITICAL,
        channels=[AlertChannel.LOG]
    )
    alert_manager.add_rule(critical_rule)
    print("  ✓ Added: Critical accuracy rule (<0.75)")

    # Drift detection rule
    drift_rule = create_drift_rule(
        rule_id="drift_detected",
        name="Data/Model Drift Detected",
        severity=AlertSeverity.ERROR,
        channels=[AlertChannel.LOG]
    )
    alert_manager.add_rule(drift_rule)
    print("  ✓ Added: Drift detection rule")

    # Simulate evaluation results
    print("\n⚡ Simulating Evaluation Results:")

    test_scenarios = [
        {'accuracy': 0.92, 'description': 'Normal performance'},
        {'accuracy': 0.88, 'description': 'Good performance'},
        {'accuracy': 0.82, 'description': 'Degraded performance'},  # Triggers warning
        {'accuracy': 0.90, 'description': 'Recovered performance'},
        {'accuracy': 0.72, 'description': 'Critical degradation'},  # Triggers critical
    ]

    for scenario in test_scenarios:
        print(f"\n  Scenario: {scenario['description']} (accuracy={scenario['accuracy']:.3f})")

        # Evaluate rules
        alerts = alert_manager.evaluate_rules(scenario, source="evaluation_system")

        if alerts:
            for alert in alerts:
                print(f"    🚨 ALERT: {alert.title} [{alert.severity.value.upper()}]")
        else:
            print(f"    ✓ No alerts triggered")

    # Show alert statistics
    print("\n📊 Alert Statistics:")
    stats = alert_manager.get_stats()

    print(f"  Total Alerts: {stats['total_alerts']}")
    print(f"  Active Alerts: {stats['active_alerts']}")
    print(f"  Acknowledged: {stats['acknowledged_alerts']}")
    print(f"\n  By Severity:")
    for severity, count in stats['severity_counts'].items():
        if count > 0:
            print(f"    {severity}: {count}")

    # Show active alerts
    print(f"\n🔔 Active Alerts:")
    active = alert_manager.get_active_alerts()

    for alert in active:
        print(f"  [{alert.severity.value.upper()}] {alert.title}")
        print(f"    Time: {alert.timestamp.strftime('%H:%M:%S')}")
        print(f"    Source: {alert.source}")

    # Acknowledge an alert
    if active:
        alert_to_ack = active[0]
        alert_manager.acknowledge_alert(alert_to_ack.alert_id, acknowledged_by="admin")
        print(f"\n✓ Acknowledged alert: {alert_to_ack.title}")

    return alert_manager


def example_integrated_workflow():
    """Example 6: Integrated continuous evaluation workflow"""
    print("\n" + "=" * 70)
    print("Example 6: Integrated Continuous Evaluation Workflow")
    print("=" * 70)

    print("\nScenario: Production ML model with continuous monitoring")

    # 1. Setup monitoring
    print("\n📊 Step 1: Setup Continuous Monitoring")
    monitor = ContinuousMonitor(
        model_name="production_model",
        metrics=['accuracy', 'precision', 'recall'],
        window_size=100,
        alert_rules={
            'accuracy': {'threshold': 0.85, 'direction': 'below'}
        }
    )
    print(f"  ✓ Monitor initialized for {monitor.model_name}")

    # 2. Setup drift detection
    print("\n🔍 Step 2: Setup Drift Detection")
    baseline_metrics = {'accuracy': 0.92, 'precision': 0.90, 'recall': 0.91}
    drift_detector = DriftDetector(baseline_metrics)
    print(f"  ✓ Drift detector configured with baseline")

    # 3. Setup alerting
    print("\n🚨 Step 3: Setup Alerting")
    alert_manager = AlertManager()

    alert_manager.add_rule(create_threshold_rule(
        rule_id="perf_degradation",
        name="Performance Degradation",
        metric_key="accuracy",
        threshold=0.85,
        operator='<',
        severity=AlertSeverity.WARNING
    ))
    print(f"  ✓ Alert rules configured")

    # 4. Simulate production evaluation loop
    print("\n🔄 Step 4: Running Production Evaluation Loop")
    print("  (Simulating 10 evaluation cycles)")

    for cycle in range(10):
        # Generate predictions
        accuracy = 0.92 - (cycle * 0.02)  # Gradual degradation
        predictions = create_mock_predictions(n_samples=50, accuracy=accuracy)
        metrics = calculate_metrics(predictions)

        # Update monitoring
        monitor.record_metrics(metrics)

        # Check for drift
        drift_reports = drift_detector.detect_all_drift(current_metrics=metrics)

        # Evaluate alert rules
        alerts = alert_manager.evaluate_rules(metrics, source="production")

        # Log summary
        if cycle % 3 == 0:
            print(f"\n  Cycle {cycle}:")
            print(f"    Accuracy: {metrics['accuracy']:.3f}")
            if drift_reports.get('model') and drift_reports['model'].detected:
                print(f"    ⚠️ Model drift detected ({drift_reports['model'].severity})")
            if alerts:
                print(f"    🚨 {len(alerts)} alert(s) triggered")

    # 5. Generate summary report
    print("\n📋 Step 5: Generate Summary Report")
    report = monitor.generate_report()

    print(f"\n  Monitoring Period: {(report.end_time - report.start_time).total_seconds():.1f}s")
    print(f"  Total Snapshots: {report.total_snapshots}")
    print(f"  Anomalies Detected: {len(report.anomalies)}")

    print(f"\n  Metric Trends:")
    for metric, trend in report.trends.items():
        print(f"    {metric}: {trend}")

    alert_stats = alert_manager.get_stats()
    print(f"\n  Alert Summary:")
    print(f"    Total Alerts: {alert_stats['total_alerts']}")
    print(f"    Active Alerts: {alert_stats['active_alerts']}")

    print("\n✅ Integrated workflow completed")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("AEVA Continuous Evaluation Examples")
    print("=" * 70)

    # Run examples
    example_continuous_monitoring()
    example_data_drift_detection()
    example_model_drift_detection()
    example_evaluation_scheduler()
    example_alert_management()
    example_integrated_workflow()

    print("\n" + "=" * 70)
    print("All Examples Completed!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Real-time performance monitoring")
    print("  ✓ Statistical anomaly detection")
    print("  ✓ Data drift detection (PSI, KL divergence)")
    print("  ✓ Model performance drift detection")
    print("  ✓ Automated evaluation scheduling")
    print("  ✓ Alert management with rules and severity")
    print("  ✓ Integrated continuous evaluation workflow")


if __name__ == '__main__':
    main()
