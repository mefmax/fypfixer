"""
Unit tests for StreakService.

Run with: pytest tests/test_streak_service.py -v
"""

import pytest
from datetime import date, timedelta
from unittest.mock import Mock, patch, MagicMock

from app.config import XP_REWARDS, XP_DEFAULT, STREAK_MILESTONES
from app.services.streak_service import StreakService


class TestStreakService:
    """Tests for StreakService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = StreakService()

    def test_xp_rewards_defined(self):
        """XP rewards should be defined for all action types."""
        assert 'follow' in XP_REWARDS
        assert 'like' in XP_REWARDS
        assert 'save' in XP_REWARDS
        assert 'not_interested' in XP_REWARDS
        assert 'plan_complete' in XP_REWARDS
        assert 'streak_milestone' in XP_REWARDS

    def test_milestones_defined(self):
        """Milestones should be defined and in order."""
        assert len(STREAK_MILESTONES) > 0
        assert STREAK_MILESTONES == sorted(STREAK_MILESTONES)
        assert 3 in STREAK_MILESTONES  # First milestone
        assert 365 in STREAK_MILESTONES  # Year milestone

    def test_get_next_milestone_start(self):
        """Next milestone for day 0 should be 3."""
        result = self.service._get_next_milestone(0)
        assert result == 3

    def test_get_next_milestone_mid(self):
        """Next milestone for day 5 should be 7."""
        result = self.service._get_next_milestone(5)
        assert result == 7

    def test_get_next_milestone_exact(self):
        """Next milestone for day 7 should be 14."""
        result = self.service._get_next_milestone(7)
        assert result == 14

    def test_get_next_milestone_max(self):
        """Next milestone after 365 should be None."""
        result = self.service._get_next_milestone(400)
        assert result is None

    @patch('app.services.streak_service.db')
    def test_record_action_completion(self, mock_db):
        """Recording action should add XP."""
        # Setup mock
        mock_stats = MagicMock()
        mock_stats.total_xp = 100
        mock_stats.current_level = 'Explorer'
        mock_stats.current_streak_days = 5
        mock_stats.total_actions_completed = 10
        mock_db.session.get.return_value = mock_stats

        # Execute
        result = self.service.record_action_completion(user_id=1, action_type='follow')

        # Verify
        assert result['xp_earned'] == XP_REWARDS['follow']
        mock_stats.add_xp.assert_called_once()
        mock_db.session.commit.assert_called_once()

    @patch('app.services.streak_service.db')
    def test_record_action_unknown_type(self, mock_db):
        """Unknown action type should use default XP."""
        mock_stats = MagicMock()
        mock_stats.total_xp = 100
        mock_stats.current_level = 'Explorer'
        mock_stats.current_streak_days = 5
        mock_stats.total_actions_completed = 10
        mock_db.session.get.return_value = mock_stats

        result = self.service.record_action_completion(user_id=1, action_type='unknown_type')

        assert result['xp_earned'] == XP_DEFAULT

    @patch('app.services.streak_service.analytics_service')
    @patch('app.services.streak_service.db')
    def test_record_plan_completion_no_milestone(self, mock_db, mock_analytics):
        """Plan completion without milestone."""
        mock_stats = MagicMock()
        mock_stats.current_streak_days = 2  # Not a milestone
        mock_stats.longest_streak_days = 5
        mock_stats.total_xp = 100
        mock_stats.total_plans_completed = 10
        mock_stats.total_days_active = 5
        mock_stats.avg_completion_rate = 0.8
        mock_stats.achievements = []
        mock_db.session.get.return_value = mock_stats

        result = self.service.record_plan_completion(user_id=1)

        assert result['milestone'] is None
        mock_stats.update_streak.assert_called_once()

    @patch('app.services.streak_service.analytics_service')
    @patch('app.services.streak_service.db')
    def test_record_plan_completion_with_milestone(self, mock_db, mock_analytics):
        """Plan completion on milestone day should give bonus XP."""
        mock_stats = MagicMock()
        mock_stats.current_streak_days = 7  # Milestone!
        mock_stats.longest_streak_days = 7
        mock_stats.total_xp = 100
        mock_stats.total_plans_completed = 10
        mock_stats.total_days_active = 7
        mock_stats.avg_completion_rate = 1.0
        mock_stats.achievements = []
        mock_stats.current_level = 'Explorer'
        mock_db.session.get.return_value = mock_stats

        result = self.service.record_plan_completion(user_id=1)

        assert result['milestone'] == 7
        # Should have called add_xp twice: once for plan, once for milestone
        assert mock_stats.add_xp.call_count == 2
        # Should track milestone event
        mock_analytics.track_event.assert_called_once()


class TestStreakServiceIntegration:
    """Integration tests requiring database."""

    @pytest.fixture
    def app(self):
        """Create test app."""
        from app import create_app, db
        app = create_app('testing')

        with app.app_context():
            db.create_all()

        yield app

        with app.app_context():
            db.session.rollback()

    @pytest.fixture
    def test_user(self, app):
        """Create a test user for integration tests."""
        import uuid
        from app import db
        from app.models import User

        with app.app_context():
            user = User(
                client_id=f'test_{uuid.uuid4().hex[:16]}',
                email='streak_test@example.com',
                password_hash='dummy_hash'
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        yield user_id

        # Cleanup
        with app.app_context():
            from app.models import UserBehaviorStats
            UserBehaviorStats.query.filter_by(user_id=user_id).delete()
            User.query.filter_by(id=user_id).delete()
            db.session.commit()

    def test_check_streak_status_new_user(self, app, test_user):
        """Check streak status for user without prior stats."""
        with app.app_context():
            service = StreakService()
            result = service.check_streak_status(user_id=test_user)

            assert result['current_streak'] == 0
            assert result['next_milestone'] == 3


# Run with: pytest tests/test_streak_service.py -v
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
