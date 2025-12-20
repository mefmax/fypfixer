"""
Initialize database: create tables and seed data.
Run from backend folder: python init_db.py
"""
import os
import sys

# Add backend to path if running from backend folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db


def init_database():
    """Initialize database with tables and seed data"""
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)

    with app.app_context():
        print("🗄️  Creating database tables...")
        db.create_all()
        print("✅ Tables created!\n")

    # Run seeds (has its own app_context)
    from seeds.seed_data import run_seeds
    run_seeds(app, db)

    print("🎉 Database initialization complete!")


if __name__ == '__main__':
    init_database()
