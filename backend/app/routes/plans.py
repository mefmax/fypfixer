from flask import Blueprint, request, g
from app.services import plan_service
from app.services.settings_service import settings_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required
from app.utils.errors import APIError

plans_bp = Blueprint('plans', __name__)

@plans_bp.route('/plans', methods=['GET'])
def get_plans():
    try:
        result = plan_service.get_plans(
            category_code=request.args.get('category'),
            language=request.args.get('language', 'en'),
            limit=min(int(request.args.get('limit', 20)), 100),
            offset=int(request.args.get('offset', 0))
        )
        return success_response(result)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)

@plans_bp.route('/plan', methods=['GET'])
def get_daily_plan():
    """Legacy endpoint for compatibility"""
    try:
        default_category = settings_service.get_default_category_code() or 'fitness'
        plan = plan_service.get_daily_plan(
            request.args.get('category', default_category),
            request.args.get('lang', 'en')
        )
        return success_response(plan)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)

@plans_bp.route('/plans/<int:plan_id>/steps/<int:step_id>/complete', methods=['POST'])
@jwt_required
def complete_step(plan_id, step_id):
    try:
        result = plan_service.complete_step(g.current_user_id, step_id)
        return success_response(result)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)
