"""
Toxic Detection Service - Identifies creators whose content user should avoid.

A creator is "toxic" if:
- User has seen their videos 5+ times (high exposure)
- User's completion rate for their videos < 50% (low engagement)

Usage:
    from app.services.toxic_detection_service import toxic_detection_service

    toxic_creators = toxic_detection_service.get_toxic_creators(user_id=1, limit=5)
    toxic_detection_service.mark_creator_blocked(user_id=1, creator_username='@badcreator')
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from sqlalchemy import func, case, and_

from app import db
from app.models import UserProgress, StepItem, PlanStep, BlockedCreator

logger = logging.getLogger(__name__)

# Thresholds for toxic detection
MIN_VIEWS_THRESHOLD = 5  # Minimum views to be considered
MAX_COMPLETION_RATE = 0.5  # Below 50% completion = toxic


class ToxicDetectionService:
    """Service for detecting and managing toxic creators."""

    def get_toxic_creators(
        self,
        user_id: int,
        category_id: Optional[int] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get list of toxic creators for a user.

        A creator is toxic if:
        - User has seen their videos 5+ times
        - Completion rate < 50%

        Args:
            user_id: User ID
            category_id: Optional category filter (not used currently)
            limit: Max number of toxic creators to return

        Returns:
            List of toxic creator objects with:
            - creator_username
            - view_count
            - completion_rate
            - reason
        """
        try:
            # Get already blocked creators to exclude them
            blocked_usernames = db.session.query(BlockedCreator.creator_username).filter(
                BlockedCreator.user_id == user_id
            ).subquery()

            # Query to find toxic creators:
            # Join user_progress -> plan_steps -> step_items to get creator info
            # Group by creator and calculate stats
            toxic_query = db.session.query(
                StepItem.creator_username,
                func.count(UserProgress.id).label('view_count'),
                func.sum(
                    case(
                        (UserProgress.completed_at.isnot(None), 1),
                        else_=0
                    )
                ).label('completed_count')
            ).join(
                PlanStep, StepItem.plan_step_id == PlanStep.id
            ).join(
                UserProgress,
                and_(
                    UserProgress.step_id == PlanStep.id,
                    UserProgress.user_id == user_id
                )
            ).filter(
                StepItem.creator_username.isnot(None),
                StepItem.creator_username != '',
                ~StepItem.creator_username.in_(blocked_usernames)
            ).group_by(
                StepItem.creator_username
            ).having(
                func.count(UserProgress.id) >= MIN_VIEWS_THRESHOLD
            ).all()

            toxic_creators = []
            for row in toxic_query:
                creator_username = row.creator_username
                view_count = row.view_count or 0
                completed_count = row.completed_count or 0

                # Calculate completion rate
                completion_rate = completed_count / view_count if view_count > 0 else 0

                # Check if below threshold (toxic)
                if completion_rate < MAX_COMPLETION_RATE:
                    toxic_creators.append({
                        'creator_username': creator_username,
                        'view_count': view_count,
                        'completion_count': completed_count,
                        'completion_rate': round(completion_rate, 2),
                        'reason': f"Low engagement - {int(completion_rate * 100)}% completion rate"
                    })

            # Sort by view count (highest exposure first) and limit
            toxic_creators.sort(key=lambda x: x['view_count'], reverse=True)
            return toxic_creators[:limit]

        except Exception as e:
            logger.error(f"Error detecting toxic creators for user {user_id}: {e}")
            return []

    def mark_creator_blocked(
        self,
        user_id: int,
        creator_username: str,
        reason: Optional[str] = None
    ) -> bool:
        """
        Block a creator for a user.

        Args:
            user_id: User ID
            creator_username: Creator's username to block
            reason: Optional reason for blocking

        Returns:
            True if blocked successfully, False if already blocked or error
        """
        try:
            # Check if already blocked
            existing = BlockedCreator.query.filter_by(
                user_id=user_id,
                creator_username=creator_username
            ).first()

            if existing:
                logger.info(f"Creator {creator_username} already blocked for user {user_id}")
                return False

            # Create new blocked entry
            blocked = BlockedCreator(
                user_id=user_id,
                creator_username=creator_username,
                reason=reason or "Blocked via toxic detection"
            )
            db.session.add(blocked)
            db.session.commit()

            logger.info(f"Blocked creator {creator_username} for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Error blocking creator {creator_username} for user {user_id}: {e}")
            db.session.rollback()
            return False

    def unblock_creator(self, user_id: int, creator_username: str) -> bool:
        """
        Unblock a creator for a user.

        Args:
            user_id: User ID
            creator_username: Creator's username to unblock

        Returns:
            True if unblocked, False if not found or error
        """
        try:
            result = BlockedCreator.query.filter_by(
                user_id=user_id,
                creator_username=creator_username
            ).delete()
            db.session.commit()

            if result > 0:
                logger.info(f"Unblocked creator {creator_username} for user {user_id}")
                return True
            return False

        except Exception as e:
            logger.error(f"Error unblocking creator {creator_username}: {e}")
            db.session.rollback()
            return False

    def get_blocked_creators(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get list of blocked creators for a user.

        Args:
            user_id: User ID

        Returns:
            List of blocked creator objects
        """
        try:
            blocked = BlockedCreator.query.filter_by(user_id=user_id).all()
            return [b.to_dict() for b in blocked]
        except Exception as e:
            logger.error(f"Error getting blocked creators for user {user_id}: {e}")
            return []

    def is_creator_blocked(self, user_id: int, creator_username: str) -> bool:
        """
        Check if a creator is blocked for a user.

        Args:
            user_id: User ID
            creator_username: Creator's username

        Returns:
            True if blocked, False otherwise
        """
        try:
            exists = BlockedCreator.query.filter_by(
                user_id=user_id,
                creator_username=creator_username
            ).first()
            return exists is not None
        except Exception as e:
            logger.error(f"Error checking blocked status: {e}")
            return False


# Singleton instance
toxic_detection_service = ToxicDetectionService()
