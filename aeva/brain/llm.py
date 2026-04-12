"""
AEVA-Brain LLM Providers
Integration with various LLM providers
"""

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        """
        Generate completion from prompt

        Args:
            prompt: Input prompt
            **kwargs: Additional parameters

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    async def complete_async(self, prompt: str, **kwargs) -> str:
        """
        Generate completion asynchronously

        Args:
            prompt: Input prompt
            **kwargs: Additional parameters

        Returns:
            Generated text
        """
        pass


class ClaudeProvider(LLMProvider):
    """
    Anthropic Claude API provider

    Uses Claude models for intelligent analysis
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Initialize Anthropic client
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
            logger.info(f"Initialized Claude provider with model: {model}")
        except ImportError:
            raise ImportError(
                "anthropic package not installed. "
                "Install with: pip install anthropic"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Claude provider: {e}")
            raise

    def complete(self, prompt: str, **kwargs) -> str:
        """Generate completion using Claude"""
        try:
            # Merge kwargs with defaults
            params = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            response = self.client.messages.create(**params)

            # Extract text from response
            if response.content and len(response.content) > 0:
                return response.content[0].text
            else:
                return ""

        except Exception as e:
            logger.error(f"Claude API call failed: {e}")
            raise

    async def complete_async(self, prompt: str, **kwargs) -> str:
        """Generate completion asynchronously using Claude"""
        try:
            from anthropic import AsyncAnthropic

            # Create async client
            async_client = AsyncAnthropic(api_key=self.client.api_key)

            params = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            response = await async_client.messages.create(**params)

            if response.content and len(response.content) > 0:
                return response.content[0].text
            else:
                return ""

        except Exception as e:
            logger.error(f"Claude async API call failed: {e}")
            raise

    def complete_with_system(
        self,
        prompt: str,
        system_prompt: str,
        **kwargs
    ) -> str:
        """Generate completion with system prompt"""
        try:
            params = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
                "system": system_prompt,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            response = self.client.messages.create(**params)

            if response.content and len(response.content) > 0:
                return response.content[0].text
            else:
                return ""

        except Exception as e:
            logger.error(f"Claude API call with system prompt failed: {e}")
            raise


class OpenAIProvider(LLMProvider):
    """
    OpenAI API provider (optional)

    Can be used as an alternative to Claude
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        max_tokens: int = 4096,
        temperature: float = 0.7
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        try:
            import openai
            openai.api_key = api_key
            self.client = openai
            logger.info(f"Initialized OpenAI provider with model: {model}")
        except ImportError:
            raise ImportError(
                "openai package not installed. "
                "Install with: pip install openai"
            )

    def complete(self, prompt: str, **kwargs) -> str:
        """Generate completion using OpenAI"""
        try:
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                temperature=kwargs.get("temperature", self.temperature),
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise

    async def complete_async(self, prompt: str, **kwargs) -> str:
        """Generate completion asynchronously using OpenAI"""
        # OpenAI async implementation
        # For simplicity, calling sync version
        return self.complete(prompt, **kwargs)
