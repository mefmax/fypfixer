"""
RecommendationService - Main orchestrator for AI-powered plan generation.
"""

import time
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Any

from app import db
from app.models import Plan, Action, Category, UserProgress
from app.models import UserBehaviorStats, UserRecommendation, MessageTemplate
from app.ai_providers import get_ai_provider
from app.ai_providers.base import UserContext, SelectedAction
from app.config import get_seed_creators, ACTION_LIMITS, DIFFICULTY
from app.services.analytics_service import analytics_service
from app.services.settings_service import settings_service


class RecommendationService:
    """Main service for generating AI-powered daily plans."""

    def __init__(self):
        self._ai_provider = None

    @property
    def ai_provider(self):
        if self._ai_provider is None:
            self._ai_provider = get_ai_provider()
        return self._ai_provider

    def _get_default_category(self) -> str:
        """Get default category from settings."""
        return settings_service.get_default_category_code() or 'fitness'

    def generate_daily_plan(
        self,
        user_id: Optional[int],
        category_code: str = None,
        language: str = 'en',
        force_regenerate: bool = False
    ) -> Dict[str, Any]:
        """Generate a personalized daily plan."""

        start_time = time.time()

        # Use default category if not provided
        if not category_code:
            category_code = self._get_default_category()

        try:
            # 1. Get category
            category = Category.query.filter_by(code=category_code, is_active=True).first()
            if not category:
                return self._error('category_not_found', f"Category '{category_code}' not found")

            # 2. Check cache
            if not force_regenerate:
                cached = self._get_cached_plan(user_id, category.id, language)
                if cached:
                    return self._format_response(cached, category, user_id, language, 'cache', 0)

            # 3. Build context
            context = self._build_context(user_id, category_code, language)

            # 4. Execute pipeline
            plan, source = self._execute_pipeline(user_id, category, context, language)

            # 5. Log and return
            gen_time = int((time.time() - start_time) * 1000)
            self._log_recommendation(user_id, category_code, context, plan, source, gen_time)

            # Track analytics event
            actions = Action.query.filter_by(plan_id=plan.id).all()
            analytics_service.track_event(
                analytics_service.EVENT_PLAN_GENERATED,
                user_id=user_id,
                properties={
                    'category': category_code,
                    'source': source,
                    'actions_count': len(actions),
                    'generation_time_ms': gen_time,
                }
            )

            return self._format_response(plan, category, user_id, language, source, gen_time)

        except Exception as e:
            print(f"RecommendationService error: {e}")
            return self._error('generation_failed', str(e))

    def _execute_pipeline(self, user_id, category, context, language):
        """Execute AI recommendation pipeline."""
        source = 'ai'

        try:
            criteria = self.ai_provider.generate_criteria(context)
            candidates = self._get_seed_candidates(category.code)
            selected = self.ai_provider.select_actions(candidates, context, context.difficulty)
        except Exception as e:
            print(f"AI failed: {e}, using seed")
            source = 'seed'
            selected = self._get_seed_actions(category.code, ACTION_LIMITS['default_count'])

        plan = self._create_plan(user_id, category, selected, language, source)
        return plan, source

    def _build_context(self, user_id, category_code, language) -> UserContext:
        """Build user context for AI."""
        context = UserContext(
            category=category_code,
            language=language,
            time_of_day=self._get_time_of_day(),
        )

        if user_id:
            stats = db.session.get(UserBehaviorStats, user_id)
            if stats:
                context.streak_days = stats.current_streak_days or 0
                context.difficulty = stats.current_difficulty or DIFFICULTY['default']

        return context

    def _get_time_of_day(self) -> str:
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        else:
            return 'evening'

    def _create_plan(self, user_id, category, actions, language, source) -> Plan:
        """Create plan with actions in database."""
        plan = Plan(
            user_id=user_id,
            category_id=category.id,
            plan_date=date.today(),
            language=language,
            title=f"Daily {category.name_en} Plan",
            is_active=True,
            is_template=False,
        )
        db.session.add(plan)
        db.session.flush()

        for i, sel in enumerate(actions):
            is_neg = sel.type == 'not_interested'
            action = Action(
                plan_id=plan.id,
                action_type=sel.type,
                action_category='negative' if is_neg else 'positive',
                target_type='content_type' if is_neg else 'creator',
                target_name=sel.creator_username or sel.description,
                target_description=sel.description,
                target_thumbnail_url=sel.thumbnail_url,
                target_tiktok_url=sel.tiktok_url,
                sort_order=i + 1,
                source=source,
                reason=sel.reason,
            )
            db.session.add(action)

        db.session.commit()
        return plan

    def _get_cached_plan(self, user_id, category_id, language):
        """Get cached plan for today."""
        q = Plan.query.filter_by(
            category_id=category_id,
            plan_date=date.today(),
            language=language,
            is_active=True,
        )
        if user_id:
            q = q.filter_by(user_id=user_id)
        return q.first()

    def _get_seed_candidates(self, category_code: str) -> List[Dict]:
        """Get seed data as candidates from config."""
        return get_seed_creators(category_code)

    def _get_seed_actions(self, category_code: str, count: int) -> List[SelectedAction]:
        """Get hardcoded seed actions."""
        candidates = self._get_seed_candidates(category_code)
        actions = []
        types = ['follow', 'like', 'save', 'like', 'not_interested']

        for i, c in enumerate(candidates[:count]):
            t = types[i % len(types)]
            if t == 'not_interested':
                actions.append(SelectedAction(
                    type='not_interested', video_id=None, creator_username='',
                    creator_display_name='', description='Dance or meme video',
                    thumbnail_url=None, tiktok_url=None,
                    reason='Mark "Not interested" on unwanted content'
                ))
            else:
                actions.append(SelectedAction(
                    type=t, video_id=None, creator_username=c['creator_username'],
                    creator_display_name=c['creator_display_name'], description=c['description'],
                    thumbnail_url=None, tiktok_url=c['tiktok_url'],
                    reason=f"Verified creator with {c['followers']:,} followers"
                ))
        return actions

    def _log_recommendation(self, user_id, category_code, context, plan, source, gen_time):
        """Log to user_recommendations."""
        try:
            actions = Action.query.filter_by(plan_id=plan.id).all()
            log = UserRecommendation(
                user_id=user_id, plan_date=date.today(), category_code=category_code,
                search_criteria=context.to_dict(),
                selected_actions=[a.to_dict() for a in actions],
                ai_provider=self.ai_provider.name, generation_time_ms=gen_time,
                success=True, source=source,
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            print(f"Log failed: {e}")
            db.session.rollback()

    def _format_response(self, plan, category, user_id, language, source, gen_time):
        """Format plan for API response."""
        actions = Action.query.filter_by(plan_id=plan.id).order_by(Action.sort_order).all()

        # OPTIMIZATION: Load all progress in ONE query instead of N+1
        progress_map = {}
        if user_id and actions:
            action_ids = [a.id for a in actions]
            progress_list = UserProgress.query.filter(
                UserProgress.user_id == user_id,
                UserProgress.action_id.in_(action_ids)
            ).all()
            progress_map = {p.action_id: p for p in progress_list}

        completed_count = len(progress_map)
        total_count = len(actions)
        progress = {'completed': completed_count, 'total': total_count}

        pct = int(progress['completed'] / progress['total'] * 100) if progress['total'] > 0 else 0
        motivation = MessageTemplate.find_best_match('progress', {'progress_pct': pct}, language)
        if not motivation:
            context = UserContext(category=category.code, language=language, time_of_day=self._get_time_of_day())
            motivation = self.ai_provider.generate_motivation(context, progress)

        return {
            'success': True,
            'data': {
                'id': f'plan-{plan.id}',
                'date': str(plan.plan_date),
                'categoryCode': category.code,
                'categoryName': category.name_en,
                'actions': [self._format_action(a, progress_map.get(a.id)) for a in actions],
                'motivation': motivation,
                'progress': progress,
                'metadata': {
                    'source': source,
                    'generatedAt': datetime.utcnow().isoformat() + 'Z',
                    'provider': self.ai_provider.name,
                    'generationTimeMs': gen_time,
                }
            }
        }

    def _format_action(self, action, progress=None):
        """Format single action with optional progress."""
        completed = progress is not None
        completed_at = progress.completed_at.isoformat() if progress and progress.completed_at else None

        return {
            'id': f'action-{action.id}',
            'type': action.action_type,
            'category': action.action_category,
            'target': {
                'type': action.target_type,
                'name': action.target_name,
                'description': action.target_description,
                'thumbnailUrl': action.target_thumbnail_url,
                'tiktokUrl': action.target_tiktok_url,
            },
            'reason': action.reason,
            'completed': completed,
            'completedAt': completed_at,
        }


    def _error(self, code, message):
        return {'success': False, 'error': {'code': code, 'message': message}}


recommendation_service = RecommendationService()
