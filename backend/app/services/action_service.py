from datetime import date, datetime
from app.models import Action, Plan, Category, UserProgress
from app import db
from app.utils.errors import NotFoundError
from app.services.streak_service import streak_service
from app.services.analytics_service import analytics_service
from app.services.settings_service import settings_service


class ActionService:
    def _get_default_category(self) -> str:
        """Get default category from settings."""
        return settings_service.get_default_category_code() or 'fitness'

    def get_daily_actions(self, category_code=None, language='en', user_id=None):
        """
        Get daily action plan for given category.
        Includes 'completed' status for each action if user_id provided.
        """
        # Use default category if not provided
        if not category_code:
            category_code = self._get_default_category()

        category = Category.query.filter_by(code=category_code, is_active=True).first()
        if not category:
            raise NotFoundError('Category')

        # Сначала ищем план на сегодня
        plan = Plan.query.filter_by(
            category_id=category.id,
            plan_date=date.today(),
            language=language,
            is_active=True
        ).first()

        # Если нет, берём template
        if not plan:
            plan = Plan.query.filter_by(
                category_id=category.id,
                is_template=True,
                language=language,
                is_active=True
            ).first()

        if not plan:
            raise NotFoundError('Plan')

        # Получаем actions для этого плана
        actions = Action.query.filter_by(plan_id=plan.id).order_by(Action.sort_order).all()

        # Get completed action IDs for this user
        completed_ids = set()
        if user_id:
            completed = UserProgress.query.filter_by(user_id=user_id).all()
            completed_ids = {progress.action_id for progress in completed}

        # Build response with completed status
        actions_list = []
        for action in actions:
            action_dict = action.to_dict()
            action_dict['completed'] = action.id in completed_ids
            actions_list.append(action_dict)

        return {
            'id': f'plan-{plan.id}',
            'date': str(plan.plan_date),
            'categoryCode': category_code,
            'categoryName': category.get_name(language),
            'actions': actions_list
        }

    def complete_action(self, user_id, action_id):
        """
        Mark action as completed by user.
        Updates progress and gamification stats.
        """
        # 1. Parse action_id (remove "action-" prefix)
        try:
            numeric_id = int(action_id.replace('action-', ''))
        except ValueError:
            raise NotFoundError('Action')

        # 2. Check if action exists
        action = db.session.get(Action, numeric_id)
        if not action:
            raise NotFoundError('Action')

        # 3. Check if already completed (idempotency)
        existing = UserProgress.query.filter_by(
            user_id=user_id,
            action_id=numeric_id
        ).first()

        if existing:
            return {
                'actionId': action_id,
                'completed': True,
                'completedAt': existing.completed_at.isoformat() + 'Z' if existing.completed_at else None
            }

        # 4. Create new progress record
        try:
            progress = UserProgress(
                user_id=user_id,
                action_id=numeric_id,
                completed_at=datetime.utcnow()
            )
            db.session.add(progress)
            db.session.flush()  # Get ID before commit

            # 5. UPDATE GAMIFICATION STATS
            gamification_result = streak_service.record_action_completion(
                user_id=user_id,
                action_type=action.action_type
            )

            # 6. Check if entire plan is completed
            plan_actions = Action.query.filter_by(plan_id=action.plan_id).all()
            plan_action_ids = [a.id for a in plan_actions]

            completed_count = UserProgress.query.filter(
                UserProgress.user_id == user_id,
                UserProgress.action_id.in_(plan_action_ids)
            ).count()

            plan_completed = False
            if completed_count >= len(plan_actions):
                # All actions done! Update streak
                streak_service.record_plan_completion(user_id)
                plan_completed = True

            db.session.commit()

            # Track action completion
            analytics_service.track_event(
                analytics_service.EVENT_ACTION_COMPLETED,
                user_id=user_id,
                properties={
                    'action_id': action_id,
                    'action_type': action.action_type,
                    'xp_earned': gamification_result.get('xp_earned', 0),
                }
            )

            # If plan completed, track that too
            if plan_completed:
                analytics_service.track_event(
                    analytics_service.EVENT_PLAN_COMPLETED,
                    user_id=user_id,
                    properties={
                        'plan_id': action.plan_id,
                        'actions_count': len(plan_actions),
                    }
                )

            return {
                'actionId': action_id,
                'completed': True,
                'completedAt': progress.completed_at.isoformat() + 'Z',
                'xpEarned': gamification_result.get('xp_earned', 0),
                'planCompleted': plan_completed,
            }

        except Exception as e:
            db.session.rollback()
            raise Exception(f'Failed to complete action: {str(e)}')

    def uncomplete_action(self, user_id, action_id):
        """
        Mark action as NOT completed (undo completion).
        Removes progress record.
        """
        # 1. Parse action_id (remove "action-" prefix)
        try:
            numeric_id = int(action_id.replace('action-', ''))
        except ValueError:
            raise NotFoundError('Action')

        # 2. Check if action exists
        action = db.session.get(Action, numeric_id)
        if not action:
            raise NotFoundError('Action')

        # 3. Find and delete progress record
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            action_id=numeric_id
        ).first()

        if not progress:
            # Already not completed - return success
            return {
                'actionId': action_id,
                'completed': False,
                'completedAt': None
            }

        try:
            db.session.delete(progress)
            db.session.commit()

            return {
                'actionId': action_id,
                'completed': False,
                'completedAt': None
            }

        except Exception as e:
            db.session.rollback()
            raise Exception(f'Failed to uncomplete action: {str(e)}')


# Singleton instance
action_service = ActionService()
