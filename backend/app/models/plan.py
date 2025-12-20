from app import db
from sqlalchemy.sql import func

class Plan(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'))
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    plan_date = db.Column(db.Date, nullable=False)
    language = db.Column(db.String(5), default='en')
    is_template = db.Column(db.Boolean, default=False)
    title = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    steps = db.relationship('PlanStep', backref='plan', lazy='dynamic', cascade='all, delete-orphan')
    category = db.relationship('Category', backref='plans')

    def to_dict(self, include_steps=False):
        data = {
            'id': self.id,
            'title': self.title,
            'plan_date': str(self.plan_date),
            'language': self.language,
            'category': self.category.to_dict() if self.category else None,
        }
        if include_steps:
            data['steps'] = [s.to_dict(include_items=True) for s in self.steps.order_by('step_order')]
        return data
