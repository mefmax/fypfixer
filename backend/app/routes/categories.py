from flask import Blueprint, request, g
from app.models import Category, PremiumWaitlist
from app.utils.responses import success_response

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    """Return all categories with premium status and waitlist info"""
    language = request.args.get('language', 'en')
    include_premium = request.args.get('include_premium', 'true').lower() == 'true'

    # Get user_id if authenticated
    user_id = getattr(g, 'current_user_id', None)

    # Build query
    query = Category.query.filter_by(is_active=True)
    if not include_premium:
        query = query.filter_by(is_premium=False)

    # Order by premium status first (free first), then by display_order
    categories = query.order_by(Category.is_premium, Category.display_order).all()

    # Convert to dict with waitlist info
    result = []
    for cat in categories:
        cat_data = cat.to_dict(language, include_waitlist=True, user_id=user_id)
        result.append(cat_data)

    return success_response({'categories': result})
