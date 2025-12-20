"""
Cache Service - Redis-based caching layer.

Provides caching for:
- Categories (long TTL)
- User categories (medium TTL)
- Settings (long TTL)
- Daily plans (short TTL)
"""

import os
import json
import logging
from typing import Any, Optional, Callable
from functools import wraps

logger = logging.getLogger(__name__)

# Global Redis client (lazy initialized)
_redis_client = None
_redis_available = None


def _get_redis():
    """Get Redis client (lazy init)."""
    global _redis_client, _redis_available

    if _redis_available is False:
        return None

    if _redis_client is None:
        try:
            import redis
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
            _redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            _redis_client.ping()
            _redis_available = True
            logger.info("Redis cache connected successfully")
        except Exception as e:
            logger.warning(f"Redis not available, using in-memory fallback: {e}")
            _redis_available = False
            return None

    return _redis_client


# In-memory fallback cache (when Redis unavailable)
_memory_cache = {}


class CacheService:
    """Redis-based cache service with fallback to memory."""

    # Cache key prefixes
    PREFIX_SETTINGS = "settings"
    PREFIX_CATEGORIES = "categories"
    PREFIX_USER_CATEGORIES = "user_cats"
    PREFIX_PLAN = "plan"

    # Default TTLs (in seconds)
    TTL_SETTINGS = 3600  # 1 hour
    TTL_CATEGORIES = 3600  # 1 hour
    TTL_USER_CATEGORIES = 300  # 5 minutes
    TTL_PLAN = 60  # 1 minute

    def __init__(self):
        pass

    def _get_key(self, prefix: str, *parts) -> str:
        """Build cache key."""
        return f"{prefix}:{':'.join(str(p) for p in parts)}"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        redis = _get_redis()

        if redis:
            try:
                value = redis.get(key)
                if value:
                    return json.loads(value)
            except Exception as e:
                logger.warning(f"Cache get error: {e}")
        else:
            # Memory fallback
            if key in _memory_cache:
                import time
                entry = _memory_cache[key]
                if entry['expires_at'] > time.time():
                    return entry['value']
                else:
                    del _memory_cache[key]

        return None

    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache."""
        redis = _get_redis()

        if redis:
            try:
                redis.setex(key, ttl, json.dumps(value))
                return True
            except Exception as e:
                logger.warning(f"Cache set error: {e}")
        else:
            # Memory fallback
            import time
            _memory_cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl
            }
            return True

        return False

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        redis = _get_redis()

        if redis:
            try:
                redis.delete(key)
                return True
            except Exception as e:
                logger.warning(f"Cache delete error: {e}")
        else:
            _memory_cache.pop(key, None)
            return True

        return False

    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern."""
        redis = _get_redis()
        count = 0

        if redis:
            try:
                keys = redis.keys(pattern)
                if keys:
                    count = redis.delete(*keys)
            except Exception as e:
                logger.warning(f"Cache delete pattern error: {e}")
        else:
            # Memory fallback - simple prefix matching
            prefix = pattern.rstrip('*')
            to_delete = [k for k in _memory_cache if k.startswith(prefix)]
            for k in to_delete:
                del _memory_cache[k]
            count = len(to_delete)

        return count

    # === High-level methods ===

    def get_settings(self) -> Optional[dict]:
        """Get all settings from cache."""
        key = self._get_key(self.PREFIX_SETTINGS, "all")
        return self.get(key)

    def set_settings(self, settings: dict) -> bool:
        """Cache all settings."""
        key = self._get_key(self.PREFIX_SETTINGS, "all")
        return self.set(key, settings, self.TTL_SETTINGS)

    def invalidate_settings(self) -> bool:
        """Invalidate settings cache."""
        key = self._get_key(self.PREFIX_SETTINGS, "all")
        return self.delete(key)

    def get_categories(self, include_inactive: bool = False) -> Optional[list]:
        """Get categories from cache."""
        key = self._get_key(self.PREFIX_CATEGORIES, "all" if include_inactive else "active")
        return self.get(key)

    def set_categories(self, categories: list, include_inactive: bool = False) -> bool:
        """Cache categories."""
        key = self._get_key(self.PREFIX_CATEGORIES, "all" if include_inactive else "active")
        return self.set(key, categories, self.TTL_CATEGORIES)

    def invalidate_categories(self) -> int:
        """Invalidate all category caches."""
        return self.delete_pattern(f"{self.PREFIX_CATEGORIES}:*")

    def get_user_categories(self, user_id: int) -> Optional[list]:
        """Get user's categories from cache."""
        key = self._get_key(self.PREFIX_USER_CATEGORIES, user_id)
        return self.get(key)

    def set_user_categories(self, user_id: int, categories: list) -> bool:
        """Cache user's categories."""
        key = self._get_key(self.PREFIX_USER_CATEGORIES, user_id)
        return self.set(key, categories, self.TTL_USER_CATEGORIES)

    def invalidate_user_categories(self, user_id: int) -> bool:
        """Invalidate user's category cache."""
        key = self._get_key(self.PREFIX_USER_CATEGORIES, user_id)
        return self.delete(key)

    def get_plan(self, user_id: Optional[int], category_id: int, date_str: str) -> Optional[dict]:
        """Get cached plan."""
        user_part = user_id or "anon"
        key = self._get_key(self.PREFIX_PLAN, user_part, category_id, date_str)
        return self.get(key)

    def set_plan(self, user_id: Optional[int], category_id: int, date_str: str, plan: dict) -> bool:
        """Cache plan."""
        user_part = user_id or "anon"
        key = self._get_key(self.PREFIX_PLAN, user_part, category_id, date_str)
        return self.set(key, plan, self.TTL_PLAN)

    def invalidate_plan(self, user_id: Optional[int], category_id: int, date_str: str) -> bool:
        """Invalidate specific plan cache."""
        user_part = user_id or "anon"
        key = self._get_key(self.PREFIX_PLAN, user_part, category_id, date_str)
        return self.delete(key)


# Singleton instance
cache_service = CacheService()


def cached(prefix: str, ttl: int = 300, key_func: Callable = None):
    """
    Decorator for caching function results.

    Usage:
        @cached('categories', ttl=3600)
        def get_categories():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key
            if key_func:
                cache_key = f"{prefix}:{key_func(*args, **kwargs)}"
            else:
                cache_key = f"{prefix}:{func.__name__}"

            # Try cache
            result = cache_service.get(cache_key)
            if result is not None:
                return result

            # Call function
            result = func(*args, **kwargs)

            # Cache result
            if result is not None:
                cache_service.set(cache_key, result, ttl)

            return result

        return wrapper
    return decorator
