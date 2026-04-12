"""
AEVA-Auto Manager
Manages automation pipelines and execution

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, Optional
import logging
import time

from aeva.core.config import AutoConfig
from aeva.core.pipeline import Pipeline
from aeva.core.result import EvaluationResult, ResultStatus
from aeva.auto.executor import PipelineExecutor

logger = logging.getLogger(__name__)


class AutomationManager:
    """
    Manages automation of evaluation pipelines

    Responsibilities:
    - Execute evaluation pipelines
    - Manage distributed execution
    - Handle task scheduling
    - Coordinate worker processes
    """

    def __init__(self, config: AutoConfig):
        self.config = config
        self.executor = PipelineExecutor(config)
        self._active_tasks: Dict[str, Any] = {}

    def execute_pipeline(
        self,
        pipeline: Pipeline,
        algorithm: Optional[Any] = None,
        **kwargs
    ) -> EvaluationResult:
        """
        Execute a pipeline synchronously

        Args:
            pipeline: Pipeline to execute
            algorithm: Algorithm to evaluate
            **kwargs: Additional parameters

        Returns:
            EvaluationResult object
        """
        logger.info(f"Executing pipeline: {pipeline.name}")

        start_time = time.time()

        # Create initial context
        context = {
            "algorithm": algorithm,
            **kwargs
        }

        # Create result object
        result = EvaluationResult(
            pipeline_name=pipeline.name,
            algorithm_name=str(algorithm) if algorithm else "unknown"
        )

        try:
            # Execute pipeline stages
            stage_results = self.executor.execute(pipeline, context)
            result.stage_results = stage_results

            # Extract metrics from stage results
            self._extract_metrics(result, stage_results)

            # Set overall status
            if all(sr.success for sr in stage_results):
                result.set_status(ResultStatus.PASSED)
            else:
                result.set_status(ResultStatus.FAILED)

                # Add errors from failed stages
                for sr in stage_results:
                    if not sr.success and sr.error:
                        result.add_error(f"Stage '{sr.stage_name}': {sr.error}")

        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            result.set_status(ResultStatus.FAILED)
            result.add_error(str(e))

        result.duration = time.time() - start_time
        logger.info(f"Pipeline execution completed in {result.duration:.2f}s")

        return result

    async def execute_pipeline_async(
        self,
        pipeline: Pipeline,
        algorithm: Optional[Any] = None,
        **kwargs
    ) -> EvaluationResult:
        """
        Execute a pipeline asynchronously

        Args:
            pipeline: Pipeline to execute
            algorithm: Algorithm to evaluate
            **kwargs: Additional parameters

        Returns:
            EvaluationResult object
        """
        logger.info(f"Executing pipeline asynchronously: {pipeline.name}")

        start_time = time.time()

        context = {
            "algorithm": algorithm,
            **kwargs
        }

        result = EvaluationResult(
            pipeline_name=pipeline.name,
            algorithm_name=str(algorithm) if algorithm else "unknown"
        )

        try:
            stage_results = await self.executor.execute_async(pipeline, context)
            result.stage_results = stage_results

            self._extract_metrics(result, stage_results)

            if all(sr.success for sr in stage_results):
                result.set_status(ResultStatus.PASSED)
            else:
                result.set_status(ResultStatus.FAILED)

                for sr in stage_results:
                    if not sr.success and sr.error:
                        result.add_error(f"Stage '{sr.stage_name}': {sr.error}")

        except Exception as e:
            logger.error(f"Async pipeline execution failed: {e}")
            result.set_status(ResultStatus.FAILED)
            result.add_error(str(e))

        result.duration = time.time() - start_time
        logger.info(f"Async pipeline execution completed in {result.duration:.2f}s")

        return result

    def _extract_metrics(self, result: EvaluationResult, stage_results: list) -> None:
        """Extract metrics from stage results and add to evaluation result"""
        for stage_result in stage_results:
            if not stage_result.success:
                continue

            # Extract metric data from stage result
            data = stage_result.data

            # Look for common metric patterns
            if "metrics" in data:
                for metric_name, metric_value in data["metrics"].items():
                    if isinstance(metric_value, (int, float)):
                        result.add_metric(
                            name=metric_name,
                            value=float(metric_value)
                        )

            # Look for direct metric values
            for key, value in data.items():
                if isinstance(value, (int, float)) and key not in ["duration", "timestamp"]:
                    result.add_metric(name=key, value=float(value))

    def submit_task(
        self,
        pipeline: Pipeline,
        algorithm: Optional[Any] = None,
        **kwargs
    ) -> str:
        """
        Submit a task for asynchronous execution

        Args:
            pipeline: Pipeline to execute
            algorithm: Algorithm to evaluate
            **kwargs: Additional parameters

        Returns:
            Task ID for tracking
        """
        import uuid

        task_id = str(uuid.uuid4())

        task_info = {
            "id": task_id,
            "pipeline": pipeline,
            "algorithm": algorithm,
            "kwargs": kwargs,
            "status": "pending",
            "created_at": time.time(),
        }

        self._active_tasks[task_id] = task_info

        logger.info(f"Submitted task {task_id} for pipeline: {pipeline.name}")

        # In a real implementation, this would submit to a task queue
        # For now, we'll just track it

        return task_id

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a submitted task"""
        return self._active_tasks.get(task_id)

    def get_status(self) -> Dict[str, Any]:
        """Get automation manager status"""
        return {
            "worker_concurrency": self.config.worker_concurrency,
            "active_tasks": len(self._active_tasks),
            "task_timeout": self.config.task_timeout,
            "retry_limit": self.config.retry_limit,
        }

    def shutdown(self) -> None:
        """Shutdown automation manager"""
        logger.info("Shutting down AutomationManager")

        # Wait for active tasks to complete or timeout
        # In production, this would gracefully shutdown workers

        self._active_tasks.clear()
        logger.info("AutomationManager shutdown complete")
