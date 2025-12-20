from flask import Blueprint, request, g
from app.models import Category, PremiumWaitlist
from app.utils.responses import success_response
from app.services.cache_service import cache_service

categories_bp = Blueprint('categories', __name__)


def _get_base_categories(include_premium: bool, language: str) -> list:
    """Get categories from cache or DB."""
    cache_key = f"active_{include_premium}_{language}"

    # Try cache
    cached = cache_service.get(f"categories:{cache_key}")
    if cached:
        return cached

    # Build query
    query = Category.query.filter_by(is_active=True)
    if not include_premium:
        query = query.filter_by(is_premium=False)

    # Order by premium status first (free first), then by display_order
    categories = query.order_by(Category.is_premium, Category.display_order).all()

    # Convert to dict
    result = [cat.to_dict(language) for cat in categories]

    # Cache result (1 hour)
    cache_service.set(f"categories:{cache_key}", result, cache_service.TTL_CATEGORIES)

    return result


@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    """Return all categories with premium status and waitlist info"""
    language = request.args.get('language', 'en')
    include_premium = request.args.get('include_premium', 'true').lower() == 'true'

    # Get user_id if authenticated
    user_id = getattr(g, 'current_user_id', None)

    # Get base categories (cached)
    base_categories = _get_base_categories(include_premium, language)

    # If no user, return base categories directly
    if not user_id:
        return success_response({'categories': base_categories})

    # For authenticated users, add waitlist info
    # OPTIMIZATION: Load all waitlist entries in ONE query instead of N+1
    waitlist_entries = PremiumWaitlist.query.filter_by(user_id=user_id).all()
    waitlist_set = {w.category_id for w in waitlist_entries}

    # Add waitlist info to premium categories
    result = []
    for cat_data in base_categories:
        if cat_data.get('is_premium') and cat_data.get('coming_soon'):
            cat_data = {**cat_data, 'on_waitlist': cat_data['id'] in waitlist_set}
        result.append(cat_data)

    return success_response({'categories': result})
