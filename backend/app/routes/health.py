import logging
from flask import Blueprint, jsonify
from datetime import datetime
from app import db, limiter
from sqlalchemy import text

logger = logging.getLogger(__name__)
health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
@limiter.limit("60 per minute")  # SECURITY: Rate limit even health endpoint
def health_check():
    status = {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat(), 'services': {}}

    try:
        db.session.execute(text('SELECT 1'))
        status['services']['database'] = 'connected'
    except Exception as e:
        # SECURITY: Don't expose internal error details
        logger.error(f"Database health check failed: {e}")
        status['services']['database'] = 'error'
        status['status'] = 'degraded'

    return jsonify(status), 200 if status['status'] == 'healthy' else 503
