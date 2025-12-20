"""
FYPFixer Backend Entry Point
Run: python main.py
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)


# CLI Commands
@app.cli.command('init-db')
def init_db_command():
    """Create tables and seed data."""
    db.create_all()
    print("✅ Tables created!")

    from seeds.seed_data import run_seeds
    run_seeds(app, db)


@app.cli.command('seed')
def seed_command():
    """Seed the database with demo data."""
    from seeds.seed_data import run_seeds
    run_seeds(app, db)


@app.cli.command('drop-db')
def drop_db_command():
    """Drop all tables (DANGEROUS!)."""
    confirm = input("Are you sure you want to drop all tables? (yes/no): ")
    if confirm.lower() == 'yes':
        db.drop_all()
        print("🗑️  All tables dropped!")
    else:
        print("Cancelled.")


if __name__ == '__main__':
    # Handle init-db argument for Docker
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        with app.app_context():
            db.create_all()
            print("✅ Tables created!")
        from seeds.seed_data import run_seeds
        run_seeds(app, db)
    else:
        # Run development server
        debug = config_name == 'development'
        app.run(host='0.0.0.0', port=8000, debug=debug)
