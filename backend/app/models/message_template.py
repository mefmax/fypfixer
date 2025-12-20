"""Message template model for psychology-based motivation."""

from app import db
from sqlalchemy import JSON
from sqlalchemy.sql import func


class MessageTemplate(db.Model):
    """
    Psychology-based message templates.

    Categories:
    - progress: Based on completion percentage (0%, 20%, 40%, 60%, 80%, 100%)
    - streak: Based on streak milestones (3, 7, 14, 30 days)
    - time_of_day: Morning/afternoon/evening greetings
    - lapse: Recovery messages after inactivity
    - achievement: Unlock notifications

    Conditions stored as JSON for flexible matching.
    """
    __tablename__ = 'message_templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    template_key = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)

    # Localized messages
    message_en = db.Column(db.Text, nullable=False)
    message_ru = db.Column(db.Text, nullable=True)
    message_es = db.Column(db.Text, nullable=True)

    # Matching conditions
    conditions = db.Column(JSON, default=dict)
    # Examples:
    # {"progress_pct": 60}
    # {"streak_days": 7}
    # {"time_start": 6, "time_end": 12}
    # {"lapse_days_min": 3, "lapse_days_max": 7}

    # Presentation
    emoji = db.Column(db.String(20), nullable=True)
    tone = db.Column(db.String(30), nullable=True)  # energetic, calm, celebratory, encouraging, welcoming

    priority = db.Column(db.Integer, default=0)  # Higher = more important
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def get_message(self, language: str = 'en') -> str:
        """Get message in requested language with fallback to English."""
        if language == 'ru' and self.message_ru:
            return self.message_ru
        if language == 'es' and self.message_es:
            return self.message_es
        return self.message_en

    def get_formatted_message(self, language: str = 'en') -> str:
        """Get message with emoji prefix."""
        msg = self.get_message(language)
        if self.emoji:
            return f"{self.emoji} {msg}"
        return msg

    def matches_conditions(self, context: dict) -> bool:
        """Check if this template matches given context."""
        if not self.conditions:
            return True

        for key, value in self.conditions.items():
            if key not in context:
                return False

            ctx_value = context[key]

            # Handle range conditions
            if key.endswith('_min'):
                base_key = key[:-4]
                if ctx_value < value:
                    return False
            elif key.endswith('_max'):
                base_key = key[:-4]
                if ctx_value > value:
                    return False
            # Handle exact match
            elif ctx_value != value:
                return False

        return True

    def to_dict(self):
        return {
            'key': self.template_key,
            'category': self.category,
            'message': {
                'en': self.message_en,
                'ru': self.message_ru,
                'es': self.message_es,
            },
            'emoji': self.emoji,
            'tone': self.tone,
            'priority': self.priority,
        }

    @classmethod
    def find_best_match(cls, category: str, context: dict, language: str = 'en'):
        """Find best matching template for given context."""
        templates = cls.query.filter_by(
            category=category,
            is_active=True
        ).order_by(cls.priority.desc()).all()

        for template in templates:
            if template.matches_conditions(context):
                return template.get_formatted_message(language)

        return None
