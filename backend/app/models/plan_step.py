from app import db
from sqlalchemy.sql import func

class PlanStep(db.Model):
    __tablename__ = 'plan_steps'

    id = db.Column(db.BigInteger, primary_key=True)
    plan_id = db.Column(db.BigInteger, db.ForeignKey('plans.id', ondelete='CASCADE'), nullable=False)
    step_order = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(32), default='watch')
    text_en = db.Column(db.Text, nullable=False)
    text_ru = db.Column(db.Text)
    text_es = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    items = db.relationship('StepItem', backref='step', lazy='dynamic', cascade='all, delete-orphan')

    def get_text(self, lang='en'):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en

    def to_dict(self, lang='en', include_items=False):
        data = {
            'id': self.id,
            'step_order': self.step_order,
            'action_type': self.action_type,
            'text': self.get_text(lang),
            'duration_minutes': self.duration_minutes
        }
        if include_items:
            data['items'] = [i.to_dict() for i in self.items]
        return data
