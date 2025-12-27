# FYPGlow Architecture v6 (Post-MVP)
## Date: 2025-12-27
## Status: Production Ready

## Tech Stack
- Frontend: React 18 + TypeScript + Tailwind + Zustand
- Backend: Flask 3.0 + SQLAlchemy 2.0 + PostgreSQL 16
- Cache: Redis 7
- Auth: TikTok OAuth 2.0 + PKCE

## Frontend Structure
```
src/
├── api/           # API calls (auth, plans, preferences, categories)
├── components/    # UI components
│   ├── common/    # ErrorBoundary, Input, Button
│   ├── plan/      # ClearStep, WatchStep, ReinforceStep
│   ├── dashboard/ # CategoryPicker, ActionCard
│   └── admin/     # MetricsCard, AdminCharts
├── hooks/         # Custom React hooks
├── pages/         # Route pages (auth, dashboard, onboarding, admin)
├── store/         # Zustand state (authStore, planStoreV2)
├── types/         # TypeScript type definitions
└── lib/           # Utilities (logger, axios, pkce)
```

## Backend Structure
```
app/
├── routes/        # Thin controllers (no business logic!)
│   ├── auth.py
│   ├── oauth.py
│   ├── plan_v2.py
│   └── admin_metrics.py
├── services/      # Business logic layer
│   ├── auth_service.py
│   ├── plan_service_v2.py
│   ├── metrics_service.py
│   └── favorites_service.py
├── models/        # SQLAlchemy ORM models
├── middleware/    # Request logging, error handling
├── tasks/         # Background tasks (health checks, alerts)
└── utils/         # Helpers (responses, decorators, errors)
```

## API Endpoints

### Auth
- `POST /api/auth/register` - Email registration
- `POST /api/auth/login` - Email login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/tiktok` - Get TikTok OAuth URL
- `POST /api/auth/tiktok/callback` - TikTok OAuth callback

### Plan V2
- `POST /api/v2/plan/generate` - Generate new plan
- `GET /api/v2/toxic-creators` - Get toxic creators for Clear step
- `POST /api/v2/toxic-creators/block` - Block a creator
- `GET /api/v2/curated-videos` - Get videos for Watch step
- `GET /api/v2/favorites` - Get user favorites
- `POST /api/v2/favorites` - Add to favorites
- `GET /api/v2/favorites/random` - Random favorite for Reinforce

### Admin
- `GET /api/admin/metrics/overview` - User stats (DAU, new, total)
- `GET /api/admin/metrics/challenge` - Challenge funnel (D0->D7)
- `GET /api/admin/metrics/plans` - Step completion rates
- `GET /api/admin/metrics/system` - API latency, errors, AI cost

## Security (OWASP 10/10)
- Rate limiting on all endpoints (100/min read, 20/min write)
- JWT auth with 15min access token expiry
- Refresh token rotation with max 5 tokens per user
- CORS whitelist (fypglow.com only in production)
- Security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)
- fail2ban protection on server
- bcrypt password hashing (12 rounds)
- No secrets in code (all via .env)

## Monitoring & Observability
- Request logging to PostgreSQL (latency, status, endpoint)
- Telegram alerts for critical errors
- Daily automated backups (PostgreSQL + Redis)
- Health check endpoint with database/redis status
- Admin dashboard with real-time metrics

## Database Schema (Key Tables)
- `users` - User accounts (email/OAuth)
- `plans` - Daily challenge plans
- `user_categories` - User's selected categories
- `favorites` - Saved videos
- `analytics_events` - User behavior tracking
- `request_logs` - API request logging
- `ai_request_logs` - AI API cost tracking
- `refresh_tokens` - JWT refresh tokens

## Deployment
- VPS: Ubuntu 22.04 on Hetzner
- Docker Compose for all services
- Nginx reverse proxy with SSL (Let's Encrypt)
- UFW firewall (only 80, 443, 22)
- Automatic daily backups to local storage
