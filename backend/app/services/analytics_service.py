"""
AnalyticsService - Track user events and calculate metrics.

Events tracked:
- plan_generated: User generated a daily plan
- plan_viewed: User viewed a plan
- detox_completed: User completed detox step
- watch_completed: User completed watch step
- reinforce_completed: User completed reinforce step
- plan_completed: User completed all steps
- action_completed: User completed an action
- streak_milestone: User hit a streak milestone
- onboarding_completed: User finished onboarding
"""

from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict

from app import db
from app.models import User, Plan, Action, UserProgress, UserBehaviorStats, UserRecommendation, AnalyticsEvent
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for tracking and calculating analytics."""

    # Event types
    EVENT_PLAN_GENERATED = 'plan_generated'
    EVENT_PLAN_VIEWED = 'plan_viewed'
    EVENT_DETOX_COMPLETED = 'detox_completed'
    EVENT_WATCH_COMPLETED = 'watch_completed'
    EVENT_REINFORCE_COMPLETED = 'reinforce_completed'
    EVENT_ACTION_COMPLETED = 'action_completed'
    EVENT_PLAN_COMPLETED = 'plan_completed'
    EVENT_STREAK_MILESTONE = 'streak_milestone'
    EVENT_ONBOARDING_COMPLETED = 'onboarding_completed'

    def track_event(
        self,
        event_type: str,
        user_id: Optional[int] = None,
        properties: Optional[Dict] = None
    ) -> Optional[AnalyticsEvent]:
        """
        Track an analytics event and save to database.

        Args:
            event_type: Type of event (e.g., 'plan_viewed', 'detox_completed')
            user_id: Optional user ID
            properties: Optional event data as dict

        Returns:
            Created AnalyticsEvent or None if error
        """
        try:
            event = AnalyticsEvent(
                user_id=user_id,
                event_type=event_type,
                event_data=properties or {}
            )
            db.session.add(event)
            db.session.commit()

            logger.info(f"[ANALYTICS] {event_type}: user={user_id} props={properties}")
            return event

        except Exception as e:
            logger.error(f"[ANALYTICS] Failed to track {event_type}: {e}")
            db.session.rollback()
            return None

    def track(
        self,
        user_id: int,
        event_type: str,
        event_data: Optional[Dict] = None
    ) -> Optional[AnalyticsEvent]:
        """
        Simplified track method for convenience.

        Args:
            user_id: User ID
            event_type: Type of event
            event_data: Optional event data

        Returns:
            Created AnalyticsEvent or None if error
        """
        return self.track_event(event_type, user_id, event_data)

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get high-level dashboard metrics."""
        today = date.today()
        week_ago = today - timedelta(days=7)

        # Total users
        total_users = User.query.count()

        # Active users (have progress in last 7 days)
        active_users = db.session.query(func.count(func.distinct(UserProgress.user_id))).filter(
            UserProgress.completed_at >= week_ago
        ).scalar() or 0

        # Plans generated today
        plans_today = Plan.query.filter(
            Plan.plan_date == today
        ).count()

        # Actions completed today
        actions_today = UserProgress.query.filter(
            func.date(UserProgress.completed_at) == today
        ).count()

        # Average streak
        avg_streak = db.session.query(
            func.avg(UserBehaviorStats.current_streak_days)
        ).scalar() or 0

        # AI vs Seed ratio (from user_recommendations)
        ai_count = UserRecommendation.query.filter(
            UserRecommendation.source == 'ai',
            UserRecommendation.plan_date >= week_ago
        ).count()

        seed_count = UserRecommendation.query.filter(
            UserRecommendation.source == 'seed',
            UserRecommendation.plan_date >= week_ago
        ).count()

        total_gen = ai_count + seed_count
        ai_ratio = round(ai_count / total_gen * 100, 1) if total_gen > 0 else 0

        return {
            'users': {
                'total': total_users,
                'activeThisWeek': active_users,
            },
            'plans': {
                'generatedToday': plans_today,
            },
            'actions': {
                'completedToday': actions_today,
            },
            'streaks': {
                'average': round(float(avg_streak), 1),
            },
            'aiPipeline': {
                'aiGeneratedPercent': ai_ratio,
                'seedFallbackPercent': round(100 - ai_ratio, 1),
            },
            'generatedAt': datetime.utcnow().isoformat() + 'Z',
        }

    def get_user_analytics(self, user_id: int) -> Dict[str, Any]:
        """Get analytics for a specific user."""
        stats = UserBehaviorStats.query.get(user_id)

        if not stats:
            return {
                'totalActions': 0,
                'totalPlansCompleted': 0,
                'currentStreak': 0,
                'longestStreak': 0,
                'totalXp': 0,
                'level': 'Beginner',
                'actionsThisWeek': 0,
            }

        # Actions this week
        week_ago = date.today() - timedelta(days=7)
        actions_week = UserProgress.query.filter(
            UserProgress.user_id == user_id,
            UserProgress.completed_at >= week_ago
        ).count()

        return {
            'totalActions': stats.total_actions_completed,
            'totalPlansCompleted': stats.total_plans_completed,
            'currentStreak': stats.current_streak_days,
            'longestStreak': stats.longest_streak_days,
            'totalXp': stats.total_xp,
            'level': stats.current_level,
            'actionsThisWeek': actions_week,
            'joinedAt': stats.created_at.isoformat() if hasattr(stats, 'created_at') else None,
        }

    def get_weekly_activity(self, user_id: int) -> List[Dict]:
        """Get daily activity for the past 7 days."""
        today = date.today()
        result = []

        for i in range(6, -1, -1):
            day = today - timedelta(days=i)

            count = UserProgress.query.filter(
                UserProgress.user_id == user_id,
                func.date(UserProgress.completed_at) == day
            ).count()

            result.append({
                'date': str(day),
                'dayName': day.strftime('%a'),
                'actionsCompleted': count,
            })

        return result

    def get_category_breakdown(self, user_id: int) -> List[Dict]:
        """Get breakdown of actions by category."""
        # Get all user's completed actions with their plans
        completed = db.session.query(
            Action.action_type,
            func.count(Action.id).label('count')
        ).join(
            UserProgress, UserProgress.action_id == Action.id
        ).filter(
            UserProgress.user_id == user_id
        ).group_by(Action.action_type).all()

        return [
            {'type': row.action_type, 'count': row.count}
            for row in completed
        ]


# Singleton
analytics_service = AnalyticsService()
