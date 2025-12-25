"""
FYPFixer Application Constants - SINGLE SOURCE OF TRUTH

All hardcoded values MUST be defined here.
Import from this module, never hardcode values in services/models.

Usage:
    from app.config.constants import XP_REWARDS, AI_TEMPERATURES
"""

from typing import Dict, List, Tuple

# =============================================================================
# GAMIFICATION - XP & Rewards
# =============================================================================

XP_REWARDS: Dict[str, int] = {
    'follow': 10,
    'like': 5,
    'save': 8,
    'not_interested': 7,
    'plan_complete': 25,
    'streak_milestone': 50,
}

# Default XP when action type not found
XP_DEFAULT: int = 5

# =============================================================================
# GAMIFICATION - Streaks
# =============================================================================

STREAK_MILESTONES: List[int] = [3, 7, 14, 21, 30, 60, 90, 180, 365]

# =============================================================================
# GAMIFICATION - Levels
# =============================================================================

LEVEL_THRESHOLDS: List[Tuple[int, str]] = [
    (0, 'Beginner'),
    (100, 'Explorer'),
    (300, 'Apprentice'),
    (600, 'Curator'),
    (1000, 'Expert'),
    (2000, 'Master'),
    (5000, 'Legend'),
]

DEFAULT_LEVEL: str = 'Beginner'

# =============================================================================
# AI PROVIDER - Temperatures
# =============================================================================

AI_TEMPERATURES: Dict[str, float] = {
    'criteria': 0.7,      # Creative for diverse queries
    'selection': 0.3,     # Consistent, logical selection
    'motivation': 0.5,    # Balanced creativity
    'fallback': 0.2,      # Most reliable output
}

# =============================================================================
# AI PROVIDER - Timeouts (seconds)
# =============================================================================

AI_TIMEOUTS: Dict[str, int] = {
    'health_check': 2,
    'default': 30,
    'criteria': 60,
    'selection': 45,
    'motivation': 10,
}

# =============================================================================
# AI PROVIDER - Defaults
# =============================================================================

AI_DEFAULTS = {
    'ollama_url': 'http://localhost:11434',
    'ollama_model': 'llama3',
    'provider': 'local',
}

# =============================================================================
# LIMITS - Actions & Plans
# =============================================================================

ACTION_LIMITS: Dict[str, int] = {
    'default_count': 5,
    'min_count': 3,
    'max_count': 8,
}

PLAN_LIMITS: Dict[str, int] = {
    'per_page': 20,
    'max_per_page': 100,
}

# =============================================================================
# LIMITS - Other
# =============================================================================

OTHER_LIMITS: Dict[str, int] = {
    'video_cache': 50,
    'leaderboard_size': 10,
    'candidates_for_ai': 20,
}

# =============================================================================
# CACHE TTL (seconds)
# =============================================================================

CACHE_TTL: Dict[str, int] = {
    'video_cache': 24 * 60 * 60,      # 24 hours
    'plan_cache': 24 * 60 * 60,       # 24 hours
    'user_stats': 5 * 60,             # 5 minutes
    'rate_limit': 60,                 # 1 minute
}

# =============================================================================
# DIFFICULTY (Flow State)
# =============================================================================

DIFFICULTY: Dict[str, int] = {
    'min': 3,
    'max': 8,
    'default': 5,
}

# =============================================================================
# CONTENT FILTERS
# =============================================================================

CONTENT_FILTERS: Dict[str, int] = {
    'min_views': 10000,
    'max_duration_sec': 180,
    'uploaded_within_days': 14,
    'creator_min_followers': 10000,
}

# =============================================================================
# DEFAULTS - Category Fallbacks
# =============================================================================

DEFAULT_CATEGORY_CODE: str = 'fitness'

# =============================================================================
# RATE LIMITS - Tiered by endpoint type
# =============================================================================

RATE_LIMITS: Dict[str, str] = {
    'auth': '10 per minute',       # login, oauth, register
    'write': '30 per minute',      # POST, PUT, DELETE
    'read': '120 per minute',      # GET endpoints
    'heavy': '5 per minute',       # AI generation, reports
}

# =============================================================================
# SECURITY - OAuth Redirect Whitelist
# =============================================================================

ALLOWED_REDIRECT_URIS: List[str] = [
    # Production
    'https://fypglow.com/auth/callback',
    'https://fypglow.com/auth/tiktok/callback',
    'https://www.fypglow.com/auth/callback',
    'https://www.fypglow.com/auth/tiktok/callback',
    # Development
    'http://localhost:3000/auth/callback',
    'http://localhost:3000/auth/tiktok/callback',
    'http://localhost:5173/auth/callback',
    'http://localhost:5173/auth/tiktok/callback',
]
