"""User recommendation log model for AI pipeline tracking."""

from app import db
from sqlalchemy import JSON
from sqlalchemy.sql import func


class UserRecommendation(db.Model):
    """
    Logs each AI pipeline execution.
    Used for analytics, debugging, and improving recommendations.

    One entry per user per day (unique constraint).
    """
    __tablename__ = 'user_recommendations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    plan_date = db.Column(db.Date, nullable=False)
    category_code = db.Column(db.String(50), nullable=False)

    # AI Pipeline Data (stored for debugging/analytics)
    search_criteria = db.Column(JSON, nullable=False)  # Stage 1 output
    scraper_results = db.Column(JSON, nullable=True)   # Raw scraper data
    selected_actions = db.Column(JSON, nullable=False)  # Stage 2 output

    # Pipeline Metadata
    ai_provider = db.Column(db.String(50), nullable=False)  # "ollama", "openai", "anthropic"
    generation_time_ms = db.Column(db.Integer, nullable=True)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(20), default='ai')  # ai, seed, cache

    # Quality Metrics
    avg_quality_score = db.Column(db.Numeric(5, 4), nullable=True)
    diversity_score = db.Column(db.Numeric(5, 4), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = db.relationship('User', backref='recommendations')

    # Unique constraint: one per user per day + index
    __table_args__ = (
        db.UniqueConstraint('user_id', 'plan_date', name='uix_user_date'),
        db.Index('idx_recommendations_user_date', 'user_id', 'plan_date'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'planDate': str(self.plan_date),
            'categoryCode': self.category_code,
            'pipeline': {
                'provider': self.ai_provider,
                'generationTimeMs': self.generation_time_ms,
                'success': self.success,
                'source': self.source,
            },
            'quality': {
                'avgScore': float(self.avg_quality_score) if self.avg_quality_score else None,
                'diversityScore': float(self.diversity_score) if self.diversity_score else None,
            },
            'createdAt': self.created_at.isoformat() if self.created_at else None,
        }
