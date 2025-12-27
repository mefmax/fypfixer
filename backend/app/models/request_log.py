"""
Request Log model for tracking API request performance.
"""

from app import db
from sqlalchemy.sql import func


class RequestLog(db.Model):
    """Logs API requests for performance monitoring."""

    __tablename__ = 'request_logs'

    id = db.Column(db.BigInteger, primary_key=True)
    endpoint = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    latency_ms = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    user = db.relationship('User', backref=db.backref('request_logs', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'endpoint': self.endpoint,
            'method': self.method,
            'status': self.status,
            'latency_ms': self.latency_ms,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
