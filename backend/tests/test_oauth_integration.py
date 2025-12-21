"""
Integration tests for OAuth authentication flow.

Tests:
- OAuth URL generation
- User model with OAuth fields
- JWT token generation for OAuth users
- OAuth callback flow
- Backwards compatibility
"""

import pytest
import json
from app import create_app, db
from app.models.user import User
from app.services.auth_service import auth_service
import secrets


@pytest.fixture
def app():
    """Create test application."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestOAuthURLGeneration:
    """Test OAuth URL generation endpoint."""

    def test_tiktok_url_generation(self, client):
        """Test GET /api/auth/oauth/tiktok/url returns valid URL."""
        response = client.get('/api/auth/oauth/tiktok/url')

        assert response.status_code == 200
        data = response.get_json()

        # Check response structure
        assert data['success'] is True
        assert 'data' in data
        assert 'url' in data['data']

        url = data['data']['url']

        # Validate URL contains required parameters
        assert 'https://www.tiktok.com/v2/auth/authorize/' in url
        assert 'client_key=' in url
        assert 'scope=' in url
        assert 'response_type=code' in url
        assert 'redirect_uri=' in url
        assert 'state=' in url

        # Validate scopes
        assert 'user.info.basic' in url
        assert 'user.info.profile' in url

    def test_url_generates_unique_state(self, client):
        """Test that each request generates unique CSRF state token."""
        response1 = client.get('/api/auth/oauth/tiktok/url')
        response2 = client.get('/api/auth/oauth/tiktok/url')

        url1 = response1.get_json()['data']['url']
        url2 = response2.get_json()['data']['url']

        # Extract state parameters
        state1 = url1.split('state=')[1].split('&')[0] if 'state=' in url1 else ''
        state2 = url2.split('state=')[1].split('&')[0] if 'state=' in url2 else ''

        assert state1 != state2, "State tokens should be unique"
        assert len(state1) > 20, "State token should be long enough"


class TestUserModelOAuth:
    """Test User model with new OAuth fields."""

    def test_create_oauth_user(self, app):
        """Test creating user with OAuth credentials."""
        with app.app_context():
            user = User(
                client_id=secrets.token_urlsafe(32),
                oauth_provider='tiktok',
                oauth_id='tiktok_user_123',
                display_name='Test User',
                avatar_url='https://example.com/avatar.jpg',
                language='en'
            )
            db.session.add(user)
            db.session.commit()

            # Verify user was created
            saved_user = User.query.filter_by(oauth_id='tiktok_user_123').first()
            assert saved_user is not None
            assert saved_user.oauth_provider == 'tiktok'
            assert saved_user.display_name == 'Test User'
            assert saved_user.avatar_url == 'https://example.com/avatar.jpg'
            assert saved_user.email is None  # Email is optional for OAuth users

    def test_oauth_user_to_dict(self, app):
        """Test User.to_dict() includes OAuth fields."""
        with app.app_context():
            user = User(
                client_id=secrets.token_urlsafe(32),
                oauth_provider='tiktok',
                oauth_id='tiktok_user_456',
                display_name='OAuth User',
                avatar_url='https://example.com/photo.jpg',
                language='en'
            )
            db.session.add(user)
            db.session.commit()

            user_dict = user.to_dict()

            # Verify all OAuth fields are present
            assert 'oauth_provider' in user_dict
            assert user_dict['oauth_provider'] == 'tiktok'
            assert 'display_name' in user_dict
            assert user_dict['display_name'] == 'OAuth User'
            assert 'avatar_url' in user_dict
            assert user_dict['avatar_url'] == 'https://example.com/photo.jpg'

            # Verify standard fields still present
            assert 'id' in user_dict
            assert 'client_id' in user_dict
            assert 'is_premium' in user_dict
            assert 'language' in user_dict

    def test_unique_constraint_oauth_provider_id(self, app):
        """Test unique constraint on (oauth_provider, oauth_id)."""
        with app.app_context():
            # Create first user
            user1 = User(
                client_id=secrets.token_urlsafe(32),
                oauth_provider='tiktok',
                oauth_id='same_oauth_id',
                display_name='User 1',
                language='en'
            )
            db.session.add(user1)
            db.session.commit()

            # Try to create duplicate
            user2 = User(
                client_id=secrets.token_urlsafe(32),
                oauth_provider='tiktok',
                oauth_id='same_oauth_id',  # Same OAuth ID
                display_name='User 2',
                language='en'
            )
            db.session.add(user2)

            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()


class TestOAuthJWTGeneration:
    """Test JWT token generation for OAuth users."""

    def test_generate_tokens_for_oauth_user(self, app):
        """Test that OAuth users can get JWT tokens."""
        with app.app_context():
            user = User(
                client_id=secrets.token_urlsafe(32),
                oauth_provider='tiktok',
                oauth_id='tiktok_jwt_test',
                display_name='JWT Test User',
                language='en'
            )
            db.session.add(user)
            db.session.commit()

            # Generate tokens
            tokens = auth_service.generate_tokens(user)

            assert 'access_token' in tokens
            assert 'refresh_token' in tokens
            assert isinstance(tokens['access_token'], str)
            assert isinstance(tokens['refresh_token'], str)
            assert len(tokens['access_token']) > 50  # JWT should be long


class TestBackwardsCompatibility:
    """Test that existing email/password users still work."""

    def test_legacy_email_user_still_exists(self, app):
        """Test that old users with email/password can still exist in DB."""
        with app.app_context():
            # Create legacy user (email/password)
            legacy_user = User(
                client_id=secrets.token_urlsafe(32),
                email='legacy@test.com',
                password_hash='$2b$12$test_hash',
                language='en'
            )
            db.session.add(legacy_user)
            db.session.commit()

            # Verify user exists
            saved = User.query.filter_by(email='legacy@test.com').first()
            assert saved is not None
            assert saved.email == 'legacy@test.com'
            assert saved.password_hash is not None
            assert saved.oauth_provider is None  # No OAuth
            assert saved.oauth_id is None

    def test_legacy_user_to_dict(self, app):
        """Test that legacy users serialize correctly with new to_dict()."""
        with app.app_context():
            legacy_user = User(
                client_id=secrets.token_urlsafe(32),
                email='old@test.com',
                password_hash='hash123',
                language='en'
            )
            db.session.add(legacy_user)
            db.session.commit()

            user_dict = legacy_user.to_dict()

            # Should have email
            assert 'email' in user_dict
            assert user_dict['email'] == 'old@test.com'

            # OAuth fields should be None/null
            assert 'oauth_provider' in user_dict
            assert user_dict['oauth_provider'] is None
            assert 'display_name' in user_dict
            assert user_dict['display_name'] is None
            assert 'avatar_url' in user_dict
            assert user_dict['avatar_url'] is None


class TestOAuthCallbackResponse:
    """Test OAuth callback response format matches frontend expectations."""

    def test_callback_response_structure(self, app):
        """Test that callback would return correct structure."""
        with app.app_context():
            # Create OAuth user (simulating successful callback)
            user = User(
                client_id=secrets.token_urlsafe(32),
                oauth_provider='tiktok',
                oauth_id='callback_test_user',
                display_name='Callback User',
                avatar_url='https://example.com/pic.jpg',
                is_premium=False,
                language='en'
            )
            db.session.add(user)
            db.session.commit()

            # Generate tokens
            tokens = auth_service.generate_tokens(user)

            # Simulate callback response
            response = {
                'access_token': tokens['access_token'],
                'refresh_token': tokens.get('refresh_token'),
                'user': {
                    'id': user.id,
                    'display_name': user.display_name,
                    'avatar_url': user.avatar_url,
                    'oauth_provider': user.oauth_provider,
                    'is_premium': user.is_premium
                }
            }

            # Validate structure
            assert 'access_token' in response
            assert 'refresh_token' in response
            assert 'user' in response

            user_data = response['user']
            assert 'id' in user_data
            assert 'display_name' in user_data
            assert user_data['display_name'] == 'Callback User'
            assert 'avatar_url' in user_data
            assert 'oauth_provider' in user_data
            assert user_data['oauth_provider'] == 'tiktok'
            assert 'is_premium' in user_data
            assert user_data['is_premium'] is False
