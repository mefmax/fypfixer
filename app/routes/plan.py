from flask import Blueprint, request, jsonify, current_app
from app.models import Category, Plan, PlanStep, StepItem
from datetime import date

plan_bp = Blueprint('plan', __name__, url_prefix='/api')

@plan_bp.route('/plan', methods=['GET'])
def get_plan():
    """
    Получить план на день.
    Query params:
    - category: код категории (personal_growth, entertainment, etc.)
    - lang: язык (en, ru, es)
    """
    category_code = request.args.get('category', 'personal_growth')
    language = request.args.get('lang', 'en')
    
    # Найти категорию
    category = Category.query.filter_by(code=category_code).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # Найти или создать план на сегодня
    today = date.today()
    plan = Plan.query.filter_by(
        category_id=category.id,
        plan_date=today,
        language=language,
        is_template=False
    ).first()
    
    # Если плана нет, используем template план (демо)
    if not plan:
        plan = Plan.query.filter_by(
            category_id=category.id,
            is_template=True,
            language=language
        ).first()
    
    # Если и template нет, вернуть демо-план (hardcode только для отладки)
    if not plan:
        # Вернуть простой демо-ответ
        return jsonify({
            'plan_date': str(today),
            'language': language,
            'category_code': category_code,
            'category_name': getattr(category, f'name_{language}', category.name_en),
            'steps': [
                {
                    'step_id': 0,
                    'order': 1,
                    'action_type': 'watch',
                    'text': f'No plan yet for {category_code}',
                    'items': []
                }
            ]
        })
    
    # Получить шаги плана
    steps = PlanStep.query.filter_by(plan_id=plan.id).order_by(PlanStep.step_order).all()
    
    # Построить ответ
    steps_data = []
    for step in steps:
        items = StepItem.query.filter_by(plan_step_id=step.id).all()
        items_data = [
            {
                'step_item_id': item.id,
                'video_id': item.video_id,
                'creator': item.creator_username,
                'title': item.title,
                'thumbnail_url': item.thumbnail_url,
                'video_url': item.video_url,
                'reason': item.reason_text
            }
            for item in items
        ]
        
        steps_data.append({
            'step_id': step.id,
            'order': step.step_order,
            'action_type': step.action_type,
            'text': getattr(step, f'text_{language}', step.text_en),
            'items': items_data
        })
    
    return jsonify({
        'plan_date': str(today),
        'language': language,
        'category_code': category_code,
        'category_name': getattr(category, f'name_{language}', category.name_en),
        'steps': steps_data
    })
