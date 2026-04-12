"""
AEVA-Brain Manager
Manages intelligent analysis and LLM integration

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, Optional
import logging

from aeva.core.config import BrainConfig
from aeva.core.result import EvaluationResult, Analysis
from aeva.brain.llm import LLMProvider, ClaudeProvider
from aeva.brain.analyzer import ResultAnalyzer

logger = logging.getLogger(__name__)


class BrainManager:
    """
    Manages intelligent analysis using LLM

    Responsibilities:
    - Analyze evaluation results
    - Identify root causes of failures
    - Generate recommendations
    - Learn from historical patterns
    """

    def __init__(self, config: BrainConfig):
        self.config = config
        self.llm_provider = self._initialize_llm_provider()
        self.analyzer = ResultAnalyzer(self.llm_provider)

    def _initialize_llm_provider(self) -> LLMProvider:
        """Initialize LLM provider based on configuration"""
        if self.config.provider == "anthropic":
            return ClaudeProvider(
                api_key=self.config.api_key,
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config.provider}")

    def analyze(self, result: EvaluationResult) -> Analysis:
        """
        Analyze evaluation result using LLM

        Args:
            result: Evaluation result to analyze

        Returns:
            Analysis object with insights and recommendations
        """
        logger.info(f"Analyzing result for pipeline: {result.pipeline_name}")

        try:
            analysis = self.analyzer.analyze(result)
            logger.info(f"Analysis completed with confidence: {analysis.confidence:.2%}")
            return analysis

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            # Return a basic analysis on error
            return Analysis(
                summary=f"Analysis failed: {str(e)}",
                severity="error",
                confidence=0.0
            )

    async def analyze_async(self, result: EvaluationResult) -> Analysis:
        """
        Analyze evaluation result asynchronously

        Args:
            result: Evaluation result to analyze

        Returns:
            Analysis object with insights and recommendations
        """
        logger.info(f"Analyzing result asynchronously for pipeline: {result.pipeline_name}")

        try:
            analysis = await self.analyzer.analyze_async(result)
            logger.info(f"Async analysis completed with confidence: {analysis.confidence:.2%}")
            return analysis

        except Exception as e:
            logger.error(f"Async analysis failed: {e}")
            return Analysis(
                summary=f"Analysis failed: {str(e)}",
                severity="error",
                confidence=0.0
            )

    def get_status(self) -> Dict[str, Any]:
        """Get brain manager status"""
        return {
            "provider": self.config.provider,
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
        }

    def shutdown(self) -> None:
        """Shutdown brain manager"""
        logger.info("Shutting down BrainManager")
        # Clean up resources if needed
        logger.info("BrainManager shutdown complete")
