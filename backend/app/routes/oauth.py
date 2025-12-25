"""
OAuth authentication routes - TikTok and future providers.

Endpoints:
- POST /api/auth/oauth/tiktok/callback - Exchange code for tokens (PKCE from frontend)
"""

import logging
import secrets
import requests
from flask import Blueprint, request

from app import db, limiter, AUTH_LIMIT
from app.models.user import User
from app.services import auth_service
from app.utils.responses import success_response, error_response
from app.config.constants import ALLOWED_REDIRECT_URIS
from config import OAuthConfig

logger = logging.getLogger(__name__)
oauth_bp = Blueprint('oauth', __name__)


@oauth_bp.route('/tiktok/callback', methods=['POST'])
@limiter.limit(AUTH_LIMIT)
def tiktok_callback():
    """
    Handle TikTok OAuth callback.

    POST body:
        code: Authorization code from TikTok

    Returns:
        {
            "success": true,
            "data": {
                "access_token": "jwt_token",
                "user": {
                    "id": 1,
                    "display_name": "...",
                    "avatar_url": "...",
                    "oauth_provider": "tiktok"
                }
            }
        }
    """
    # Get code and code_verifier from POST body (frontend handles state validation via localStorage)
    data = request.get_json() or {}
    code = data.get('code')
    code_verifier = data.get('code_verifier')
    redirect_uri = data.get('redirect_uri') or OAuthConfig.TIKTOK_REDIRECT_URI

    # SEC-001: Validate redirect_uri against whitelist
    if redirect_uri not in ALLOWED_REDIRECT_URIS:
        logger.warning(f"OAuth redirect_uri rejected: {redirect_uri} (IP: {request.remote_addr})")
        return error_response('invalid_redirect_uri', 'Redirect URI not allowed', status_code=400)

    if not code:
        return error_response('invalid_request', 'Missing authorization code', status_code=400)

    # Exchange code for access token
    try:
        token_data_payload = {
            'client_key': OAuthConfig.TIKTOK_CLIENT_KEY,
            'client_secret': OAuthConfig.TIKTOK_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code_verifier': code_verifier,
        }

        token_response = requests.post(
            OAuthConfig.TIKTOK_TOKEN_URL,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=token_data_payload,
            timeout=10
        )

        token_response.raise_for_status()
        token_data = token_response.json()
    except requests.RequestException as e:
        logger.error(f"Token exchange failed: {str(e)}")
        return error_response(
            'oauth_token_error',
            f'Failed to exchange code for token: {str(e)}',
            status_code=502
        )

    access_token = token_data.get('access_token')
    open_id = token_data.get('open_id')

    if not access_token or not open_id:
        logger.error(f"Invalid token response from TikTok: missing access_token or open_id")
        return error_response(
            'oauth_token_invalid',
            'Invalid token response from TikTok',
            status_code=502
        )

    # 3. Get user info from TikTok
    try:
        userinfo_response = requests.get(
            OAuthConfig.TIKTOK_USERINFO_URL,
            headers={'Authorization': f'Bearer {access_token}'},
            params={'fields': 'open_id,display_name,avatar_url'},
            timeout=10
        )
        userinfo_response.raise_for_status()
        userinfo_data = userinfo_response.json()
    except requests.RequestException as e:
        return error_response(
            'oauth_userinfo_error',
            f'Failed to fetch user info: {str(e)}',
            status_code=502
        )

    tiktok_user = userinfo_data.get('data', {}).get('user', {})
    display_name = tiktok_user.get('display_name')
    avatar_url = tiktok_user.get('avatar_url')

    # 4. Find or create user
    user = User.query.filter_by(
        oauth_provider='tiktok',
        oauth_id=open_id
    ).first()

    if user:
        # Update existing user info
        user.display_name = display_name
        user.avatar_url = avatar_url
        db.session.commit()
    else:
        # Create new user
        client_id = secrets.token_urlsafe(32)
        user = User(
            client_id=client_id,
            oauth_provider='tiktok',
            oauth_id=open_id,
            display_name=display_name,
            avatar_url=avatar_url,
            language='en'
        )
        db.session.add(user)
        db.session.commit()

    # 5. Generate JWT tokens
    tokens = auth_service.generate_tokens(user)

    # 6. Return response
    return success_response({
        'access_token': tokens['access_token'],
        'refresh_token': tokens.get('refresh_token'),
        'user': {
            'id': user.id,
            'display_name': user.display_name,
            'avatar_url': user.avatar_url,
            'oauth_provider': user.oauth_provider,
            'is_premium': user.is_premium
        }
    })
