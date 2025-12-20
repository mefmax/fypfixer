from flask import Flask, render_template, request, jsonify
from flask_babel import Babel, gettext

app = Flask(__name__)

# Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

def get_locale():
    return request.args.get('lang') or request.accept_languages.best_match(['en', 'ru', 'es']) or 'en'

babel = Babel(app, locale_selector=get_locale)

@app.route('/')
def index():
    return render_template('index.html')

@app.context_processor
def inject_gettext():
    return dict(_=gettext)

# Планы на разных языках
PLANS = {
    'en': {
        'it': {
            'name': 'IT & Tech',
            'steps': [
                {'action': 'Search for "Python tutorials" or "Web development"', 'time': '2 min'},
                {'action': 'Like 5 tech/coding videos that interest you', 'time': '3 min'},
                {'action': 'Follow 2 tech creators or developers', 'time': '2 min'},
                {'action': 'Use "Not interested" on non-tech content', 'time': '2 min'},
                {'action': 'Refresh your For You feed', 'time': '1 min'}
            ]
        },
        'fitness': {
            'name': 'Fitness & Workout',
            'steps': [
                {'action': 'Search for "home workout" or "gym tips"', 'time': '2 min'},
                {'action': 'Like 5 fitness videos that motivate you', 'time': '3 min'},
                {'action': 'Follow 2 fitness trainers or athletes', 'time': '2 min'},
                {'action': 'Remove unrelated content with "Not interested"', 'time': '2 min'},
                {'action': 'Refresh your feed', 'time': '1 min'}
            ]
        },
        'fashion': {
            'name': 'Fashion & Style',
            'steps': [
                {'action': 'Search for "fashion trends" or your style', 'time': '2 min'},
                {'action': 'Like 5 fashion videos you love', 'time': '3 min'},
                {'action': 'Follow 2 fashion creators or stylists', 'time': '2 min'},
                {'action': 'Hide non-fashion content', 'time': '2 min'},
                {'action': 'Refresh your feed', 'time': '1 min'}
            ]
        },
        'default': {
            'name': 'Train Your FYP',
            'steps': [
                {'action': 'Search for your interest', 'time': '2 min'},
                {'action': 'Like 5 videos that interest you', 'time': '3 min'},
                {'action': 'Follow 2 creators in your niche', 'time': '2 min'},
                {'action': 'Use "Not interested" on unwanted content', 'time': '2 min'},
                {'action': 'Refresh your For You feed', 'time': '1 min'}
            ]
        }
    },
    'ru': {
        'it': {
            'name': 'IT и Технологии',
            'steps': [
                {'action': 'Найди "Уроки Python" или "Веб-разработка"', 'time': '2 мин'},
                {'action': 'Лайкни 5 видео про технологии или код', 'time': '3 мин'},
                {'action': 'Подпишись на 2 IT-создателей', 'time': '2 мин'},
                {'action': 'Нажми "Не интересно" на контент не про IT', 'time': '2 мин'},
                {'action': 'Обнови свою ленту', 'time': '1 мин'}
            ]
        },
        'fitness': {
            'name': 'Фитнес и Тренировки',
            'steps': [
                {'action': 'Найди "Тренировки дома" или "Советы для зала"', 'time': '2 мин'},
                {'action': 'Лайкни 5 мотивирующих фитнес-видео', 'time': '3 мин'},
                {'action': 'Подпишись на 2 тренеров или атлетов', 'time': '2 мин'},
                {'action': 'Убери несвязанный контент через "Не интересно"', 'time': '2 мин'},
                {'action': 'Обнови ленту', 'time': '1 мин'}
            ]
        },
        'fashion': {
            'name': 'Мода и Стиль',
            'steps': [
                {'action': 'Найди "Модные тренды" или свой стиль', 'time': '2 мин'},
                {'action': 'Лайкни 5 видео о моде, которые тебе нравятся', 'time': '3 мин'},
                {'action': 'Подпишись на 2 модных блогеров', 'time': '2 мин'},
                {'action': 'Скрой контент не про моду', 'time': '2 мин'},
                {'action': 'Обнови ленту', 'time': '1 мин'}
            ]
        },
        'default': {
            'name': 'Тренируй свой FYP',
            'steps': [
                {'action': 'Найди то, что тебе интересно', 'time': '2 мин'},
                {'action': 'Лайкни 5 интересных видео', 'time': '3 мин'},
                {'action': 'Подпишись на 2 создателей в своей нише', 'time': '2 мин'},
                {'action': 'Нажми "Не интересно" на ненужный контент', 'time': '2 мин'},
                {'action': 'Обнови свою ленту "Для тебя"', 'time': '1 мин'}
            ]
        }
    },
    'es': {
        'it': {
            'name': 'IT y Tecnología',
            'steps': [
                {'action': 'Busca "Tutoriales de Python" o "Desarrollo web"', 'time': '2 min'},
                {'action': 'Dale me gusta a 5 videos de tecnología', 'time': '3 min'},
                {'action': 'Sigue a 2 creadores de tecnología', 'time': '2 min'},
                {'action': 'Usa "No me interesa" en contenido no técnico', 'time': '2 min'},
                {'action': 'Actualiza tu feed Para Ti', 'time': '1 min'}
            ]
        },
        'fitness': {
            'name': 'Fitness y Entrenamiento',
            'steps': [
                {'action': 'Busca "Entrenamiento en casa" o "Consejos de gimnasio"', 'time': '2 min'},
                {'action': 'Dale me gusta a 5 videos motivadores', 'time': '3 min'},
                {'action': 'Sigue a 2 entrenadores o atletas', 'time': '2 min'},
                {'action': 'Elimina contenido no relacionado', 'time': '2 min'},
                {'action': 'Actualiza tu feed', 'time': '1 min'}
            ]
        },
        'fashion': {
            'name': 'Moda y Estilo',
            'steps': [
                {'action': 'Busca "Tendencias de moda" o tu estilo', 'time': '2 min'},
                {'action': 'Dale me gusta a 5 videos de moda', 'time': '3 min'},
                {'action': 'Sigue a 2 creadores de moda', 'time': '2 min'},
                {'action': 'Oculta contenido que no sea de moda', 'time': '2 min'},
                {'action': 'Actualiza tu feed', 'time': '1 min'}
            ]
        },
        'default': {
            'name': 'Entrena tu FYP',
            'steps': [
                {'action': 'Busca lo que te interesa', 'time': '2 min'},
                {'action': 'Dale me gusta a 5 videos interesantes', 'time': '3 min'},
                {'action': 'Sigue a 2 creadores en tu nicho', 'time': '2 min'},
                {'action': 'Usa "No me interesa" en contenido no deseado', 'time': '2 min'},
                {'action': 'Actualiza tu feed Para Ti', 'time': '1 min'}
            ]
        }
    }
}

@app.route('/api/plan')
def api_plan():
    goal = request.args.get('goal', 'default').lower()
    lang = request.args.get('lang', 'en')
    
    # Получаем планы для текущего языка
    lang_plans = PLANS.get(lang, PLANS['en'])
    
    # Определяем категорию
    category = 'default'
    if any(kw in goal for kw in ['python', 'code', 'programming', 'developer', 'it', 'tech', 'ai']):
        category = 'it'
    elif any(kw in goal for kw in ['fitness', 'workout', 'gym', 'sport', 'фитнес', 'спорт', 'тренировка']):
        category = 'fitness'
    elif any(kw in goal for kw in ['fashion', 'style', 'outfit', 'мода', 'стиль']):
        category = 'fashion'
    
    plan = lang_plans.get(category, lang_plans['default'])
    
    steps = []
    for i, step in enumerate(plan['steps'], 1):
        steps.append({
            'num': i,
            'action': step['action'],
            'time': step['time']
        })
    
    return jsonify({
        'goal': plan['name'],
        'total_time': '10 min',
        'steps': steps
    })

@app.route('/api/hashtags')
def api_hashtags():
    return jsonify({'total': 0})

if __name__ == '__main__':
    print("🚀 FYPFixer MVP запущен!")
    print("Доступен по адресу: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
