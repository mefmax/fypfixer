"""
API Contract Tests - Verify API responses match frontend expectations.

These tests ensure that:
1. Response structure matches TypeScript interfaces
2. Field names use correct camelCase
3. All required fields are present
4. Data types are correct

Run with: pytest tests/test_api_contracts.py -v
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

        # Seed test categories (free + premium)
        if not Category.query.filter_by(code='fitness').first():
            categories = [
                Category(
                    code='fitness',
                    name_en='Fitness',
                    name_ru='Фитнес',
                    is_active=True,
                    is_premium=False,
                    display_order=1,
                ),
                Category(
                    code='wellness',
                    name_en='Wellness',
                    name_ru='Здоровье',
                    is_active=True,
                    is_premium=False,
                    display_order=2,
                ),
                Category(
                    code='premium_category',
                    name_en='Premium Category',
                    name_ru='Премиум категория',
                    is_active=True,
                    is_premium=True,
                    price=4.99,
                    coming_soon=True,
                    display_order=10,
                ),
            ]
            for cat in categories:
                db.session.add(cat)
            db.session.commit()

        yield app

        db.session.remove()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return headers with strong password."""
    import time
    unique = str(int(time.time() * 1000))

    # Register user with strong password (10+ chars, upper, lower, digit, special)
    response = client.post('/api/auth/register', json={
        'email': f'test_{unique}@example.com',
        'password': 'TestPass123!'  # Strong password
    })

    data = json.loads(response.data)
    if not data.get('success'):
        pytest.skip(f"Registration failed: {data}")

    token = data['data']['token']
    return {'Authorization': f'Bearer {token}'}


class TestAuthResponseContract:
    """
    Frontend expects:
    AuthResponse {
        success: boolean,
        data: {
            user: User,
            token: string,
            refresh_token: string
        }
    }
    """

    def test_register_response_format(self, client):
        """Registration response must match AuthResponse interface."""
        import time
        unique = str(int(time.time() * 1000))

        response = client.post('/api/auth/register', json={
            'email': f'contract_{unique}@example.com',
            'password': 'TestPass123!'
        })

        assert response.status_code == 201
        data = json.loads(response.data)

        # Check structure
        assert 'success' in data
        assert data['success'] is True
        assert 'data' in data

        # Check data fields
        assert 'user' in data['data'], "Missing 'user' in response"
        assert 'token' in data['data'], "Missing 'token' in response"
        assert 'refresh_token' in data['data'], "Missing 'refresh_token' in response"

        # Check user fields
        user = data['data']['user']
        assert 'id' in user
        assert 'email' in user

    def test_login_response_format(self, client):
        """Login response must match AuthResponse interface."""
        import time
        unique = str(int(time.time() * 1000))

        # First register
        client.post('/api/auth/register', json={
            'email': f'login_{unique}@example.com',
            'password': 'TestPass123!'
        })

        # Then login
        response = client.post('/api/auth/login', json={
            'email': f'login_{unique}@example.com',
            'password': 'TestPass123!'
        })

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True
        assert 'user' in data['data']
        assert 'token' in data['data']
        assert 'refresh_token' in data['data']


class TestUserStatsResponseContract:
    """
    Frontend expects:
    UserStats {
        streak: {
            currentStreak: number,
            longestStreak: number,
            lastActiveDate: string | null,
            nextMilestone: number | null
        },
        gamification: {
            level: string,
            xp: number,
            actionsCompleted: number,
            plansCompleted: number
        }
    }
    """

    def test_user_stats_response_format(self, client, auth_headers):
        """GET /api/user/stats must match UserStats interface."""
        response = client.get('/api/user/stats', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True

        # Check streak object
        streak = data['data']['streak']
        assert 'currentStreak' in streak, "Missing 'currentStreak' (was 'current'?)"
        assert 'longestStreak' in streak, "Missing 'longestStreak' (was 'max'?)"
        assert 'lastActiveDate' in streak, "Missing 'lastActiveDate'"
        assert 'nextMilestone' in streak, "Missing 'nextMilestone'"

        # Check types
        assert isinstance(streak['currentStreak'], int)
        assert isinstance(streak['longestStreak'], int)
        assert streak['lastActiveDate'] is None or isinstance(streak['lastActiveDate'], str)
        assert streak['nextMilestone'] is None or isinstance(streak['nextMilestone'], int)

        # Check gamification object
        gamification = data['data']['gamification']
        assert 'level' in gamification, "Missing 'level'"
        assert 'xp' in gamification, "Missing 'xp'"
        assert 'actionsCompleted' in gamification, "Missing 'actionsCompleted'"
        assert 'plansCompleted' in gamification, "Missing 'plansCompleted'"

        # Check types
        assert isinstance(gamification['level'], str)
        assert isinstance(gamification['xp'], int)
        assert isinstance(gamification['actionsCompleted'], int)
        assert isinstance(gamification['plansCompleted'], int)


class TestStreakInfoResponseContract:
    """
    Frontend expects:
    StreakInfo {
        currentStreak: number,
        longestStreak: number,
        nextMilestone: number | null,
        totalXp: number,
        level: string
    }
    """

    def test_streak_response_format(self, client, auth_headers):
        """GET /api/user/streak must match StreakInfo interface."""
        response = client.get('/api/user/streak', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True
        streak = data['data']

        # Check required fields
        assert 'currentStreak' in streak, "Missing 'currentStreak'"
        assert 'longestStreak' in streak, "Missing 'longestStreak'"
        assert 'nextMilestone' in streak, "Missing 'nextMilestone'"
        assert 'totalXp' in streak, "Missing 'totalXp'"
        assert 'level' in streak, "Missing 'level'"

        # Check types
        assert isinstance(streak['currentStreak'], int)
        assert isinstance(streak['longestStreak'], int)
        assert streak['nextMilestone'] is None or isinstance(streak['nextMilestone'], int)
        assert isinstance(streak['totalXp'], int)
        assert isinstance(streak['level'], str)


class TestPreferencesResponseContract:
    """
    Frontend expects:
    UserPreferences {
        hasCompletedOnboarding: boolean,
        selectedGoals: string[],
        preferredCategory: string,
        language: string
    }
    """

    def test_get_preferences_response_format(self, client, auth_headers):
        """GET /api/preferences must return all 4 fields."""
        response = client.get('/api/preferences', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True
        prefs = data['data']

        # Check all required fields
        assert 'hasCompletedOnboarding' in prefs
        assert 'selectedGoals' in prefs
        assert 'preferredCategory' in prefs
        assert 'language' in prefs, "Missing 'language' in GET response"

        # Check types
        assert isinstance(prefs['hasCompletedOnboarding'], bool)
        assert isinstance(prefs['selectedGoals'], list)
        assert isinstance(prefs['preferredCategory'], str)
        assert isinstance(prefs['language'], str)

    def test_put_preferences_response_format(self, client, auth_headers):
        """PUT /api/preferences must return all 4 fields including language."""
        response = client.put('/api/preferences',
            json={'preferredCategory': 'fitness'},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True
        prefs = data['data']

        # Check all required fields
        assert 'hasCompletedOnboarding' in prefs
        assert 'selectedGoals' in prefs
        assert 'preferredCategory' in prefs
        assert 'language' in prefs, "Missing 'language' in PUT response"


class TestCategoriesResponseContract:
    """
    Frontend expects:
    Category {
        id: number,
        code: string,
        name: string,
        emoji?: string,
        description?: string,
        is_premium: boolean,
        price?: number,
        coming_soon?: boolean,
        on_waitlist?: boolean
    }
    """

    def test_categories_response_format(self, client):
        """GET /api/categories must match Category interface."""
        response = client.get('/api/categories')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True
        assert 'categories' in data['data']
        categories = data['data']['categories']
        assert len(categories) > 0, "No categories returned"

        # Check first category has required fields
        cat = categories[0]
        assert 'id' in cat
        assert 'code' in cat
        assert 'name' in cat
        assert 'is_premium' in cat

        # Check types
        assert isinstance(cat['id'], int)
        assert isinstance(cat['code'], str)
        assert isinstance(cat['name'], str)
        assert isinstance(cat['is_premium'], bool)

    def test_categories_include_premium_info(self, client):
        """Premium categories must include price and coming_soon fields."""
        response = client.get('/api/categories?include_premium=true')

        assert response.status_code == 200
        data = json.loads(response.data)

        categories = data['data']['categories']
        premium_cats = [c for c in categories if c['is_premium']]

        if premium_cats:
            cat = premium_cats[0]
            assert 'price' in cat, "Premium category missing 'price'"
            assert 'coming_soon' in cat, "Premium category missing 'coming_soon'"


class TestDailyActionPlanResponseContract:
    """
    Frontend expects:
    DailyActionPlan {
        id: string,
        date: string,
        categoryCode: string,
        categoryName: string,
        actions: PlanAction[],
        motivation?: string,
        progress: { completed: number, total: number },
        metadata?: object
    }
    """

    def test_plans_today_response_format(self, client):
        """GET /api/v1/plans/today must match DailyActionPlan interface."""
        response = client.get('/api/v1/plans/today?category=fitness')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True
        plan = data['data']

        # Check required fields
        assert 'id' in plan, "Missing 'id'"
        assert 'date' in plan, "Missing 'date'"
        assert 'categoryCode' in plan, "Missing 'categoryCode'"
        assert 'categoryName' in plan, "Missing 'categoryName'"
        assert 'actions' in plan, "Missing 'actions'"
        assert 'progress' in plan, "Missing 'progress'"

        # Check progress structure
        progress = plan['progress']
        assert 'completed' in progress
        assert 'total' in progress

        # Check actions array
        assert isinstance(plan['actions'], list)
        if plan['actions']:
            action = plan['actions'][0]
            assert 'id' in action
            assert 'type' in action
            assert 'title' in action
            assert 'completed' in action

    def test_plans_generate_response_format(self, client):
        """POST /api/v1/plans/generate must match DailyActionPlan interface."""
        response = client.post('/api/v1/plans/generate', json={
            'category': 'fitness',
            'language': 'en'
        })

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True
        plan = data['data']

        # Check same structure as /today
        assert 'id' in plan
        assert 'date' in plan
        assert 'actions' in plan
        assert 'progress' in plan


class TestCompleteActionResponseContract:
    """
    Frontend expects:
    CompleteActionResponse {
        actionId: string,
        completed: boolean,
        xpEarned?: number,
        planCompleted?: boolean
    }
    """

    def test_complete_action_response_format(self, client, auth_headers):
        """POST /api/actions/{id}/complete must match CompleteActionResponse."""
        # First generate a plan
        plan_response = client.post(
            '/api/v1/plans/generate',
            json={'category': 'fitness'},
            headers=auth_headers
        )
        plan_data = json.loads(plan_response.data)

        if not plan_data['success'] or not plan_data['data']['actions']:
            pytest.skip("No actions in plan")

        action_id = plan_data['data']['actions'][0]['id']

        # Complete the action
        response = client.post(
            f'/api/actions/{action_id}/complete',
            headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True
        result = data['data']

        # Check required fields
        assert 'completed' in result, "Missing 'completed'"
        assert isinstance(result['completed'], bool)

        # Check optional fields if present
        if 'xpEarned' in result:
            assert isinstance(result['xpEarned'], int)
        if 'planCompleted' in result:
            assert isinstance(result['planCompleted'], bool)


class TestUserCategoriesResponseContract:
    """
    Frontend expects:
    UserCategoriesResponse {
        categories: UserCategory[],
        stats: CategoryStats
    }
    """

    def test_user_categories_response_format(self, client, auth_headers):
        """GET /api/user/categories must match UserCategoriesResponse."""
        response = client.get('/api/user/categories', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True

        # Check structure
        assert 'categories' in data['data'], "Missing 'categories'"
        assert 'stats' in data['data'], "Missing 'stats'"

        # Check stats structure
        stats = data['data']['stats']
        assert 'freeActive' in stats, "Missing 'freeActive' in stats"
        assert 'freeLimit' in stats, "Missing 'freeLimit' in stats"
        assert 'freeRemaining' in stats, "Missing 'freeRemaining' in stats"


class TestWaitlistResponseContract:
    """
    Frontend expects:
    JoinWaitlistResponse {
        message: string,
        category: string,
        position?: number
    }
    """

    def test_join_waitlist_response_format(self, client, auth_headers):
        """POST /api/waitlist/join must match JoinWaitlistResponse."""
        # Get premium category ID
        cats_response = client.get('/api/categories')
        cats_data = json.loads(cats_response.data)
        premium_cats = [c for c in cats_data['data']['categories'] if c['is_premium']]

        if not premium_cats:
            pytest.skip("No premium categories")

        # Join waitlist
        response = client.post('/api/waitlist/join',
            json={'category_id': premium_cats[0]['id']},
            headers=auth_headers
        )

        assert response.status_code in [200, 201]
        data = json.loads(response.data)

        assert data['success'] is True

        # Check required fields
        assert 'message' in data['data'], "Missing 'message'"
        assert 'category' in data['data'], "Missing 'category'"

        # Check optional field
        if 'position' in data['data']:
            assert isinstance(data['data']['position'], int)


class TestConfigResponseContract:
    """
    Frontend expects:
    AppConfig {
        defaultCategoryCode: string | null,
        maxFreeCategories: number,
        premiumAccessDays: number,
        actionsPerPlan: number
    }
    """

    def test_config_defaults_response_format(self, client):
        """GET /api/config/defaults must match AppConfig interface."""
        response = client.get('/api/config/defaults')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data['success'] is True
        config = data['data']

        # Check required fields
        assert 'defaultCategoryCode' in config, "Missing 'defaultCategoryCode'"
        assert 'maxFreeCategories' in config, "Missing 'maxFreeCategories'"
        assert 'premiumAccessDays' in config, "Missing 'premiumAccessDays'"
        assert 'actionsPerPlan' in config, "Missing 'actionsPerPlan'"

        # Check types
        assert config['defaultCategoryCode'] is None or isinstance(config['defaultCategoryCode'], str)
        assert isinstance(config['maxFreeCategories'], int)
        assert isinstance(config['premiumAccessDays'], int)
        assert isinstance(config['actionsPerPlan'], int)


# Run with: pytest tests/test_api_contracts.py -v
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
