"""
User Stats API - Streak and gamification endpoints.

Endpoints:
- GET /api/user/stats - Get user statistics
- GET /api/user/streak - Get streak info
"""

from flask import Blueprint, g
from app.services.streak_service import streak_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required

user_stats_bp = Blueprint('user_stats', __name__)


@user_stats_bp.route('/stats', methods=['GET'])
@jwt_required
def get_user_stats():
    """
    Get user statistics and gamification data.

    Response:
    {
        "success": true,
        "data": {
            "streak": {"current": 5, "max": 12, "status": "active"},
            "engagement": {"totalActions": 45, "totalDays": 10},
            "gamification": {"level": "Explorer", "xp": 250}
        }
    }
    """
    user_id = g.current_user_id

    stats = streak_service.get_or_create_stats(user_id)
    streak_status = streak_service.check_streak_status(user_id)

    return success_response({
        'streak': {
            'current': stats.current_streak_days,
            'max': stats.max_streak_days,
            'status': streak_status['status'],
            'nextMilestone': streak_status['next_milestone'],
        },
        'engagement': {
            'totalActions': stats.total_actions_completed,
            'totalDays': stats.total_days_active,
            'avgCompletionRate': float(stats.avg_completion_rate) if stats.avg_completion_rate else 0,
        },
        'gamification': {
            'level': stats.current_level,
            'xp': stats.total_xp,
            'achievements': stats.achievements or [],
        }
    })


@user_stats_bp.route('/streak', methods=['GET'])
@jwt_required
def get_streak():
    """
    Get streak info only (lighter endpoint).
    """
    user_id = g.current_user_id
    status = streak_service.check_streak_status(user_id)

    return success_response(status)


@user_stats_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Get top users by streak (public endpoint).
    """
    leaderboard = streak_service.get_leaderboard(limit=10)
    return success_response({'leaderboard': leaderboard})
