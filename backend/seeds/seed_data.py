"""
Seed data for FYPFixer database.
Run from backend folder: python -m seeds.seed_data
Or via init_db.py: python init_db.py
"""
from datetime import date


def seed_categories(db, Category):
    """Seed 8 categories (5 free + 3 premium)"""
    categories = [
        # Free categories
        {'code': 'personal_growth', 'name_en': 'Personal Growth', 'name_ru': 'Личное развитие', 'name_es': 'Crecimiento Personal', 'icon': '🎯', 'display_order': 1, 'is_premium': False},
        {'code': 'entertainment', 'name_en': 'Entertainment', 'name_ru': 'Развлечение', 'name_es': 'Entretenimiento', 'icon': '🎬', 'display_order': 2, 'is_premium': False},
        {'code': 'wellness', 'name_en': 'Wellness & Lifestyle', 'name_ru': 'Здоровье и Образ жизни', 'name_es': 'Bienestar y Estilo de vida', 'icon': '🧘', 'display_order': 3, 'is_premium': False},
        {'code': 'creative', 'name_en': 'Creative & Arts', 'name_ru': 'Творчество и Искусство', 'name_es': 'Creatividad y Arte', 'icon': '🎨', 'display_order': 4, 'is_premium': False},
        {'code': 'learning', 'name_en': 'Learning & Education', 'name_ru': 'Обучение и Образование', 'name_es': 'Aprendizaje y Educación', 'icon': '📚', 'display_order': 5, 'is_premium': False},
        # Premium categories
        {'code': 'science_tech', 'name_en': 'Science & Technology', 'name_ru': 'Наука и Технология', 'name_es': 'Ciencia y Tecnología', 'icon': '🔬', 'display_order': 6, 'is_premium': True},
        {'code': 'food', 'name_en': 'Food & Cooking', 'name_ru': 'Еда и Кулинария', 'name_es': 'Comida y Cocina', 'icon': '🍳', 'display_order': 7, 'is_premium': True},
        {'code': 'travel', 'name_en': 'Travel & Adventure', 'name_ru': 'Путешествия и Приключения', 'name_es': 'Viajes y Aventura', 'icon': '✈️', 'display_order': 8, 'is_premium': True},
    ]

    for cat_data in categories:
        existing = Category.query.filter_by(code=cat_data['code']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
            print(f"  ✓ Added category: {cat_data['code']}")
        else:
            print(f"  - Category exists: {cat_data['code']}")

    db.session.commit()
    return Category.query.all()


def seed_demo_plan(db, Category, Plan, PlanStep, StepItem):
    """Seed demo plan for personal_growth category"""
    category = Category.query.filter_by(code='personal_growth').first()
    if not category:
        print("  ✗ Category 'personal_growth' not found! Run seed_categories first.")
        return None

    # Check if demo plan exists
    existing = Plan.query.filter_by(
        category_id=category.id,
        is_template=True,
        language='en'
    ).first()

    if existing:
        print(f"  - Demo plan already exists (id={existing.id})")
        return existing

    # Create demo plan
    plan = Plan(
        category_id=category.id,
        plan_date=date.today(),
        language='en',
        is_template=True,
        title='Daily Personal Growth Plan',
        is_active=True
    )
    db.session.add(plan)
    db.session.flush()  # Get plan.id

    # Create steps with videos
    steps_data = [
        {
            'step_order': 1,
            'action_type': 'watch',
            'text_en': 'Watch these videos about personal growth',
            'text_ru': 'Посмотри эти видео о личном развитии',
            'text_es': 'Mira estos videos sobre crecimiento personal',
            'duration_minutes': 5,
            'items': [
                {
                    'video_id': '7288965558730713349',
                    'creator_username': '@growthcoach',
                    'title': '5 Habits to Change Your Life',
                    'thumbnail_url': 'https://p16-sign.tiktokcdn.com/obj/tos-maliva-p-0068/thumb1.jpg',
                    'video_url': 'https://www.tiktok.com/@growthcoach/video/7288965558730713349',
                    'engagement_score': 0.85,
                    'reason_text': 'High engagement, great for beginners'
                },
                {
                    'video_id': '7300442445678901234',
                    'creator_username': '@mindsetmastery',
                    'title': 'Morning Routine of Successful People',
                    'thumbnail_url': 'https://p16-sign.tiktokcdn.com/obj/tos-maliva-p-0068/thumb2.jpg',
                    'video_url': 'https://www.tiktok.com/@mindsetmastery/video/7300442445678901234',
                    'engagement_score': 0.78,
                    'reason_text': 'Practical tips, highly rated'
                },
                {
                    'video_id': '7295123456789012345',
                    'creator_username': '@lifeoptimizer',
                    'title': 'How to Set Goals That Stick',
                    'thumbnail_url': 'https://p16-sign.tiktokcdn.com/obj/tos-maliva-p-0068/thumb3.jpg',
                    'video_url': 'https://www.tiktok.com/@lifeoptimizer/video/7295123456789012345',
                    'engagement_score': 0.72,
                    'reason_text': 'Science-backed strategies'
                },
            ]
        },
        {
            'step_order': 2,
            'action_type': 'like',
            'text_en': 'Like your favorite video from the list',
            'text_ru': 'Лайкни своё любимое видео из списка',
            'text_es': 'Dale me gusta a tu video favorito',
            'duration_minutes': 1,
            'items': []
        },
        {
            'step_order': 3,
            'action_type': 'follow',
            'text_en': 'Follow 2 creators who inspire you',
            'text_ru': 'Подпишись на 2 авторов, которые тебя вдохновляют',
            'text_es': 'Sigue a 2 creadores que te inspiren',
            'duration_minutes': 2,
            'items': []
        },
    ]

    for step_data in steps_data:
        # Сохраняем step_order до pop
        step_order = step_data['step_order']
        action_type = step_data['action_type']
        items = step_data.pop('items')

        step = PlanStep(plan_id=plan.id, **step_data)
        db.session.add(step)
        db.session.flush()

        for item_data in items:
            item = StepItem(plan_step_id=step.id, **item_data)
            db.session.add(item)

        print(f"  ✓ Added step {step_order}: {action_type} ({len(items)} videos)")

    db.session.commit()
    print(f"  ✓ Created demo plan (id={plan.id})")
    return plan


def seed_actions(db, Plan, Action):
    """Seed actions for personal_growth demo plan"""
    # Get the demo plan
    plan = Plan.query.filter_by(is_template=True, language='en').first()
    if not plan:
        print("  ✗ Demo plan not found! Run seed_demo_plan first.")
        return

    # Check if actions already exist
    existing = Action.query.filter_by(plan_id=plan.id).first()
    if existing:
        print(f"  - Actions already exist for plan {plan.id}")
        return

    # Create actions (from BACKEND_API_SPEC_v2.md)
    actions_data = [
        {
            'action_type': 'follow',
            'action_category': 'positive',
            'target_type': 'creator',
            'target_name': '@jayshetty',
            'target_description': 'Мотивация, осознанность, привычки',
            'target_thumbnail_url': 'https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/placeholder.jpeg',
            'target_tiktok_url': 'https://www.tiktok.com/@jayshetty',
            'sort_order': 1
        },
        {
            'action_type': 'follow',
            'action_category': 'positive',
            'target_type': 'creator',
            'target_name': '@spencer.barbosa',
            'target_description': 'Self-care, уверенность, эмоциональное здоровье',
            'target_thumbnail_url': 'https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/placeholder.jpeg',
            'target_tiktok_url': 'https://www.tiktok.com/@spencer.barbosa',
            'sort_order': 2
        },
        {
            'action_type': 'like',
            'action_category': 'positive',
            'target_type': 'creator',
            'target_name': '@tabithabrown',
            'target_description': 'Забота о себе, позитивный настрой',
            'target_thumbnail_url': 'https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/placeholder.jpeg',
            'target_tiktok_url': 'https://www.tiktok.com/@tabithabrown',
            'sort_order': 3
        },
        {
            'action_type': 'not_interested',
            'action_category': 'negative',
            'target_type': 'content_type',
            'target_name': 'Танцевальные челленджи',
            'target_description': 'Видео с танцами без образовательной ценности',
            'target_thumbnail_url': None,
            'target_tiktok_url': None,
            'sort_order': 4
        },
        {
            'action_type': 'not_interested',
            'action_category': 'negative',
            'target_type': 'content_type',
            'target_name': 'Драма и скандалы',
            'target_description': 'Конфликты между блогерами, сплетни, негатив',
            'target_thumbnail_url': None,
            'target_tiktok_url': None,
            'sort_order': 5
        }
    ]

    for action_data in actions_data:
        action = Action(plan_id=plan.id, **action_data)
        db.session.add(action)
        print(f"  ✓ Added action: {action_data['action_type']} - {action_data['target_name']}")

    db.session.commit()
    print(f"  ✓ Created {len(actions_data)} actions for plan {plan.id}")


def run_seeds(app, db):
    """Run all seed functions within app context"""
    from app.models import Category, Plan, PlanStep, StepItem, Action

    with app.app_context():
        print("\n🌱 Seeding database...")

        print("\n📁 Categories:")
        seed_categories(db, Category)

        print("\n📋 Demo Plan:")
        seed_demo_plan(db, Category, Plan, PlanStep, StepItem)

        print("\n🎯 Actions:")
        seed_actions(db, Plan, Action)

        print("\n✅ Seeding complete!\n")


if __name__ == '__main__':
    # Standalone execution
    from app import create_app, db
    app = create_app('development')
    run_seeds(app, db)
