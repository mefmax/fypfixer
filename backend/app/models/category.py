from app import db
from sqlalchemy.sql import func

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.BigInteger, primary_key=True)
    # Legacy fields (keeping for backward compatibility)
    code = db.Column(db.String(32), unique=True, nullable=True)
    name_en = db.Column(db.Text, nullable=True)
    name_ru = db.Column(db.Text)
    name_es = db.Column(db.Text)
    icon = db.Column(db.String(10))
    # New premium fields
    name = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(50), unique=True, nullable=True)
    emoji = db.Column(db.String(10))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(5, 2), default=0)
    access_days = db.Column(db.Integer)
    # Common fields
    display_order = db.Column(db.Integer, default=0)
    is_premium = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def get_name(self, lang='en'):
        # Prefer new name field, fallback to multilingual
        if self.name:
            return self.name
        return getattr(self, f'name_{lang}', self.name_en) or self.name_en

    def to_dict(self, lang='en', on_waitlist=None):
        """
        Convert category to dict.

        Args:
            lang: Language code for name
            on_waitlist: Pre-computed waitlist status (avoids N+1 queries).
                         Pass None to exclude from response, or True/False for status.
        """
        result = {
            'id': self.id,
            'slug': self.slug or self.code,
            'name': self.get_name(lang),
            'emoji': self.emoji or self.icon,
            'description': self.description,
            'is_premium': self.is_premium,
            'price': float(self.price) if self.price else 0,
            'access_days': self.access_days,
            'coming_soon': self.is_premium,  # All premium are coming soon for now
        }

        # Add waitlist status only if explicitly provided (pre-computed by caller)
        if on_waitlist is not None:
            result['on_waitlist'] = on_waitlist
        elif self.is_premium:
            result['on_waitlist'] = False  # Default for premium categories

        return result
