"""
Pipeline Celery Tasks

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import httpx
from uuid import UUID
from typing import Dict, Any

from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.core.config import settings
from app.models.pipeline import PipelineStatus, StepStatus
from app.services.pipeline_service import PipelineService


@celery_app.task(bind=True, max_retries=3)
def execute_pipeline(self, pipeline_id: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Execute a pipeline asynchronously.

    Args:
        pipeline_id: UUID of the pipeline to execute
        metadata: Optional execution metadata

    Returns:
        Execution results
    """
    db = SessionLocal()
    try:
        pipeline_uuid = UUID(pipeline_id)

        # Update pipeline status to running
        PipelineService.update_pipeline_status(
            db, pipeline_uuid, PipelineStatus.RUNNING
        )

        # Get pipeline steps
        steps = PipelineService.get_pipeline_steps(db, pipeline_uuid)

        results = {}

        # Execute each step in order
        for step in steps:
            try:
                # Execute step based on type
                if step.step_type == "benchmark":
                    step_result = execute_benchmark_step(step.config)
                elif step.step_type == "validate":
                    step_result = execute_validation_step(step.config, results.get("benchmark"))
                elif step.step_type == "analyze":
                    step_result = execute_analysis_step(step.config, results)
                else:
                    raise ValueError(f"Unknown step type: {step.step_type}")

                # Update step status
                PipelineService.update_step_status(
                    db,
                    step.id,
                    StepStatus.COMPLETED,
                    results=step_result
                )

                results[step.step_type] = step_result

                # Check if step resulted in blocking
                if step.step_type == "validate" and step_result.get("blocked"):
                    # Pipeline is blocked
                    PipelineService.update_pipeline_status(
                        db,
                        pipeline_uuid,
                        PipelineStatus.BLOCKED,
                        results=results
                    )
                    return {
                        "status": "blocked",
                        "message": "Pipeline blocked by quality gate",
                        "results": results
                    }

            except Exception as step_error:
                # Update step status to failed
                PipelineService.update_step_status(
                    db,
                    step.id,
                    StepStatus.FAILED,
                    error_message=str(step_error)
                )

                # Mark pipeline as failed
                PipelineService.update_pipeline_status(
                    db,
                    pipeline_uuid,
                    PipelineStatus.FAILED,
                    error_message=f"Step '{step.name}' failed: {str(step_error)}",
                    results=results
                )

                raise

        # Mark pipeline as completed
        PipelineService.update_pipeline_status(
            db,
            pipeline_uuid,
            PipelineStatus.COMPLETED,
            results=results
        )

        return {
            "status": "completed",
            "message": "Pipeline executed successfully",
            "results": results
        }

    except Exception as e:
        # Retry logic
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=settings.RETRY_DELAY)

        # Final failure
        PipelineService.update_pipeline_status(
            db,
            UUID(pipeline_id),
            PipelineStatus.FAILED,
            error_message=str(e)
        )

        return {
            "status": "failed",
            "message": f"Pipeline execution failed: {str(e)}"
        }

    finally:
        db.close()


def execute_benchmark_step(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute benchmark step by calling Bench Service.

    Args:
        config: Step configuration

    Returns:
        Benchmark results
    """
    benchmark_id = config.get("benchmark_id")
    if not benchmark_id:
        raise ValueError("benchmark_id is required for benchmark step")

    # Call Bench Service
    with httpx.Client(timeout=settings.DEFAULT_TIMEOUT) as client:
        response = client.post(
            f"{settings.BENCH_SERVICE_URL}/v1/benchmark/{benchmark_id}/run"
        )
        response.raise_for_status()
        return response.json()


def execute_validation_step(
    config: Dict[str, Any],
    benchmark_results: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Execute validation step by calling Guard Service.

    Args:
        config: Step configuration
        benchmark_results: Results from benchmark step

    Returns:
        Validation results
    """
    gate_id = config.get("gate_id")
    if not gate_id:
        raise ValueError("gate_id is required for validation step")

    # Extract metrics from benchmark results
    metrics = {}
    if benchmark_results and "result" in benchmark_results:
        result_data = benchmark_results["result"]
        if "accuracy" in result_data:
            metrics["accuracy"] = result_data["accuracy"]
        if "f1_score" in result_data:
            metrics["f1_score"] = result_data["f1_score"]
        if "precision" in result_data:
            metrics["precision"] = result_data["precision"]
        if "recall" in result_data:
            metrics["recall"] = result_data["recall"]

    # Call Guard Service
    with httpx.Client(timeout=settings.DEFAULT_TIMEOUT) as client:
        response = client.post(
            f"{settings.GUARD_SERVICE_URL}/v1/gate/{gate_id}/validate",
            json={
                "metrics": metrics,
                "metadata": config.get("metadata", {})
            }
        )
        response.raise_for_status()
        return response.json()


def execute_analysis_step(
    config: Dict[str, Any],
    previous_results: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Execute analysis step by calling Brain Service.

    Args:
        config: Step configuration
        previous_results: Results from previous steps

    Returns:
        Analysis results
    """
    analysis_type = config.get("analysis_type", "basic")

    # Call Brain Service
    with httpx.Client(timeout=settings.DEFAULT_TIMEOUT) as client:
        response = client.post(
            f"{settings.BRAIN_SERVICE_URL}/v1/analysis",
            json={
                "analysis_type": analysis_type,
                "data": previous_results,
                "config": config
            }
        )
        response.raise_for_status()
        return response.json()
