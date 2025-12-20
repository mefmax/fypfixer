"""
Recommendations API - AI-powered plan generation endpoints.

Endpoints:
- POST /api/v1/plans/generate - Generate new AI plan
- GET /api/v1/plans/today - Get today's plan (cached or new)
- GET /api/v1/plans/status - Get plan status only
"""

from flask import Blueprint, request, g
from app.services.recommendation_service import recommendation_service
from app.services.motivation_service import motivation_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required, jwt_optional

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/plans/generate', methods=['POST'])
@jwt_optional
def generate_plan():
    """
    Generate AI-powered daily plan.

    Request body:
    {
        "category": "personal_growth",  // optional
        "language": "en",               // optional
        "forceRegenerate": false        // optional
    }

    Response:
    {
        "success": true,
        "data": {
            "id": "plan-123",
            "date": "2025-12-18",
            "categoryCode": "personal_growth",
            "categoryName": "Personal Growth",
            "actions": [...],
            "motivation": "Your plan is ready!",
            "progress": {"completed": 0, "total": 5},
            "metadata": {...}
        }
    }
    """
    data = request.get_json() or {}

    result = recommendation_service.generate_daily_plan(
        user_id=getattr(g, 'current_user_id', None),
        category_code=data.get('category', 'personal_growth'),
        language=data.get('language', 'en'),
        force_regenerate=data.get('forceRegenerate', False),
    )

    if result.get('success'):
        return success_response(result['data'])
    else:
        return error_response(
            result['error']['code'],
            result['error']['message'],
            status_code=500
        )


@recommendations_bp.route('/plans/today', methods=['GET'])
@jwt_optional
def get_today_plan():
    """
    Get today's plan (returns cached if exists).

    Query params:
    - category: category code (default: personal_growth)
    - language: language code (default: en)
    """
    result = recommendation_service.generate_daily_plan(
        user_id=getattr(g, 'current_user_id', None),
        category_code=request.args.get('category', 'personal_growth'),
        language=request.args.get('language', 'en'),
        force_regenerate=False,  # Use cache
    )

    if result.get('success'):
        return success_response(result['data'])
    else:
        return error_response(
            result['error']['code'],
            result['error']['message'],
            status_code=500
        )


@recommendations_bp.route('/plans/status', methods=['GET'])
@jwt_optional
def get_plan_status():
    """
    Get current plan status (lighter response).

    Response:
    {
        "success": true,
        "data": {
            "hasPlan": true,
            "planId": "plan-123",
            "progress": {"completed": 2, "total": 5, "percentage": 40}
        }
    }
    """
    result = recommendation_service.generate_daily_plan(
        user_id=getattr(g, 'current_user_id', None),
        category_code=request.args.get('category', 'personal_growth'),
        language=request.args.get('language', 'en'),
        force_regenerate=False,
    )

    if result.get('success'):
        data = result['data']
        progress = data.get('progress', {'completed': 0, 'total': 5})
        pct = int(progress['completed'] / progress['total'] * 100) if progress['total'] > 0 else 0

        return success_response({
            'hasPlan': True,
            'planId': data['id'],
            'progress': {
                'completed': progress['completed'],
                'total': progress['total'],
                'percentage': pct,
            }
        })
    else:
        return success_response({
            'hasPlan': False,
            'planId': None,
            'progress': None,
        })
