"""
Integration tests for API endpoints.

Run with: pytest tests/test_api.py -v

Note: These tests require PostgreSQL database.
SQLite has compatibility issues with BigInteger PK, RETURNING clause, etc.
"""

import pytest
import json
from app import create_app, db
from app.models import User, Category

@pytest.fixture(scope='module')
def app():
    """Create test application."""
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        # Seed test category
        if not Category.query.filter_by(code='personal_growth').first():
            category = Category(
                code='personal_growth',
                name_en='Personal Growth',
                name_ru='Личный рост',
                is_active=True
            )
            db.session.add(category)
            db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return headers."""
    import time
    unique = str(int(time.time() * 1000))

    # Register user
    client.post('/api/auth/register', json={
        'username': f'testuser_{unique}',
        'email': f'test_{unique}@example.com',
        'password': 'testpass123'
    })

    # Login
    response = client.post('/api/auth/login', json={
        'email': f'test_{unique}@example.com',
        'password': 'testpass123'
    })

    data = json.loads(response.data)
    token = data['data']['token']

    return {'Authorization': f'Bearer {token}'}


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Health endpoint should return OK."""
        response = client.get('/api/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestAuthEndpoints:
    """Tests for authentication endpoints."""

    def test_register_success(self, client):
        """Registration should create user."""
        response = client.post('/api/auth/register', json={
            'email': 'new@example.com',
            'password': 'password123'
        })

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'token' in data['data']

    def test_register_duplicate_email(self, client):
        """Duplicate email should fail."""
        # First registration
        client.post('/api/auth/register', json={
            'email': 'duplicate@example.com',
            'password': 'password123'
        })

        # Second registration with same email
        response = client.post('/api/auth/register', json={
            'email': 'duplicate@example.com',
            'password': 'password123'
        })

        assert response.status_code in [400, 409]

    def test_login_success(self, client):
        """Login with correct credentials should succeed."""
        # Register first
        client.post('/api/auth/register', json={
            'email': 'login@example.com',
            'password': 'password123'
        })

        # Login
        response = client.post('/api/auth/login', json={
            'email': 'login@example.com',
            'password': 'password123'
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data['data']
        assert 'refresh_token' in data['data']

    def test_login_wrong_password(self, client):
        """Login with wrong password should fail."""
        response = client.post('/api/auth/login', json={
            'email': 'login@example.com',
            'password': 'wrongpassword'
        })

        assert response.status_code == 401


class TestCategoriesEndpoint:
    """Tests for categories endpoint."""

    def test_get_categories(self, client):
        """Should return list of categories."""
        response = client.get('/api/categories')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'categories' in data['data']


class TestPlansEndpoints:
    """Tests for plans/recommendations endpoints."""

    def test_generate_plan_anonymous(self, client):
        """Anonymous user should be able to generate plan."""
        response = client.post('/api/v1/plans/generate', json={
            'category': 'personal_growth'
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'actions' in data['data']

    def test_generate_plan_authenticated(self, client, auth_headers):
        """Authenticated user should get personalized plan."""
        response = client.post(
            '/api/v1/plans/generate',
            json={'category': 'personal_growth'},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['actions']) > 0

    def test_get_today_plan(self, client):
        """Should return today's plan."""
        response = client.get('/api/v1/plans/today?category=personal_growth')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    def test_plan_status(self, client):
        """Should return plan status."""
        response = client.get('/api/v1/plans/status?category=personal_growth')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'hasPlan' in data['data']


class TestActionsEndpoints:
    """Tests for actions endpoints."""

    def test_get_daily_actions(self, client):
        """Should return daily actions."""
        # First generate a plan
        client.post('/api/v1/plans/generate', json={
            'category': 'personal_growth'
        })

        response = client.get('/api/actions?category=personal_growth')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'actions' in data['data']

    def test_complete_action_requires_auth(self, client):
        """Completing action should require authentication."""
        response = client.post('/api/actions/action-1/complete')

        assert response.status_code == 401

    def test_complete_action_authenticated(self, client, auth_headers):
        """Authenticated user should be able to complete action."""
        # Generate plan first
        plan_response = client.post(
            '/api/v1/plans/generate',
            json={'category': 'personal_growth'},
            headers=auth_headers
        )
        plan_data = json.loads(plan_response.data)

        if plan_data['success'] and plan_data['data']['actions']:
            action_id = plan_data['data']['actions'][0]['id']

            response = client.post(
                f'/api/actions/{action_id}/complete',
                headers=auth_headers
            )

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['data']['completed'] is True


class TestUserStatsEndpoints:
    """Tests for user stats endpoints."""

    def test_get_stats_requires_auth(self, client):
        """Stats endpoint should require auth."""
        response = client.get('/api/user/stats')

        assert response.status_code == 401

    def test_get_stats_authenticated(self, client, auth_headers):
        """Authenticated user should get stats."""
        response = client.get('/api/user/stats', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'streak' in data['data']
        assert 'gamification' in data['data']

    def test_get_leaderboard(self, client):
        """Leaderboard should be public."""
        response = client.get('/api/user/leaderboard')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'leaderboard' in data['data']


# Run with: pytest tests/test_api.py -v
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
