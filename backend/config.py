import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY and os.environ.get('FLASK_ENV') == 'production':
        raise RuntimeError("SECRET_KEY environment variable is required in production!")
    SECRET_KEY = SECRET_KEY or 'dev-secret-key-NOT-FOR-PRODUCTION'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY and os.environ.get('FLASK_ENV') == 'production':
        raise RuntimeError("JWT_SECRET_KEY environment variable is required in production!")
    JWT_SECRET_KEY = JWT_SECRET_KEY or 'dev-jwt-secret-NOT-FOR-PRODUCTION'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
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
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://fypfixer:fypfixer@localhost:5432/fypfixer_test'
    )

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
