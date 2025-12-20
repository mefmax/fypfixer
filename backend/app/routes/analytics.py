"""
Analytics API - Dashboard metrics and user analytics.

Endpoints:
- GET /api/analytics/dashboard - Admin metrics (requires admin role)
- GET /api/analytics/me - Current user's analytics
- GET /api/analytics/me/weekly - User's weekly activity
"""

import logging
from flask import Blueprint, g
from app.services.analytics_service import analytics_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required, jwt_optional
from app import limiter

logger = logging.getLogger(__name__)
analytics_bp = Blueprint('analytics', __name__)


def _is_admin(user_id: int) -> bool:
    """Check if user has admin role."""
    # TODO: Implement proper admin role check from database
    # For now, check if user_id is in admin list (should be in app_settings)
    from app.models import User
    user = User.query.get(user_id)
    if user and hasattr(user, 'is_admin'):
        return user.is_admin
    return False


@analytics_bp.route('/analytics/dashboard', methods=['GET'])
@jwt_required  # SECURITY: Now requires authentication
@limiter.limit("10 per minute")  # SECURITY: Rate limit
def get_dashboard_metrics():
    """
    Get high-level dashboard metrics.
    SECURITY: Requires admin role.

    Response:
    {
        "success": true,
        "data": {
            "users": {"total": 100, "activeThisWeek": 45},
            "plans": {"generatedToday": 23},
            "actions": {"completedToday": 89},
            "streaks": {"average": 4.2},
            "aiPipeline": {"aiGeneratedPercent": 78.5}
        }
    }
    """
    # SECURITY: Check admin role
    if not _is_admin(g.current_user_id):
        return error_response('forbidden', 'Admin access required', status_code=403)

    try:
        metrics = analytics_service.get_dashboard_metrics()
        return success_response(metrics)
    except Exception as e:
        logger.exception("Dashboard metrics error")
        # SECURITY: Don't expose internal error details
        return error_response('analytics_error', 'Failed to load dashboard metrics', status_code=500)


@analytics_bp.route('/analytics/me', methods=['GET'])
@jwt_required
@limiter.limit("30 per minute")  # SECURITY: Rate limit
def get_my_analytics():
    """
    Get current user's analytics.

    Response:
    {
        "success": true,
        "data": {
            "totalActions": 45,
            "totalPlansCompleted": 12,
            "currentStreak": 7,
            "longestStreak": 14,
            "totalXp": 850,
            "level": "Curator",
            "actionsThisWeek": 23
        }
    }
    """
    try:
        analytics = analytics_service.get_user_analytics(g.current_user_id)
        return success_response(analytics)
    except Exception as e:
        logger.exception("User analytics error")
        # SECURITY: Don't expose internal error details
        return error_response('analytics_error', 'Failed to load analytics', status_code=500)


@analytics_bp.route('/analytics/me/weekly', methods=['GET'])
@jwt_required
@limiter.limit("30 per minute")  # SECURITY: Rate limit
def get_weekly_activity():
    """
    Get user's activity for the past 7 days.

    Response:
    {
        "success": true,
        "data": [
            {"date": "2025-12-12", "dayName": "Thu", "actionsCompleted": 5},
            {"date": "2025-12-13", "dayName": "Fri", "actionsCompleted": 3},
            ...
        ]
    }
    """
    try:
        weekly = analytics_service.get_weekly_activity(g.current_user_id)
        return success_response(weekly)
    except Exception as e:
        logger.exception("Weekly activity error")
        # SECURITY: Don't expose internal error details
        return error_response('analytics_error', 'Failed to load weekly activity', status_code=500)


@analytics_bp.route('/analytics/me/breakdown', methods=['GET'])
@jwt_required
@limiter.limit("30 per minute")  # SECURITY: Rate limit
def get_category_breakdown():
    """
    Get breakdown of completed actions by type.

    Response:
    {
        "success": true,
        "data": [
            {"type": "follow", "count": 15},
            {"type": "like", "count": 23},
            {"type": "save", "count": 8},
            {"type": "not_interested", "count": 12}
        ]
    }
    """
    try:
        breakdown = analytics_service.get_category_breakdown(g.current_user_id)
        return success_response(breakdown)
    except Exception as e:
        logger.exception("Category breakdown error")
        # SECURITY: Don't expose internal error details
        return error_response('analytics_error', 'Failed to load breakdown', status_code=500)
