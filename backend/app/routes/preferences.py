"""User Preferences API."""

from flask import Blueprint, request, g
from app import db
from app.models import UserPreferences
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required
from app.services.analytics_service import analytics_service
from app.services.settings_service import settings_service
from app.config.constants import DEFAULT_CATEGORY_CODE

preferences_bp = Blueprint('preferences', __name__)


def _get_default_category() -> str:
    """Get default category from settings."""
    return settings_service.get_default_category_code() or DEFAULT_CATEGORY_CODE


@preferences_bp.route('/preferences', methods=['GET'])
@jwt_required
def get_preferences():
    """Get user preferences."""
    prefs = UserPreferences.query.filter_by(user_id=g.current_user_id).first()

    if not prefs:
        return success_response({
            'hasCompletedOnboarding': False,
            'selectedGoals': [],
            'preferredCategory': _get_default_category(),
            'language': 'en',
        })

    return success_response({
        'hasCompletedOnboarding': prefs.has_completed_onboarding,
        'selectedGoals': prefs.selected_goals or [],
        'preferredCategory': prefs.preferred_category,
        'language': prefs.language,
    })


@preferences_bp.route('/preferences', methods=['PUT'])
@jwt_required
def update_preferences():
    """Update user preferences."""
    data = request.get_json() or {}

    prefs = UserPreferences.query.filter_by(user_id=g.current_user_id).first()
    if not prefs:
        prefs = UserPreferences(user_id=g.current_user_id)
        db.session.add(prefs)

    if 'selectedGoals' in data:
        prefs.selected_goals = data['selectedGoals']
    if 'preferredCategory' in data:
        prefs.preferred_category = data['preferredCategory']
    if 'language' in data:
        prefs.language = data['language']
    if 'hasCompletedOnboarding' in data:
        prefs.has_completed_onboarding = data['hasCompletedOnboarding']

    db.session.commit()

    return success_response({
        'hasCompletedOnboarding': prefs.has_completed_onboarding,
        'selectedGoals': prefs.selected_goals,
        'preferredCategory': prefs.preferred_category,
        'language': prefs.language,
    })


@preferences_bp.route('/preferences/complete-onboarding', methods=['POST'])
@jwt_required
def complete_onboarding():
    """Mark onboarding complete with selected goals."""
    data = request.get_json() or {}
    goals = data.get('goals', [])
    category = data.get('category', _get_default_category())

    prefs = UserPreferences.query.filter_by(user_id=g.current_user_id).first()
    if not prefs:
        prefs = UserPreferences(user_id=g.current_user_id)
        db.session.add(prefs)

    prefs.selected_goals = goals
    prefs.preferred_category = category
    prefs.has_completed_onboarding = True

    db.session.commit()

    # Track onboarding completion
    analytics_service.track_event(
        analytics_service.EVENT_ONBOARDING_COMPLETED,
        user_id=g.current_user_id,
        properties={
            'goals_count': len(goals),
            'selected_goals': goals,
            'category': category,
        }
    )

    return success_response({
        'message': 'Onboarding completed',
        'redirectTo': '/dashboard',
    })
