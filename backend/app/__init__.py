from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

def get_limiter_storage():
    redis_url = os.environ.get('REDIS_URL')
    if redis_url:
        return f"redis://{redis_url.split('://')[-1]}"
    return "memory://"

def create_app(config_name='default'):
    from config import config

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configure rate limiting
    app.config['RATELIMIT_STORAGE_URI'] = get_limiter_storage()
    app.config['RATELIMIT_DEFAULT'] = "200 per day;50 per hour"

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # Exempt OPTIONS requests from rate limiting (CORS preflight)
    @limiter.request_filter
    def exempt_options():
        return request.method == 'OPTIONS'

    cors_origins = app.config.get('CORS_ORIGINS')
    if not cors_origins:
        if app.config.get('DEBUG'):
            cors_origins = ['http://localhost:5173', 'http://localhost:3000']
        else:
            cors_origins = ['https://fypglow.com', 'https://www.fypglow.com', 'https://fypglow.app']
    elif isinstance(cors_origins, str):
        cors_origins = [o.strip() for o in cors_origins.split(',')]
    CORS(app,
         origins=cors_origins,
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         expose_headers=['Content-Type', 'Authorization'],
         max_age=3600)  # Cache preflight for 1 hour

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
