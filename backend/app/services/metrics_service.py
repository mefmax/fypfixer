"""
Metrics Service - Admin dashboard metrics business logic.

Extracted from routes/admin_metrics.py for proper separation of concerns.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Dict, Any, List

from sqlalchemy import func, text
from app import db
from app.models import User, AnalyticsEvent, RequestLog, AIRequestLog

logger = logging.getLogger(__name__)


class MetricsService:
    """Service for admin dashboard metrics."""

    def get_overview_metrics(self) -> Dict[str, Any]:
        """
        Get user overview metrics.

        Returns:
            Dict with dau, new_today, total_users
        """
        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())

        # DAU: distinct users with events today
        dau = db.session.query(
            func.count(func.distinct(AnalyticsEvent.user_id))
        ).filter(
            AnalyticsEvent.created_at >= today_start,
            AnalyticsEvent.user_id.isnot(None)
        ).scalar() or 0

        # New users today
        new_today = User.query.filter(
            User.created_at >= today_start
        ).count()

        # Total active users
        total_users = User.query.filter(
            User.is_active == True
        ).count()

        return {
            'dau': dau,
            'new_today': new_today,
            'total_users': total_users
        }

    def get_challenge_metrics(self) -> Dict[str, Any]:
        """
        Get challenge funnel metrics.

        Returns:
            Dict with funnel array and d7_completion_rate
        """
        # Get users who started challenge (day 0)
        started_users = db.session.query(
            func.count(func.distinct(AnalyticsEvent.user_id))
        ).filter(
            AnalyticsEvent.event_type == 'challenge_started'
        ).scalar() or 0

        if started_users == 0:
            # Fallback: count users with any plan_viewed event
            started_users = db.session.query(
                func.count(func.distinct(AnalyticsEvent.user_id))
            ).filter(
                AnalyticsEvent.event_type == 'plan_viewed'
            ).scalar() or 1

        funnel = [{'day': 0, 'count': started_users, 'percent': 100.0}]

        # Get counts for each day milestone
        for day in [1, 3, 7]:
            day_count = db.session.query(
                func.count(func.distinct(AnalyticsEvent.user_id))
            ).filter(
                AnalyticsEvent.event_type == 'challenge_day_completed',
                AnalyticsEvent.event_data['day'].astext.cast(db.Integer) >= day
            ).scalar() or 0

            # Fallback: count plan_completed events
            if day_count == 0:
                day_count = db.session.query(
                    func.count(func.distinct(AnalyticsEvent.user_id))
                ).filter(
                    AnalyticsEvent.event_type == 'plan_completed',
                    AnalyticsEvent.event_data['day'].astext.cast(db.Integer) >= day
                ).scalar() or 0

            percent = round((day_count / started_users) * 100, 1) if started_users > 0 else 0
            funnel.append({'day': day, 'count': day_count, 'percent': percent})

        d7_completion = funnel[-1]['percent'] if funnel else 0

        return {
            'funnel': funnel,
            'd7_completion_rate': d7_completion
        }

    def get_plan_metrics(self) -> Dict[str, Any]:
        """
        Get plan performance metrics.

        Returns:
            Dict with step_completion, avg_duration_seconds, signals
        """
        # Total plans started (plan_viewed events)
        total_plans = db.session.query(
            func.count(AnalyticsEvent.id)
        ).filter(
            AnalyticsEvent.event_type == 'plan_viewed'
        ).scalar() or 1

        # Step completions
        step_types = ['detox', 'watch', 'reinforce']
        step_completion = {}

        for step in step_types:
            completed = db.session.query(
                func.count(AnalyticsEvent.id)
            ).filter(
                AnalyticsEvent.event_type == f'{step}_completed'
            ).scalar() or 0

            step_name = 'clear' if step == 'detox' else step
            step_completion[step_name] = round((completed / total_plans) * 100, 1) if total_plans > 0 else 0

        # Average signal counts from event_data
        signal_types = {
            'blocks': 'detox_completed',
            'watches_full': 'watch_completed',
            'likes': 'watch_completed',
            'follows': 'watch_completed',
            'shares': 'reinforce_completed'
        }

        signals = {}
        for signal, event_type in signal_types.items():
            result = db.session.query(
                func.avg(
                    func.coalesce(
                        AnalyticsEvent.event_data[signal].astext.cast(db.Float),
                        0
                    )
                )
            ).filter(
                AnalyticsEvent.event_type == event_type
            ).scalar()

            signals[signal] = round(float(result), 1) if result else 0

        # Average duration (from plan_completed events)
        avg_duration = db.session.query(
            func.avg(
                AnalyticsEvent.event_data['duration_seconds'].astext.cast(db.Integer)
            )
        ).filter(
            AnalyticsEvent.event_type == 'plan_completed'
        ).scalar()

        return {
            'step_completion': step_completion,
            'avg_duration_seconds': int(avg_duration) if avg_duration else 690,
            'signals': signals
        }

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get system health metrics.

        Returns:
            Dict with api_latency_p95_ms, error_rate_percent, ai_cost_today_usd, status
        """
        now = datetime.utcnow()
        hour_ago = now - timedelta(hours=1)
        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())

        # P95 latency from request_logs (last hour)
        latency_p95 = db.session.execute(text("""
            SELECT PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms)
            FROM request_logs
            WHERE created_at >= :hour_ago
        """), {'hour_ago': hour_ago}).scalar()

        # Error rate (4xx and 5xx)
        total_requests = db.session.query(
            func.count(RequestLog.id)
        ).filter(
            RequestLog.created_at >= hour_ago
        ).scalar() or 1

        error_requests = db.session.query(
            func.count(RequestLog.id)
        ).filter(
            RequestLog.created_at >= hour_ago,
            RequestLog.status >= 400
        ).scalar() or 0

        error_rate = round((error_requests / total_requests) * 100, 2) if total_requests > 0 else 0

        # AI cost today
        ai_cost = db.session.query(
            func.sum(AIRequestLog.cost_usd)
        ).filter(
            AIRequestLog.created_at >= today_start
        ).scalar() or 0

        # Determine status
        status = 'operational'
        if error_rate > 5:
            status = 'degraded'
        if error_rate > 20:
            status = 'outage'

        return {
            'api_latency_p95_ms': int(latency_p95) if latency_p95 else 0,
            'error_rate_percent': error_rate,
            'ai_cost_today_usd': round(float(ai_cost), 2) if ai_cost else 0,
            'status': status
        }


# Singleton instance
metrics_service = MetricsService()
