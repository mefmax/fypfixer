"""
Challenge model for 7-day challenge tracking.
"""

from app import db
from sqlalchemy.sql import func


class Challenge(db.Model):
    """Tracks user's 7-day challenge progress."""

    __tablename__ = 'challenges'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    started_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    current_day = db.Column(db.Integer, default=1, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('challenges', lazy='dynamic'))
    category = db.relationship('Category', backref=db.backref('challenges', lazy='dynamic'))
    plans = db.relationship('Plan', backref='challenge', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'current_day': self.current_day,
            'is_active': self.is_active,
        }
