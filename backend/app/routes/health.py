from flask import Blueprint, jsonify
from datetime import datetime
from app import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    status = {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat(), 'services': {}}

    try:
        db.session.execute(text('SELECT 1'))
        status['services']['database'] = 'connected'
    except Exception as e:
        status['services']['database'] = f'error: {str(e)}'
        status['status'] = 'degraded'

    return jsonify(status), 200 if status['status'] == 'healthy' else 503
