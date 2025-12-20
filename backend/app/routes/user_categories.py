"""
User categories routes - manage user's category subscriptions.

Endpoints:
- GET  /api/user/categories - get user's categories
- POST /api/user/categories - add category
- DELETE /api/user/categories/<id> - remove category
- GET  /api/user/categories/stats - get stats
"""
from flask import Blueprint, request, g
from app.services.user_category_service import user_category_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required
from app.utils.errors import APIError

user_categories_bp = Blueprint('user_categories', __name__)


@user_categories_bp.route('/user/categories', methods=['GET'])
@jwt_required
def get_my_categories():
    """
    Get user's category subscriptions.
    Query params:
    - include_inactive: bool (default: false)
    """
    include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'

    categories = user_category_service.get_user_categories(
        g.current_user_id,
        include_inactive=include_inactive
    )
    stats = user_category_service.get_category_stats(g.current_user_id)

    return success_response({
        'categories': categories,
        'stats': stats,
    })


@user_categories_bp.route('/user/categories', methods=['POST'])
@jwt_required
def add_category():
    """
    Add a category to user's list.
    Body: { "categoryId": int, "isPurchased": bool }
    """
    data = request.get_json() or {}
    category_id = data.get('categoryId')
    is_purchased = data.get('isPurchased', False)

    if not category_id:
        return error_response('validation_error', 'categoryId is required', status_code=400)

    try:
        result = user_category_service.add_category(
            g.current_user_id,
            category_id,
            is_purchased=is_purchased
        )
        return success_response(result)
    except APIError as e:
        return error_response(e.code, e.message, status_code=e.status_code)


@user_categories_bp.route('/user/categories/<int:category_id>', methods=['DELETE'])
@jwt_required
def remove_category(category_id):
    """Remove a category from user's list."""
    removed = user_category_service.remove_category(g.current_user_id, category_id)

    if removed:
        return success_response({'removed': True})
    else:
        return error_response('not_found', 'Category not in your list', status_code=404)


@user_categories_bp.route('/user/categories/stats', methods=['GET'])
@jwt_required
def get_category_stats():
    """Get category subscription stats."""
    stats = user_category_service.get_category_stats(g.current_user_id)
    return success_response(stats)
