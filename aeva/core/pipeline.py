"""
AEVA Pipeline - Evaluation workflow orchestration

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import List, Optional, Dict, Any, Callable
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class StageType(Enum):
    """Pipeline stage types"""
    BENCHMARK = "benchmark"
    GUARD = "guard"
    ANALYSIS = "analysis"
    CUSTOM = "custom"


@dataclass
class StageResult:
    """Result from a pipeline stage"""
    stage_name: str
    stage_type: StageType
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration: float = 0.0


class Stage(ABC):
    """Abstract base class for pipeline stages"""

    def __init__(self, name: str, stage_type: StageType = StageType.CUSTOM):
        self.name = name
        self.stage_type = stage_type

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> StageResult:
        """
        Execute the stage

        Args:
            context: Execution context containing data from previous stages

        Returns:
            StageResult object
        """
        pass

    async def execute_async(self, context: Dict[str, Any]) -> StageResult:
        """
        Execute the stage asynchronously

        Default implementation calls synchronous execute
        Override for true async behavior
        """
        return self.execute(context)

    def validate(self, context: Dict[str, Any]) -> bool:
        """
        Validate stage can execute with given context

        Args:
            context: Execution context

        Returns:
            True if valid, False otherwise
        """
        return True


class FunctionStage(Stage):
    """Stage that wraps a custom function"""

    def __init__(
        self,
        name: str,
        function: Callable[[Dict[str, Any]], Dict[str, Any]],
        stage_type: StageType = StageType.CUSTOM
    ):
        super().__init__(name, stage_type)
        self.function = function

    def execute(self, context: Dict[str, Any]) -> StageResult:
        """Execute the wrapped function"""
        import time

        start_time = time.time()

        try:
            result_data = self.function(context)
            duration = time.time() - start_time

            return StageResult(
                stage_name=self.name,
                stage_type=self.stage_type,
                success=True,
                data=result_data,
                duration=duration
            )
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Stage {self.name} failed: {str(e)}")

            return StageResult(
                stage_name=self.name,
                stage_type=self.stage_type,
                success=False,
                error=str(e),
                duration=duration
            )


class Pipeline:
    """
    Evaluation pipeline that orchestrates multiple stages
    """

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.stages: List[Stage] = []
        self._context: Dict[str, Any] = {}

    def add_stage(self, stage: Stage) -> "Pipeline":
        """
        Add a stage to the pipeline

        Args:
            stage: Stage to add

        Returns:
            Self for chaining
        """
        self.stages.append(stage)
        logger.info(f"Added stage '{stage.name}' to pipeline '{self.name}'")
        return self

    def add_function(
        self,
        name: str,
        function: Callable[[Dict[str, Any]], Dict[str, Any]],
        stage_type: StageType = StageType.CUSTOM
    ) -> "Pipeline":
        """
        Add a function as a stage

        Args:
            name: Stage name
            function: Function to execute
            stage_type: Type of stage

        Returns:
            Self for chaining
        """
        stage = FunctionStage(name, function, stage_type)
        return self.add_stage(stage)

    def set_context(self, key: str, value: Any) -> "Pipeline":
        """
        Set a context variable

        Args:
            key: Context key
            value: Context value

        Returns:
            Self for chaining
        """
        self._context[key] = value
        return self

    def get_context(self) -> Dict[str, Any]:
        """Get the current context"""
        return self._context.copy()

    def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> List[StageResult]:
        """
        Execute the pipeline

        Args:
            initial_context: Initial context to merge with pipeline context

        Returns:
            List of StageResult objects
        """
        logger.info(f"Executing pipeline: {self.name}")

        # Merge contexts
        context = self._context.copy()
        if initial_context:
            context.update(initial_context)

        results = []

        for stage in self.stages:
            logger.info(f"Executing stage: {stage.name}")

            # Validate stage
            if not stage.validate(context):
                logger.warning(f"Stage {stage.name} validation failed, skipping")
                results.append(StageResult(
                    stage_name=stage.name,
                    stage_type=stage.stage_type,
                    success=False,
                    error="Stage validation failed"
                ))
                continue

            # Execute stage
            result = stage.execute(context)
            results.append(result)

            # Update context with stage results
            context[f"{stage.name}_result"] = result.data

            # Stop on failure if critical
            if not result.success and self._is_critical_stage(stage):
                logger.error(f"Critical stage {stage.name} failed, stopping pipeline")
                break

        logger.info(f"Pipeline execution completed: {self.name}")
        return results

    async def execute_async(
        self,
        initial_context: Optional[Dict[str, Any]] = None
    ) -> List[StageResult]:
        """
        Execute the pipeline asynchronously

        Args:
            initial_context: Initial context to merge with pipeline context

        Returns:
            List of StageResult objects
        """
        logger.info(f"Executing pipeline asynchronously: {self.name}")

        context = self._context.copy()
        if initial_context:
            context.update(initial_context)

        results = []

        for stage in self.stages:
            logger.info(f"Executing stage: {stage.name}")

            if not stage.validate(context):
                logger.warning(f"Stage {stage.name} validation failed, skipping")
                results.append(StageResult(
                    stage_name=stage.name,
                    stage_type=stage.stage_type,
                    success=False,
                    error="Stage validation failed"
                ))
                continue

            result = await stage.execute_async(context)
            results.append(result)

            context[f"{stage.name}_result"] = result.data

            if not result.success and self._is_critical_stage(stage):
                logger.error(f"Critical stage {stage.name} failed, stopping pipeline")
                break

        logger.info(f"Async pipeline execution completed: {self.name}")
        return results

    def _is_critical_stage(self, stage: Stage) -> bool:
        """Determine if a stage is critical (failure should stop pipeline)"""
        # By default, guard stages are critical
        return stage.stage_type == StageType.GUARD

    def __len__(self) -> int:
        """Return number of stages"""
        return len(self.stages)

    def __repr__(self) -> str:
        return f"Pipeline(name='{self.name}', stages={len(self.stages)})"
