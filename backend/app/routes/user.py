from flask import Blueprint, request, g
from app.models import User
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET'])
@jwt_required
def get_profile():
    user = User.query.get(g.current_user_id)
    if not user:
        return error_response('not_found', 'User not found', status_code=404)
    return success_response(user.to_dict())
