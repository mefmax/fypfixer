from app import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    language = db.Column(db.String(5), nullable=False, default='en')
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_premium = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    plans = db.relationship('Plan', backref='user', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'email': self.email,
            'language': self.language,
            'is_premium': self.is_premium,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
