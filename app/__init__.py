from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
import os
from dotenv import load_dotenv

# Загрузить .env
load_dotenv()

# Инициализировать расширения (без приложения)
db = SQLAlchemy()
babel = Babel()

def create_app():
    """Создать и сконфигурировать Flask приложение."""
    import os
    app = Flask(__name__, 
               template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
               static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    # Конфиг БД
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://fypfixer:fypfixer@db:5432/fypfixer'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
    
    # Инициализировать расширения с приложением
    db.init_app(app)
    babel.init_app(app)
    
    # Регистрировать blueprints
    from app.routes.plan import plan_bp
    from app.routes.health import health_bp
    
    app.register_blueprint(plan_bp)
    app.register_blueprint(health_bp)
    
    # КРИТИЧНО: Импортировать модели ПЕРЕД create_all()
    from app.models import User, Category, Plan, PlanStep, StepItem
    
    # Маршрут для главной страницы
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    
    # Создать таблицы (если не существуют)
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified")
    
    return app  # ✅ ПРАВИЛЬНО — return в кон
