"""
Seed data for FYPFixer database.
Run from backend folder: python -m seeds.seed_data
Or via init_db.py: python init_db.py
"""
from datetime import date


def seed_categories(db, Category):
    """Seed 12 categories (6 free + 6 premium) per niche strategy"""
    categories = [
        # ===== FREE CATEGORIES (mass market, viral growth) =====
        {
            'code': 'fitness',
            'name_en': 'Fitness & Gym',
            'name_ru': 'Фитнес',
            'icon': '💪',
            'emoji': '💪',
            'description': 'Workouts, training tips, gym motivation',
            'display_order': 1,
            'is_premium': False,
            'price': 0,
        },
        {
            'code': 'cooking',
            'name_en': 'Cooking & Recipes',
            'name_ru': 'Кулинария',
            'icon': '🍳',
            'emoji': '🍳',
            'description': 'Recipes, cooking hacks, food inspiration',
            'display_order': 2,
            'is_premium': False,
            'price': 0,
        },
        {
            'code': 'fashion',
            'name_en': 'Fashion & Style',
            'name_ru': 'Мода',
            'icon': '👗',
            'emoji': '👗',
            'description': 'Outfits, trends, style tips',
            'display_order': 3,
            'is_premium': False,
            'price': 0,
        },
        {
            'code': 'music',
            'name_en': 'Music & Production',
            'name_ru': 'Музыка',
            'icon': '🎵',
            'emoji': '🎵',
            'description': 'Music creation, production tips, artist content',
            'display_order': 4,
            'is_premium': False,
            'price': 0,
        },
        {
            'code': 'pets',
            'name_en': 'Pets & Animals',
            'name_ru': 'Питомцы',
            'icon': '🐕',
            'emoji': '🐕',
            'description': 'Pet care, cute animals, training tips',
            'display_order': 5,
            'is_premium': False,
            'price': 0,
        },
        {
            'code': 'gaming',
            'name_en': 'Gaming',
            'name_ru': 'Игры',
            'icon': '🎮',
            'emoji': '🎮',
            'description': 'Game clips, reviews, esports',
            'display_order': 6,
            'is_premium': False,
            'price': 0,
        },

        # ===== PREMIUM CATEGORIES (high monetization) =====
        {
            'code': 'finance',
            'name_en': 'Finance & Investing',
            'name_ru': 'Финансы',
            'icon': '💰',
            'emoji': '💰',
            'description': 'Personal finance, investing tips, money management',
            'display_order': 7,
            'is_premium': True,
            'price': 1.29,
            'access_days': 14,
        },
        {
            'code': 'coding',
            'name_en': 'Coding & Tech',
            'name_ru': 'Программирование',
            'icon': '💻',
            'emoji': '💻',
            'description': 'Programming tutorials, tech news, developer content',
            'display_order': 8,
            'is_premium': True,
            'price': 1.29,
            'access_days': 14,
        },
        {
            'code': 'books',
            'name_en': 'Books & Reading',
            'name_ru': 'Книги',
            'icon': '📚',
            'emoji': '📚',
            'description': 'Book recommendations, summaries, reading tips',
            'display_order': 9,
            'is_premium': True,
            'price': 0.99,
            'access_days': 14,
        },
        {
            'code': 'art',
            'name_en': 'Art & Design',
            'name_ru': 'Искусство',
            'icon': '🎨',
            'emoji': '🎨',
            'description': 'Digital art, design tutorials, creative inspiration',
            'display_order': 10,
            'is_premium': True,
            'price': 0.99,
            'access_days': 14,
        },
        {
            'code': 'wellness',
            'name_en': 'Wellness & Mental Health',
            'name_ru': 'Здоровье',
            'icon': '🧘',
            'emoji': '🧘',
            'description': 'Meditation, self-care, mental health tips',
            'display_order': 11,
            'is_premium': True,
            'price': 1.29,
            'access_days': 14,
        },
        {
            'code': 'science',
            'name_en': 'Science & Space',
            'name_ru': 'Наука',
            'icon': '🔬',
            'emoji': '🔬',
            'description': 'Science facts, space exploration, discoveries',
            'display_order': 12,
            'is_premium': True,
            'price': 0.99,
            'access_days': 14,
        },
    ]

    for cat_data in categories:
        existing = Category.query.filter_by(code=cat_data['code']).first()
        if existing:
            # Update existing category
            for key, value in cat_data.items():
                setattr(existing, key, value)
            print(f"  ✓ Updated category: {cat_data['code']}")
        else:
            # Create new category
            category = Category(**cat_data)
            db.session.add(category)
            print(f"  ✓ Added category: {cat_data['code']}")

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

    # Create actions with English descriptions
    actions_data = [
        {
            'action_type': 'follow',
            'action_category': 'positive',
            'target_type': 'creator',
            'target_name': '@jayshetty',
            'target_description': 'Motivation, mindfulness, purpose',
            'target_thumbnail_url': 'https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/placeholder.jpeg',
            'target_tiktok_url': 'https://www.tiktok.com/@jayshetty',
            'sort_order': 1
        },
        {
            'action_type': 'follow',
            'action_category': 'positive',
            'target_type': 'creator',
            'target_name': '@spencer.barbosa',
            'target_description': 'Self-care, confidence, emotional health',
            'target_thumbnail_url': 'https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/placeholder.jpeg',
            'target_tiktok_url': 'https://www.tiktok.com/@spencer.barbosa',
            'sort_order': 2
        },
        {
            'action_type': 'like',
            'action_category': 'positive',
            'target_type': 'creator',
            'target_name': '@tabithabrown',
            'target_description': 'Self-care, positive mindset',
            'target_thumbnail_url': 'https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/placeholder.jpeg',
            'target_tiktok_url': 'https://www.tiktok.com/@tabithabrown',
            'sort_order': 3
        },
        {
            'action_type': 'not_interested',
            'action_category': 'negative',
            'target_type': 'content_type',
            'target_name': 'Dance challenges',
            'target_description': 'Dance videos without educational value',
            'target_thumbnail_url': None,
            'target_tiktok_url': None,
            'sort_order': 4
        },
        {
            'action_type': 'not_interested',
            'action_category': 'negative',
            'target_type': 'content_type',
            'target_name': 'Drama and scandals',
            'target_description': 'Conflicts between influencers, gossip, negativity',
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
