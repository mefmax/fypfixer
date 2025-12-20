from functools import wraps
from flask import request, g
import jwt
from config import Config
from .errors import AuthenticationError

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationError('Token is missing')

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'access':
                raise AuthenticationError('Invalid token type')
            g.current_user_id = int(payload['sub'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationError('Invalid token')

        return f(*args, **kwargs)
    return decorated


def jwt_optional(f):
    """
    Optional JWT authentication.
    Sets g.current_user_id if valid token present, otherwise sets to None.
    Does not raise error if token is missing or invalid.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        g.current_user_id = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
                if payload.get('type') == 'access':
                    g.current_user_id = int(payload['sub'])
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                pass  # Silently ignore invalid tokens

        return f(*args, **kwargs)
    return decorated
