from flask import Blueprint, request, g
import logging
from app.services.action_service import action_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required, jwt_optional
from app.utils.errors import APIError

actions_bp = Blueprint('actions', __name__)


@actions_bp.route('/actions', methods=['GET'])
@jwt_optional
def get_daily_actions():
    """
    Get daily action plan
    Query params:
    - category: category code (default: personal_growth)
    - lang: language (default: en)

    If authenticated, returns completed status for each action.
    """
    try:
        result = action_service.get_daily_actions(
            category_code=request.args.get('category', 'personal_growth'),
            language=request.args.get('lang', 'en'),
            user_id=g.current_user_id
        )
        return success_response(result)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return error_response('server_error', 'Internal server error', status_code=500)


@actions_bp.route('/actions/<action_id>/complete', methods=['POST'])
@jwt_required
def complete_action(action_id):
    """
    Mark action as completed
    Requires authentication
    """
    try:
        result = action_service.complete_action(g.current_user_id, action_id)
        return success_response(result)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return error_response('server_error', 'Internal server error', status_code=500)
