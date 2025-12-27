"""
MetricsDaily model for aggregated dashboard metrics.
"""

from app import db
from sqlalchemy.dialects.postgresql import JSONB


class MetricsDaily(db.Model):
    """Stores aggregated daily metrics for dashboard."""

    __tablename__ = 'metrics_daily'

    id = db.Column(db.Integer, primary_key=True)
    metric_date = db.Column(db.Date, nullable=False)
    metric_name = db.Column(db.String(50), nullable=False)
    metric_value = db.Column(db.Numeric, nullable=False)
    dimensions = db.Column(JSONB, server_default='{}', nullable=False)

    __table_args__ = (
        db.UniqueConstraint('metric_date', 'metric_name', 'dimensions', name='uq_metrics_daily'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'metric_date': self.metric_date.isoformat() if self.metric_date else None,
            'metric_name': self.metric_name,
            'metric_value': float(self.metric_value) if self.metric_value else 0,
            'dimensions': self.dimensions
        }
