"""
Abstract base class for AI providers.

All AI providers must implement:
1. generate_criteria() - Stage 1: Create search parameters
2. select_actions() - Stage 2: Select best actions from candidates
3. generate_motivation() - Get contextual motivation message
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class UserContext:
    """Context passed to AI for personalization."""
    category: str                    # e.g., 'personal_growth'
    language: str                    # e.g., 'en', 'ru'
    time_of_day: str                 # 'morning', 'afternoon', 'evening'
    streak_days: int = 0             # Current streak
    difficulty: int = 5              # Actions per day (3-8)
    preferred_creators: List[str] = None   # Known good creators
    preferred_topics: List[str] = None     # Known good topics
    already_following: List[str] = None    # Skip these creators

    def __post_init__(self):
        self.preferred_creators = self.preferred_creators or []
        self.preferred_topics = self.preferred_topics or []
        self.already_following = self.already_following or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            'category': self.category,
            'language': self.language,
            'time_of_day': self.time_of_day,
            'streak_days': self.streak_days,
            'difficulty': self.difficulty,
            'preferred_creators': self.preferred_creators,
            'preferred_topics': self.preferred_topics,
            'already_following': self.already_following,
        }


@dataclass
class SearchCriteria:
    """Output from Stage 1: Search parameters for TikTok scraper."""
    search_queries: List[str]        # ["morning routine", "productivity tips"]
    hashtags: List[str]              # ["personalgrowth", "motivation"]
    filters: Dict[str, Any] = None   # {"min_views": 10000, "max_duration": 180}

    def __post_init__(self):
        self.filters = self.filters or {
            'min_views': 10000,
            'max_duration_sec': 180,
            'uploaded_within_days': 14,
            'creator_min_followers': 10000,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            'search_queries': self.search_queries,
            'hashtags': self.hashtags,
            'filters': self.filters,
        }


@dataclass
class SelectedAction:
    """Single action selected by AI."""
    type: str                        # 'follow', 'like', 'save', 'not_interested'
    video_id: Optional[str]          # TikTok video ID (None for follow/not_interested)
    creator_username: str            # '@username'
    creator_display_name: str        # 'Display Name'
    description: str                 # Action description
    thumbnail_url: Optional[str]     # Preview image
    tiktok_url: Optional[str]        # Direct link to TikTok
    reason: str                      # Why this action (shown to user)
    metadata: Dict[str, Any] = None  # Additional data

    def __post_init__(self):
        self.metadata = self.metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'video_id': self.video_id,
            'creator_username': self.creator_username,
            'creator_display_name': self.creator_display_name,
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'tiktok_url': self.tiktok_url,
            'reason': self.reason,
            'metadata': self.metadata,
        }


class AIProvider(ABC):
    """
    Abstract base class for AI recommendation providers.

    Implementations:
    - LocalProvider (Ollama) - Free, local inference
    - OpenAIProvider - GPT-3.5/4 API
    - AnthropicProvider - Claude API
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Provider name for logging and analytics.
        Example: "ollama/llama3", "openai/gpt-3.5-turbo"
        """
        pass

    @abstractmethod
    def generate_criteria(self, context: UserContext) -> SearchCriteria:
        """
        Stage 1: Generate search criteria for TikTok scraper.

        Based on user context (category, time, preferences), generate:
        - Search queries for finding relevant content
        - Hashtags to search
        - Filters for quality content

        Args:
            context: User context with category, time, preferences

        Returns:
            SearchCriteria with queries, hashtags, and filters

        Temperature: 0.7 (creative for diverse queries)
        """
        pass

    @abstractmethod
    def select_actions(
        self,
        candidates: List[Dict[str, Any]],
        context: UserContext,
        count: int = 5
    ) -> List[SelectedAction]:
        """
        Stage 2: Select best actions from candidate videos.

        From scraped TikTok videos, select the best ones for user's plan.

        Rules:
        - Max 1 action per creator (diversity)
        - Mix of action types: ~2 follow, ~2 like, ~1 save, ~1 not_interested
        - Prioritize high engagement rate (>5%)
        - Prioritize recent content (<7 days)
        - Include motivating reasons

        Args:
            candidates: List of video/creator dicts from scraper
            context: User context for personalization
            count: Number of actions to select (default: 5)

        Returns:
            List of SelectedAction objects

        Temperature: 0.3 (consistent, logical selection)
        """
        pass

    @abstractmethod
    def generate_motivation(
        self,
        context: UserContext,
        progress: Dict[str, int]
    ) -> str:
        """
        Generate personalized motivation message.

        Called when database templates don't match or for personalization.

        Args:
            context: User context
            progress: {'completed': int, 'total': int}

        Returns:
            Motivation message string with emoji

        Temperature: 0.5 (balanced creativity)
        """
        pass

    def health_check(self) -> bool:
        """
        Check if provider is available and responding.

        Returns:
            True if healthy, False otherwise
        """
        try:
            # Simple test call
            test_context = UserContext(
                category='personal_growth',
                language='en',
                time_of_day='morning'
            )
            result = self.generate_motivation(test_context, {'completed': 0, 'total': 5})
            return bool(result)
        except Exception:
            return False
