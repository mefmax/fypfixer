from app import db
from sqlalchemy.sql import func
from sqlalchemy import JSON


class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)

    # Onboarding
    has_completed_onboarding = db.Column(db.Boolean, default=False)
    selected_goals = db.Column(JSON, default=list)  # ['more-educational', 'less-doomscroll']

    # Preferences
    preferred_category = db.Column(db.String(50), default='personal_growth')
    language = db.Column(db.String(10), default='en')
    dark_mode = db.Column(db.Boolean, default=True)
    notifications_enabled = db.Column(db.Boolean, default=False)

    # Timestamps
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = db.relationship('User', backref=db.backref('preferences', uselist=False))
