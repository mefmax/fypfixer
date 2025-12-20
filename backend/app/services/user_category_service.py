"""
UserCategoryService - manages user category subscriptions.

Business rules:
- FREE categories: max N (from settings), permanent access
- PREMIUM categories: unlimited, N days from purchase (from settings)
- Expired premium categories become inactive (greyed out)
"""
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from sqlalchemy.orm import joinedload
from app import db
from app.models import UserCategory, Category, User
from app.utils.errors import APIError, NotFoundError, ValidationError
from app.services.settings_service import get_setting
from app.services.cache_service import cache_service


class UserCategoryService:
    """Service for managing user category subscriptions."""

    def get_user_categories(self, user_id: int, include_inactive: bool = False) -> List[Dict]:
        """
        Get all categories for a user with their subscription status.
        Uses eager loading to avoid N+1 queries.
        Uses Redis cache for performance.
        """
        # First, check and deactivate expired categories
        self._deactivate_expired(user_id)

        # Try cache (only for active categories)
        if not include_inactive:
            cached = cache_service.get_user_categories(user_id)
            if cached:
                return cached

        query = UserCategory.query.options(
            joinedload(UserCategory.category)  # Eager load to avoid N+1
        ).filter_by(user_id=user_id)

        if not include_inactive:
            query = query.filter_by(is_active=True)

        user_cats = query.all()

        result = []
        for uc in user_cats:
            data = uc.to_dict()
            data['category'] = uc.category.to_dict() if uc.category else None
            result.append(data)

        # Cache active categories
        if not include_inactive:
            cache_service.set_user_categories(user_id, result)

        return result

    def get_active_category_ids(self, user_id: int) -> List[int]:
        """Get list of active category IDs for plan generation."""
        self._deactivate_expired(user_id)

        active = UserCategory.query.filter_by(
            user_id=user_id,
            is_active=True
        ).all()

        return [uc.category_id for uc in active if not uc.is_expired]

    def add_category(self, user_id: int, category_id: int, is_purchased: bool = False) -> Dict:
        """
        Add a category to user's list.

        Args:
            user_id: User ID
            category_id: Category to add
            is_purchased: True if this is a premium purchase

        Raises:
            ValidationError: If free category limit exceeded
            NotFoundError: If category doesn't exist
        """
        # 1. Check category exists
        category = db.session.get(Category, category_id)
        if not category:
            raise NotFoundError('Category')

        # 2. Check if already exists
        existing = UserCategory.query.filter_by(
            user_id=user_id,
            category_id=category_id
        ).first()

        # Get settings
        max_free = get_setting('max_free_categories', 3)
        premium_days = get_setting('premium_access_days', 14)

        if existing:
            if existing.is_expired and is_purchased:
                # Reactivate expired premium
                existing.is_active = True
                existing.purchased_at = datetime.now(timezone.utc)
                existing.expires_at = datetime.now(timezone.utc) + timedelta(days=premium_days)
                db.session.commit()
                return existing.to_dict()
            elif existing.is_active:
                # Already active
                return existing.to_dict()

        # 3. For FREE categories - check limit
        if not category.is_premium:
            free_count = UserCategory.query.join(Category).filter(
                UserCategory.user_id == user_id,
                UserCategory.is_active == True,
                Category.is_premium == False
            ).count()

            if free_count >= max_free:
                raise ValidationError(
                    f'Maximum {max_free} free categories allowed. '
                    'Remove one to add another.'
                )

        # 4. For PREMIUM - must be purchased
        if category.is_premium and not is_purchased:
            raise ValidationError('Premium category requires purchase')

        # 5. Create subscription
        user_cat = UserCategory(
            user_id=user_id,
            category_id=category_id,
            is_active=True,
        )

        if category.is_premium:
            user_cat.purchased_at = datetime.now(timezone.utc)
            user_cat.expires_at = datetime.now(timezone.utc) + timedelta(days=premium_days)

        db.session.add(user_cat)
        db.session.commit()

        # Invalidate cache
        cache_service.invalidate_user_categories(user_id)

        return user_cat.to_dict()

    def remove_category(self, user_id: int, category_id: int) -> bool:
        """
        Remove a category from user's list.
        Returns True if removed, False if not found.
        """
        user_cat = UserCategory.query.filter_by(
            user_id=user_id,
            category_id=category_id
        ).first()

        if not user_cat:
            return False

        db.session.delete(user_cat)
        db.session.commit()

        # Invalidate cache
        cache_service.invalidate_user_categories(user_id)

        return True

    def deactivate_category(self, user_id: int, category_id: int) -> bool:
        """Deactivate (not delete) a category."""
        user_cat = UserCategory.query.filter_by(
            user_id=user_id,
            category_id=category_id
        ).first()

        if not user_cat:
            return False

        user_cat.is_active = False
        db.session.commit()

        # Invalidate cache
        cache_service.invalidate_user_categories(user_id)

        return True

    def _deactivate_expired(self, user_id: int):
        """Check and deactivate expired premium categories."""
        expired = UserCategory.query.filter(
            UserCategory.user_id == user_id,
            UserCategory.is_active == True,
            UserCategory.expires_at != None,
            UserCategory.expires_at < datetime.now(timezone.utc)
        ).all()

        for uc in expired:
            uc.is_active = False

        if expired:
            db.session.commit()
            # Invalidate cache after expiring categories
            cache_service.invalidate_user_categories(user_id)

    def get_category_stats(self, user_id: int) -> Dict:
        """Get stats about user's categories."""
        self._deactivate_expired(user_id)

        # Eager load to avoid N+1
        all_cats = UserCategory.query.options(
            joinedload(UserCategory.category)
        ).filter_by(user_id=user_id).all()

        free_active = sum(1 for uc in all_cats if uc.is_active and not uc.category.is_premium)
        premium_active = sum(1 for uc in all_cats if uc.is_active and uc.category.is_premium)
        premium_expired = sum(1 for uc in all_cats if not uc.is_active and uc.category.is_premium)

        max_free = get_setting('max_free_categories', 3)

        return {
            'freeActive': free_active,
            'freeLimit': max_free,
            'freeRemaining': max_free - free_active,
            'premiumActive': premium_active,
            'premiumExpired': premium_expired,
            'totalActive': free_active + premium_active,
        }


# Singleton
user_category_service = UserCategoryService()
