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

    Response (camelCase for frontend compatibility):
    {
        "success": true,
        "data": {
            "streak": {"currentStreak": 5, "longestStreak": 12, "lastActiveDate": "2024-01-15", "nextMilestone": 7},
            "gamification": {"level": "Explorer", "xp": 250, "actionsCompleted": 45, "plansCompleted": 10}
        }
    }
    """
    user_id = g.current_user_id

    stats = streak_service.get_or_create_stats(user_id)
    streak_status = streak_service.check_streak_status(user_id)

    # Return camelCase fields to match frontend expectations
    return success_response({
        'streak': {
            'currentStreak': stats.current_streak_days,
            'longestStreak': stats.max_streak_days,
            'lastActiveDate': stats.last_completed_date.isoformat() if stats.last_completed_date else None,
            'nextMilestone': streak_status['nextMilestone'],
        },
        'gamification': {
            'level': stats.current_level,
            'xp': stats.total_xp,
            'actionsCompleted': stats.total_actions_completed,
            'plansCompleted': stats.total_days_active,
        },
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
