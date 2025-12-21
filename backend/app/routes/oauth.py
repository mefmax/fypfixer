"""
OAuth authentication routes - TikTok and future providers.

Endpoints:
- GET /api/auth/oauth/tiktok/url - Get TikTok authorization URL
- GET /api/auth/oauth/tiktok/callback - Handle TikTok OAuth callback
"""

import secrets
import requests
from flask import Blueprint, request, session, g
from urllib.parse import urlencode

from app import db
from app.models.user import User
from app.services import auth_service
from app.utils.responses import success_response, error_response
from config import OAuthConfig

oauth_bp = Blueprint('oauth', __name__)


@oauth_bp.route('/tiktok/url', methods=['GET'])
def get_tiktok_auth_url():
    """
    Generate TikTok OAuth authorization URL.

    Returns:
        {
            "success": true,
            "data": {
                "url": "https://www.tiktok.com/v2/auth/authorize/?...."
            }
        }
    """
    # Validate configuration
    if not OAuthConfig.TIKTOK_CLIENT_KEY or not OAuthConfig.TIKTOK_AUTH_URL:
        return error_response(
            'oauth_misconfigured',
            'TikTok OAuth is not properly configured',
            status_code=500
        )

    # Generate CSRF token
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state

    # Build authorization URL from config
    params = {
        'client_key': OAuthConfig.TIKTOK_CLIENT_KEY,
        'scope': OAuthConfig.TIKTOK_SCOPES,
        'response_type': 'code',
        'redirect_uri': OAuthConfig.TIKTOK_REDIRECT_URI,
        'state': state,
    }

    auth_url = f"{OAuthConfig.TIKTOK_AUTH_URL}?{urlencode(params)}"

    return success_response({'url': auth_url})


@oauth_bp.route('/tiktok/callback', methods=['GET'])
def tiktok_callback():
    """
    Handle TikTok OAuth callback.

    Query params:
        code: Authorization code from TikTok
        state: CSRF token to verify

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
    # 1. Validate state (CSRF protection)
    code = request.args.get('code')
    state = request.args.get('state')

    if not code or not state:
        return error_response('invalid_request', 'Missing code or state parameter', status_code=400)

    stored_state = session.pop('oauth_state', None)
    if not stored_state or stored_state != state:
        return error_response('invalid_state', 'Invalid or expired state token', status_code=400)

    # 2. Exchange code for access token
    try:
        token_response = requests.post(
            OAuthConfig.TIKTOK_TOKEN_URL,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'client_key': OAuthConfig.TIKTOK_CLIENT_KEY,
                'client_secret': OAuthConfig.TIKTOK_CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': OAuthConfig.TIKTOK_REDIRECT_URI,
            },
            timeout=10
        )
        token_response.raise_for_status()
        token_data = token_response.json()
    except requests.RequestException as e:
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
