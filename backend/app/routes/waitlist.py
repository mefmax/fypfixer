from flask import Blueprint, request, g
from app.models import PremiumWaitlist, Category, User
from app import db
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required

waitlist_bp = Blueprint('waitlist', __name__)

@waitlist_bp.route('/waitlist/join', methods=['POST'])
@jwt_required
def join_waitlist():
    """Add user to premium category waitlist"""
    data = request.get_json()
    category_id = data.get('category_id')

    if not category_id:
        return error_response('MISSING_CATEGORY_ID', 'category_id is required', status_code=400)

    # Check category exists and is premium
    category = Category.query.get(category_id)
    if not category:
        return error_response('CATEGORY_NOT_FOUND', 'Category not found', status_code=404)
    if not category.is_premium:
        return error_response('NOT_PREMIUM', 'Category is not premium', status_code=400)

    # Check if already on waitlist
    existing = PremiumWaitlist.query.filter_by(
        user_id=g.current_user_id,
        category_id=category_id
    ).first()

    if existing:
        return success_response({
            'message': 'Already on waitlist',
            'category': category.get_name()
        })

    # Get user email
    user = User.query.get(g.current_user_id)

    # Add to waitlist
    waitlist_entry = PremiumWaitlist(
        user_id=g.current_user_id,
        category_id=category_id,
        email=user.email if user else None
    )
    db.session.add(waitlist_entry)
    db.session.commit()

    # Get position in waitlist
    position = PremiumWaitlist.query.filter_by(category_id=category_id).count()

    return success_response({
        'message': 'Added to waitlist',
        'category': category.get_name(),
        'position': position
    })

@waitlist_bp.route('/waitlist/leave', methods=['POST'])
@jwt_required
def leave_waitlist():
    """Remove user from waitlist"""
    data = request.get_json()
    category_id = data.get('category_id')

    if not category_id:
        return error_response('MISSING_CATEGORY_ID', 'category_id is required', status_code=400)

    # Remove from waitlist
    deleted = PremiumWaitlist.query.filter_by(
        user_id=g.current_user_id,
        category_id=category_id
    ).delete()

    db.session.commit()

    if deleted:
        return success_response({'message': 'Removed from waitlist'})
    else:
        return success_response({'message': 'Not on waitlist'})
