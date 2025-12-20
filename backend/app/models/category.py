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

    def to_dict(self, lang='en', include_waitlist=False, user_id=None):
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

        # Check if user is on waitlist (if requested and user_id provided)
        if include_waitlist and user_id and self.is_premium:
            from app.models.premium_waitlist import PremiumWaitlist
            on_waitlist = PremiumWaitlist.query.filter_by(
                user_id=user_id,
                category_id=self.id
            ).first()
            result['on_waitlist'] = on_waitlist is not None
        else:
            result['on_waitlist'] = False

        return result
