"""
Seed message templates for FYPFixer AI pipeline.
Psychology-based motivation messages for user engagement.
Run from backend folder: python -m seeds.seed_messages
"""


def seed_message_templates(db, MessageTemplate):
    """Seed ~16 psychology-based motivation message templates"""

    templates = [
        # === STREAK MESSAGES (Commitment/Consistency) ===
        {
            'template_key': 'streak_start',
            'category': 'streak',
            'message_en': 'Day 1 begins! Small steps lead to big changes.',
            'message_ru': 'День 1 начинается! Маленькие шаги ведут к большим переменам.',
            'conditions': {'streak_days': 1},
            'emoji': '🌱',
            'tone': 'encouraging'
        },
        {
            'template_key': 'streak_3_days',
            'category': 'streak',
            'message_en': '3 days strong! You\'re building a new habit.',
            'message_ru': '3 дня подряд! Ты формируешь новую привычку.',
            'conditions': {'streak_days': 3},
            'emoji': '🔥',
            'tone': 'celebratory'
        },
        {
            'template_key': 'streak_7_days',
            'category': 'streak',
            'message_en': 'One week! Your FYP algorithm is already learning.',
            'message_ru': 'Неделя! Алгоритм FYP уже учится под тебя.',
            'conditions': {'streak_days': 7},
            'emoji': '🎯',
            'tone': 'proud'
        },
        {
            'template_key': 'streak_14_days',
            'category': 'streak',
            'message_en': '2 weeks of dedication! You\'re transforming your feed.',
            'message_ru': '2 недели упорства! Ты трансформируешь свою ленту.',
            'conditions': {'streak_days': 14},
            'emoji': '⭐',
            'tone': 'proud'
        },
        {
            'template_key': 'streak_30_days',
            'category': 'streak',
            'message_en': '30 days! You\'ve mastered your TikTok algorithm.',
            'message_ru': '30 дней! Ты освоил алгоритм TikTok.',
            'conditions': {'streak_days': 30},
            'emoji': '🏆',
            'tone': 'triumphant'
        },

        # === COMPLETION MESSAGES (Achievement/Progress) ===
        {
            'template_key': 'action_complete_first',
            'category': 'completion',
            'message_en': 'First action done! Every step counts.',
            'message_ru': 'Первое действие выполнено! Каждый шаг важен.',
            'conditions': {'total_actions': 1},
            'emoji': '✅',
            'tone': 'encouraging'
        },
        {
            'template_key': 'action_complete_half',
            'category': 'completion',
            'message_en': 'Halfway there! Keep going, you\'re doing great.',
            'message_ru': 'Половина пути! Продолжай, ты молодец.',
            'conditions': {'progress_percent': 50},
            'emoji': '💪',
            'tone': 'motivating'
        },
        {
            'template_key': 'action_complete_all',
            'category': 'completion',
            'message_en': 'All done for today! Your future self thanks you.',
            'message_ru': 'Всё на сегодня! Твоё будущее я тебе благодарно.',
            'conditions': {'progress_percent': 100},
            'emoji': '🎉',
            'tone': 'celebratory'
        },

        # === COMEBACK MESSAGES (Re-engagement) ===
        {
            'template_key': 'comeback_1_day',
            'category': 'comeback',
            'message_en': 'Welcome back! Ready to continue your journey?',
            'message_ru': 'С возвращением! Готов продолжить путь?',
            'conditions': {'days_inactive': 1},
            'emoji': '👋',
            'tone': 'warm'
        },
        {
            'template_key': 'comeback_3_days',
            'category': 'comeback',
            'message_en': 'We missed you! Your FYP is waiting to improve.',
            'message_ru': 'Мы скучали! Твой FYP ждёт улучшений.',
            'conditions': {'days_inactive': 3},
            'emoji': '🌟',
            'tone': 'warm'
        },
        {
            'template_key': 'comeback_7_days',
            'category': 'comeback',
            'message_en': 'It\'s never too late to restart. Let\'s go!',
            'message_ru': 'Никогда не поздно начать заново. Вперёд!',
            'conditions': {'days_inactive': 7},
            'emoji': '🚀',
            'tone': 'encouraging'
        },

        # === DIFFICULTY MESSAGES (Adaptive Challenge) ===
        {
            'template_key': 'difficulty_easy',
            'category': 'difficulty',
            'message_en': 'Starting light today. Consistency beats intensity.',
            'message_ru': 'Сегодня полегче. Постоянство важнее интенсивности.',
            'conditions': {'difficulty_level': 'easy'},
            'emoji': '🌤️',
            'tone': 'calm'
        },
        {
            'template_key': 'difficulty_medium',
            'category': 'difficulty',
            'message_en': 'A balanced challenge awaits. You\'ve got this!',
            'message_ru': 'Сбалансированный вызов ждёт. У тебя получится!',
            'conditions': {'difficulty_level': 'medium'},
            'emoji': '⚡',
            'tone': 'confident'
        },
        {
            'template_key': 'difficulty_hard',
            'category': 'difficulty',
            'message_en': 'Ready for a challenge? Let\'s level up your feed!',
            'message_ru': 'Готов к вызову? Давай прокачаем твою ленту!',
            'conditions': {'difficulty_level': 'hard'},
            'emoji': '🔥',
            'tone': 'energetic'
        },

        # === ACHIEVEMENT MESSAGES (Gamification) ===
        {
            'template_key': 'achievement_first_week',
            'category': 'achievement',
            'message_en': 'Achievement Unlocked: First Week Warrior!',
            'message_ru': 'Достижение разблокировано: Воин Первой Недели!',
            'conditions': {'achievement': 'first_week'},
            'emoji': '🏅',
            'tone': 'celebratory'
        },
        {
            'template_key': 'achievement_perfect_day',
            'category': 'achievement',
            'message_en': 'Perfect Day! You completed everything!',
            'message_ru': 'Идеальный день! Ты выполнил всё!',
            'conditions': {'achievement': 'perfect_day'},
            'emoji': '💯',
            'tone': 'triumphant'
        },
    ]

    added_count = 0
    for template_data in templates:
        existing = MessageTemplate.query.filter_by(
            template_key=template_data['template_key']
        ).first()

        if not existing:
            template = MessageTemplate(**template_data)
            db.session.add(template)
            print(f"  ✓ Added message: {template_data['template_key']}")
            added_count += 1
        else:
            print(f"  - Message exists: {template_data['template_key']}")

    db.session.commit()
    print(f"\n  ✓ Added {added_count} new message templates")
    return MessageTemplate.query.all()


def run_message_seeds(app, db):
    """Run message template seeds within app context"""
    from app.models import MessageTemplate

    with app.app_context():
        print("\n📨 Seeding message templates...")
        seed_message_templates(db, MessageTemplate)
        print("\n✅ Message seeding complete!\n")


if __name__ == '__main__':
    # Standalone execution
    from app import create_app, db
    app = create_app('development')
    run_message_seeds(app, db)
