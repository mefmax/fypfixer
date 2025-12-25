"""
Plan Service V2 - Generates plan v2.0 structure.

Plan v2.0 has 3 steps:
1. CLEAR (Detox) - Block toxic creators
2. WATCH - Watch 4 curated videos
3. REINFORCE - Rewatch favorite + Share

Usage:
    from app.services.plan_service_v2 import plan_service_v2

    plan = plan_service_v2.generate_plan(user_id=1, category_id=2)
"""

import logging
import uuid
from datetime import datetime, date
from typing import Dict, Any, Optional

from app import db
from app.models import Plan, Challenge, Category
from app.services.cache_service import cache_service
from app.services.toxic_detection_service import toxic_detection_service
from app.services.curation_service import curation_service
from app.services.favorites_service import favorites_service

logger = logging.getLogger(__name__)

# Target signals per day (54 = 6 hours x 9 actions per hour estimate)
TARGET_SIGNALS = 54


class PlanServiceV2:
    """Service for generating Plan v2.0 with Clear/Watch/Reinforce steps."""

    def generate_plan(
        self,
        user_id: int,
        category_id: int,
        category_slug: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a plan v2.0 for the user.

        Args:
            user_id: User ID
            category_id: Category ID
            category_slug: Category slug (for cache key, optional)

        Returns:
            Plan dict with steps structure
        """
        try:
            # Get category slug for cache key if not provided
            if not category_slug:
                category = Category.query.get(category_id)
                category_slug = category.slug if category else str(category_id)

            # Check cache first
            cached = cache_service.get_guided_plan(user_id, category_slug)
            if cached:
                logger.info(f"Returning cached plan for user {user_id}")
                return cached

            # Get or create active challenge
            challenge = self._get_or_create_challenge(user_id, category_id)

            # Step 1: CLEAR - Get toxic creators
            toxic_creators = toxic_detection_service.get_toxic_creators(
                user_id=user_id,
                category_id=category_id,
                limit=5
            )

            # Step 2: WATCH - Get curated videos
            curated_videos = curation_service.get_curated_videos(
                user_id=user_id,
                category_id=category_id,
                count=4
            )

            # Step 3: REINFORCE - Get random favorite
            favorite_video = favorites_service.get_random_favorite(user_id=user_id)

            # Build plan object
            plan_id = str(uuid.uuid4())
            plan = {
                'plan_id': plan_id,
                'user_id': user_id,
                'category_id': category_id,
                'day_of_challenge': challenge.current_day,
                'created_at': datetime.utcnow().isoformat(),
                'steps': {
                    'clear': {
                        'type': 'CLEAR',
                        'title': 'Digital Detox',
                        'description': 'Block creators that drain your energy',
                        'toxic_creators': toxic_creators,
                        'completed': False
                    },
                    'watch': {
                        'type': 'WATCH',
                        'title': 'Mindful Watching',
                        'description': 'Watch these inspiring videos',
                        'videos': curated_videos,
                        'completed': False
                    },
                    'reinforce': {
                        'type': 'REINFORCE',
                        'title': 'Reinforce the Good',
                        'description': 'Rewatch your favorite and share',
                        'favorite_video': favorite_video,
                        'show_share': challenge.current_day >= 3,
                        'completed': False
                    }
                },
                'target_signals': TARGET_SIGNALS
            }

            # Save to DB
            db_plan = self._save_plan(user_id, category_id, challenge.id, plan)
            plan['db_id'] = db_plan.id

            # Cache with 24h TTL
            cache_service.set_guided_plan(user_id, category_slug, plan)

            logger.info(f"Generated plan v2 for user {user_id}, challenge day {challenge.current_day}")
            return plan

        except Exception as e:
            logger.error(f"Error generating plan for user {user_id}: {e}")
            raise

    def _get_or_create_challenge(self, user_id: int, category_id: int) -> Challenge:
        """
        Get active challenge or create new one.

        Args:
            user_id: User ID
            category_id: Category ID

        Returns:
            Challenge instance
        """
        # Look for active challenge in this category
        challenge = Challenge.query.filter_by(
            user_id=user_id,
            category_id=category_id,
            is_active=True
        ).first()

        if challenge:
            # Check if challenge is still valid (within 7 days)
            days_since_start = (date.today() - challenge.started_at.date()).days
            if days_since_start < 7:
                # Update current day if needed
                new_day = days_since_start + 1
                if challenge.current_day != new_day:
                    challenge.current_day = new_day
                    db.session.commit()
                return challenge
            else:
                # Challenge expired, mark as completed
                challenge.is_active = False
                challenge.completed_at = datetime.utcnow()
                db.session.commit()

        # Create new challenge
        challenge = Challenge(
            user_id=user_id,
            category_id=category_id,
            current_day=1,
            is_active=True
        )
        db.session.add(challenge)
        db.session.commit()

        logger.info(f"Created new challenge for user {user_id}, category {category_id}")
        return challenge

    def _save_plan(
        self,
        user_id: int,
        category_id: int,
        challenge_id: int,
        plan_data: Dict[str, Any]
    ) -> Plan:
        """
        Save plan to database.

        Args:
            user_id: User ID
            category_id: Category ID
            challenge_id: Challenge ID
            plan_data: Plan dictionary

        Returns:
            Plan model instance
        """
        # Check if plan already exists for today
        today = date.today()
        existing = Plan.query.filter_by(
            user_id=user_id,
            category_id=category_id,
            plan_date=today
        ).first()

        if existing:
            # Update existing plan
            existing.day_of_challenge = plan_data.get('day_of_challenge', 1)
            existing.challenge_id = challenge_id
            db.session.commit()
            return existing

        # Create new plan
        plan = Plan(
            user_id=user_id,
            category_id=category_id,
            challenge_id=challenge_id,
            plan_date=today,
            day_of_challenge=plan_data.get('day_of_challenge', 1),
            title=f"Day {plan_data.get('day_of_challenge', 1)} Plan",
            is_active=True
        )
        db.session.add(plan)
        db.session.commit()

        return plan

    def mark_step_completed(
        self,
        user_id: int,
        plan_id: int,
        step_type: str
    ) -> bool:
        """
        Mark a step as completed.

        Args:
            user_id: User ID (for validation)
            plan_id: Plan DB ID
            step_type: 'clear', 'watch', or 'reinforce'

        Returns:
            True if updated, False otherwise
        """
        try:
            plan = Plan.query.filter_by(id=plan_id, user_id=user_id).first()
            if not plan:
                return False

            if step_type == 'clear':
                plan.step_clear_completed = True
            elif step_type == 'watch':
                plan.step_watch_completed = True
            elif step_type == 'reinforce':
                plan.step_reinforce_completed = True
            else:
                return False

            db.session.commit()
            logger.info(f"Marked step {step_type} completed for plan {plan_id}")
            return True

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error marking step completed: {e}")
            return False

    def get_plan_progress(self, user_id: int, plan_id: int) -> Optional[Dict[str, Any]]:
        """
        Get plan completion progress.

        Args:
            user_id: User ID
            plan_id: Plan DB ID

        Returns:
            Progress dict or None
        """
        plan = Plan.query.filter_by(id=plan_id, user_id=user_id).first()
        if not plan:
            return None

        completed_steps = sum([
            plan.step_clear_completed,
            plan.step_watch_completed,
            plan.step_reinforce_completed
        ])

        return {
            'plan_id': plan.id,
            'day_of_challenge': plan.day_of_challenge,
            'steps': {
                'clear': plan.step_clear_completed,
                'watch': plan.step_watch_completed,
                'reinforce': plan.step_reinforce_completed,
            },
            'completed_steps': completed_steps,
            'total_steps': 3,
            'signals_count': plan.signals_count,
            'target_signals': TARGET_SIGNALS,
        }


# Singleton instance
plan_service_v2 = PlanServiceV2()
