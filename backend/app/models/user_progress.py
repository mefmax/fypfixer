from app import db
from sqlalchemy.sql import func

class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    step_id = db.Column(db.BigInteger, db.ForeignKey('plan_steps.id', ondelete='CASCADE'), nullable=True)
    action_id = db.Column(db.BigInteger, db.ForeignKey('actions.id', ondelete='CASCADE'), nullable=True, index=True)
    completed_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        db.UniqueConstraint('user_id', 'step_id', name='user_progress_user_id_step_id_key'),
        db.UniqueConstraint('user_id', 'action_id', name='unique_user_action'),
        db.Index('idx_user_progress_user_action', 'user_id', 'action_id'),
    )

    def to_dict(self):
        return {
            'userId': self.user_id,
            'actionId': f'action-{self.action_id}' if self.action_id else None,
            'completedAt': self.completed_at.isoformat() if self.completed_at else None
        }
