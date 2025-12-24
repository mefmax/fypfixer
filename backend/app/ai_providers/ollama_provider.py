"""
Ollama Provider for local AI inference.

Usage:
    provider = OllamaProvider()
    response = provider.generate("Hello")
    json_data = provider.generate_json("Generate a plan...")
"""

import os
import json
import logging
import httpx
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class OllamaProvider:
    """Локальный Ollama провайдер для разработки"""

    def __init__(self):
        self.base_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'llama3')
        self.timeout = 60.0

    @property
    def name(self) -> str:
        return f"ollama/{self.model}"

    def is_available(self) -> bool:
        """Проверка доступности Ollama"""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    model_names = [m.get('name', '').split(':')[0] for m in models]
                    return self.model in model_names or f"{self.model}:latest" in [m.get('name') for m in models]
                return False
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False

    def generate(self, prompt: str, system: Optional[str] = None, temperature: float = 0.7) -> str:
        """Генерация текста через Ollama"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }

            if system:
                payload["system"] = system

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")

        except httpx.TimeoutException:
            logger.error(f"Ollama timeout after {self.timeout}s")
            raise
        except Exception as e:
            logger.error(f"Ollama generate error: {e}")
            raise

    def generate_json(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """Генерация структурированного JSON"""
        json_prompt = f"{prompt}\n\nRespond ONLY with valid JSON, no markdown or other text."

        response_text = self.generate(json_prompt, system, temperature=0.3)

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
            logger.error(f"Failed to parse JSON from Ollama: {response_text[:200]}")
            raise ValueError(f"AI returned invalid JSON: {e}")

    def generate_plan(self, categories: List[str], display_name: str, streak: int = 0, language: str = 'ru') -> Dict[str, Any]:
        """Генерация персонализированного плана"""
        from .prompts import PLAN_GENERATOR_SYSTEM, PLAN_GENERATION_PROMPT

        prompt = PLAN_GENERATION_PROMPT.format(
            categories=", ".join(categories),
            streak=streak,
            display_name=display_name or "друг"
        )

        return self.generate_json(prompt, PLAN_GENERATOR_SYSTEM)

    def generate_motivation(self, display_name: str, streak: int, time_of_day: str = 'day') -> str:
        """Генерация мотивационного сообщения"""
        prompt = f"""Generate a short motivational greeting in Russian for user "{display_name}".
Their current streak is {streak} days. Time of day: {time_of_day}.
Response should be 1-2 sentences, friendly, with max 1 emoji.
Respond with just the message, nothing else."""

        return self.generate(prompt, temperature=0.5)


def test_ollama():
    """Тест Ollama провайдера"""
    provider = OllamaProvider()
    print(f"Provider: {provider.name}")
    print(f"Available: {provider.is_available()}")

    if provider.is_available():
        print("\nTesting generate...")
        response = provider.generate("Say hello in Russian")
        print(f"Response: {response[:100]}")

        print("\nTesting generate_json...")
        json_response = provider.generate_json("Generate a simple JSON with name and age fields")
        print(f"JSON: {json_response}")


if __name__ == '__main__':
    test_ollama()
