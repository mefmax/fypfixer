"""
AI Request Log model for tracking AI API usage, cost, and latency.
"""

from app import db
from sqlalchemy.sql import func


class AIRequestLog(db.Model):
    """Logs all AI API requests for monitoring and cost tracking."""

    __tablename__ = 'ai_request_logs'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=True, index=True)
    provider = db.Column(db.String(20), nullable=False)  # 'anthropic', 'static', 'ollama'
    model = db.Column(db.String(50), nullable=False)  # 'claude-3-haiku-20240307', etc.
    prompt_tokens = db.Column(db.Integer, nullable=True)
    completion_tokens = db.Column(db.Integer, nullable=True)
    latency_ms = db.Column(db.Integer, nullable=False)
    cost_usd = db.Column(db.Numeric(10, 6), nullable=True)
    error = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationship
    user = db.relationship('User', backref=db.backref('ai_requests', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'provider': self.provider,
            'model': self.model,
            'prompt_tokens': self.prompt_tokens,
            'completion_tokens': self.completion_tokens,
            'latency_ms': self.latency_ms,
            'cost_usd': float(self.cost_usd) if self.cost_usd else None,
            'error': self.error,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
