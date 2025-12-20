"""
Settings Service - centralized access to application settings.

Provides caching and easy access to app_settings table.
Falls back to defaults if database is unavailable.
Uses Redis for distributed caching.
"""

from typing import Any, Optional, Dict
from app.models.app_setting import AppSetting, DEFAULT_SETTINGS
from app import db
import logging

logger = logging.getLogger(__name__)

# In-memory cache for settings (refreshed periodically)
_settings_cache: Dict[str, Any] = {}
_cache_loaded = False


def _get_cache_service():
    """Lazy import cache service to avoid circular imports."""
    try:
        from app.services.cache_service import cache_service
        return cache_service
    except ImportError:
        return None


class SettingsService:
    """Service for accessing application settings."""

    # Hardcoded defaults (fallback if DB unavailable)
    DEFAULTS = {
        'max_free_categories': 3,
        'premium_access_days': 14,
        'default_category_code': None,
        'actions_per_plan': 5,
        'min_actions_per_plan': 3,
        'max_actions_per_plan': 8,
        'jwt_access_expires_minutes': 15,
        'jwt_refresh_expires_days': 7,
        'rate_limit_per_day': 200,
        'rate_limit_per_hour': 50,
        'cache_categories_ttl': 3600,
        'cache_user_categories_ttl': 300,
    }

    def __init__(self):
        # Lazy loading - don't load on init to avoid app context issues
        pass

    def _ensure_loaded(self):
        """Ensure cache is loaded (lazy loading)."""
        global _cache_loaded
        if not _cache_loaded:
            self._load_cache()

    def _load_cache(self):
        """Load all settings into memory cache."""
        global _settings_cache, _cache_loaded

        # Try Redis cache first
        cache = _get_cache_service()
        if cache:
            cached = cache.get_settings()
            if cached:
                _settings_cache = cached
                _cache_loaded = True
                logger.debug("Loaded settings from Redis cache")
                return

        # Load from database
        try:
            settings = AppSetting.query.all()
            _settings_cache = {s.key: s.get_typed_value() for s in settings}
            _cache_loaded = True
            logger.debug(f"Loaded {len(_settings_cache)} settings into cache")

            # Store in Redis
            if cache:
                cache.set_settings(_settings_cache)

        except Exception as e:
            logger.warning(f"Failed to load settings from DB: {e}")
            _settings_cache = self.DEFAULTS.copy()

    def refresh_cache(self):
        """Force refresh the settings cache."""
        global _cache_loaded
        _cache_loaded = False

        # Invalidate Redis cache
        cache = _get_cache_service()
        if cache:
            cache.invalidate_settings()

        self._load_cache()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value.

        Priority:
        1. Memory cache
        2. Database
        3. Hardcoded default
        4. Provided default
        """
        # Ensure cache is loaded
        self._ensure_loaded()

        # Try cache first
        if key in _settings_cache:
            return _settings_cache[key]

        # Try database
        try:
            value = AppSetting.get(key)
            if value is not None:
                _settings_cache[key] = value
                return value
        except Exception as e:
            logger.warning(f"DB error getting setting {key}: {e}")

        # Fallback to hardcoded defaults
        if key in self.DEFAULTS:
            return self.DEFAULTS[key]

        return default

    def set(self, key: str, value: Any, value_type: str = None, description: str = None):
        """Set a setting value (updates both DB and cache)."""
        try:
            # Determine type if not provided
            if value_type is None:
                if isinstance(value, bool):
                    value_type = 'bool'
                elif isinstance(value, int):
                    value_type = 'int'
                elif isinstance(value, float):
                    value_type = 'float'
                elif isinstance(value, (dict, list)):
                    value_type = 'json'
                else:
                    value_type = 'string'

            AppSetting.set(key, value, value_type, description)
            _settings_cache[key] = value
            return True
        except Exception as e:
            logger.error(f"Failed to set setting {key}: {e}")
            return False

    def get_public_settings(self) -> Dict[str, Any]:
        """Get all public settings for frontend."""
        try:
            return AppSetting.get_public_settings()
        except Exception as e:
            logger.warning(f"Failed to get public settings: {e}")
            # Return safe defaults
            return {
                'max_free_categories': self.DEFAULTS['max_free_categories'],
                'premium_access_days': self.DEFAULTS['premium_access_days'],
                'actions_per_plan': self.DEFAULTS['actions_per_plan'],
            }

    def get_default_category_code(self) -> Optional[str]:
        """
        Get default category code.

        Logic:
        1. If explicit setting exists, use it
        2. Otherwise, return first FREE category by display_order
        """
        # Check explicit setting
        explicit = self.get('default_category_code')
        if explicit:
            return explicit

        # Get first free category from DB
        try:
            from app.models import Category
            first_free = Category.query.filter_by(
                is_premium=False
            ).order_by(Category.display_order).first()

            if first_free:
                return first_free.code
        except Exception as e:
            logger.warning(f"Failed to get default category from DB: {e}")

        return None  # Frontend will handle fallback

    # Convenience properties for common settings
    @property
    def max_free_categories(self) -> int:
        return self.get('max_free_categories', 3)

    @property
    def premium_access_days(self) -> int:
        return self.get('premium_access_days', 14)

    @property
    def actions_per_plan(self) -> int:
        return self.get('actions_per_plan', 5)


# Singleton instance
settings_service = SettingsService()


# Convenience functions for direct access
def get_setting(key: str, default: Any = None) -> Any:
    """Get a setting value."""
    return settings_service.get(key, default)


def set_setting(key: str, value: Any, **kwargs) -> bool:
    """Set a setting value."""
    return settings_service.set(key, value, **kwargs)


def seed_default_settings():
    """Seed default settings into database (run once during setup)."""
    for setting_data in DEFAULT_SETTINGS:
        existing = AppSetting.query.filter_by(key=setting_data['key']).first()
        if not existing:
            setting = AppSetting(
                key=setting_data['key'],
                value=setting_data['value'],
                value_type=setting_data['value_type'],
                description=setting_data['description'],
                is_public=setting_data.get('is_public', False),
            )
            db.session.add(setting)
            logger.info(f"Seeded setting: {setting_data['key']}")

    db.session.commit()
    settings_service.refresh_cache()
