import logging
import bcrypt
import jwt
from datetime import datetime, timedelta
import uuid
from config import Config
from app.models import User, RefreshToken
from app import db
from app.utils.errors import AuthenticationError, ConflictError

logger = logging.getLogger(__name__)

# Security: Limit refresh tokens per user to prevent accumulation
MAX_REFRESH_TOKENS_PER_USER = 5


class AuthService:
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()

    def verify_password(self, password, password_hash):
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    def generate_tokens(self, user):
        access_payload = {
            'sub': str(user.id),
            'email': user.email,
            'type': 'access',
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        }
        refresh_payload = {
            'sub': str(user.id),
            'type': 'refresh',
            'exp': datetime.utcnow() + Config.JWT_REFRESH_TOKEN_EXPIRES
        }

        access_token = jwt.encode(access_payload, Config.JWT_SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, Config.JWT_SECRET_KEY, algorithm='HS256')

        # Save refresh token
        token_hash = bcrypt.hashpw(refresh_token.encode(), bcrypt.gensalt(4)).decode()
        db.session.add(RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + Config.JWT_REFRESH_TOKEN_EXPIRES
        ))
        db.session.commit()

        # Cleanup old tokens - keep only MAX_REFRESH_TOKENS_PER_USER most recent
        self._cleanup_old_tokens(user.id)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def _cleanup_old_tokens(self, user_id):
        """Remove old refresh tokens, keeping only the most recent ones."""
        tokens = RefreshToken.query.filter_by(
            user_id=user_id,
            is_revoked=False
        ).order_by(RefreshToken.created_at.desc()).all()

        if len(tokens) > MAX_REFRESH_TOKENS_PER_USER:
            tokens_to_delete = tokens[MAX_REFRESH_TOKENS_PER_USER:]
            deleted_count = len(tokens_to_delete)

            for token in tokens_to_delete:
                db.session.delete(token)
            db.session.commit()

            logger.info(f"Cleaned up {deleted_count} old refresh tokens for user {user_id}")

    def revoke_all_tokens(self, user_id):
        """Revoke all refresh tokens for a user. Returns count of deleted tokens."""
        result = RefreshToken.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        logger.info(f"Revoked all {result} refresh tokens for user {user_id}")
        return result

    def register(self, email, password, language='en'):
        if User.query.filter_by(email=email.lower()).first():
            raise ConflictError('Email already registered')

        user = User(
            client_id=str(uuid.uuid4()),
            email=email.lower(),
            password_hash=self.hash_password(password),
            language=language
        )
        db.session.add(user)
        db.session.commit()
        return user, self.generate_tokens(user)

    def login(self, email, password):
        user = User.query.filter_by(email=email.lower(), is_active=True).first()
        if not user or not user.password_hash:
            raise AuthenticationError('Invalid credentials')
        if not self.verify_password(password, user.password_hash):
            raise AuthenticationError('Invalid credentials')
        return user, self.generate_tokens(user)

    def logout(self, user_id):
        RefreshToken.query.filter_by(user_id=user_id).update({'is_revoked': True})
        db.session.commit()

    def find_or_create_oauth_user(
        self,
        provider: str,
        oauth_id: str,
        display_name: str = None,
        avatar_url: str = None
    ) -> User:
        """
        Find existing OAuth user or create new one.

        Args:
            provider: OAuth provider (e.g., 'tiktok')
            oauth_id: Unique ID from provider (e.g., open_id)
            display_name: User's display name from provider
            avatar_url: User's avatar URL from provider

        Returns:
            User instance (existing or newly created)
        """
        user = User.query.filter_by(
            oauth_provider=provider,
            oauth_id=oauth_id
        ).first()

        if user:
            # Update existing user info
            if display_name:
                user.display_name = display_name
            if avatar_url:
                user.avatar_url = avatar_url
            db.session.commit()
            logger.info(f"Updated existing OAuth user: {user.id}")
        else:
            # Create new user
            client_id = str(uuid.uuid4())
            user = User(
                client_id=client_id,
                oauth_provider=provider,
                oauth_id=oauth_id,
                display_name=display_name,
                avatar_url=avatar_url,
                language='en'
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created new OAuth user: {user.id}")

        return user
