from .auth import auth_bp
from .oauth import oauth_bp
from .plans import plans_bp
from .categories import categories_bp
from .health import health_bp
from .user import user_bp
from .actions import actions_bp
from .recommendations import recommendations_bp
from .user_stats import user_stats_bp
from .preferences import preferences_bp
from .analytics import analytics_bp
from .waitlist import waitlist_bp
from .user_categories import user_categories_bp
from .config import config_bp
from .plans_v2 import plans_v2_bp
from .analytics_v2 import analytics_v2_bp
from .admin_metrics import admin_metrics_bp


def register_blueprints(app):
    """Register all blueprints with the Flask app."""

    # Auth routes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(oauth_bp, url_prefix='/api/auth/oauth')
    app.register_blueprint(plans_bp, url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(actions_bp, url_prefix='/api')

    # AI Pipeline routes
    app.register_blueprint(recommendations_bp, url_prefix='/api/v1')
    app.register_blueprint(user_stats_bp, url_prefix='/api/user')

    # Preferences
    app.register_blueprint(preferences_bp, url_prefix='/api')

    # Analytics
    app.register_blueprint(analytics_bp, url_prefix='/api')

    # Waitlist (Premium)
    app.register_blueprint(waitlist_bp, url_prefix='/api')

    # User Categories (Multi-select)
    app.register_blueprint(user_categories_bp, url_prefix='/api')

    # Config (Public settings)
    app.register_blueprint(config_bp, url_prefix='/api')

    # V2 API (Plans v2, Toxic Creators)
    app.register_blueprint(plans_v2_bp, url_prefix='/api/v2')
    # Analytics V2
    app.register_blueprint(analytics_v2_bp, url_prefix='/api/v2/analytics')

    # Admin Metrics Dashboard
    app.register_blueprint(admin_metrics_bp, url_prefix='/api/admin/metrics')
