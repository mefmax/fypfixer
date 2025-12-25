"""
Anthropic Claude Provider for production AI inference.

Usage:
    provider = AnthropicProvider()
    response = provider.generate("Hello")
    json_data = provider.generate_json("Generate a plan...")
"""

import os
import json
import logging
import time
import httpx
from typing import Dict, Any, Optional, List

from app.utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)

# Lazy import for ai_log_service to avoid circular imports
_ai_log_service = None

def _get_ai_log_service():
    global _ai_log_service
    if _ai_log_service is None:
        from app.services.ai_log_service import ai_log_service
        _ai_log_service = ai_log_service
    return _ai_log_service

# Exceptions to retry on
RETRYABLE_EXCEPTIONS = (
    httpx.TimeoutException,
    httpx.ConnectError,
    httpx.RemoteProtocolError,
)


class AnthropicProvider:
    """Anthropic Claude провайдер для продакшена"""

    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-haiku-20240307')
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.timeout = 30.0

        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not set!")

    @property
    def name(self) -> str:
        return f"anthropic/{self.model}"

    def is_available(self) -> bool:
        """Проверка доступности API ключа"""
        return bool(self.api_key)

    def generate(self, prompt: str, system: Optional[str] = None, max_tokens: int = 1024) -> str:
        """Генерация текста через Claude API"""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not configured")

        return self._call_api(prompt, system, max_tokens)

    def _call_api(self, prompt: str, system: Optional[str], max_tokens: int) -> str:
        """Internal method to call Anthropic API with retry logic."""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }

        if system:
            payload["system"] = system

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )

                # Check for rate limit (429) - should be retried
                if response.status_code == 429:
                    raise httpx.TimeoutException("Rate limited by API")

                response.raise_for_status()
                data = response.json()

                content = data.get("content", [])
                if content and len(content) > 0:
                    return content[0].get("text", "")
                return ""

        except httpx.HTTPStatusError as e:
            logger.error(f"Anthropic API error: {e.response.status_code} - {e.response.text}")
            # Server errors (5xx) should be retried
            if e.response.status_code >= 500:
                raise httpx.ConnectError(f"Server error: {e.response.status_code}")
            raise
        except RETRYABLE_EXCEPTIONS:
            raise
        except Exception as e:
            logger.error(f"Anthropic request failed: {e}")
            raise

    def generate_json(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """Генерация структурированного JSON"""
        json_prompt = f"{prompt}\n\nRespond ONLY with valid JSON, no markdown or other text."

        response_text = self.generate(json_prompt, system)

        try:
            # Убираем возможные markdown блоки
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            return json.loads(cleaned.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Claude: {response_text[:200]}")
            raise ValueError(f"AI returned invalid JSON: {e}")

    def generate_plan(self, categories: List[str], display_name: str, streak: int = 0, language: str = 'ru', user_id: int = None) -> Dict[str, Any]:
        """Генерация персонализированного плана с retry, fallback и logging"""
        from .prompts import PLAN_GENERATOR_SYSTEM, PLAN_GENERATION_PROMPT

        prompt = PLAN_GENERATION_PROMPT.format(
            categories=", ".join(categories),
            streak=streak,
            display_name=display_name or "друг"
        )

        start_time = time.time()
        error_msg = None
        used_fallback = False

        # Create a retryable function with fallback to StaticProvider
        @retry_with_backoff(
            max_attempts=3,
            backoff_seconds=(2, 4, 8),
            exceptions=RETRYABLE_EXCEPTIONS + (ValueError,),  # Include JSON parse errors
            fallback=lambda: self._static_fallback_with_flag(categories, display_name, streak, language)
        )
        def _generate():
            return self.generate_json(prompt, PLAN_GENERATOR_SYSTEM)

        try:
            result = _generate()

            # Check if we used fallback (result will have a flag)
            if isinstance(result, tuple):
                result, used_fallback = result

        except Exception as e:
            error_msg = str(e)
            raise
        finally:
            # Log the request
            latency_ms = int((time.time() - start_time) * 1000)

            try:
                log_service = _get_ai_log_service()
                log_service.log_request(
                    user_id=user_id,
                    provider='static' if used_fallback else 'anthropic',
                    model='static/fallback' if used_fallback else self.model,
                    latency_ms=latency_ms,
                    prompt_tokens=None,  # Anthropic API returns this, but we're not parsing yet
                    completion_tokens=None,
                    error=error_msg
                )
            except Exception as log_error:
                logger.warning(f"Failed to log AI request: {log_error}")

        return result

    def _static_fallback_with_flag(self, categories: List[str], display_name: str, streak: int, language: str):
        """Fallback to StaticProvider, returns tuple with fallback flag"""
        result = self._static_fallback(categories, display_name, streak, language)
        return (result, True)  # Return with flag indicating fallback was used

    def _static_fallback(self, categories: List[str], display_name: str, streak: int, language: str) -> Dict[str, Any]:
        """Fallback to StaticProvider when Anthropic fails"""
        from .static_provider import StaticProvider
        logger.warning("AnthropicProvider: Falling back to StaticProvider")
        static = StaticProvider()
        return static.generate_plan(categories, display_name, streak, language)

    def generate_motivation(self, display_name: str, streak: int, time_of_day: str = 'day') -> str:
        """Генерация мотивационного сообщения"""
        prompt = f"""Generate a short motivational greeting in Russian for user "{display_name}".
Their current streak is {streak} days. Time of day: {time_of_day}.
Response should be 1-2 sentences, friendly, with max 1 emoji.
Respond with just the message, nothing else."""

        return self.generate(prompt)


def test_anthropic():
    """Тест Anthropic провайдера"""
    provider = AnthropicProvider()
    print(f"Provider: {provider.name}")
    print(f"Available: {provider.is_available()}")

    if provider.is_available():
        print("\nTesting generate...")
        response = provider.generate("Say hello in Russian")
        print(f"Response: {response[:100]}")


if __name__ == '__main__':
    test_anthropic()
