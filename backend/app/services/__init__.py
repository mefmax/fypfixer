from .auth_service import AuthService
from .plan_service import PlanService
from .action_service import ActionService
from .recommendation_service import recommendation_service
from .streak_service import streak_service
from .motivation_service import motivation_service
from .analytics_service import analytics_service, AnalyticsService
from .metrics_service import metrics_service, MetricsService

auth_service = AuthService()
plan_service = PlanService()
action_service = ActionService()

__all__ = [
    'auth_service',
    'plan_service',
    'action_service',
    'recommendation_service',
    'streak_service',
    'motivation_service',
    'analytics_service',
    'AnalyticsService',
    'metrics_service',
    'MetricsService',
]
