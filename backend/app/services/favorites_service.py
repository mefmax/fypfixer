"""
Favorites Service - Manages user's favorite/liked videos.

Used for the Reinforce step where users rewatch favorite content.

Usage:
    from app.services.favorites_service import favorites_service

    favorites = favorites_service.get_favorites(user_id=1, limit=10)
    favorites_service.add_favorite(user_id=1, video_id='abc123')
    favorites_service.remove_favorite(user_id=1, video_id='abc123')
    random_video = favorites_service.get_random_favorite(user_id=1)
"""

import logging
import random
from typing import List, Dict, Any, Optional

from sqlalchemy.exc import IntegrityError

from app import db
from app.models import UserLikedVideo, TiktokVideo

logger = logging.getLogger(__name__)


class FavoritesService:
    """Service for managing user's favorite videos."""

    def get_favorites(
        self,
        user_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get user's favorite videos, most recent first.

        Args:
            user_id: User ID
            limit: Max number of favorites to return (default 10)

        Returns:
            List of video objects with full metadata
        """
        try:
            # Get user's liked videos with metadata from tiktok_videos
            favorites = db.session.query(UserLikedVideo, TiktokVideo).outerjoin(
                TiktokVideo, UserLikedVideo.video_id == TiktokVideo.video_id
            ).filter(
                UserLikedVideo.user_id == user_id
            ).order_by(
                UserLikedVideo.liked_at.desc()
            ).limit(limit).all()

            result = []
            for liked, video in favorites:
                if video:
                    # Full metadata available
                    result.append({
                        'video_id': liked.video_id,
                        'video_url': video.url,
                        'thumbnail_url': video.thumbnail_url,
                        'creator_name': video.creator_username,
                        'creator_display_name': video.creator_display_name,
                        'duration_seconds': video.duration_sec,
                        'description': video.description[:100] if video.description else None,
                        'liked_at': liked.liked_at.isoformat() if liked.liked_at else None,
                    })
                else:
                    # Video not in cache, minimal data
                    result.append({
                        'video_id': liked.video_id,
                        'video_url': None,
                        'thumbnail_url': None,
                        'creator_name': None,
                        'liked_at': liked.liked_at.isoformat() if liked.liked_at else None,
                    })

            logger.info(f"Retrieved {len(result)} favorites for user {user_id}")
            return result

        except Exception as e:
            logger.error(f"Error getting favorites for user {user_id}: {e}")
            return []

    def add_favorite(
        self,
        user_id: int,
        video_id: str
    ) -> Dict[str, Any]:
        """
        Add a video to user's favorites.

        Args:
            user_id: User ID
            video_id: TikTok video ID

        Returns:
            Dict with 'added': True if new, False if already exists
        """
        try:
            # Check if already favorited
            existing = UserLikedVideo.query.filter_by(
                user_id=user_id,
                video_id=video_id
            ).first()

            if existing:
                logger.debug(f"Video {video_id} already in favorites for user {user_id}")
                return {'added': False, 'message': 'Already in favorites'}

            # Add new favorite
            favorite = UserLikedVideo(
                user_id=user_id,
                video_id=video_id
            )
            db.session.add(favorite)
            db.session.commit()

            logger.info(f"Added video {video_id} to favorites for user {user_id}")
            return {'added': True}

        except IntegrityError:
            db.session.rollback()
            logger.debug(f"Duplicate favorite attempt for user {user_id}, video {video_id}")
            return {'added': False, 'message': 'Already in favorites'}

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding favorite for user {user_id}: {e}")
            raise

    def remove_favorite(
        self,
        user_id: int,
        video_id: str
    ) -> bool:
        """
        Remove a video from user's favorites.

        Args:
            user_id: User ID
            video_id: TikTok video ID

        Returns:
            True if removed, False if not found
        """
        try:
            favorite = UserLikedVideo.query.filter_by(
                user_id=user_id,
                video_id=video_id
            ).first()

            if not favorite:
                logger.debug(f"Video {video_id} not in favorites for user {user_id}")
                return False

            db.session.delete(favorite)
            db.session.commit()

            logger.info(f"Removed video {video_id} from favorites for user {user_id}")
            return True

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error removing favorite for user {user_id}: {e}")
            raise

    def get_random_favorite(
        self,
        user_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get a random favorite video for the Reinforce step.

        Args:
            user_id: User ID

        Returns:
            Video dict or None if no favorites
        """
        try:
            # Get all user's favorites
            favorites = UserLikedVideo.query.filter_by(
                user_id=user_id
            ).all()

            if not favorites:
                logger.debug(f"No favorites found for user {user_id}")
                return None

            # Pick a random one
            chosen = random.choice(favorites)

            # Get video metadata if available
            video = TiktokVideo.query.filter_by(
                video_id=chosen.video_id
            ).first()

            if video:
                return {
                    'video_id': chosen.video_id,
                    'video_url': video.url,
                    'thumbnail_url': video.thumbnail_url,
                    'creator_name': video.creator_username,
                    'creator_display_name': video.creator_display_name,
                    'duration_seconds': video.duration_sec,
                    'description': video.description[:100] if video.description else None,
                    'liked_at': chosen.liked_at.isoformat() if chosen.liked_at else None,
                }
            else:
                return {
                    'video_id': chosen.video_id,
                    'video_url': None,
                    'thumbnail_url': None,
                    'creator_name': None,
                    'liked_at': chosen.liked_at.isoformat() if chosen.liked_at else None,
                }

        except Exception as e:
            logger.error(f"Error getting random favorite for user {user_id}: {e}")
            return None

    def get_favorites_count(self, user_id: int) -> int:
        """
        Get count of user's favorites.

        Args:
            user_id: User ID

        Returns:
            Number of favorites
        """
        try:
            return UserLikedVideo.query.filter_by(user_id=user_id).count()
        except Exception as e:
            logger.error(f"Error counting favorites for user {user_id}: {e}")
            return 0

    def is_favorited(self, user_id: int, video_id: str) -> bool:
        """
        Check if a video is in user's favorites.

        Args:
            user_id: User ID
            video_id: Video ID

        Returns:
            True if favorited, False otherwise
        """
        try:
            return UserLikedVideo.query.filter_by(
                user_id=user_id,
                video_id=video_id
            ).first() is not None
        except Exception as e:
            logger.error(f"Error checking favorite status: {e}")
            return False


# Singleton instance
favorites_service = FavoritesService()
