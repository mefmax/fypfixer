"""
Pytest configuration and shared fixtures.
"""

import pytest
import json
import os

# Ensure we use testing config
os.environ['FLASK_ENV'] = 'testing'

from app import create_app, db
from app.models import Category, User


@pytest.fixture(scope='module')
def app():
    """Create application for testing."""
    app = create_app('testing')

    with app.app_context():
        # Create all tables
        db.create_all()

        # Seed required data
        _seed_test_data()

        yield app

        # Cleanup - drop all data but keep tables
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


def _seed_test_data():
    """Seed minimum required data for tests."""
    # Check if already seeded
    if Category.query.filter_by(code='personal_growth').first():
        return

    # Add categories
    categories = [
        Category(
            code='personal_growth',
            name_en='Personal Growth',
            name_ru='Личный рост',
            is_active=True
        ),
        Category(
            code='wellness',
            name_en='Wellness',
            name_ru='Здоровье',
            is_active=True
        ),
    ]

    for cat in categories:
        db.session.add(cat)

    db.session.commit()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Create database session for testing."""
    with app.app_context():
        yield db.session
        db.session.rollback()


@pytest.fixture
def auth_headers(client, app):
    """Create authenticated user and return headers."""
    with app.app_context():
        import time
        unique = str(int(time.time() * 1000))

        # Register unique user
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

        if data.get('success') and data.get('data', {}).get('token'):
            return {'Authorization': f'Bearer {data["data"]["token"]}'}

        return {}
