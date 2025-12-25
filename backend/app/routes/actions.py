from flask import Blueprint, request, g
import logging
from app.services.action_service import action_service
from app.services.settings_service import settings_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required, jwt_optional
from app.utils.errors import APIError
from app import limiter, READ_LIMIT, WRITE_LIMIT
from app.config.constants import DEFAULT_CATEGORY_CODE

logger = logging.getLogger(__name__)
actions_bp = Blueprint('actions', __name__)


@actions_bp.route('/actions', methods=['GET'])
@jwt_optional
@limiter.limit(READ_LIMIT)
def get_daily_actions():
    """
    Get daily action plan
    Query params:
    - category: category code (default: from settings)
    - lang: language (default: en)

    If authenticated, returns completed status for each action.
    """
    try:
        default_category = settings_service.get_default_category_code() or DEFAULT_CATEGORY_CODE
        result = action_service.get_daily_actions(
            category_code=request.args.get('category', default_category),
            language=request.args.get('lang', 'en'),
            user_id=g.current_user_id
        )
        return success_response(result)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)
    except Exception as e:
        logger.exception("Failed to get daily actions")
        return error_response('server_error', 'Failed to load actions', status_code=500)


@actions_bp.route('/actions/<action_id>/complete', methods=['POST'])
@jwt_required
@limiter.limit(WRITE_LIMIT)
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
        logger.exception("Failed to complete action")
        return error_response('server_error', 'Failed to complete action', status_code=500)


@actions_bp.route('/actions/<action_id>/uncomplete', methods=['POST'])
@jwt_required
@limiter.limit(WRITE_LIMIT)
def uncomplete_action(action_id):
    """
    Mark action as not completed (undo completion)
    Requires authentication
    """
    try:
        result = action_service.uncomplete_action(g.current_user_id, action_id)
        return success_response(result)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)
    except Exception as e:
        logger.exception("Failed to uncomplete action")
        return error_response('server_error', 'Failed to uncomplete action', status_code=500)
