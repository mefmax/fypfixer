import os
import json
import logging
import httpx
from typing import Dict, Any, Optional, List
from .base import AIProvider

logger = logging.getLogger(__name__)


class AnthropicProvider(AIProvider):
    """Anthropic Claude провайдер для продакшена"""

    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-haiku-20240307')
        self.base_url = "https://api.anthropic.com/v1/messages"

        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not set!")

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate_text(self, prompt: str, system: Optional[str] = None, max_tokens: int = 1024) -> str:
        """Генерация текста через Claude API"""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not configured")

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
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                content = data.get("content", [])
                if content and len(content) > 0:
                    return content[0].get("text", "")
                return ""

        except httpx.HTTPStatusError as e:
            logger.error(f"Anthropic API error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Anthropic request failed: {e}")
            raise

    def generate_json(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """Генерация структурированного JSON"""
        json_prompt = f"{prompt}\n\nRespond ONLY with valid JSON, no markdown or other text."

        response_text = self.generate_text(json_prompt, system)

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

    def generate_criteria(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация критериев для рекомендаций"""
        from .prompts import CRITERIA_PROMPT, SYSTEM_PROMPT

        prompt = CRITERIA_PROMPT.format(**user_context)
        return self.generate_json(prompt, SYSTEM_PROMPT)

    def select_actions(
        self,
        candidates: List[Dict[str, Any]],
        user_context: Dict[str, Any],
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """Выбор действий из кандидатов"""
        from .prompts import ACTION_SELECTION_PROMPT, SYSTEM_PROMPT

        prompt = ACTION_SELECTION_PROMPT.format(
            candidates=json.dumps(candidates, ensure_ascii=False),
            user_context=json.dumps(user_context, ensure_ascii=False),
            count=count
        )

        result = self.generate_json(prompt, SYSTEM_PROMPT)
        return result.get('selected_actions', [])

    def generate_motivation(self, user_context: Dict[str, Any]) -> Dict[str, str]:
        """Генерация мотивационных сообщений"""
        from .prompts import MOTIVATION_PROMPT, SYSTEM_PROMPT

        prompt = MOTIVATION_PROMPT.format(**user_context)
        return self.generate_json(prompt, SYSTEM_PROMPT)
