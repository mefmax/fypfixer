"""
Plans V2 API - New plan structure, toxic creators, curation, and favorites.

Endpoints:
- POST /api/v2/plan/generate - Generate plan v2.0 (Clear/Watch/Reinforce)
- GET /api/v2/toxic-creators - Get list of toxic creators for user
- GET /api/v2/curated-videos - Get curated videos for Watch step
- GET /api/v2/favorites - Get user's favorite videos
- POST /api/v2/favorites - Add video to favorites
- DELETE /api/v2/favorites - Remove video from favorites
"""

import logging
from flask import Blueprint, request, g

from app import limiter, WRITE_LIMIT, READ_LIMIT, HEAVY_LIMIT
from app.models import Category
from app.services.toxic_detection_service import toxic_detection_service
from app.services.curation_service import curation_service
from app.services.favorites_service import favorites_service
from app.services.plan_service_v2 import plan_service_v2
from app.services.analytics_service import analytics_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required

logger = logging.getLogger(__name__)
plans_v2_bp = Blueprint('plans_v2', __name__)


# ============ PLAN GENERATION ============

@plans_v2_bp.route('/plan/generate', methods=['POST'])
@limiter.limit(HEAVY_LIMIT)  # 5/min - heavy operation
@jwt_required
def generate_plan():
    """
    Generate a plan v2.0 with Clear/Watch/Reinforce steps.

    Request body:
    {
        "category": "fitness"  // category slug or ID
    }

    Returns:
    {
        "success": true,
        "data": {
            "plan": {
                "plan_id": "uuid",
                "day_of_challenge": 3,
                "steps": {
                    "clear": {...},
                    "watch": {...},
                    "reinforce": {...}
                }
            }
        }
    }
    """
    try:
        user_id = g.current_user_id
        data = request.get_json() or {}

        category_param = data.get('category')
        if not category_param:
            return error_response('validation_error', 'category is required', status_code=400)

        # Look up category by slug or ID
        category = None
        if isinstance(category_param, int) or category_param.isdigit():
            category = Category.query.get(int(category_param))
        else:
            category = Category.query.filter_by(slug=category_param).first()
            if not category:
                category = Category.query.filter_by(code=category_param).first()

        if not category:
            return error_response('not_found', f"Category '{category_param}' not found", status_code=404)

        # Generate plan
        plan = plan_service_v2.generate_plan(
            user_id=user_id,
            category_id=category.id,
            category_slug=category.slug or category.code
        )

        # Track plan viewed event
        analytics_service.track(
            user_id=user_id,
            event_type='plan_viewed',
            event_data={
                'plan_id': plan.get('plan_id'),
                'day': plan.get('day_of_challenge')
            }
        )

        return success_response({
            'plan': plan
        })

    except Exception as e:
        logger.error(f"Error generating plan: {e}")
        return error_response('plan_error', str(e), status_code=500)


# ============ TOXIC CREATORS ============

@plans_v2_bp.route('/toxic-creators', methods=['GET'])
@limiter.limit(WRITE_LIMIT)  # 30/min as specified
@jwt_required
def get_toxic_creators():
    """
    Get list of toxic creators for the authenticated user.

    Query params:
    - category: Optional category filter (defaults to user's active category)
    - limit: Max number to return (default 5)

    Returns:
    {
        "success": true,
        "data": {
            "toxic_creators": [...],
            "count": N
        }
    }
    """
    try:
        user_id = g.current_user_id

        # Get optional category filter
        category_id = request.args.get('category', type=int)
        limit = request.args.get('limit', 5, type=int)
        limit = min(limit, 20)  # Cap at 20

        # Get toxic creators
        toxic_creators = toxic_detection_service.get_toxic_creators(
            user_id=user_id,
            category_id=category_id,
            limit=limit
        )

        return success_response({
            'toxic_creators': toxic_creators,
            'count': len(toxic_creators)
        })

    except Exception as e:
        logger.error(f"Error getting toxic creators: {e}")
        return error_response('toxic_error', str(e), status_code=500)


@plans_v2_bp.route('/toxic-creators/block', methods=['POST'])
@limiter.limit(WRITE_LIMIT)
@jwt_required
def block_creator():
    """
    Block a toxic creator.

    Request body:
    {
        "creator_username": "@username",
        "reason": "optional reason"
    }
    """
    try:
        user_id = g.current_user_id
        data = request.get_json() or {}

        creator_username = data.get('creator_username')
        if not creator_username:
            return error_response('validation_error', 'creator_username is required', status_code=400)

        reason = data.get('reason')

        success = toxic_detection_service.mark_creator_blocked(
            user_id=user_id,
            creator_username=creator_username,
            reason=reason
        )

        if success:
            return success_response({'blocked': True, 'creator_username': creator_username})
        else:
            return success_response({'blocked': False, 'message': 'Already blocked'})

    except Exception as e:
        logger.error(f"Error blocking creator: {e}")
        return error_response('block_error', str(e), status_code=500)


@plans_v2_bp.route('/toxic-creators/unblock', methods=['POST'])
@limiter.limit(WRITE_LIMIT)
@jwt_required
def unblock_creator():
    """
    Unblock a creator.

    Request body:
    {
        "creator_username": "@username"
    }
    """
    try:
        user_id = g.current_user_id
        data = request.get_json() or {}

        creator_username = data.get('creator_username')
        if not creator_username:
            return error_response('validation_error', 'creator_username is required', status_code=400)

        success = toxic_detection_service.unblock_creator(
            user_id=user_id,
            creator_username=creator_username
        )

        if success:
            return success_response({'unblocked': True, 'creator_username': creator_username})
        else:
            return error_response('not_found', 'Creator not found in blocked list', status_code=404)

    except Exception as e:
        logger.error(f"Error unblocking creator: {e}")
        return error_response('unblock_error', str(e), status_code=500)


@plans_v2_bp.route('/blocked-creators', methods=['GET'])
@limiter.limit(READ_LIMIT)
@jwt_required
def get_blocked_creators():
    """
    Get list of blocked creators for user.
    """
    try:
        user_id = g.current_user_id
        blocked = toxic_detection_service.get_blocked_creators(user_id)

        return success_response({
            'blocked_creators': blocked,
            'count': len(blocked)
        })

    except Exception as e:
        logger.error(f"Error getting blocked creators: {e}")
        return error_response('blocked_error', str(e), status_code=500)


# ============ CURATED VIDEOS ============

@plans_v2_bp.route('/curated-videos', methods=['GET'])
@limiter.limit(READ_LIMIT)
@jwt_required
def get_curated_videos():
    """
    Get curated videos for the Watch step.

    Query params:
    - category: Optional category ID filter
    - count: Number of videos (default 4, max 10)

    Returns:
    {
        "success": true,
        "data": {
            "videos": [...],
            "count": N
        }
    }
    """
    try:
        user_id = g.current_user_id

        # Get optional params
        category_id = request.args.get('category', type=int)
        count = request.args.get('count', 4, type=int)
        count = min(count, 10)  # Cap at 10

        # Get curated videos using service
        videos = curation_service.get_curated_videos(
            user_id=user_id,
            category_id=category_id,
            count=count
        )

        return success_response({
            'videos': videos,
            'count': len(videos)
        })

    except Exception as e:
        logger.error(f"Error getting curated videos: {e}")
        return error_response('curation_error', str(e), status_code=500)


# ============ FAVORITES ============

@plans_v2_bp.route('/favorites', methods=['GET'])
@limiter.limit(READ_LIMIT)
@jwt_required
def get_favorites():
    """
    Get user's favorite videos.

    Query params:
    - limit: Max number to return (default 10, max 50)

    Returns:
    {
        "success": true,
        "data": {
            "favorites": [...],
            "count": N
        }
    }
    """
    try:
        user_id = g.current_user_id
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 50)  # Cap at 50

        favorites = favorites_service.get_favorites(
            user_id=user_id,
            limit=limit
        )

        return success_response({
            'favorites': favorites,
            'count': len(favorites)
        })

    except Exception as e:
        logger.error(f"Error getting favorites: {e}")
        return error_response('favorites_error', str(e), status_code=500)


@plans_v2_bp.route('/favorites', methods=['POST'])
@limiter.limit(WRITE_LIMIT)
@jwt_required
def add_favorite():
    """
    Add a video to favorites.

    Request body:
    {
        "video_id": "abc123"
    }

    Returns success or already_exists.
    """
    try:
        user_id = g.current_user_id
        data = request.get_json() or {}

        video_id = data.get('video_id')
        if not video_id:
            return error_response('validation_error', 'video_id is required', status_code=400)

        result = favorites_service.add_favorite(
            user_id=user_id,
            video_id=video_id
        )

        if result.get('added'):
            return success_response({'added': True, 'video_id': video_id})
        else:
            return success_response({'added': False, 'message': 'Already in favorites'})

    except Exception as e:
        logger.error(f"Error adding favorite: {e}")
        return error_response('favorite_error', str(e), status_code=500)


@plans_v2_bp.route('/favorites', methods=['DELETE'])
@limiter.limit(WRITE_LIMIT)
@jwt_required
def remove_favorite():
    """
    Remove a video from favorites.

    Request body:
    {
        "video_id": "abc123"
    }
    """
    try:
        user_id = g.current_user_id
        data = request.get_json() or {}

        video_id = data.get('video_id')
        if not video_id:
            return error_response('validation_error', 'video_id is required', status_code=400)

        success = favorites_service.remove_favorite(
            user_id=user_id,
            video_id=video_id
        )

        if success:
            return success_response({'removed': True, 'video_id': video_id})
        else:
            return error_response('not_found', 'Video not in favorites', status_code=404)

    except Exception as e:
        logger.error(f"Error removing favorite: {e}")
        return error_response('favorite_error', str(e), status_code=500)


@plans_v2_bp.route('/favorites/random', methods=['GET'])
@limiter.limit(READ_LIMIT)
@jwt_required
def get_random_favorite():
    """
    Get a random favorite video for Reinforce step.

    Returns:
    {
        "success": true,
        "data": {
            "video": {...} or null
        }
    }
    """
    try:
        user_id = g.current_user_id

        video = favorites_service.get_random_favorite(user_id=user_id)

        return success_response({
            'video': video
        })

    except Exception as e:
        logger.error(f"Error getting random favorite: {e}")
        return error_response('favorite_error', str(e), status_code=500)
