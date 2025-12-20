from app import db
from sqlalchemy.sql import func

class PremiumWaitlist(db.Model):
    __tablename__ = 'premium_waitlist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    notified_at = db.Column(db.DateTime(timezone=True))

    # Relationships
    user = db.relationship('User', backref='waitlist_entries', lazy=True)
    category = db.relationship('Category', backref='waitlist_entries', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'category_id', name='uq_user_category_waitlist'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'notified_at': self.notified_at.isoformat() if self.notified_at else None,
        }
