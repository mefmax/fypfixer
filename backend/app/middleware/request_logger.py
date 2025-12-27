"""
Request Logger Middleware - Logs all API requests for monitoring.

Records:
- endpoint
- method
- status code
- latency_ms
- user_id (if authenticated)
- ip_address
"""

import time
import logging
from flask import request, g

logger = logging.getLogger(__name__)


class RequestLoggerMiddleware:
    """Middleware to log all API requests to the database."""

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize middleware with Flask app."""
        app.before_request(self._before_request)
        app.after_request(self._after_request)

    def _before_request(self):
        """Record request start time."""
        g.request_start_time = time.time()

    def _after_request(self, response):
        """Log request to database after response."""
        # Skip logging for static files and health checks
        if request.path.startswith('/static') or request.path == '/api/health':
            return response

        try:
            # Calculate latency
            start_time = getattr(g, 'request_start_time', None)
            if start_time:
                latency_ms = int((time.time() - start_time) * 1000)
            else:
                latency_ms = 0

            # Get user ID if authenticated
            user_id = getattr(g, 'current_user_id', None)

            # Get client IP (handle proxies)
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ip_address and ',' in ip_address:
                ip_address = ip_address.split(',')[0].strip()

            # Truncate endpoint to fit column
            endpoint = request.path[:100] if request.path else ''

            # Import here to avoid circular imports
            from app import db
            from app.models import RequestLog

            # Create log entry
            log_entry = RequestLog(
                endpoint=endpoint,
                method=request.method,
                status=response.status_code,
                latency_ms=latency_ms,
                user_id=user_id,
                ip_address=ip_address[:45] if ip_address else None
            )

            db.session.add(log_entry)
            db.session.commit()

        except Exception as e:
            # Don't fail the request if logging fails
            logger.error(f"Failed to log request: {e}")
            try:
                from app import db
                db.session.rollback()
            except Exception:
                pass

        return response


# Singleton instance
request_logger = RequestLoggerMiddleware()
