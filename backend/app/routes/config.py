"""
Config API - public application settings for frontend.

Endpoints:
- GET /api/config/defaults - get public app settings
"""

from flask import Blueprint
from app.services.settings_service import settings_service
from app.utils.responses import success_response

config_bp = Blueprint('config', __name__)


@config_bp.route('/config/defaults', methods=['GET'])
def get_defaults():
    """
    Get public application settings.

    Response:
    {
        "success": true,
        "data": {
            "defaultCategoryCode": "fitness",
            "maxFreeCategories": 3,
            "premiumAccessDays": 14,
            "actionsPerPlan": 5
        }
    }
    """
    public_settings = settings_service.get_public_settings()
    default_category = settings_service.get_default_category_code()

    return success_response({
        'defaultCategoryCode': default_category,
        'maxFreeCategories': public_settings.get('max_free_categories', 3),
        'premiumAccessDays': public_settings.get('premium_access_days', 14),
        'actionsPerPlan': public_settings.get('actions_per_plan', 5),
    })
