import logging
from datetime import datetime
from flask import Blueprint, request, g
from app.services import plan_service
from app.services.settings_service import settings_service
from app.services.cache_service import cache_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required
from app.utils.errors import APIError

logger = logging.getLogger(__name__)
plans_bp = Blueprint('plans', __name__)


# =============================================================================
# AI-POWERED GUIDED PLAN (v4.2)
# =============================================================================

@plans_bp.route('/plan/guided', methods=['GET'])
@jwt_required
def get_guided_plan():
    """
    Get AI-generated personalized plan for today.

    Returns:
        GuidedPlanResponse with steps, motivation, and streak info
    """
    from app.models.user import User
    from app.models.user_category import UserCategory
    from app.models.category import Category

    try:
        # Get current user
        user = User.query.get(g.current_user_id)
        if not user:
            return error_response('user_not_found', 'User not found', status_code=404)

        # Get user's active categories
        user_categories = UserCategory.query.filter_by(
            user_id=user.id,
            is_active=True
        ).all()

        category_names = []
        for uc in user_categories:
            if uc.category and not uc.is_expired:
                name = uc.category.get_name(user.language or 'ru')
                category_names.append(name)

        # Default category if none selected
        if not category_names:
            category_names = ['Общее развитие']

        # Get streak (placeholder - no streak field yet)
        streak_current = getattr(user, 'streak_current', 0) or 0
        streak_best = getattr(user, 'streak_best', 0) or 0

        # Create cache key from categories
        cache_category = ','.join(sorted(category_names))

        # Check cache first
        cached_response = cache_service.get_guided_plan(user.id, cache_category)
        if cached_response:
            logger.info(f"Returning cached plan for user {user.id}")
            # Update streak info in cached response (might have changed)
            cached_response['streak'] = {
                'current': streak_current,
                'best': streak_best
            }
            cached_response['from_cache'] = True
            return success_response(cached_response)

        # Generate plan via AI (cache miss)
        try:
            from app.ai_providers import get_ai_provider

            provider = get_ai_provider()
            logger.info(f"Generating plan with {provider.name} for user {user.id}")

            if provider.is_available():
                plan_data = provider.generate_plan(
                    categories=category_names,
                    display_name=user.display_name or 'друг',
                    streak=streak_current,
                    language=user.language or 'ru',
                    user_id=user.id
                )
                logger.info(f"AI plan generated successfully")
            else:
                logger.warning(f"AI provider {provider.name} not available, using fallback")
                plan_data = _get_fallback_plan(category_names, user.display_name, streak_current)

        except Exception as e:
            logger.error(f"AI plan generation failed: {e}")
            plan_data = _get_fallback_plan(category_names, user.display_name, streak_current)

        # Build response
        steps = plan_data.get('steps', [])
        for step in steps:
            step['completed'] = False

        response = {
            'id': f"plan_{user.id}_{datetime.now().strftime('%Y%m%d')}",
            'steps': steps,
            'total_duration_minutes': sum(s.get('duration_minutes', 0) for s in steps),
            'completion_rate': 0.0,
            'motivation': plan_data.get('motivation', _get_default_motivation(user.display_name, streak_current)),
            'streak': {
                'current': streak_current,
                'best': streak_best
            },
            'generated_at': datetime.utcnow().isoformat(),
            'from_cache': False
        }

        # Save to cache for 24 hours
        cache_service.set_guided_plan(user.id, cache_category, response)

        return success_response(response)

    except Exception as e:
        logger.error(f"Error in get_guided_plan: {e}")
        return error_response('plan_error', str(e), status_code=500)


def _get_fallback_plan(categories: list, display_name: str, streak: int) -> dict:
    """Fallback план если AI недоступен"""
    return {
        'motivation': _get_default_motivation(display_name, streak),
        'steps': [
            {
                'order': 1,
                'type': 'detox',
                'title': 'Очистка ленты',
                'description': 'Убираем нерелевантный контент из FYP',
                'instruction': "Пролистай 15 видео. На неинтересных нажми 'Не интересно'",
                'duration_minutes': 5,
                'target_count': 15
            },
            {
                'order': 2,
                'type': 'watch',
                'title': 'Качественный просмотр',
                'description': f"Смотрим контент по темам: {', '.join(categories)}",
                'instruction': 'Досмотри 3 видео до конца и поставь лайк',
                'duration_minutes': 10,
                'account_count': 3
            },
            {
                'order': 3,
                'type': 'browse',
                'title': 'Исследование',
                'description': 'Ищем новый интересный контент',
                'instruction': 'Поищи видео по хештегам из любимых категорий',
                'duration_minutes': 5
            }
        ]
    }


def _get_default_motivation(display_name: str, streak: int) -> dict:
    """Дефолтные мотивационные сообщения"""
    name = display_name or 'друг'

    if streak > 0:
        encouragement = f"Ты на {streak}-дневном streak! Продолжай в том же духе!"
    else:
        encouragement = "Начни свой первый streak сегодня!"

    return {
        'greeting': f"Привет, {name}! 👋 Вот твой план на сегодня",
        'tip': "Совет: досматривай видео до конца — это главный сигнал для алгоритма",
        'encouragement': encouragement
    }


# =============================================================================
# LEGACY ENDPOINTS
# =============================================================================

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
