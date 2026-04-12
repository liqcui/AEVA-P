"""
Tests for AEVA-Guard module
"""

import pytest
from aeva.core.config import GuardConfig
from aeva.core.result import EvaluationResult
from aeva.guard import GuardManager, ThresholdGate, MultiMetricGate


def test_guard_manager_initialization():
    """Test GuardManager initialization"""
    config = GuardConfig(enabled=True, default_threshold=0.85)
    manager = GuardManager(config)

    assert manager is not None
    assert manager.config.enabled is True
    assert manager.config.default_threshold == 0.85


def test_threshold_gate():
    """Test ThresholdGate validation"""
    gate = ThresholdGate(
        name="accuracy_gate",
        threshold=0.90,
        metric_name="accuracy"
    )

    # Create result with passing metric
    result = EvaluationResult("test", "test")
    result.add_metric("accuracy", 0.95)

    gate_result = gate.evaluate(result)

    assert gate_result.passed is True
    assert gate_result.score == 0.95

    # Create result with failing metric
    result2 = EvaluationResult("test", "test")
    result2.add_metric("accuracy", 0.85)

    gate_result2 = gate.evaluate(result2)

    assert gate_result2.passed is False
    assert gate_result2.reason is not None


def test_multi_metric_gate():
    """Test MultiMetricGate validation"""
    gate = MultiMetricGate(
        name="combined_gate",
        metric_thresholds={
            "accuracy": 0.90,
            "precision": 0.85,
            "recall": 0.85
        }
    )

    # All metrics pass
    result = EvaluationResult("test", "test")
    result.add_metric("accuracy", 0.92)
    result.add_metric("precision", 0.88)
    result.add_metric("recall", 0.90)

    gate_result = gate.evaluate(result)
    assert gate_result.passed is True

    # One metric fails
    result2 = EvaluationResult("test", "test")
    result2.add_metric("accuracy", 0.92)
    result2.add_metric("precision", 0.80)  # Below threshold
    result2.add_metric("recall", 0.90)

    gate_result2 = gate.evaluate(result2)
    assert gate_result2.passed is False


def test_guard_manager_validation():
    """Test GuardManager validation"""
    config = GuardConfig(enabled=True)
    manager = GuardManager(config)

    # Add gate
    gate = ThresholdGate("test_gate", 0.90, "accuracy")
    manager.add_gate(gate)

    # Create result
    result = EvaluationResult("test", "test")
    result.add_metric("accuracy", 0.95)

    # Validate
    gate_result = manager.validate(result)

    assert gate_result is not None
    assert gate_result.passed is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
