"""Static fallback provider - returns hardcoded plans without AI."""

from typing import Dict, Any, Optional, List, Union
from .base import UserContext, SearchCriteria, SelectedAction


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

    def generate_motivation(self, context_or_name: Union[UserContext, str], progress_or_streak: Union[Dict, int] = 0, time_of_day: str = 'day') -> str:
        """Генерация статичного мотивационного сообщения.

        Supports two signatures:
        - generate_motivation(context: UserContext, progress: dict)  # RecommendationService
        - generate_motivation(display_name: str, streak: int, time_of_day: str)  # Direct
        """
        # Handle UserContext signature (from RecommendationService)
        if isinstance(context_or_name, UserContext):
            streak = context_or_name.streak_days
            name = "друг"
        else:
            name = context_or_name or "друг"
            streak = progress_or_streak if isinstance(progress_or_streak, int) else 0

        if streak > 7:
            return f"Отлично, {name}! {streak} дней подряд — ты на пути к успеху!"
        elif streak > 0:
            return f"Привет, {name}! Продолжай в том же духе, streak: {streak}!"
        else:
            return f"Привет, {name}! Начни свой streak сегодня!"

    def generate_criteria(self, context: UserContext) -> SearchCriteria:
        """Generate static search criteria."""
        category_queries = {
            'fitness': ['fitness motivation', 'workout tips', 'gym routine'],
            'personal_growth': ['self improvement', 'productivity tips', 'motivation'],
            'education': ['learning tips', 'study motivation', 'education'],
            'creative': ['creative process', 'art tips', 'design inspiration'],
        }
        category_hashtags = {
            'fitness': ['fitness', 'gym', 'workout', 'motivation'],
            'personal_growth': ['personalgrowth', 'selfimprovement', 'motivation'],
            'education': ['education', 'learning', 'studytok'],
            'creative': ['creative', 'art', 'design'],
        }

        queries = category_queries.get(context.category, ['motivation', 'tips'])
        hashtags = category_hashtags.get(context.category, ['motivation', 'tips'])

        return SearchCriteria(
            search_queries=queries,
            hashtags=hashtags
        )

    def select_actions(self, candidates: List[Dict], context: UserContext, count: int = 5) -> List[SelectedAction]:
        """Select actions from candidates (static fallback)."""
        actions = []
        types = ['follow', 'like', 'save', 'like', 'not_interested']

        for i, c in enumerate(candidates[:count]):
            t = types[i % len(types)]
            if t == 'not_interested':
                actions.append(SelectedAction(
                    type='not_interested',
                    video_id=None,
                    creator_username='',
                    creator_display_name='',
                    description='Irrelevant content',
                    thumbnail_url=None,
                    tiktok_url=None,
                    reason='Mark content you don\'t want to see'
                ))
            else:
                actions.append(SelectedAction(
                    type=t,
                    video_id=None,
                    creator_username=c.get('creator_username', ''),
                    creator_display_name=c.get('creator_display_name', ''),
                    description=c.get('description', ''),
                    thumbnail_url=c.get('thumbnail_url'),
                    tiktok_url=c.get('tiktok_url'),
                    reason=f"Quality creator in {context.category}"
                ))

        return actions
