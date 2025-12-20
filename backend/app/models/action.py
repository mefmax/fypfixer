from app import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import NUMERIC


class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.BigInteger, primary_key=True)
    plan_id = db.Column(db.BigInteger, db.ForeignKey('plans.id', ondelete='CASCADE'), index=True)

    action_type = db.Column(db.String(32), nullable=False)  # follow, like, save, not_interested
    action_category = db.Column(db.String(16), nullable=False)  # positive, negative

    target_type = db.Column(db.String(32), nullable=False)  # creator, video, content_type
    target_name = db.Column(db.String(256), nullable=False)
    target_description = db.Column(db.Text)
    target_thumbnail_url = db.Column(db.Text)
    target_tiktok_url = db.Column(db.Text)

    # AI pipeline fields
    source = db.Column(db.String(50))  # 'ai_generated', 'manual', 'template'
    reason = db.Column(db.Text)  # AI explanation for recommendation
    quality_score = db.Column(NUMERIC(5, 4))  # 0.0000 to 1.0000

    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    plan = db.relationship('Plan', backref='actions')

    def to_dict(self):
        return {
            'id': f'action-{self.id}',
            'type': self.action_type,
            'category': self.action_category,
            'target': {
                'type': self.target_type,
                'name': self.target_name,
                'description': self.target_description,
                'thumbnailUrl': self.target_thumbnail_url,
                'tiktokUrl': self.target_tiktok_url,
            },
            'completed': False  # TODO: проверять в user_progress
        }
