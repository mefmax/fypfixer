"""
Admin Metrics API - Dashboard metrics for admin users.

Endpoints:
- GET /api/admin/metrics/overview - Users stats (DAU, new, total)
- GET /api/admin/metrics/challenge - Challenge funnel (D0->D7)
- GET /api/admin/metrics/plans - Step completion and signals
- GET /api/admin/metrics/system - API latency, errors, AI cost
"""

import logging
from functools import wraps
from flask import Blueprint, g

from app import limiter, READ_LIMIT
from app.models import User
from app.services.metrics_service import metrics_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required

logger = logging.getLogger(__name__)
admin_metrics_bp = Blueprint('admin_metrics', __name__)


def _is_admin(user_id: int) -> bool:
    """Check if user has admin role."""
    user = User.query.get(user_id)
    if user and hasattr(user, 'is_admin') and user.is_admin:
        return True
    # Fallback: check email domain
    if user and user.email and user.email.endswith('@fypglow.com'):
        return True
    return False


def admin_required(f):
    """Decorator to require admin access."""
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
    """Get user overview metrics."""
    try:
        data = metrics_service.get_overview_metrics()
        return success_response(data)
    except Exception as e:
        logger.exception("Error getting overview metrics")
        return error_response('metrics_error', 'Failed to load overview', status_code=500)


@admin_metrics_bp.route('/challenge', methods=['GET'])
@jwt_required
@admin_required
@limiter.limit(READ_LIMIT)
def get_challenge():
    """Get challenge funnel metrics."""
    try:
        data = metrics_service.get_challenge_metrics()
        return success_response(data)
    except Exception as e:
        logger.exception("Error getting challenge metrics")
        return error_response('metrics_error', 'Failed to load challenge funnel', status_code=500)


@admin_metrics_bp.route('/plans', methods=['GET'])
@jwt_required
@admin_required
@limiter.limit(READ_LIMIT)
def get_plans():
    """Get plan performance metrics."""
    try:
        data = metrics_service.get_plan_metrics()
        return success_response(data)
    except Exception as e:
        logger.exception("Error getting plan metrics")
        return error_response('metrics_error', 'Failed to load plan metrics', status_code=500)


@admin_metrics_bp.route('/system', methods=['GET'])
@jwt_required
@admin_required
@limiter.limit(READ_LIMIT)
def get_system():
    """Get system health metrics."""
    try:
        data = metrics_service.get_system_metrics()
        return success_response(data)
    except Exception as e:
        logger.exception("Error getting system metrics")
        return error_response('metrics_error', 'Failed to load system metrics', status_code=500)
