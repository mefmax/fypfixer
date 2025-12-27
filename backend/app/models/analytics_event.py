"""
Analytics Event model for tracking user events and actions.
"""

from app import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB


class AnalyticsEvent(db.Model):
    """Logs user events for analytics and insights."""

    __tablename__ = 'analytics_events'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    event_type = db.Column(db.String(50), nullable=False)
    event_data = db.Column(JSONB, server_default='{}', nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    user = db.relationship('User', backref=db.backref('analytics_events', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'event_data': self.event_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
