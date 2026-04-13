"""
LLM Client for AI Analysis

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import json
from typing import Dict, Any, Optional
from app.core.config import settings


class LLMClient:
    """Client for interacting with LLM providers"""

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS

    async def generate_analysis(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        system_message: Optional[str] = None
    ) -> str:
        """
        Generate AI analysis using LLM.

        Args:
            prompt: User prompt for analysis
            context: Additional context data
            system_message: System message for LLM

        Returns:
            Generated analysis text
        """
        # Build full prompt with context
        full_prompt = self._build_prompt(prompt, context)

        # Call appropriate provider
        if self.provider == "openai":
            return await self._call_openai(full_prompt, system_message)
        elif self.provider == "anthropic":
            return await self._call_anthropic(full_prompt, system_message)
        elif self.provider == "ollama":
            return await self._call_ollama(full_prompt, system_message)
        else:
            # Fallback to mock response for testing
            return await self._mock_response(full_prompt, context)

    def _build_prompt(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Build full prompt with context"""
        if not context:
            return prompt

        context_str = json.dumps(context, indent=2)
        return f"{prompt}\n\nContext Data:\n{context_str}"

    async def _call_openai(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Call OpenAI API"""
        try:
            import openai

            if settings.LLM_API_KEY:
                openai.api_key = settings.LLM_API_KEY

            if settings.LLM_BASE_URL:
                openai.api_base = settings.LLM_BASE_URL

            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"

    async def _call_anthropic(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Call Anthropic API"""
        try:
            import anthropic

            client = anthropic.AsyncAnthropic(api_key=settings.LLM_API_KEY)

            response = await client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_message or "",
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text

        except Exception as e:
            return f"Error calling Anthropic: {str(e)}"

    async def _call_ollama(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Call Ollama API"""
        try:
            import httpx

            base_url = settings.LLM_BASE_URL or "http://localhost:11434"

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "system": system_message,
                        "stream": False
                    }
                )
                response.raise_for_status()
                return response.json()["response"]

        except Exception as e:
            return f"Error calling Ollama: {str(e)}"

    async def _mock_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate mock response for testing"""
        analysis = {
            "summary": "This is a mock AI analysis response.",
            "findings": [
                "The evaluation shows good overall performance.",
                "Metrics are within acceptable ranges.",
                "No critical issues detected."
            ],
            "recommendations": [
                "Consider monitoring performance trends over time.",
                "Implement additional validation checks for edge cases.",
                "Review error handling in production scenarios."
            ],
            "confidence": 0.85
        }

        if context:
            if "benchmark" in context:
                analysis["findings"].append("Benchmark results analyzed successfully.")
            if "validate" in context:
                analysis["findings"].append("Validation results reviewed.")

        return json.dumps(analysis, indent=2)


# Global LLM client instance
llm_client = LLMClient()
