"""
AEVA-Brain Result Analyzer
Analyzes evaluation results using LLM

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, List
import json
import logging

from aeva.core.result import EvaluationResult, Analysis
from aeva.brain.llm import LLMProvider

logger = logging.getLogger(__name__)


class ResultAnalyzer:
    """
    Analyzes evaluation results using LLM

    Uses prompt engineering to:
    - Identify root causes of failures
    - Generate actionable recommendations
    - Assess severity and confidence
    - Detect patterns and anomalies
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def analyze(self, result: EvaluationResult) -> Analysis:
        """
        Analyze evaluation result

        Args:
            result: Evaluation result to analyze

        Returns:
            Analysis object with insights
        """
        # Build analysis prompt
        prompt = self._build_analysis_prompt(result)

        # Get LLM analysis
        try:
            response = self.llm_provider.complete(prompt)
            analysis = self._parse_analysis_response(response)
            return analysis

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return Analysis(
                summary="Analysis failed due to LLM error",
                severity="error",
                confidence=0.0
            )

    async def analyze_async(self, result: EvaluationResult) -> Analysis:
        """
        Analyze evaluation result asynchronously

        Args:
            result: Evaluation result to analyze

        Returns:
            Analysis object with insights
        """
        prompt = self._build_analysis_prompt(result)

        try:
            response = await self.llm_provider.complete_async(prompt)
            analysis = self._parse_analysis_response(response)
            return analysis

        except Exception as e:
            logger.error(f"Async analysis failed: {e}")
            return Analysis(
                summary="Analysis failed due to LLM error",
                severity="error",
                confidence=0.0
            )

    def _build_analysis_prompt(self, result: EvaluationResult) -> str:
        """Build analysis prompt for LLM"""
        # Convert result to readable format
        result_summary = self._format_result_for_analysis(result)

        prompt = f"""You are an expert AI system for analyzing algorithm evaluation results.

Given the following evaluation result, provide a comprehensive analysis:

{result_summary}

Please provide your analysis in the following JSON format:
{{
    "summary": "A concise 1-2 sentence summary of the evaluation result",
    "root_causes": ["List of potential root causes for any failures or issues"],
    "recommendations": ["List of actionable recommendations to improve performance"],
    "severity": "One of: info, warning, error, critical",
    "confidence": 0.85  // Float between 0 and 1 indicating your confidence in this analysis
}}

Focus on:
1. Identifying specific issues with metrics or performance
2. Providing actionable, technical recommendations
3. Explaining the severity and impact of any problems
4. Being precise and data-driven in your analysis

Respond with ONLY the JSON object, no additional text."""

        return prompt

    def _format_result_for_analysis(self, result: EvaluationResult) -> str:
        """Format result into readable text for analysis"""
        lines = [
            f"Pipeline: {result.pipeline_name}",
            f"Algorithm: {result.algorithm_name}",
            f"Status: {result.status.value}",
            f"Duration: {result.duration:.2f}s",
            "",
            "Metrics:",
        ]

        for name, metric in result.metrics.items():
            status = "PASS" if metric.passed else "FAIL"
            threshold_info = f" (threshold: {metric.threshold})" if metric.threshold else ""
            lines.append(
                f"  [{status}] {name}: {metric.value:.4f}{metric.unit}{threshold_info}"
            )

        if result.gate_result:
            lines.extend([
                "",
                "Quality Gate:",
                f"  Score: {result.gate_result.score:.4f}",
                f"  Threshold: {result.gate_result.threshold:.4f}",
                f"  Passed: {result.gate_result.passed}",
                f"  Blocked: {result.gate_result.blocked}",
            ])

            if result.gate_result.reason:
                lines.append(f"  Reason: {result.gate_result.reason}")

        if result.errors:
            lines.extend(["", "Errors:"])
            for error in result.errors:
                lines.append(f"  - {error}")

        if result.warnings:
            lines.extend(["", "Warnings:"])
            for warning in result.warnings:
                lines.append(f"  - {warning}")

        return "\n".join(lines)

    def _parse_analysis_response(self, response: str) -> Analysis:
        """Parse LLM response into Analysis object"""
        try:
            # Try to extract JSON from response
            # Handle case where LLM adds extra text
            response = response.strip()

            # Find JSON object in response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
            else:
                # No JSON found, parse as text
                data = self._parse_text_response(response)

            return Analysis(
                summary=data.get("summary", "No summary provided"),
                root_causes=data.get("root_causes", []),
                recommendations=data.get("recommendations", []),
                severity=data.get("severity", "info"),
                confidence=float(data.get("confidence", 0.5))
            )

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            # Fall back to text parsing
            return self._parse_text_response(response)

        except Exception as e:
            logger.error(f"Failed to parse analysis response: {e}")
            return Analysis(
                summary=response[:200] if len(response) > 200 else response,
                severity="info",
                confidence=0.3
            )

    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse non-JSON text response into structured format"""
        # Basic text parsing as fallback
        lines = text.split('\n')

        summary = lines[0] if lines else "Analysis completed"
        recommendations = []
        root_causes = []

        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('*'):
                recommendations.append(line[1:].strip())

        return {
            "summary": summary,
            "root_causes": root_causes,
            "recommendations": recommendations,
            "severity": "info",
            "confidence": 0.5
        }
