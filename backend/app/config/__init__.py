"""
Configuration module - import constants from here.

Usage:
    from app.config import XP_REWARDS, AI_TEMPERATURES
    from app.config import get_seed_creators
"""

from .constants import (
    # Gamification
    XP_REWARDS,
    XP_DEFAULT,
    STREAK_MILESTONES,
    LEVEL_THRESHOLDS,
    DEFAULT_LEVEL,
    # AI
    AI_TEMPERATURES,
    AI_TIMEOUTS,
    AI_DEFAULTS,
    # Limits
    ACTION_LIMITS,
    PLAN_LIMITS,
    OTHER_LIMITS,
    # Cache
    CACHE_TTL,
    # Difficulty
    DIFFICULTY,
    # Content
    CONTENT_FILTERS,
)

from .seed_creators import (
    SEED_CREATORS,
    DEFAULT_CATEGORY,
    get_seed_creators,
)

__all__ = [
    'XP_REWARDS',
    'XP_DEFAULT',
    'STREAK_MILESTONES',
    'LEVEL_THRESHOLDS',
    'DEFAULT_LEVEL',
    'AI_TEMPERATURES',
    'AI_TIMEOUTS',
    'AI_DEFAULTS',
    'ACTION_LIMITS',
    'PLAN_LIMITS',
    'OTHER_LIMITS',
    'CACHE_TTL',
    'DIFFICULTY',
    'CONTENT_FILTERS',
    'SEED_CREATORS',
    'DEFAULT_CATEGORY',
    'get_seed_creators',
]
