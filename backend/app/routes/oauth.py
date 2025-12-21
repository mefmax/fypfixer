"""
OAuth authentication routes - TikTok and future providers.

Endpoints:
- GET /api/auth/oauth/tiktok/url - Get TikTok authorization URL
- GET /api/auth/oauth/tiktok/callback - Handle TikTok OAuth callback
"""

import secrets
import hashlib
import base64
import requests
from flask import Blueprint, request, session, g
from urllib.parse import urlencode

from app import db
from app.models.user import User
from app.services import auth_service
from app.utils.responses import success_response, error_response
from config import OAuthConfig

oauth_bp = Blueprint('oauth', __name__)


def generate_pkce_pair():
    """Generate PKCE code_verifier and code_challenge for OAuth 2.0."""
    # Generate code_verifier (43-128 characters, URL-safe)
    code_verifier = secrets.token_urlsafe(64)

    # Generate code_challenge (SHA256 hash of verifier, base64url encoded)
    code_challenge_digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge_digest).rstrip(b'=').decode('utf-8')

    return code_verifier, code_challenge


@oauth_bp.route('/tiktok/url', methods=['GET'])
def get_tiktok_auth_url():
    """
    Generate TikTok OAuth authorization URL with PKCE.

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

    import logging
    logger = logging.getLogger(__name__)

    # Generate CSRF token
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state

    # Generate PKCE pair
    code_verifier, code_challenge = generate_pkce_pair()
    session['oauth_code_verifier'] = code_verifier

    logger.warning(f"Generated PKCE - verifier hash: {hashlib.sha256(code_verifier.encode()).hexdigest()[:16]}, challenge: {code_challenge[:20]}...")

    # Build authorization URL from config with PKCE
    params = {
        'client_key': OAuthConfig.TIKTOK_CLIENT_KEY,
        'scope': OAuthConfig.TIKTOK_SCOPES,
        'response_type': 'code',
        'redirect_uri': OAuthConfig.TIKTOK_REDIRECT_URI,
        'state': state,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
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

    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"OAuth callback - code present: {bool(code)}, state: {state[:20] if state else None}...")
    logger.warning(f"Session keys: {list(session.keys())}")

    if not code or not state:
        return error_response('invalid_request', 'Missing code or state parameter', status_code=400)

    stored_state = session.pop('oauth_state', None)
    code_verifier = session.pop('oauth_code_verifier', None)

    if code_verifier:
        logger.warning(f"Callback PKCE - verifier hash: {hashlib.sha256(code_verifier.encode()).hexdigest()[:16]}")
    logger.warning(f"Stored state: {stored_state[:20] if stored_state else None}..., code_verifier present: {bool(code_verifier)}")

    if not stored_state or stored_state != state:
        logger.error(f"State mismatch! Received: {state}, Stored: {stored_state}")
        return error_response('invalid_state', 'Invalid or expired state token', status_code=400)

    if not code_verifier:
        logger.error("Code verifier missing from session")
        return error_response('invalid_request', 'Missing code verifier - please start OAuth flow again', status_code=400)

    # 2. Exchange code for access token (with PKCE code_verifier)
    try:
        logger.warning(f"Exchanging code for token at {OAuthConfig.TIKTOK_TOKEN_URL}")
        token_response = requests.post(
            OAuthConfig.TIKTOK_TOKEN_URL,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'client_key': OAuthConfig.TIKTOK_CLIENT_KEY,
                'client_secret': OAuthConfig.TIKTOK_CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': OAuthConfig.TIKTOK_REDIRECT_URI,
                'code_verifier': code_verifier,
            },
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
