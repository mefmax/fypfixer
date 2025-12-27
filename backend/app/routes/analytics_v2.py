"""
Analytics V2 API - Track user events.

Endpoints:
- POST /api/v2/analytics/track - Track an analytics event
"""

import logging
from flask import Blueprint, request, g

from app import limiter, WRITE_LIMIT
from app.services.analytics_service import analytics_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required

logger = logging.getLogger(__name__)
analytics_v2_bp = Blueprint('analytics_v2', __name__)

# Valid event types that frontend can send
VALID_EVENT_TYPES = {
    'detox_completed',
    'watch_completed',
    'reinforce_completed',
    'plan_completed',
    'video_liked',
    'video_shared',
    'creator_blocked',
    'creator_followed',
}


@analytics_v2_bp.route('/track', methods=['POST'])
@limiter.limit(WRITE_LIMIT)  # 30/min
@jwt_required
def track_event():
    """
    Track an analytics event from frontend.

    Request body:
    {
        "event_type": "detox_completed",
        "event_data": {
            "plan_id": "uuid",
            "blocked_creators_count": 3
        }
    }

    Valid event_types:
    - detox_completed
    - watch_completed
    - reinforce_completed
    - plan_completed
    - video_liked
    - video_shared
    - creator_blocked
    - creator_followed

    Returns:
    {
        "success": true,
        "data": {
            "tracked": true,
            "event_id": 123
        }
    }
    """
    try:
        user_id = g.current_user_id
        data = request.get_json() or {}

        event_type = data.get('event_type')
        if not event_type:
            return error_response('validation_error', 'event_type is required', status_code=400)

        if event_type not in VALID_EVENT_TYPES:
            return error_response(
                'validation_error',
                f"Invalid event_type. Valid types: {', '.join(sorted(VALID_EVENT_TYPES))}",
                status_code=400
            )

        event_data = data.get('event_data', {})

        # Track the event
        event = analytics_service.track(
            user_id=user_id,
            event_type=event_type,
            event_data=event_data
        )

        if event:
            return success_response({
                'tracked': True,
                'event_id': event.id
            })
        else:
            return error_response('tracking_error', 'Failed to track event', status_code=500)

    except Exception as e:
        logger.error(f"Error tracking event: {e}")
        return error_response('tracking_error', str(e), status_code=500)
