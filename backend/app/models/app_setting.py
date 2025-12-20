"""
AppSetting model for storing application configuration in database.

This allows changing business rules without code deployment:
- max_free_categories
- premium_access_days
- default_category_code
- rate limits
- etc.
"""

from app import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
import json


class AppSetting(db.Model):
    """Application settings stored in database for runtime configuration."""

    __tablename__ = 'app_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(JSONB, nullable=False)
    value_type = db.Column(db.String(20), default='string')  # string, int, float, bool, json
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)  # Can be exposed to frontend
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<AppSetting {self.key}={self.value}>'

    def get_typed_value(self):
        """Return value cast to appropriate type."""
        if self.value_type == 'int':
            return int(self.value)
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'bool':
            return bool(self.value)
        elif self.value_type == 'json':
            return self.value  # Already JSONB
        else:
            return str(self.value) if self.value else None

    def to_dict(self):
        return {
            'key': self.key,
            'value': self.get_typed_value(),
            'description': self.description,
        }

    @classmethod
    def get(cls, key: str, default=None):
        """Get setting value by key with optional default."""
        setting = cls.query.filter_by(key=key).first()
        if setting:
            return setting.get_typed_value()
        return default

    @classmethod
    def set(cls, key: str, value, value_type: str = 'string', description: str = None):
        """Set or update a setting."""
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            if value_type:
                setting.value_type = value_type
            if description:
                setting.description = description
        else:
            setting = cls(
                key=key,
                value=value,
                value_type=value_type,
                description=description
            )
            db.session.add(setting)
        db.session.commit()
        return setting

    @classmethod
    def get_public_settings(cls) -> dict:
        """Get all settings marked as public (for frontend)."""
        settings = cls.query.filter_by(is_public=True).all()
        return {s.key: s.get_typed_value() for s in settings}


# Default settings to seed
DEFAULT_SETTINGS = [
    {
        'key': 'max_free_categories',
        'value': 3,
        'value_type': 'int',
        'description': 'Maximum number of free categories a user can select',
        'is_public': True,
    },
    {
        'key': 'premium_access_days',
        'value': 14,
        'value_type': 'int',
        'description': 'Number of days premium category access lasts after purchase',
        'is_public': True,
    },
    {
        'key': 'default_category_code',
        'value': None,  # Will be set dynamically from DB
        'value_type': 'string',
        'description': 'Default category code for new users (null = first free category)',
        'is_public': True,
    },
    {
        'key': 'actions_per_plan',
        'value': 5,
        'value_type': 'int',
        'description': 'Default number of actions in a daily plan',
        'is_public': True,
    },
    {
        'key': 'min_actions_per_plan',
        'value': 3,
        'value_type': 'int',
        'description': 'Minimum actions in a plan',
        'is_public': False,
    },
    {
        'key': 'max_actions_per_plan',
        'value': 8,
        'value_type': 'int',
        'description': 'Maximum actions in a plan',
        'is_public': False,
    },
    {
        'key': 'jwt_access_expires_minutes',
        'value': 15,
        'value_type': 'int',
        'description': 'JWT access token expiration in minutes',
        'is_public': False,
    },
    {
        'key': 'jwt_refresh_expires_days',
        'value': 7,
        'value_type': 'int',
        'description': 'JWT refresh token expiration in days',
        'is_public': False,
    },
    {
        'key': 'rate_limit_per_day',
        'value': 200,
        'value_type': 'int',
        'description': 'API rate limit per day per user',
        'is_public': False,
    },
    {
        'key': 'rate_limit_per_hour',
        'value': 50,
        'value_type': 'int',
        'description': 'API rate limit per hour per user',
        'is_public': False,
    },
    {
        'key': 'cache_categories_ttl',
        'value': 3600,
        'value_type': 'int',
        'description': 'Categories cache TTL in seconds (1 hour)',
        'is_public': False,
    },
    {
        'key': 'cache_user_categories_ttl',
        'value': 300,
        'value_type': 'int',
        'description': 'User categories cache TTL in seconds (5 minutes)',
        'is_public': False,
    },
]
