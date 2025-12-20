# 🔵 FYPFixer — ПЛАН МИГРАЦИИ BACKEND

**Для:** Claude Code (Backend Sonnet) в VS Code  
**Репозиторий:** mefmax/fypfixer  
**Время:** ~4.5 часа

---

## 📋 ОБЗОР ЗАДАЧИ

Создать новую структуру backend в папке `backend/` согласно спецификации из `docs/01_BACKEND_ARCHITECTURE.md`.

**Важно:** 
- НЕ удалять существующую папку `app/` пока не проверите новый backend
- Читать целевую архитектуру в `docs/01_BACKEND_ARCHITECTURE.md`
- Seed данные взять из `db/seeds/`

---

## Фаза B1: Создание структуры (30 мин)

### 1.1 Создать папки

```bash
cd fypfixer
mkdir -p backend/app/models
mkdir -p backend/app/routes  
mkdir -p backend/app/services
mkdir -p backend/app/utils
mkdir -p backend/app/middleware
mkdir -p backend/migrations/versions
mkdir -p backend/tests
```

### 1.2 Создать `backend/config.py`

```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    APIFY_API_KEY = os.environ.get('APIFY_API_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'postgresql://fypfixer:fypfixer@localhost:5432/fypfixer'
    )

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

### 1.3 Создать `backend/.env.example`

```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://fypfixer:fypfixer@db:5432/fypfixer
REDIS_URL=redis://redis:6379/0
JWT_SECRET_KEY=your-jwt-secret
APIFY_API_KEY=your-apify-key
CORS_ORIGINS=http://localhost:5173
```

---

## Фаза B2: Модели (45 мин)

### 2.1 `backend/app/models/__init__.py`

```python
from .user import User
from .category import Category
from .plan import Plan
from .plan_step import PlanStep
from .step_item import StepItem
from .user_progress import UserProgress
from .user_preferences import UserPreferences
from .refresh_token import RefreshToken

__all__ = ['User', 'Category', 'Plan', 'PlanStep', 'StepItem', 
           'UserProgress', 'UserPreferences', 'RefreshToken']
```

### 2.2 `backend/app/models/user.py`

```python
from app import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    language = db.Column(db.String(5), nullable=False, default='en')
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_premium = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    plans = db.relationship('Plan', backref='user', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'email': self.email,
            'language': self.language,
            'is_premium': self.is_premium,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

### 2.3 `backend/app/models/category.py`

```python
from app import db
from sqlalchemy.sql import func

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    name_en = db.Column(db.Text, nullable=False)
    name_ru = db.Column(db.Text)
    name_es = db.Column(db.Text)
    icon = db.Column(db.String(10))
    display_order = db.Column(db.Integer, default=0)
    is_premium = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def get_name(self, lang='en'):
        return getattr(self, f'name_{lang}', self.name_en) or self.name_en
    
    def to_dict(self, lang='en'):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.get_name(lang),
            'icon': self.icon,
            'is_premium': self.is_premium
        }
```

### 2.4 `backend/app/models/plan.py`

```python
from app import db
from sqlalchemy.sql import func

class Plan(db.Model):
    __tablename__ = 'plans'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'))
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    plan_date = db.Column(db.Date, nullable=False)
    language = db.Column(db.String(5), default='en')
    is_template = db.Column(db.Boolean, default=False)
    title = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    steps = db.relationship('PlanStep', backref='plan', lazy='dynamic', cascade='all, delete-orphan')
    category = db.relationship('Category', backref='plans')
    
    def to_dict(self, include_steps=False):
        data = {
            'id': self.id,
            'title': self.title,
            'plan_date': str(self.plan_date),
            'language': self.language,
            'category': self.category.to_dict() if self.category else None,
        }
        if include_steps:
            data['steps'] = [s.to_dict(include_items=True) for s in self.steps.order_by('step_order')]
        return data
```

### 2.5 `backend/app/models/plan_step.py`

```python
from app import db
from sqlalchemy.sql import func

class PlanStep(db.Model):
    __tablename__ = 'plan_steps'
    
    id = db.Column(db.BigInteger, primary_key=True)
    plan_id = db.Column(db.BigInteger, db.ForeignKey('plans.id', ondelete='CASCADE'), nullable=False)
    step_order = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(32), default='watch')
    text_en = db.Column(db.Text, nullable=False)
    text_ru = db.Column(db.Text)
    text_es = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    items = db.relationship('StepItem', backref='step', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_text(self, lang='en'):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en
    
    def to_dict(self, lang='en', include_items=False):
        data = {
            'id': self.id,
            'step_order': self.step_order,
            'action_type': self.action_type,
            'text': self.get_text(lang),
            'duration_minutes': self.duration_minutes
        }
        if include_items:
            data['items'] = [i.to_dict() for i in self.items]
        return data
```

### 2.6 `backend/app/models/step_item.py`

```python
from app import db
from sqlalchemy.sql import func

class StepItem(db.Model):
    __tablename__ = 'step_items'
    
    id = db.Column(db.BigInteger, primary_key=True)
    plan_step_id = db.Column(db.BigInteger, db.ForeignKey('plan_steps.id', ondelete='CASCADE'), nullable=False)
    video_id = db.Column(db.String(256))
    creator_username = db.Column(db.String(256))
    title = db.Column(db.Text)
    thumbnail_url = db.Column(db.Text)
    video_url = db.Column(db.Text, nullable=False)
    engagement_score = db.Column(db.Float)
    reason_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'video_id': self.video_id,
            'creator_username': self.creator_username,
            'title': self.title,
            'thumbnail_url': self.thumbnail_url,
            'video_url': self.video_url,
            'engagement_score': self.engagement_score,
            'reason_text': self.reason_text
        }
```

### 2.7 `backend/app/models/user_progress.py`

```python
from app import db
from sqlalchemy.sql import func

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    step_id = db.Column(db.BigInteger, db.ForeignKey('plan_steps.id', ondelete='CASCADE'), nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (db.UniqueConstraint('user_id', 'step_id'),)
```

### 2.8 `backend/app/models/user_preferences.py`

```python
from app import db
from sqlalchemy.sql import func

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    dark_mode = db.Column(db.Boolean, default=True)
    notifications_enabled = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

### 2.9 `backend/app/models/refresh_token.py`

```python
from app import db
from sqlalchemy.sql import func

class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token_hash = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    is_revoked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
```

---

## Фаза B3: Utils (30 мин)

### 3.1 `backend/app/utils/__init__.py`

```python
from .responses import success_response, error_response
from .errors import APIError, ValidationError, AuthenticationError, NotFoundError
```

### 3.2 `backend/app/utils/responses.py`

```python
from flask import jsonify

def success_response(data=None, message=None, status_code=200):
    response = {'success': True}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response), status_code

def error_response(code, message, details=None, status_code=400):
    response = {
        'success': False,
        'error': {'code': code, 'message': message}
    }
    if details:
        response['error']['details'] = details
    return jsonify(response), status_code
```

### 3.3 `backend/app/utils/errors.py`

```python
class APIError(Exception):
    def __init__(self, code, message, status_code=400, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)

class ValidationError(APIError):
    def __init__(self, message, details=None):
        super().__init__('validation_error', message, 400, details)

class AuthenticationError(APIError):
    def __init__(self, message='Authentication failed'):
        super().__init__('unauthorized', message, 401)

class NotFoundError(APIError):
    def __init__(self, resource='Resource'):
        super().__init__('not_found', f'{resource} not found', 404)

class ConflictError(APIError):
    def __init__(self, message='Resource already exists'):
        super().__init__('conflict', message, 409)
```

### 3.4 `backend/app/utils/validators.py`

```python
import re
from .errors import ValidationError

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_email(email):
    if not email:
        raise ValidationError('Email is required')
    if not EMAIL_REGEX.match(email):
        raise ValidationError('Invalid email format')
    return email.lower().strip()

def validate_password(password):
    if not password or len(password) < 8:
        raise ValidationError('Password must be at least 8 characters')
    return password

def validate_language(lang):
    if lang not in ['en', 'ru', 'es']:
        raise ValidationError('Language must be en, ru, or es')
    return lang
```

### 3.5 `backend/app/utils/decorators.py`

```python
from functools import wraps
from flask import request, g
import jwt
from config import Config
from .errors import AuthenticationError

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationError('Token is missing')
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            g.current_user_id = int(payload['sub'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationError('Invalid token')
        
        return f(*args, **kwargs)
    return decorated
```

---

## Фаза B4: Services (60 мин)

### 4.1 `backend/app/services/__init__.py`

```python
from .auth_service import AuthService
from .plan_service import PlanService

auth_service = AuthService()
plan_service = PlanService()
```

### 4.2 `backend/app/services/auth_service.py`

```python
import bcrypt
import jwt
from datetime import datetime, timedelta
import uuid
from config import Config
from app.models import User, RefreshToken
from app import db
from app.utils.errors import AuthenticationError, ConflictError

class AuthService:
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()
    
    def verify_password(self, password, password_hash):
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    
    def generate_tokens(self, user):
        access_payload = {
            'sub': str(user.id),
            'email': user.email,
            'type': 'access',
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        }
        refresh_payload = {
            'sub': str(user.id),
            'type': 'refresh',
            'exp': datetime.utcnow() + Config.JWT_REFRESH_TOKEN_EXPIRES
        }
        
        access_token = jwt.encode(access_payload, Config.JWT_SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, Config.JWT_SECRET_KEY, algorithm='HS256')
        
        # Save refresh token
        token_hash = bcrypt.hashpw(refresh_token.encode(), bcrypt.gensalt(4)).decode()
        db.session.add(RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + Config.JWT_REFRESH_TOKEN_EXPIRES
        ))
        db.session.commit()
        
        return {'access_token': access_token, 'refresh_token': refresh_token}
    
    def register(self, email, password, language='en'):
        if User.query.filter_by(email=email.lower()).first():
            raise ConflictError('Email already registered')
        
        user = User(
            client_id=str(uuid.uuid4()),
            email=email.lower(),
            password_hash=self.hash_password(password),
            language=language
        )
        db.session.add(user)
        db.session.commit()
        return user, self.generate_tokens(user)
    
    def login(self, email, password):
        user = User.query.filter_by(email=email.lower(), is_active=True).first()
        if not user or not user.password_hash:
            raise AuthenticationError('Invalid credentials')
        if not self.verify_password(password, user.password_hash):
            raise AuthenticationError('Invalid credentials')
        return user, self.generate_tokens(user)
    
    def logout(self, user_id):
        RefreshToken.query.filter_by(user_id=user_id).update({'is_revoked': True})
        db.session.commit()
```

### 4.3 `backend/app/services/plan_service.py`

```python
from datetime import date
from app.models import Plan, Category, UserProgress
from app import db
from app.utils.errors import NotFoundError

class PlanService:
    def get_plans(self, category_code=None, language='en', limit=20, offset=0):
        query = Plan.query.filter_by(is_active=True, is_template=True, language=language)
        
        if category_code:
            cat = Category.query.filter_by(code=category_code, is_active=True).first()
            if cat:
                query = query.filter_by(category_id=cat.id)
        
        total = query.count()
        plans = query.order_by(Plan.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            'plans': [p.to_dict() for p in plans],
            'pagination': {'total': total, 'limit': limit, 'offset': offset}
        }
    
    def get_daily_plan(self, category_code, language='en'):
        category = Category.query.filter_by(code=category_code, is_active=True).first()
        if not category:
            raise NotFoundError('Category')
        
        # Сначала ищем план на сегодня
        plan = Plan.query.filter_by(
            category_id=category.id,
            plan_date=date.today(),
            language=language,
            is_active=True
        ).first()
        
        # Если нет, берём template
        if not plan:
            plan = Plan.query.filter_by(
                category_id=category.id,
                is_template=True,
                language=language,
                is_active=True
            ).first()
        
        if not plan:
            raise NotFoundError('Plan')
        
        return plan.to_dict(include_steps=True)
    
    def complete_step(self, user_id, step_id):
        from datetime import datetime
        progress = UserProgress.query.filter_by(user_id=user_id, step_id=step_id).first()
        if not progress:
            progress = UserProgress(user_id=user_id, step_id=step_id)
            db.session.add(progress)
        progress.completed_at = datetime.utcnow()
        db.session.commit()
        return {'step_id': step_id, 'completed': True}
```

---

## Фаза B5: Routes (45 мин)

### 5.1 `backend/app/routes/__init__.py`

```python
from .auth import auth_bp
from .plans import plans_bp
from .categories import categories_bp
from .health import health_bp
from .user import user_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plans_bp, url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
```

### 5.2 `backend/app/routes/auth.py`

```python
from flask import Blueprint, request, g
from app.services import auth_service
from app.utils.responses import success_response, error_response
from app.utils.validators import validate_email, validate_password
from app.utils.decorators import jwt_required
from app.utils.errors import APIError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    try:
        email = validate_email(data.get('email'))
        password = validate_password(data.get('password'))
        language = data.get('language', 'en')
        
        user, tokens = auth_service.register(email, password, language)
        return success_response({
            'user': user.to_dict(),
            'token': tokens['access_token'],
            'refresh_token': tokens['refresh_token']
        }, status_code=201)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    try:
        email = validate_email(data.get('email'))
        password = data.get('password')
        if not password:
            return error_response('validation_error', 'Password required')
        
        user, tokens = auth_service.login(email, password)
        return success_response({
            'user': user.to_dict(),
            'token': tokens['access_token'],
            'refresh_token': tokens['refresh_token']
        })
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    auth_service.logout(g.current_user_id)
    return '', 204
```

### 5.3 `backend/app/routes/plans.py`

```python
from flask import Blueprint, request, g
from app.services import plan_service
from app.utils.responses import success_response, error_response
from app.utils.decorators import jwt_required
from app.utils.errors import APIError

plans_bp = Blueprint('plans', __name__)

@plans_bp.route('/plans', methods=['GET'])
def get_plans():
    try:
        result = plan_service.get_plans(
            category_code=request.args.get('category'),
            language=request.args.get('language', 'en'),
            limit=min(int(request.args.get('limit', 20)), 100),
            offset=int(request.args.get('offset', 0))
        )
        return success_response(result)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)

@plans_bp.route('/plan', methods=['GET'])
def get_daily_plan():
    """Legacy endpoint for compatibility"""
    try:
        plan = plan_service.get_daily_plan(
            request.args.get('category', 'personal_growth'),
            request.args.get('lang', 'en')
        )
        return success_response(plan)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)

@plans_bp.route('/plans/<int:plan_id>/steps/<int:step_id>/complete', methods=['POST'])
@jwt_required
def complete_step(plan_id, step_id):
    try:
        result = plan_service.complete_step(g.current_user_id, step_id)
        return success_response(result)
    except APIError as e:
        return error_response(e.code, e.message, e.details, e.status_code)
```

### 5.4 `backend/app/routes/categories.py`

```python
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
```

### 5.5 `backend/app/routes/health.py`

```python
from flask import Blueprint, jsonify
from datetime import datetime
from app import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    status = {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat(), 'services': {}}
    
    try:
        db.session.execute(text('SELECT 1'))
        status['services']['database'] = 'connected'
    except Exception as e:
        status['services']['database'] = f'error: {str(e)}'
        status['status'] = 'degraded'
    
    return jsonify(status), 200 if status['status'] == 'healthy' else 503
```

### 5.6 `backend/app/routes/user.py`

```python
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
```

---

## Фаза B6: App Factory (30 мин)

### 6.1 `backend/app/__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    from config import config
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    cors_origins = app.config.get('CORS_ORIGINS', '*')
    if isinstance(cors_origins, str):
        cors_origins = cors_origins.split(',')
    CORS(app, origins=cors_origins)
    
    from app.routes import register_blueprints
    register_blueprints(app)
    
    from app.utils.errors import APIError
    from app.utils.responses import error_response
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return error_response(error.code, error.message, error.details, error.status_code)
    
    @app.errorhandler(404)
    def handle_404(error):
        return error_response('not_found', 'Resource not found', status_code=404)
    
    from app import models  # noqa: F401
    
    return app
```

### 6.2 `backend/main.py`

```python
import os
from app import create_app

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
```

---

## Фаза B7: Requirements (10 мин)

### `backend/requirements.txt`

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-CORS==4.0.0
PyJWT==2.8.0
bcrypt==4.1.2
psycopg2-binary==2.9.9
SQLAlchemy==2.0.23
email-validator==2.1.0
redis==5.0.1
python-dotenv==1.0.0
gunicorn==21.2.0
```

---

## Фаза B8: Dockerfile (15 мин)

### `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 FLASK_ENV=production
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "main:app"]
```

---

## ✅ ЧЕК-ЛИСТ BACKEND

### Фаза B1: Структура
- [ ] Создать `backend/` папку
- [ ] Создать подпапки: `app/models`, `app/routes`, `app/services`, `app/utils`, `app/middleware`
- [ ] Создать `backend/migrations/versions/`
- [ ] Создать `backend/tests/`
- [ ] Создать `backend/config.py`
- [ ] Создать `backend/.env.example`

### Фаза B2: Модели
- [ ] Создать `backend/app/models/__init__.py`
- [ ] Создать `backend/app/models/user.py`
- [ ] Создать `backend/app/models/category.py`
- [ ] Создать `backend/app/models/plan.py`
- [ ] Создать `backend/app/models/plan_step.py`
- [ ] Создать `backend/app/models/step_item.py`
- [ ] Создать `backend/app/models/user_progress.py`
- [ ] Создать `backend/app/models/user_preferences.py`
- [ ] Создать `backend/app/models/refresh_token.py`

### Фаза B3: Utils
- [ ] Создать `backend/app/utils/__init__.py`
- [ ] Создать `backend/app/utils/responses.py`
- [ ] Создать `backend/app/utils/errors.py`
- [ ] Создать `backend/app/utils/validators.py`
- [ ] Создать `backend/app/utils/decorators.py`

### Фаза B4: Services
- [ ] Создать `backend/app/services/__init__.py`
- [ ] Создать `backend/app/services/auth_service.py`
- [ ] Создать `backend/app/services/plan_service.py`

### Фаза B5: Routes
- [ ] Создать `backend/app/routes/__init__.py`
- [ ] Создать `backend/app/routes/auth.py`
- [ ] Создать `backend/app/routes/plans.py`
- [ ] Создать `backend/app/routes/categories.py`
- [ ] Создать `backend/app/routes/health.py`
- [ ] Создать `backend/app/routes/user.py`

### Фаза B6: App Factory
- [ ] Создать `backend/app/__init__.py`
- [ ] Создать `backend/main.py`

### Фаза B7: Dependencies
- [ ] Создать `backend/requirements.txt`

### Фаза B8: Docker
- [ ] Создать `backend/Dockerfile`

### Проверка
- [ ] `cd backend && pip install -r requirements.txt`
- [ ] `python main.py` запускается без ошибок
- [ ] `curl localhost:8000/api/health` возвращает JSON со статусом "healthy"
- [ ] `curl localhost:8000/api/categories` возвращает список категорий

---

## ⚠️ ВАЖНЫЕ ЗАМЕЧАНИЯ

1. **НЕ удалять** существующую папку `app/` пока не проверите новый backend
2. **Сохранить** логику из `app/routes/plan.py` — там рабочий код, который нужно адаптировать
3. **Скопировать** seed данные из `db/seeds/` в новые миграции
4. **JWT_SECRET_KEY** должен быть одинаковым для dev и prod
5. **Тестировать** каждую фазу перед переходом к следующей
6. **Коммитить** после каждой фазы

---

**Общее время: ~4.5 часа**
