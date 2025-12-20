from datetime import date
from app.models import Plan, Category, UserProgress
from app import db
from app.utils.errors import NotFoundError, APIError

class PlanService:
    def get_plans(self, category_code=None, language='en', limit=20, offset=0):
        query = Plan.query.filter_by(is_active=True, is_template=True, language=language)

        if category_code:
            cat = Category.query.filter_by(code=category_code, is_active=True).first()
            if cat:
                # Block premium categories (Coming Soon)
                if cat.is_premium:
                    raise APIError(
                        code='PREMIUM_COMING_SOON',
                        message=f'{cat.get_name(language)} is coming soon! Join the waitlist to get early access.',
                        status_code=403
                    )
                query = query.filter_by(category_id=cat.id)

        total = query.count()
        plans = query.order_by(Plan.created_at.desc()).offset(offset).limit(limit).all()

        return {
            'plans': [p.to_dict() for p in plans],
            'pagination': {'total': total, 'limit': limit, 'offset': offset}
        }

    def get_daily_plan(self, category_code, language='en'):
        category = Category.query.filter_by(code=category_code, is_active=True).first()
        if not category:
            raise NotFoundError('Category')

        # Block premium categories (Coming Soon)
        if category.is_premium:
            raise APIError(
                code='PREMIUM_COMING_SOON',
                message=f'{category.get_name(language)} is coming soon! Join the waitlist to get early access.',
                status_code=403
            )

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

        return plan.to_dict(include_steps=True)

    def complete_step(self, user_id, step_id):
        from datetime import datetime
        progress = UserProgress.query.filter_by(user_id=user_id, step_id=step_id).first()
        if not progress:
            progress = UserProgress(user_id=user_id, step_id=step_id)
            db.session.add(progress)
        progress.completed_at = datetime.utcnow()
        db.session.commit()
        return {'step_id': step_id, 'completed': True}
