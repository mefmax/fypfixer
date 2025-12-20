# FYPFixer Backend

Flask REST API for FYPFixer - TikTok FYP optimization tool.

## Structure

```
backend/
├── app/
│   ├── models/         # SQLAlchemy models
│   ├── routes/         # Flask blueprints
│   ├── services/       # Business logic
│   ├── utils/          # Helpers, decorators, validators
│   └── middleware/     # Custom middleware
├── migrations/         # Alembic migrations
├── tests/             # Unit tests
├── config.py          # Configuration classes
├── main.py           # Application entry point
├── requirements.txt   # Python dependencies
└── Dockerfile        # Docker image definition

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Run migrations:
```bash
flask db upgrade
```

5. Start development server:
```bash
python main.py
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user (requires JWT)

### Plans
- `GET /api/plans` - Get all plans (with filters)
- `GET /api/plan` - Get daily plan (legacy)
- `POST /api/plans/:id/steps/:id/complete` - Mark step as completed (requires JWT)

### Categories
- `GET /api/categories` - Get all categories

### User
- `GET /api/user` - Get user profile (requires JWT)

### Health
- `GET /api/health` - Health check

## Environment Variables

See `.env.example` for required environment variables.

## Docker

Build image:
```bash
docker build -t fypfixer-backend .
```

Run container:
```bash
docker run -p 8000:8000 --env-file .env fypfixer-backend
```

## Testing

```bash
pytest
```
