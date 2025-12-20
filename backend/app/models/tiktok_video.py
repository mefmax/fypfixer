"""TikTok video cache model for scraped content."""

from datetime import datetime
from app import db
from sqlalchemy import JSON
from sqlalchemy.sql import func


class TiktokVideo(db.Model):
    """
    Cached TikTok video metadata from Apify scraper.
    TTL: 24 hours (content freshness requirement).

    Used by AI pipeline for selecting best actions.
    """
    __tablename__ = 'tiktok_videos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.String(50), nullable=False, unique=True)
    url = db.Column(db.Text, nullable=False)

    # Creator info
    creator_username = db.Column(db.String(100), nullable=False, index=True)
    creator_display_name = db.Column(db.String(200), nullable=True)
    creator_follower_count = db.Column(db.Integer, nullable=True)
    creator_verified = db.Column(db.Boolean, default=False)

    # Video metadata
    description = db.Column(db.Text, nullable=True)
    hashtags = db.Column(JSON, default=list)
    duration_sec = db.Column(db.Integer, nullable=True)
    upload_date = db.Column(db.DateTime(timezone=True), nullable=True)
    thumbnail_url = db.Column(db.Text, nullable=True)

    # Engagement metrics
    views = db.Column(db.Integer, nullable=True)
    likes = db.Column(db.Integer, nullable=True)
    comments = db.Column(db.Integer, nullable=True)
    shares = db.Column(db.Integer, nullable=True)
    engagement_rate = db.Column(db.Numeric(7, 6), nullable=True)

    # AI Analysis
    topics = db.Column(JSON, default=list)  # ["motivation", "productivity"]
    quality_score = db.Column(db.Numeric(5, 4), nullable=True)  # 0.0 - 1.0
    category_scores = db.Column(JSON, default=dict)  # {"personal_growth": 0.85}

    # Cache management
    scraped_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    cache_expires_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True)

    __table_args__ = (
        db.Index('idx_videos_quality', quality_score.desc()),
    )

    def is_expired(self) -> bool:
        """Check if cached data has expired."""
        if self.cache_expires_at is None:
            return True
        return datetime.utcnow() > self.cache_expires_at.replace(tzinfo=None)

    def calculate_engagement_rate(self):
        """Calculate engagement rate from metrics."""
        if self.views and self.views > 0:
            interactions = (self.likes or 0) + (self.comments or 0) + (self.shares or 0)
            self.engagement_rate = interactions / self.views

    def to_dict(self):
        return {
            'videoId': self.video_id,
            'url': self.url,
            'creator': {
                'username': self.creator_username,
                'displayName': self.creator_display_name,
                'followers': self.creator_follower_count,
                'verified': self.creator_verified,
            },
            'description': self.description,
            'hashtags': self.hashtags or [],
            'thumbnailUrl': self.thumbnail_url,
            'metrics': {
                'views': self.views,
                'likes': self.likes,
                'comments': self.comments,
                'shares': self.shares,
                'engagementRate': float(self.engagement_rate) if self.engagement_rate else None,
            },
            'analysis': {
                'topics': self.topics or [],
                'qualityScore': float(self.quality_score) if self.quality_score else None,
            },
        }

    def to_candidate_dict(self):
        """Format for AI selection prompt."""
        return {
            'video_id': self.video_id,
            'creator_username': self.creator_username,
            'creator_display_name': self.creator_display_name,
            'description': self.description[:100] if self.description else '',
            'views': self.views,
            'likes': self.likes,
            'engagement_rate': float(self.engagement_rate) if self.engagement_rate else 0,
            'verified': self.creator_verified,
            'followers': self.creator_follower_count,
            'upload_date': str(self.upload_date.date()) if self.upload_date else None,
            'thumbnail_url': self.thumbnail_url,
            'tiktok_url': self.url,
        }

    @classmethod
    def get_valid_cache(cls, category: str, limit: int = 50):
        """Get non-expired videos for a category."""
        return cls.query.filter(
            cls.cache_expires_at > datetime.utcnow(),
            cls.category_scores[category].astext.cast(db.Float) > 0.5
        ).order_by(cls.quality_score.desc()).limit(limit).all()
