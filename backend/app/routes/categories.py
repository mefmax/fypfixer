from flask import Blueprint, request
from app.models import Category
from app.utils.responses import success_response

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    language = request.args.get('language', 'en')
    include_premium = request.args.get('include_premium', 'false').lower() == 'true'

    query = Category.query.filter_by(is_active=True)
    if not include_premium:
        query = query.filter_by(is_premium=False)

    categories = query.order_by(Category.display_order).all()
    return success_response({'categories': [c.to_dict(language) for c in categories]})
