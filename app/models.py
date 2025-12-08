from app import db
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.String(64), unique=True, nullable=False)
    language = db.Column(db.String(5), nullable=False, default='en')
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    name_en = db.Column(db.Text, nullable=False)
    name_ru = db.Column(db.Text)
    name_es = db.Column(db.Text)
    is_premium = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

class Plan(db.Model):
    __tablename__ = 'plans'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    plan_date = db.Column(db.Date, nullable=False)
    language = db.Column(db.String(5), nullable=False, default='en')
    is_template = db.Column(db.Boolean, nullable=False, default=False)
    title = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    steps = db.relationship('PlanStep', backref='plan', cascade='all, delete-orphan')

class PlanStep(db.Model):
    __tablename__ = 'plan_steps'
    
    id = db.Column(db.BigInteger, primary_key=True)
    plan_id = db.Column(db.BigInteger, db.ForeignKey('plans.id', ondelete='CASCADE'), nullable=False)
    step_order = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(32))
    text_en = db.Column(db.Text, nullable=False)
    text_ru = db.Column(db.Text)
    text_es = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    
    items = db.relationship('StepItem', backref='step', cascade='all, delete-orphan')

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
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
