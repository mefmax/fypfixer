"""
Health Check Tasks - Monitor system health and send alerts.

Run every 5 minutes via cron:
*/5 * * * * cd /opt/fypfixer && docker-compose exec -T backend python -c "from app.tasks.health_tasks import check_system_health; check_system_health()"
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy import func, text

logger = logging.getLogger(__name__)

# Thresholds
ERROR_RATE_THRESHOLD = 5.0  # percent
LATENCY_P95_THRESHOLD = 1000  # ms
AI_COST_THRESHOLD = 50.0  # USD


def get_error_rate_last_hour() -> float:
    """Calculate error rate (4xx + 5xx) in the last hour."""
    from app import db
    from app.models import RequestLog

    hour_ago = datetime.utcnow() - timedelta(hours=1)

    total = db.session.query(func.count(RequestLog.id)).filter(
        RequestLog.created_at >= hour_ago
    ).scalar() or 1

    errors = db.session.query(func.count(RequestLog.id)).filter(
        RequestLog.created_at >= hour_ago,
        RequestLog.status >= 400
    ).scalar() or 0

    return round((errors / total) * 100, 2) if total > 0 else 0


def get_api_latency_p95() -> int:
    """Get P95 latency in the last hour."""
    from app import db

    hour_ago = datetime.utcnow() - timedelta(hours=1)

    result = db.session.execute(text("""
        SELECT PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms)
        FROM request_logs
        WHERE created_at >= :hour_ago
    """), {'hour_ago': hour_ago}).scalar()

    return int(result) if result else 0


def get_ai_cost_today() -> float:
    """Get total AI cost for today."""
    from app import db
    from app.models import AIRequestLog
    from datetime import date

    today_start = datetime.combine(date.today(), datetime.min.time())

    result = db.session.query(func.sum(AIRequestLog.cost_usd)).filter(
        AIRequestLog.created_at >= today_start
    ).scalar()

    return float(result) if result else 0


def check_system_health():
    """
    Check system health and send alerts if thresholds exceeded.

    Should run every 5 minutes.
    """
    from app import create_app
    from app.services.alerting_service import alerting_service

    app = create_app()

    with app.app_context():
        alerts_sent = 0

        # Check error rate
        try:
            error_rate = get_error_rate_last_hour()
            if error_rate > ERROR_RATE_THRESHOLD:
                alerting_service.send_critical(
                    'High Error Rate',
                    f'Error rate: {error_rate}%\nThreshold: {ERROR_RATE_THRESHOLD}%'
                )
                alerts_sent += 1
        except Exception as e:
            logger.error(f"Error checking error rate: {e}")

        # Check API latency
        try:
            latency = get_api_latency_p95()
            if latency > LATENCY_P95_THRESHOLD:
                alerting_service.send_warning(
                    'Slow API Response',
                    f'P95 latency: {latency}ms\nThreshold: {LATENCY_P95_THRESHOLD}ms'
                )
                alerts_sent += 1
        except Exception as e:
            logger.error(f"Error checking latency: {e}")

        # Check AI cost
        try:
            ai_cost = get_ai_cost_today()
            if ai_cost > AI_COST_THRESHOLD:
                alerting_service.send_warning(
                    'High AI Cost',
                    f'Cost today: ${ai_cost:.2f}\nThreshold: ${AI_COST_THRESHOLD}'
                )
                alerts_sent += 1
        except Exception as e:
            logger.error(f"Error checking AI cost: {e}")

        logger.info(f"Health check complete. Alerts sent: {alerts_sent}")
        return alerts_sent


if __name__ == '__main__':
    check_system_health()
