from flask import Blueprint, request, g
from app.services import auth_service
from app.utils.responses import success_response, error_response
from app.utils.validators import validate_email, validate_password
from app.utils.decorators import jwt_required
from app.utils.errors import APIError
from app import limiter

auth_bp = Blueprint('auth', __name__)

# DEPRECATED: Email/password authentication is disabled
# Use OAuth endpoints instead (/api/auth/oauth/tiktok/url)

# @auth_bp.route('/register', methods=['POST'])
# @limiter.limit("5 per minute")
# def register():
#     data = request.get_json() or {}
#     try:
#         email = validate_email(data.get('email'))
#         password = validate_password(data.get('password'))
#         language = data.get('language', 'en')
#
#         user, tokens = auth_service.register(email, password, language)
#         return success_response({
#             'user': user.to_dict(),
#             'token': tokens['access_token'],
#             'refresh_token': tokens['refresh_token']
#         }, status_code=201)
#     except APIError as e:
#         return error_response(e.code, e.message, e.details, e.status_code)

# @auth_bp.route('/login', methods=['POST'])
# @limiter.limit("10 per minute")
# def login():
#     data = request.get_json() or {}
#     try:
#         email = validate_email(data.get('email'))
#         password = data.get('password')
#         if not password:
#             return error_response('validation_error', 'Password required')
#
#         user, tokens = auth_service.login(email, password)
#         return success_response({
#             'user': user.to_dict(),
#             'token': tokens['access_token'],
#             'refresh_token': tokens['refresh_token']
#         })
#     except APIError as e:
#         return error_response(e.code, e.message, e.details, e.status_code)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    auth_service.logout(g.current_user_id)
    return '', 204
