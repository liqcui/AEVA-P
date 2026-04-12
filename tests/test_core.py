"""
Tests for AEVA core functionality
"""

import pytest
from aeva import AEVA, AEVAConfig
from aeva.core.pipeline import Pipeline, FunctionStage, StageType
from aeva.core.result import EvaluationResult, ResultStatus


def test_aeva_initialization():
    """Test AEVA platform initialization"""
    config = AEVAConfig()
    aeva = AEVA(config=config)

    assert aeva is not None
    assert aeva.config == config
    assert aeva.guard is not None
    assert aeva.bench is not None
    assert aeva.auto is not None
    assert aeva.brain is not None


def test_pipeline_creation():
    """Test pipeline creation"""
    config = AEVAConfig()
    aeva = AEVA(config=config)

    pipeline = aeva.create_pipeline(name="test_pipeline")

    assert pipeline is not None
    assert pipeline.name == "test_pipeline"
    assert len(pipeline.stages) == 0


def test_pipeline_execution():
    """Test basic pipeline execution"""
    config = AEVAConfig()
    aeva = AEVA(config=config)

    # Create simple pipeline
    pipeline = Pipeline(name="test")

    def simple_stage(context):
        return {"result": "success", "metrics": {"accuracy": 0.95}}

    pipeline.add_function("test_stage", simple_stage, StageType.BENCHMARK)

    # Execute pipeline
    result = aeva.run(pipeline)

    assert result is not None
    assert result.pipeline_name == "test"
    assert len(result.stage_results) > 0


def test_evaluation_result():
    """Test evaluation result creation"""
    result = EvaluationResult(
        pipeline_name="test_pipeline",
        algorithm_name="test_algorithm"
    )

    # Add metrics
    result.add_metric("accuracy", 0.95, threshold=0.90)
    result.add_metric("precision", 0.85, threshold=0.90)

    assert len(result.metrics) == 2
    assert result.metrics["accuracy"].passed is True
    assert result.metrics["precision"].passed is False

    # Check overall score
    score = result.get_overall_score()
    assert score == 0.5  # 1 passed / 2 total


def test_pipeline_stages():
    """Test pipeline with multiple stages"""
    pipeline = Pipeline(name="multi_stage")

    def stage1(context):
        return {"value": 10}

    def stage2(context):
        prev_value = context.get("stage1_result", {}).get("value", 0)
        return {"value": prev_value + 5}

    pipeline.add_function("stage1", stage1)
    pipeline.add_function("stage2", stage2)

    results = pipeline.execute()

    assert len(results) == 2
    assert results[0].success
    assert results[1].success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
