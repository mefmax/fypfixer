"""
StreakService - Manage user streak calculations.

Psychology basis:
- Streaks leverage loss aversion ("don't break the chain")
- Visual feedback increases commitment
- Milestones (3, 7, 14, 30 days) provide dopamine hits
"""

from datetime import date, timedelta
from typing import Dict, Optional

from app import db
from app.models import UserBehaviorStats, UserProgress
from app.config import XP_REWARDS, XP_DEFAULT, STREAK_MILESTONES
from app.services.analytics_service import analytics_service


class StreakService:
    """Service for managing user streaks and engagement stats."""

    def get_or_create_stats(self, user_id: int) -> UserBehaviorStats:
        """Get or create user behavior stats record."""
        stats = db.session.get(UserBehaviorStats, user_id)
        if not stats:
            stats = UserBehaviorStats(user_id=user_id)
            db.session.add(stats)
            db.session.commit()
        return stats

    def record_action_completion(self, user_id: int, action_type: str) -> Dict:
        """
        Record action completion and update stats.

        Returns:
            {
                'xp_earned': int,
                'new_total_xp': int,
                'streak': int,
                'streak_milestone': int | None,
                'level_up': bool,
                'new_level': str
            }
        """
        stats = self.get_or_create_stats(user_id)
        old_level = stats.current_level

        # Add XP
        xp = XP_REWARDS.get(action_type, XP_DEFAULT)
        stats.add_xp(xp)

        # Update action count
        stats.total_actions_completed += 1

        # Check for level up
        level_up = stats.current_level != old_level

        db.session.commit()

        return {
            'xp_earned': xp,
            'new_total_xp': stats.total_xp,
            'streak': stats.current_streak_days,
            'streak_milestone': None,
            'level_up': level_up,
            'new_level': stats.current_level,
        }

    def record_plan_completion(self, user_id: int) -> Dict:
        """
        Record daily plan completion.

        Called when user completes all actions for the day.
        Updates streak and checks for milestones.
        """
        stats = self.get_or_create_stats(user_id)
        old_streak = stats.current_streak_days

        # Update streak
        stats.update_streak(date.today())

        # Add completion XP
        xp = XP_REWARDS['plan_complete']
        stats.add_xp(xp)

        # Check for milestone
        milestone = None
        if stats.current_streak_days in STREAK_MILESTONES:
            milestone = stats.current_streak_days
            # Bonus XP for milestone
            stats.add_xp(XP_REWARDS['streak_milestone'])

            # Record achievement
            achievement = f'streak_{milestone}'
            if stats.achievements is None:
                stats.achievements = []
            if achievement not in stats.achievements:
                stats.achievements = stats.achievements + [achievement]

            # Track milestone event
            analytics_service.track_event(
                analytics_service.EVENT_STREAK_MILESTONE,
                user_id=user_id,
                properties={
                    'milestone_days': milestone,
                    'total_xp': stats.total_xp,
                    'level': stats.current_level,
                }
            )

        # Update completion rate
        stats.avg_completion_rate = (
            (stats.avg_completion_rate * stats.total_days_active + 1.0)
            / (stats.total_days_active + 1)
        ) if stats.total_days_active > 0 else 1.0

        db.session.commit()

        return {
            'streak': stats.current_streak_days,
            'streak_increased': stats.current_streak_days > old_streak,
            'milestone': milestone,
            'total_xp': stats.total_xp,
            'level': stats.current_level,
            'achievements': stats.achievements,
        }

    def check_streak_status(self, user_id: int) -> Dict:
        """
        Check user's current streak status.
        Returns camelCase fields for frontend compatibility.
        """
        stats = self.get_or_create_stats(user_id)

        days_since = stats.get_days_since_last_activity()

        status = 'active'
        if days_since == 0:
            status = 'completed_today'
        elif days_since == 1:
            status = 'at_risk'
        elif days_since > 1:
            status = 'broken'

        # Return camelCase for frontend
        return {
            'currentStreak': stats.current_streak_days,
            'longestStreak': stats.max_streak_days,
            'nextMilestone': self._get_next_milestone(stats.current_streak_days),
            'totalXp': stats.total_xp or 0,
            'level': stats.current_level or 'Beginner',
            'status': status,
            'daysSinceActivity': days_since,
        }

    def _get_next_milestone(self, current: int) -> Optional[int]:
        """Get next streak milestone."""
        for m in STREAK_MILESTONES:
            if m > current:
                return m
        return None

    def get_leaderboard(self, limit: int = 10) -> list:
        """Get top users by streak."""
        top = UserBehaviorStats.query.order_by(
            UserBehaviorStats.current_streak_days.desc()
        ).limit(limit).all()

        return [
            {
                'user_id': s.user_id,
                'streak': s.current_streak_days,
                'level': s.current_level,
                'xp': s.total_xp,
            }
            for s in top
        ]


streak_service = StreakService()
