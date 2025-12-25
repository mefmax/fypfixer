"""User liked videos model for favorites tracking."""

from app import db
from sqlalchemy.sql import func


class UserLikedVideo(db.Model):
    """
    Tracks user's favorite/liked videos for Reinforce step.

    Used by FavoritesService for:
    - Storing favorites
    - Retrieving for rewatch suggestions
    - Random selection for Reinforce step
    """
    __tablename__ = 'user_liked_videos'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    video_id = db.Column(db.String(50), nullable=False)
    liked_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship to User
    user = db.relationship('User', backref=db.backref('liked_videos', lazy='dynamic'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'video_id', name='uq_user_liked_videos_user_video'),
        db.Index('idx_user_liked_videos_liked_at', 'user_id', 'liked_at'),
    )

    def to_dict(self):
        """Convert to dict for API responses."""
        return {
            'id': self.id,
            'video_id': self.video_id,
            'liked_at': self.liked_at.isoformat() if self.liked_at else None,
        }

    def __repr__(self):
        return f'<UserLikedVideo user={self.user_id} video={self.video_id}>'
