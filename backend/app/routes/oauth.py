"""
OAuth authentication routes - TikTok and future providers.

Endpoints:
- POST /api/auth/oauth/tiktok/callback - Exchange code for tokens (PKCE from frontend)
"""

import logging
import requests
from flask import Blueprint, request

from app import limiter, AUTH_LIMIT
from app.services import auth_service
from app.utils.responses import success_response, error_response
from app.config.constants import ALLOWED_REDIRECT_URIS
from config import OAuthConfig

logger = logging.getLogger(__name__)
oauth_bp = Blueprint('oauth', __name__)


def _exchange_tiktok_code(code: str, code_verifier: str, redirect_uri: str) -> dict:
    """
    Exchange authorization code for TikTok tokens.

    Args:
        code: Authorization code from TikTok
        code_verifier: PKCE code verifier
        redirect_uri: Callback URI

    Returns:
        Dict with access_token, open_id

    Raises:
        requests.RequestException: If token exchange fails
    """
    token_data_payload = {
        'client_key': OAuthConfig.TIKTOK_CLIENT_KEY,
        'client_secret': OAuthConfig.TIKTOK_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier,
    }

    response = requests.post(
        OAuthConfig.TIKTOK_TOKEN_URL,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=token_data_payload,
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def _get_tiktok_user_info(access_token: str) -> dict:
    """
    Get user info from TikTok API.

    Args:
        access_token: TikTok access token

    Returns:
        Dict with display_name, avatar_url

    Raises:
        requests.RequestException: If user info fetch fails
    """
    response = requests.get(
        OAuthConfig.TIKTOK_USERINFO_URL,
        headers={'Authorization': f'Bearer {access_token}'},
        params={'fields': 'open_id,display_name,avatar_url'},
        timeout=10
    )
    response.raise_for_status()
    data = response.json()
    return data.get('data', {}).get('user', {})


@oauth_bp.route('/tiktok/callback', methods=['POST'])
@limiter.limit(AUTH_LIMIT)
def tiktok_callback():
    """
    Handle TikTok OAuth callback.

    POST body:
        code: Authorization code from TikTok
        code_verifier: PKCE code verifier
        redirect_uri: Optional redirect URI

    Returns:
        {
            "success": true,
            "data": {
                "access_token": "jwt_token",
                "refresh_token": "jwt_refresh_token",
                "user": {
                    "id": 1,
                    "display_name": "...",
                    "avatar_url": "...",
                    "oauth_provider": "tiktok",
                    "is_premium": false
                }
            }
        }
    """
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

    # Step 1: Exchange code for TikTok tokens
    try:
        token_data = _exchange_tiktok_code(code, code_verifier, redirect_uri)
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
        logger.error("Invalid token response from TikTok: missing access_token or open_id")
        return error_response(
            'oauth_token_invalid',
            'Invalid token response from TikTok',
            status_code=502
        )

    # Step 2: Get user info from TikTok
    try:
        tiktok_user = _get_tiktok_user_info(access_token)
    except requests.RequestException as e:
        logger.error(f"Failed to fetch user info: {str(e)}")
        return error_response(
            'oauth_userinfo_error',
            f'Failed to fetch user info: {str(e)}',
            status_code=502
        )

    display_name = tiktok_user.get('display_name')
    avatar_url = tiktok_user.get('avatar_url')

    # Step 3: Find or create user (delegated to AuthService)
    user = auth_service.find_or_create_oauth_user(
        provider='tiktok',
        oauth_id=open_id,
        display_name=display_name,
        avatar_url=avatar_url
    )

    # Step 4: Generate JWT tokens (delegated to AuthService)
    tokens = auth_service.generate_tokens(user)

    # Step 5: Return response
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
