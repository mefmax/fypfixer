from app import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    name_en = db.Column(db.Text, nullable=False)
    name_ru = db.Column(db.Text)
    name_es = db.Column(db.Text)
    is_premium = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)


class PlanStep(db.Model):
    __tablename__ = 'plan_steps'

    id = db.Column(db.BigInteger, primary_key=True)
    plan_id = db.Column(db.BigInteger, db.ForeignKey('plans.id', ondelete='CASCADE'), nullable=False)
    step_order = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(32))
    text_en = db.Column(db.Text, nullable=False)
    text_ru = db.Column(db.Text)
    text_es = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    items = db.relationship('StepItem', backref='plan_step', order_by='StepItem.id')


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
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
