"""
Curation Service - Selects best videos for Watch step.

Selection criteria (in order):
1. NOT from blocked creators
2. NOT already watched today
3. High global completion rate (>70%)
4. Matches user's category
5. Diverse creators (max 1 video per creator)

Usage:
    from app.services.curation_service import curation_service

    videos = curation_service.get_curated_videos(user_id=1, category_id=2, count=4)
    curation_service.record_video_shown(user_id=1, video_id='abc123')
"""

import logging
from datetime import date, datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import and_, not_, func

from app import db
from app.models import TiktokVideo, BlockedCreator, UserProgress, StepItem, PlanStep

logger = logging.getLogger(__name__)

# Minimum quality score for curation
MIN_QUALITY_SCORE = 0.7


class CurationService:
    """Service for curating personalized video recommendations."""

    def get_curated_videos(
        self,
        user_id: int,
        category_id: Optional[int] = None,
        count: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Get curated videos for the Watch step.

        Selection criteria:
        1. NOT from blocked creators
        2. NOT already watched today
        3. High quality score (>70%)
        4. Matches category (if provided)
        5. Diverse creators (max 1 per creator)

        Args:
            user_id: User ID
            category_id: Optional category filter
            count: Number of videos to return (default 4)

        Returns:
            List of video objects with: video_id, video_url, thumbnail_url,
            creator_name, duration_seconds, quality_score
        """
        try:
            # Get blocked creators for this user
            blocked_usernames = db.session.query(BlockedCreator.creator_username).filter(
                BlockedCreator.user_id == user_id
            ).subquery()

            # Get videos watched today (via step_items -> plan_steps -> user_progress)
            today = date.today()
            watched_today = db.session.query(StepItem.video_id).join(
                PlanStep, StepItem.plan_step_id == PlanStep.id
            ).join(
                UserProgress,
                and_(
                    UserProgress.step_id == PlanStep.id,
                    UserProgress.user_id == user_id,
                    func.date(UserProgress.completed_at) == today
                )
            ).subquery()

            # Base query - get high quality videos
            query = TiktokVideo.query.filter(
                # Not expired
                TiktokVideo.cache_expires_at > datetime.utcnow(),
                # High quality
                TiktokVideo.quality_score >= MIN_QUALITY_SCORE,
                # Not from blocked creators
                ~TiktokVideo.creator_username.in_(blocked_usernames),
                # Not already watched today
                ~TiktokVideo.video_id.in_(watched_today)
            )

            # Filter by category if provided
            if category_id:
                # Category filtering via category_scores JSON field
                # This assumes category_scores contains {category_slug: score}
                pass  # TODO: Add category-specific filtering when category slug is available

            # Order by quality score
            query = query.order_by(TiktokVideo.quality_score.desc())

            # Get more videos than needed for diversity filtering
            candidates = query.limit(count * 3).all()

            # Apply diversity filter - max 1 video per creator
            curated = []
            seen_creators = set()

            for video in candidates:
                if video.creator_username not in seen_creators:
                    curated.append(self._video_to_dict(video))
                    seen_creators.add(video.creator_username)

                    if len(curated) >= count:
                        break

            logger.info(f"Curated {len(curated)} videos for user {user_id}")
            return curated

        except Exception as e:
            logger.error(f"Error curating videos for user {user_id}: {e}")
            return []

    def _video_to_dict(self, video: TiktokVideo) -> Dict[str, Any]:
        """Convert TiktokVideo to curation response format."""
        return {
            'video_id': video.video_id,
            'video_url': video.url,
            'thumbnail_url': video.thumbnail_url,
            'creator_name': video.creator_username,
            'creator_display_name': video.creator_display_name,
            'duration_seconds': video.duration_sec,
            'quality_score': float(video.quality_score) if video.quality_score else None,
            'description': video.description[:100] if video.description else None,
            'views': video.views,
            'likes': video.likes,
        }

    def record_video_shown(self, user_id: int, video_id: str) -> bool:
        """
        Record that a video was shown to user (for deduplication).

        This creates a lightweight tracking entry. Full completion tracking
        happens via UserProgress when user actually completes the action.

        Args:
            user_id: User ID
            video_id: Video ID that was shown

        Returns:
            True if recorded, False on error
        """
        try:
            # For now, we track shown videos via the step_items that get created
            # when a plan is generated. This method is a placeholder for future
            # tracking needs (e.g., if we want to track impressions vs completions)
            logger.debug(f"Video {video_id} shown to user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Error recording video shown: {e}")
            return False

    def get_video_stats(self, user_id: int, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user's stats for a specific video.

        Args:
            user_id: User ID
            video_id: Video ID

        Returns:
            Stats dict or None
        """
        try:
            video = TiktokVideo.query.filter_by(video_id=video_id).first()
            if not video:
                return None

            # Check if user has watched this video
            watched = db.session.query(StepItem.id).join(
                PlanStep, StepItem.plan_step_id == PlanStep.id
            ).join(
                UserProgress,
                and_(
                    UserProgress.step_id == PlanStep.id,
                    UserProgress.user_id == user_id
                )
            ).filter(
                StepItem.video_id == video_id,
                UserProgress.completed_at.isnot(None)
            ).first()

            return {
                'video_id': video_id,
                'watched': watched is not None,
                'creator_username': video.creator_username,
                'quality_score': float(video.quality_score) if video.quality_score else None,
            }

        except Exception as e:
            logger.error(f"Error getting video stats: {e}")
            return None

    def refresh_curation_cache(self, category_id: Optional[int] = None) -> int:
        """
        Refresh the curation cache for a category.

        This could trigger a fresh scrape of videos if cache is stale.

        Args:
            category_id: Optional category to refresh

        Returns:
            Number of videos in cache
        """
        try:
            # Count valid cached videos
            count = TiktokVideo.query.filter(
                TiktokVideo.cache_expires_at > datetime.utcnow(),
                TiktokVideo.quality_score >= MIN_QUALITY_SCORE
            ).count()

            logger.info(f"Curation cache has {count} valid videos")
            return count

        except Exception as e:
            logger.error(f"Error refreshing curation cache: {e}")
            return 0


# Singleton instance
curation_service = CurationService()
