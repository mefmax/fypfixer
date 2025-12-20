"""
UserCategory model - tracks user's category subscriptions.

Business rules:
- FREE categories: max 3, no expiration
- PREMIUM categories: unlimited, 14-day access from purchase
"""
from app import db
from sqlalchemy.sql import func
from datetime import datetime, timezone


class UserCategory(db.Model):
    __tablename__ = 'user_categories'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)

    is_active = db.Column(db.Boolean, default=True)
    purchased_at = db.Column(db.DateTime(timezone=True))
    expires_at = db.Column(db.DateTime(timezone=True))

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = db.relationship('User', backref=db.backref('user_categories', lazy='dynamic'))
    category = db.relationship('Category', backref=db.backref('user_categories', lazy='dynamic'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'category_id', name='uq_user_category'),
    )

    @property
    def is_expired(self) -> bool:
        """Check if premium category has expired."""
        if not self.expires_at:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def days_remaining(self) -> int | None:
        """Days until expiration (None for free categories)."""
        if not self.expires_at:
            return None
        delta = self.expires_at - datetime.now(timezone.utc)
        return max(0, delta.days)

    def to_dict(self):
        return {
            'id': self.id,
            'categoryId': self.category_id,
            'isActive': self.is_active and not self.is_expired,
            'isPremium': self.category.is_premium if self.category else False,
            'purchasedAt': self.purchased_at.isoformat() if self.purchased_at else None,
            'expiresAt': self.expires_at.isoformat() if self.expires_at else None,
            'daysRemaining': self.days_remaining,
            'isExpired': self.is_expired,
        }
