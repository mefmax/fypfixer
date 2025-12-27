"""
Admin Metrics API - Dashboard metrics for admin users.

Endpoints:
- GET /api/admin/metrics/overview - Users stats (DAU, new, total)
- GET /api/admin/metrics/challenge - Challenge funnel (D0->D7)
- GET /api/admin/metrics/plans - Step completion and signals
- GET /api/admin/metrics/system - API latency, errors, AI cost
"""

import logging
from datetime import date, datetime, timedelta
from flask import Blueprint, g
from sqlalchemy import func, text
from app import db, limiter, READ_LIMIT
from app.models import User, AnalyticsEvent, RequestLog, AIRequestLog
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required

logger = logging.getLogger(__name__)
admin_metrics_bp = Blueprint('admin_metrics', __name__)


def _is_admin(user_id: int) -> bool:
    """Check if user has admin role."""
    from app.models import User
    user = User.query.get(user_id)
    if user and hasattr(user, 'is_admin') and user.is_admin:
        return True
    # Fallback: check email domain or specific user IDs
    if user and user.email and user.email.endswith('@fypglow.com'):
        return True
    # TODO: Add proper admin role in users table
    return False


def admin_required(f):
    """Decorator to require admin access."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'current_user_id') or not g.current_user_id:
            return error_response('unauthorized', 'Authentication required', status_code=401)
        if not _is_admin(g.current_user_id):
            return error_response('forbidden', 'Admin access required', status_code=403)
        return f(*args, **kwargs)
    return decorated


@admin_metrics_bp.route('/overview', methods=['GET'])
@jwt_required
@admin_required
@limiter.limit(READ_LIMIT)
def get_overview():
    """
    Get user overview metrics.

    Response:
    {
        "success": true,
        "data": {
            "dau": 127,
            "new_today": 23,
            "total_users": 1847
        }
    }
    """
    try:
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

        return success_response({
            'dau': dau,
            'new_today': new_today,
            'total_users': total_users
        })

    except Exception as e:
        logger.exception("Error getting overview metrics")
        return error_response('metrics_error', 'Failed to load overview', status_code=500)


@admin_metrics_bp.route('/challenge', methods=['GET'])
@jwt_required
@admin_required
@limiter.limit(READ_LIMIT)
def get_challenge():
    """
    Get challenge funnel metrics.

    Response:
    {
        "success": true,
        "data": {
            "funnel": [
                {"day": 0, "count": 100, "percent": 100},
                {"day": 1, "count": 68, "percent": 68},
                ...
            ],
            "d7_completion_rate": 24.0
        }
    }
    """
    try:
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

        return success_response({
            'funnel': funnel,
            'd7_completion_rate': d7_completion
        })

    except Exception as e:
        logger.exception("Error getting challenge metrics")
        return error_response('metrics_error', 'Failed to load challenge funnel', status_code=500)


@admin_metrics_bp.route('/plans', methods=['GET'])
@jwt_required
@admin_required
@limiter.limit(READ_LIMIT)
def get_plans():
    """
    Get plan performance metrics.

    Response:
    {
        "success": true,
        "data": {
            "step_completion": {
                "clear": 92.0,
                "watch": 85.0,
                "reinforce": 62.0
            },
            "avg_duration_seconds": 690,
            "signals": {
                "blocks": 3.2,
                "watches_full": 3.8,
                "likes": 3.5,
                "follows": 2.1,
                "shares": 0.8
            }
        }
    }
    """
    try:
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
            # Query average of signal count from event_data
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

        return success_response({
            'step_completion': step_completion,
            'avg_duration_seconds': int(avg_duration) if avg_duration else 690,
            'signals': signals
        })

    except Exception as e:
        logger.exception("Error getting plan metrics")
        return error_response('metrics_error', 'Failed to load plan metrics', status_code=500)


@admin_metrics_bp.route('/system', methods=['GET'])
@jwt_required
@admin_required
@limiter.limit(READ_LIMIT)
def get_system():
    """
    Get system health metrics.

    Response:
    {
        "success": true,
        "data": {
            "api_latency_p95_ms": 145,
            "error_rate_percent": 0.3,
            "ai_cost_today_usd": 8.50,
            "status": "operational"
        }
    }
    """
    try:
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

        return success_response({
            'api_latency_p95_ms': int(latency_p95) if latency_p95 else 0,
            'error_rate_percent': error_rate,
            'ai_cost_today_usd': round(float(ai_cost), 2) if ai_cost else 0,
            'status': status
        })

    except Exception as e:
        logger.exception("Error getting system metrics")
        return error_response('metrics_error', 'Failed to load system metrics', status_code=500)
