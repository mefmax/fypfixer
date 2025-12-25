"""
BlockedCreator model for tracking creators user has blocked.
"""

from app import db
from sqlalchemy.sql import func


class BlockedCreator(db.Model):
    """Tracks creators that user has blocked (toxic detection)."""

    __tablename__ = 'blocked_creators'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    creator_username = db.Column(db.String(256), nullable=False)
    blocked_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    reason = db.Column(db.Text, nullable=True)

    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'creator_username', name='unique_user_blocked_creator'),
    )

    # Relationships
    user = db.relationship('User', backref=db.backref('blocked_creators', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'creator_username': self.creator_username,
            'blocked_at': self.blocked_at.isoformat() if self.blocked_at else None,
            'reason': self.reason,
        }
