from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, gettext
import os
from pathlib import Path

db = SQLAlchemy()
babel = Babel()


def create_app():
    # базовая директория проекта: /app
    BASE_DIR = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    # Babel конфиг
    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = str(BASE_DIR / "translations")

    # БД конфиг
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        database_url = database_url.replace("postgresql://", "postgresql+psycopg2://")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///fypfixer.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    babel.init_app(app, locale_selector=lambda: get_locale())

    # контекстный процессор для {{ _(...) }}
    @app.context_processor
    def inject_gettext():
        return dict(_=gettext)

    from app.routes.health import health_bp
    from app.routes.plan import plan_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(plan_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


def get_locale():
    return request.args.get("lang") or request.accept_languages.best_match(
        ["en", "ru", "es"]
    ) or "en"
