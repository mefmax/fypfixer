from app import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.UniqueConstraint('oauth_provider', 'oauth_id', name='uq_oauth_provider_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.String(64), unique=True, nullable=False)

    # Email/password (deprecated, for legacy users)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)

    # OAuth fields
    oauth_provider = db.Column(db.String(20), nullable=True)  # 'tiktok', 'google', 'apple', 'facebook'
    oauth_id = db.Column(db.String(255), nullable=True)  # Unique ID from provider
    display_name = db.Column(db.String(255), nullable=True)  # Display name from provider
    avatar_url = db.Column(db.String(512), nullable=True)  # Avatar URL from provider

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
            'display_name': self.display_name,
            'avatar_url': self.avatar_url,
            'oauth_provider': self.oauth_provider,
            'language': self.language,
            'is_premium': self.is_premium,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
