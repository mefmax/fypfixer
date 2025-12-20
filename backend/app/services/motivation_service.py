"""
MotivationService - Context-aware motivation messages.

Psychology basis:
- Progress messages increase completion rates
- Time-of-day adaptation matches energy levels
- Lapse recovery reduces guilt and encourages return
"""

from datetime import datetime
from typing import Dict, Optional

from app.models import MessageTemplate, UserBehaviorStats
from app.config import STREAK_MILESTONES


class MotivationService:
    """Service for generating context-aware motivation messages."""

    def get_message(
        self,
        user_id: Optional[int],
        progress: Dict[str, int],
        language: str = 'en'
    ) -> str:
        """
        Get best motivation message for user's current state.

        Priority:
        1. Streak milestones (highest priority)
        2. Progress-based messages
        3. Time-of-day greetings
        4. Lapse recovery (if applicable)

        Args:
            user_id: User ID (None for anonymous)
            progress: {'completed': int, 'total': int}
            language: Language code

        Returns:
            Formatted motivation message with emoji
        """
        completed = progress.get('completed', 0)
        total = progress.get('total', 5)
        percentage = int((completed / total) * 100) if total > 0 else 0

        # Get user stats for context
        streak = 0
        days_inactive = 0

        if user_id:
            stats = UserBehaviorStats.query.get(user_id)
            if stats:
                streak = stats.current_streak_days or 0
                days_inactive = stats.get_days_since_last_activity()

        # Priority 1: Check for streak milestone (first 7 milestones for messages)
        if streak in STREAK_MILESTONES[:7]:
            msg = MessageTemplate.find_best_match(
                'streak',
                {'streak_days': streak},
                language
            )
            if msg:
                return msg

        # Priority 2: Check for lapse recovery
        if days_inactive >= 3:
            msg = MessageTemplate.find_best_match(
                'lapse',
                {'lapse_days_min': days_inactive},
                language
            )
            if msg:
                return msg

        # Priority 3: Progress-based message
        msg = MessageTemplate.find_best_match(
            'progress',
            {'progress_pct': percentage},
            language
        )
        if msg:
            return msg

        # Priority 4: Time-of-day greeting
        hour = datetime.now().hour
        msg = MessageTemplate.find_best_match(
            'time_of_day',
            {'time_start': hour, 'time_end': hour + 1},
            language
        )
        if msg:
            return msg

        # Fallback
        return self._get_fallback_message(percentage)

    def _get_fallback_message(self, percentage: int) -> str:
        """Fallback messages if no templates match."""
        if percentage == 0:
            return "🚀 Your daily plan is ready!"
        elif percentage == 100:
            return "🎉 Amazing! Plan completed!"
        elif percentage >= 60:
            return f"🔥 More than halfway! Keep going!"
        elif percentage >= 20:
            return f"💪 Good progress! You've got this!"
        else:
            return f"✨ Great start! Keep the momentum!"

    def get_action_celebration(self, action_type: str) -> str:
        """Get celebration message after completing an action."""
        celebrations = {
            'follow': "✅ Great follow! Your algorithm is learning.",
            'like': "👍 Like registered! TikTok noticed.",
            'save': "📌 Saved! Strong signal sent.",
            'not_interested': "🚫 Removed! Your feed is cleaner.",
        }
        return celebrations.get(action_type, "✅ Action completed!")

    def get_streak_message(self, streak: int, language: str = 'en') -> Optional[str]:
        """Get streak-specific message."""
        return MessageTemplate.find_best_match(
            'streak',
            {'streak_days': streak},
            language
        )

    def get_lapse_recovery_message(self, days_inactive: int, language: str = 'en') -> Optional[str]:
        """Get lapse recovery message."""
        return MessageTemplate.find_best_match(
            'lapse',
            {'lapse_days_min': days_inactive},
            language
        )


motivation_service = MotivationService()
