"""
Unit tests for RecommendationService.

Run with: pytest tests/test_recommendation_service.py -v
"""

import pytest
from datetime import date, datetime
from unittest.mock import Mock, patch, MagicMock

from app.services.recommendation_service import RecommendationService
from app.ai_providers.base import UserContext, SelectedAction


class TestRecommendationService:
    """Tests for RecommendationService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = RecommendationService()

    def test_get_time_of_day_morning(self):
        """Test morning detection."""
        with patch('app.services.recommendation_service.datetime') as mock_dt:
            mock_dt.now.return_value = MagicMock(hour=9)
            result = self.service._get_time_of_day()
            assert result == 'morning'

    def test_get_time_of_day_afternoon(self):
        """Test afternoon detection."""
        with patch('app.services.recommendation_service.datetime') as mock_dt:
            mock_dt.now.return_value = MagicMock(hour=14)
            result = self.service._get_time_of_day()
            assert result == 'afternoon'

    def test_get_time_of_day_evening(self):
        """Test evening detection."""
        with patch('app.services.recommendation_service.datetime') as mock_dt:
            mock_dt.now.return_value = MagicMock(hour=20)
            result = self.service._get_time_of_day()
            assert result == 'evening'

    def test_get_seed_candidates_personal_growth(self):
        """Test seed candidates for personal_growth category."""
        candidates = self.service._get_seed_candidates('personal_growth')

        assert len(candidates) > 0
        assert all('creator_username' in c for c in candidates)
        assert all('tiktok_url' in c for c in candidates)

    def test_get_seed_candidates_wellness(self):
        """Test seed candidates for wellness category."""
        candidates = self.service._get_seed_candidates('wellness')

        assert len(candidates) > 0
        assert candidates != self.service._get_seed_candidates('personal_growth')

    def test_get_seed_candidates_unknown_fallback(self):
        """Unknown category should fallback to personal_growth."""
        candidates = self.service._get_seed_candidates('unknown_category')
        expected = self.service._get_seed_candidates('personal_growth')

        assert candidates == expected

    def test_get_seed_actions(self):
        """Test seed action generation."""
        actions = self.service._get_seed_actions('personal_growth', 5)

        assert len(actions) == 5
        assert all(isinstance(a, SelectedAction) for a in actions)

        # Should have variety of action types
        types = [a.type for a in actions]
        assert 'follow' in types or 'like' in types or 'save' in types

    def test_get_seed_actions_includes_not_interested(self):
        """Seed actions should include 'not_interested' type."""
        actions = self.service._get_seed_actions('personal_growth', 5)
        types = [a.type for a in actions]

        assert 'not_interested' in types

    def test_build_context_anonymous(self):
        """Build context for anonymous user."""
        with patch.object(self.service, '_get_time_of_day', return_value='morning'):
            context = self.service._build_context(
                user_id=None,
                category_code='personal_growth',
                language='en'
            )

        assert isinstance(context, UserContext)
        assert context.category == 'personal_growth'
        assert context.language == 'en'
        assert context.streak_days == 0
        assert context.difficulty == 5

    @patch('app.services.recommendation_service.db')
    def test_build_context_authenticated(self, mock_db):
        """Build context for authenticated user."""
        mock_stats = MagicMock()
        mock_stats.current_streak_days = 7
        mock_stats.current_difficulty = 6
        mock_db.session.get.return_value = mock_stats

        with patch.object(self.service, '_get_time_of_day', return_value='afternoon'):
            context = self.service._build_context(
                user_id=123,
                category_code='wellness',
                language='ru'
            )

        assert context.streak_days == 7
        assert context.difficulty == 6

    def test_error_response(self):
        """Test error response format."""
        result = self.service._error('test_code', 'Test message')

        assert result['success'] is False
        assert result['error']['code'] == 'test_code'
        assert result['error']['message'] == 'Test message'


class TestRecommendationServiceAI:
    """Tests for AI pipeline in RecommendationService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = RecommendationService()

    @patch('app.services.recommendation_service.db')
    @patch('app.services.recommendation_service.get_ai_provider')
    def test_pipeline_fallback_on_ai_failure(self, mock_get_provider, mock_db):
        """AI failure should fallback to seed data."""
        # Setup mock AI provider that fails
        mock_provider = MagicMock()
        mock_provider.generate_criteria.side_effect = Exception("AI failed")
        mock_get_provider.return_value = mock_provider

        # Setup context
        context = UserContext(
            category='personal_growth',
            language='en',
            time_of_day='morning'
        )
        mock_category = MagicMock(code='personal_growth')

        with patch.object(self.service, '_create_plan') as mock_create:
            mock_plan = MagicMock()
            mock_create.return_value = mock_plan

            plan, source = self.service._execute_pipeline(
                user_id=1,
                category=mock_category,
                context=context,
                language='en'
            )

        # Should have used seed data (source='seed')
        assert source == 'seed'
        mock_create.assert_called_once()


class TestUserContext:
    """Tests for UserContext dataclass."""

    def test_user_context_defaults(self):
        """Test UserContext default values."""
        context = UserContext(
            category='test',
            language='en',
            time_of_day='morning'
        )

        assert context.category == 'test'
        assert context.language == 'en'
        assert context.time_of_day == 'morning'
        assert context.streak_days == 0
        assert context.difficulty == 5

    def test_user_context_to_dict(self):
        """Test UserContext serialization."""
        context = UserContext(
            category='wellness',
            language='ru',
            time_of_day='evening',
            streak_days=5,
            difficulty=7
        )

        result = context.to_dict()

        assert result['category'] == 'wellness'
        assert result['language'] == 'ru'
        assert result['time_of_day'] == 'evening'
        assert result['streak_days'] == 5
        assert result['difficulty'] == 7


# Run with: pytest tests/test_recommendation_service.py -v
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
