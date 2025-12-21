"""
OAuth authentication routes - TikTok and future providers.

Endpoints:
- POST /api/auth/oauth/tiktok/callback - Exchange code for tokens (PKCE from frontend)
"""

import secrets
import requests
from flask import Blueprint, request

from app import db
from app.models.user import User
from app.services import auth_service
from app.utils.responses import success_response, error_response
from config import OAuthConfig

oauth_bp = Blueprint('oauth', __name__)


@oauth_bp.route('/tiktok/callback', methods=['POST'])
def tiktok_callback():
    """
    Handle TikTok OAuth callback.

    POST body:
        code: Authorization code from TikTok
        code_verifier: PKCE code verifier from frontend

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
    import logging
    logger = logging.getLogger(__name__)

    # Get code and code_verifier from POST body (frontend handles state validation)
    data = request.get_json() or {}
    code = data.get('code')
    code_verifier = data.get('code_verifier')

    logger.warning(f"OAuth callback - code present: {bool(code)}, verifier length: {len(code_verifier) if code_verifier else 0}")
    logger.warning(f"FULL code_verifier received: {code_verifier}")

    # Compute what the code_challenge SHOULD be for this verifier
    import hashlib
    import base64
    if code_verifier:
        sha256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        expected_challenge = base64.urlsafe_b64encode(sha256_hash).rstrip(b'=').decode('utf-8')
        logger.warning(f"Expected code_challenge for this verifier: {expected_challenge}")

    if not code:
        return error_response('invalid_request', 'Missing authorization code', status_code=400)

    if not code_verifier:
        return error_response('invalid_request', 'Missing code verifier', status_code=400)

    # 2. Exchange code for access token (Desktop app uses PKCE - code_verifier instead of client_secret)
    try:
        logger.warning(f"Exchanging code for token at {OAuthConfig.TIKTOK_TOKEN_URL}")
        logger.warning(f"Client key: {OAuthConfig.TIKTOK_CLIENT_KEY}")
        logger.warning(f"Redirect URI: {OAuthConfig.TIKTOK_REDIRECT_URI}")
        logger.warning(f"Code verifier to send: {code_verifier[:10]}... (length: {len(code_verifier)})")

        # Send both client_secret AND code_verifier (TikTok may need both)
        token_data_payload = {
            'client_key': OAuthConfig.TIKTOK_CLIENT_KEY,
            'client_secret': OAuthConfig.TIKTOK_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': OAuthConfig.TIKTOK_REDIRECT_URI,
            'code_verifier': code_verifier,
        }
        logger.warning(f"Token request payload keys: {list(token_data_payload.keys())}")

        token_response = requests.post(
            OAuthConfig.TIKTOK_TOKEN_URL,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=token_data_payload,
            timeout=10
        )
        logger.warning(f"TikTok token response status: {token_response.status_code}")
        logger.warning(f"TikTok token response body: {token_response.text[:500]}")
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
