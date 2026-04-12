"""
AEVA-Auto Pipeline Executor
Executes pipeline stages with retry and error handling

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, List
import logging
import time

from aeva.core.config import AutoConfig
from aeva.core.pipeline import Pipeline, StageResult

logger = logging.getLogger(__name__)


class PipelineExecutor:
    """
    Executes pipeline stages with advanced features:
    - Retry logic
    - Timeout handling
    - Error recovery
    - Performance tracking
    """

    def __init__(self, config: AutoConfig):
        self.config = config

    def execute(self, pipeline: Pipeline, context: Dict[str, Any]) -> List[StageResult]:
        """
        Execute pipeline stages synchronously

        Args:
            pipeline: Pipeline to execute
            context: Execution context

        Returns:
            List of StageResult objects
        """
        logger.info(f"Executing pipeline: {pipeline.name}")

        results = []

        for stage in pipeline.stages:
            logger.info(f"Executing stage: {stage.name}")

            # Execute stage with retry logic
            result = self._execute_stage_with_retry(stage, context)
            results.append(result)

            # Update context with stage results
            context[f"{stage.name}_result"] = result.data

            # Stop on critical failure
            if not result.success:
                logger.error(f"Stage {stage.name} failed, checking if critical")
                if self._is_critical_failure(stage, result):
                    logger.error("Critical failure detected, stopping pipeline")
                    break

        return results

    async def execute_async(
        self,
        pipeline: Pipeline,
        context: Dict[str, Any]
    ) -> List[StageResult]:
        """
        Execute pipeline stages asynchronously

        Args:
            pipeline: Pipeline to execute
            context: Execution context

        Returns:
            List of StageResult objects
        """
        logger.info(f"Executing pipeline asynchronously: {pipeline.name}")

        results = []

        for stage in pipeline.stages:
            logger.info(f"Executing stage: {stage.name}")

            result = await self._execute_stage_async_with_retry(stage, context)
            results.append(result)

            context[f"{stage.name}_result"] = result.data

            if not result.success and self._is_critical_failure(stage, result):
                logger.error("Critical failure detected, stopping pipeline")
                break

        return results

    def _execute_stage_with_retry(
        self,
        stage: Any,
        context: Dict[str, Any]
    ) -> StageResult:
        """Execute a stage with retry logic"""
        last_error = None
        retry_count = 0

        while retry_count <= self.config.retry_limit:
            try:
                # Execute stage with timeout
                result = self._execute_with_timeout(stage, context)
                return result

            except TimeoutError as e:
                last_error = f"Stage execution timed out: {str(e)}"
                logger.warning(f"Stage {stage.name} timed out (attempt {retry_count + 1})")
                retry_count += 1

            except Exception as e:
                last_error = str(e)
                logger.error(f"Stage {stage.name} failed (attempt {retry_count + 1}): {e}")
                retry_count += 1

            # Wait before retry (exponential backoff)
            if retry_count <= self.config.retry_limit:
                wait_time = min(2 ** retry_count, 60)  # Max 60 seconds
                logger.info(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)

        # All retries failed
        logger.error(f"Stage {stage.name} failed after {retry_count} attempts")
        return StageResult(
            stage_name=stage.name,
            stage_type=stage.stage_type,
            success=False,
            error=last_error or "Unknown error",
        )

    async def _execute_stage_async_with_retry(
        self,
        stage: Any,
        context: Dict[str, Any]
    ) -> StageResult:
        """Execute a stage asynchronously with retry logic"""
        import asyncio

        last_error = None
        retry_count = 0

        while retry_count <= self.config.retry_limit:
            try:
                result = await stage.execute_async(context)
                return result

            except asyncio.TimeoutError as e:
                last_error = f"Stage execution timed out: {str(e)}"
                logger.warning(f"Stage {stage.name} timed out (attempt {retry_count + 1})")
                retry_count += 1

            except Exception as e:
                last_error = str(e)
                logger.error(f"Stage {stage.name} failed (attempt {retry_count + 1}): {e}")
                retry_count += 1

            if retry_count <= self.config.retry_limit:
                wait_time = min(2 ** retry_count, 60)
                logger.info(f"Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)

        logger.error(f"Stage {stage.name} failed after {retry_count} attempts")
        return StageResult(
            stage_name=stage.name,
            stage_type=stage.stage_type,
            success=False,
            error=last_error or "Unknown error",
        )

    def _execute_with_timeout(
        self,
        stage: Any,
        context: Dict[str, Any]
    ) -> StageResult:
        """Execute stage with timeout"""
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError(f"Stage execution exceeded {self.config.task_timeout}s")

        # Set timeout alarm (Unix only)
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.config.task_timeout)

            result = stage.execute(context)

            signal.alarm(0)  # Cancel alarm
            return result

        except AttributeError:
            # Windows doesn't support signal.SIGALRM
            # Fall back to simple execution
            return stage.execute(context)

    def _is_critical_failure(self, stage: Any, result: StageResult) -> bool:
        """Determine if a stage failure is critical"""
        # Stage types that are critical
        from aeva.core.pipeline import StageType

        critical_types = [StageType.GUARD]

        return stage.stage_type in critical_types
