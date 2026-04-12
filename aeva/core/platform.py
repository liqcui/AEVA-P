"""
AEVA Platform - Main orchestration class
"""

from typing import Optional, Dict, Any, List
import logging
from pathlib import Path

from aeva.core.config import AEVAConfig
from aeva.core.pipeline import Pipeline
from aeva.core.result import EvaluationResult

logger = logging.getLogger(__name__)


class AEVA:
    """
    Main AEVA Platform class

    Orchestrates all four subsystems:
    - AEVA-Guard: Quality gates
    - AEVA-Bench: Benchmarking
    - AEVA-Auto: Automation
    - AEVA-Brain: Intelligent analysis
    """

    def __init__(
        self,
        config: Optional[AEVAConfig] = None,
        config_path: Optional[str] = None
    ):
        """
        Initialize AEVA platform

        Args:
            config: AEVAConfig object
            config_path: Path to YAML configuration file
        """
        if config is None:
            if config_path:
                self.config = AEVAConfig.from_yaml(config_path)
            else:
                # Try to load from environment or use defaults
                try:
                    self.config = AEVAConfig.from_env()
                except Exception:
                    self.config = AEVAConfig()
        else:
            self.config = config

        self._setup_logging()
        self._initialize_components()

        logger.info(f"AEVA Platform v{self.config.version} initialized")

    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def _initialize_components(self) -> None:
        """Initialize all AEVA components"""
        from aeva.guard import GuardManager
        from aeva.bench import BenchmarkManager
        from aeva.auto import AutomationManager
        from aeva.brain import BrainManager

        self.guard = GuardManager(self.config.guard)
        self.bench = BenchmarkManager(self.config.bench)
        self.auto = AutomationManager(self.config.auto)
        self.brain = BrainManager(self.config.brain)

        logger.info("All AEVA components initialized")

    def run(
        self,
        pipeline: Pipeline,
        algorithm: Optional[Any] = None,
        **kwargs
    ) -> EvaluationResult:
        """
        Execute an evaluation pipeline

        Args:
            pipeline: Pipeline to execute
            algorithm: Algorithm to evaluate (optional)
            **kwargs: Additional parameters

        Returns:
            EvaluationResult object
        """
        logger.info(f"Starting pipeline execution: {pipeline.name}")

        try:
            # Execute pipeline through automation manager
            result = self.auto.execute_pipeline(
                pipeline=pipeline,
                algorithm=algorithm,
                **kwargs
            )

            # Apply quality gates
            if self.config.guard.enabled:
                gate_result = self.guard.validate(result)
                result.set_gate_result(gate_result)

            # Run intelligent analysis if enabled
            if result.should_analyze():
                analysis = self.brain.analyze(result)
                result.set_analysis(analysis)

            logger.info(f"Pipeline execution completed: {pipeline.name}")
            return result

        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            raise

    async def run_async(
        self,
        pipeline: Pipeline,
        algorithm: Optional[Any] = None,
        **kwargs
    ) -> EvaluationResult:
        """
        Execute an evaluation pipeline asynchronously

        Args:
            pipeline: Pipeline to execute
            algorithm: Algorithm to evaluate (optional)
            **kwargs: Additional parameters

        Returns:
            EvaluationResult object
        """
        logger.info(f"Starting async pipeline execution: {pipeline.name}")

        # Async implementation
        result = await self.auto.execute_pipeline_async(
            pipeline=pipeline,
            algorithm=algorithm,
            **kwargs
        )

        if self.config.guard.enabled:
            gate_result = await self.guard.validate_async(result)
            result.set_gate_result(gate_result)

        if result.should_analyze():
            analysis = await self.brain.analyze_async(result)
            result.set_analysis(analysis)

        logger.info(f"Async pipeline execution completed: {pipeline.name}")
        return result

    def create_pipeline(self, name: str) -> Pipeline:
        """Create a new pipeline"""
        return Pipeline(name=name)

    def get_status(self) -> Dict[str, Any]:
        """Get platform status"""
        return {
            "version": self.config.version,
            "components": {
                "guard": self.guard.get_status(),
                "bench": self.bench.get_status(),
                "auto": self.auto.get_status(),
                "brain": self.brain.get_status(),
            },
            "config": {
                "debug": self.config.debug,
                "log_level": self.config.log_level,
            }
        }

    def shutdown(self) -> None:
        """Gracefully shutdown AEVA platform"""
        logger.info("Shutting down AEVA platform")

        self.auto.shutdown()
        self.brain.shutdown()

        logger.info("AEVA platform shutdown complete")
