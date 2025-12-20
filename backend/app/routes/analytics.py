"""
Analytics API - Dashboard metrics and user analytics.

Endpoints:
- GET /api/analytics/dashboard - Admin metrics (future: require admin role)
- GET /api/analytics/me - Current user's analytics
- GET /api/analytics/me/weekly - User's weekly activity
"""

from flask import Blueprint, g
from app.services.analytics_service import analytics_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required, jwt_optional

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/analytics/dashboard', methods=['GET'])
@jwt_optional  # TODO: Change to admin-only in production
def get_dashboard_metrics():
    """
    Get high-level dashboard metrics.

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
    try:
        metrics = analytics_service.get_dashboard_metrics()
        return success_response(metrics)
    except Exception as e:
        return error_response('analytics_error', str(e), status_code=500)


@analytics_bp.route('/analytics/me', methods=['GET'])
@jwt_required
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
        return error_response('analytics_error', str(e), status_code=500)


@analytics_bp.route('/analytics/me/weekly', methods=['GET'])
@jwt_required
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
        return error_response('analytics_error', str(e), status_code=500)


@analytics_bp.route('/analytics/me/breakdown', methods=['GET'])
@jwt_required
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
        return error_response('analytics_error', str(e), status_code=500)
