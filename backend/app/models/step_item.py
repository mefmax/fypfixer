from app import db
from sqlalchemy.sql import func

class StepItem(db.Model):
    __tablename__ = 'step_items'

    id = db.Column(db.BigInteger, primary_key=True)
    plan_step_id = db.Column(db.BigInteger, db.ForeignKey('plan_steps.id', ondelete='CASCADE'), nullable=False)
    video_id = db.Column(db.String(256))
    creator_username = db.Column(db.String(256))
    title = db.Column(db.Text)
    thumbnail_url = db.Column(db.Text)
    video_url = db.Column(db.Text, nullable=False)
    engagement_score = db.Column(db.Float)
    reason_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'video_id': self.video_id,
            'creator_username': self.creator_username,
            'title': self.title,
            'thumbnail_url': self.thumbnail_url,
            'video_url': self.video_url,
            'engagement_score': self.engagement_score,
            'reason_text': self.reason_text
        }
