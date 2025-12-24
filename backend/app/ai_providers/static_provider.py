"""Static fallback provider - returns hardcoded plans without AI."""

from typing import Dict, Any, Optional, List


class StaticProvider:
    """Провайдер со статичными планами - не требует AI"""

    @property
    def name(self) -> str:
        return "static/fallback"

    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str, system: Optional[str] = None, max_tokens: int = 1024) -> str:
        """Static provider does not support text generation"""
        return "Static provider does not support text generation"

    def generate_json(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """Static provider does not support JSON generation"""
        return {"error": "Static provider does not support JSON generation"}

    def generate_plan(self, categories: List[str], display_name: str, streak: int = 0, language: str = 'ru') -> Dict[str, Any]:
        """Генерация статичного плана без AI"""
        cat_text = ", ".join(categories[:2]) if categories else "интересного контента"
        name = display_name or "друг"

        return {
            "motivation": {
                "greeting": f"Привет, {name}!",
                "tip": "Досматривай видео до конца — это улучшает рекомендации",
                "encouragement": f"Ты на {streak}-дневном streak!" if streak > 0 else "Начни свой streak сегодня!"
            },
            "steps": [
                {
                    "order": 1,
                    "type": "detox",
                    "title": "Очистка ленты",
                    "description": "Пролистай 15 видео, которые не интересны — это сигнал алгоритму",
                    "duration_minutes": 5,
                    "target_count": 15
                },
                {
                    "order": 2,
                    "type": "watch",
                    "title": f"Смотри {cat_text}",
                    "description": "Досмотри 3 видео до конца по интересным темам",
                    "duration_minutes": 10,
                    "target_count": 3
                },
                {
                    "order": 3,
                    "type": "browse",
                    "title": "Исследуй новое",
                    "description": "Найди и подпишись на 2 новых авторов",
                    "duration_minutes": 5,
                    "target_count": 2
                }
            ],
            "total_duration_minutes": 20
        }

    def generate_motivation(self, display_name: str, streak: int, time_of_day: str = 'day') -> str:
        """Генерация статичного мотивационного сообщения"""
        name = display_name or "друг"
        if streak > 7:
            return f"Отлично, {name}! {streak} дней подряд — ты на пути к успеху!"
        elif streak > 0:
            return f"Привет, {name}! Продолжай в том же духе, streak: {streak}!"
        else:
            return f"Привет, {name}! Начни свой streak сегодня!"
