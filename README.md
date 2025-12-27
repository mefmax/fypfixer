# FYPGlow - TikTok Detox Challenge

7-day challenge to reset your TikTok For You Page by training the algorithm with positive signals.

## Features
- TikTok OAuth login
- Personalized daily detox plans (Clear/Watch/Reinforce)
- Block toxic creators, watch curated content
- Track progress with streaks and analytics
- Admin dashboard for metrics

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Git

### Local Development
```bash
# Clone repository
git clone https://github.com/mefmax/fypfixer.git
cd fypfixer

# Start backend services
docker-compose up -d

# Start frontend (in another terminal)
cd Frontend
npm install
npm run dev
```
Open http://localhost:5173

### Production Build
```bash
cd Frontend
npm run build
```

## Documentation
- [Architecture v6](FYPGLOW_ARCHITECTURE_v6.md) - System architecture, API endpoints, security
- [Developer Handbook](DEV_HANDBOOK.md) - Code standards, git workflow, debugging
- [Deployment Guide](DEPLOYMENT.md) - Production deployment instructions
- [Lessons Learned](LESSONS_LEARNED.md) - Project retrospective

### Legacy Docs
- [Architecture v4.2](docs/FYPGLOW_ARCHITECTURE_v4.2.md) - Previous architecture version
- [TikTok OAuth PKCE](docs/TIKTOK_OAUTH_PKCE_LESSONS_LEARNED.md) - OAuth implementation notes

## Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | React 18, TypeScript, Tailwind CSS, Zustand |
| Backend | Flask 3.0, SQLAlchemy 2.0, PostgreSQL 16 |
| Cache | Redis 7 |
| Auth | TikTok OAuth 2.0 + PKCE, JWT |
| Deploy | Docker, Nginx, Ubuntu 22.04 |

## Project Status
- MVP: Complete and deployed
- Version: v2.0 (Post-MVP)
- See [LESSONS_LEARNED.md](LESSONS_LEARNED.md) for technical debt items

## License
Proprietary - All rights reserved
