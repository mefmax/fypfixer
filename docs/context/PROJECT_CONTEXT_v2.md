FYPFixer – Project Context Snapshot v2 (2025‑12‑07, 13:55 MSK)
1. Purpose & Vision (Updated)
Идея (эволюция):

v1 (исходная): FYPFixer помогает пользователю "приручить" TikTok‑ленту через чек‑листы советов.

v2 (текущая, правильная): FYPFixer — это AI‑помощник, который генерирует конкретные действия с готовыми ссылками на видео. Пользователь только жмёт кнопки; FYPFixer — мозг, пользователь — руки.

Миссия:

Give users simple, AI-powered daily checklists with concrete TikTok video links. No searching, no thinking — just tap and watch. Train your FYP in 10 minutes a day.

Видение:

Стать стандартом "управляемого FYP" на TikTok (позже — Instagram, YouTube Shorts).

Вводить оба варианта: free (2 видео/шаг, 1x/день) и premium ($4.99–$9.99/месяц, 5–7 видео/шаг, обновление 6ч).

Международная аудитория (EN основной, RU/ES локализованы).

2. Target Audience (Finalized)
Primary ЦА: Вариант A

Демография: 18–35 лет, пользователи TikTok.

Психография: хотят "чистый, качественный контент без мусора", но не готовы сами искать и анализировать.

Боль: мусор в FYP, потеря времени на поиск, информационный хаос.

Решение: FYPFixer даёт готовые действия с конкретными видео.

Категории (8 штук, 5 free + 3 premium):

#	Code	EN	RU	ES	is_premium
1	personal_growth	Personal Growth	Личное развитие	Crecimiento Personal	FALSE
2	entertainment	Entertainment	Развлечение	Entretenimiento	FALSE
3	wellness	Wellness & Lifestyle	Здоровье и Образ жизни	Bienestar y Estilo de vida	FALSE
4	creative	Creative & Arts	Творчество и Искусство	Creatividad y Arte	FALSE
5	learning	Learning & Education	Обучение и Образование	Aprendizaje y Educación	FALSE
6	science_tech	Science & Technology	Наука и Технология	Ciencia y Tecnología	TRUE
7	food	Food & Cooking	Еда и Кулинария	Comida y Cocina	TRUE
8	travel	Travel & Adventure	Путешествия и Приключения	Viajes y Aventura	TRUE
3. Product Values & Principles (Updated)
Safety & Compliance: Only public TikTok videos, no account access, transparent scraping.

Simplicity: User taps button → action completed (watch, like, block, follow, search).

Concrete Value: Not advice, but ready-to-use actions with video links.

AI-Powered: LLM + Vector DB generates recommendations, not manual templates.

Engagement Over Friction: Minimize user thinking; maximize button-tapping.

4. Current Product State (MVP v2)
Implemented:

Landing page (Flask + Jinja2, 3 languages EN/RU/ES).

/api/health — health check with DB connectivity.

/api/plan — returns plan with 5 steps, but steps still contain generic advice, not video links yet.

Categories table in PostgreSQL with is_premium flag (8 base categories seeded).

Docker Compose infrastructure (web, Postgres 16, Redis 7).

What's missing for v2:

TikTok video scraper (Firecrawl or similar).

step_items table (video links + metadata for each step).

trending_videos table (cache of public trending videos).

user_actions table (tracking: user watched/liked/blocked video).

AI layer (LLM generates: "pick 5 videos for step X").

Vector DB (Qdrant) for similarity search of videos.

UI component to display videos and track completion.

5. Tech Stack (Target, refined)
Backend

Python 3.11 + Flask + Flask-SQLAlchemy.

REST API (/api/plan, /api/plan/{id}/step, /api/plan/{id}/complete-step, /api/recommendations).

Flask-Babel for i18n (UI + Plan content).

Database

PostgreSQL 16 (users, categories, plans, plan_steps, step_items, trending_videos, user_actions).

Redis 7 (cache trending videos, session tokens, rate limits).

AI & Data

TikTok Scraper: Firecrawl.dev or Apify for public trending videos (parse hashtags, metadata).

LLM: Ollama (local, llama3) or OpenAI (fallback/premium).

Vector DB: Qdrant — embed and store videos; query by semantic similarity.

Data Pipeline: Scheduled job (n8n or cron) to update trending_videos table every 1–6 hours per category.

Frontend

Flask templates + vanilla JS + CSS (mobile-first, dark theme).

PWA approach (offline support, installable).

Progressive disclosure: free users see 2 videos/step, premium see 5–7.

Infrastructure

Docker Compose (local dev): web, Postgres, Redis, Ollama, Qdrant, n8n, Grafana, Prometheus, Nginx.

Production: Hetzner / DigitalOcean + Kubernetes (later).

Observability: Prometheus, Grafana, Loki, Sentry.

Backups: Daily Postgres snapshots to S3-compatible storage.

6. High-Level Architecture (C4 Overview, Updated)
Level 1 — System Context

FYPFixer: generates daily checklists with concrete TikTok video actions.

TikTok User / Premium User / Admin interact with FYPFixer.

TikTok Platform: source of video data (scraping public content).

Payment Provider (Stripe): handles premium billing.

Email Service: sends notifications.

Level 2 — Containers (Key Update)

Web App (Flask): serve HTML, static files, user interface.

API (Flask REST): /api/plan, /api/plan/{id}/step, /api/recommendations.

AI Orchestrator (n8n): workflow for video recommendation generation (input: category + language → output: 5 videos + reasons).

TikTok Scraper (scheduled job): fetch trending videos, enrich metadata, store in trending_videos table.

Data Layer: PostgreSQL, Redis.

Vector DB (Qdrant): semantic search for videos.

Observability: Prometheus, Grafana, Loki, Sentry.

Ingress: Nginx (SSL, rate limiting).

Level 3 — Components (Detailed later)

7. Database Schema (v2, Updated)
Existing tables:

users (client_id, language, created_at, updated_at).

categories (code, name_en/ru/es, is_premium).

plans (user_id, category_id, plan_date, language, is_template, title).

plan_steps (plan_id, step_order, action_type, text_en/ru/es).

NEW tables (for video links):

sql
step_items (
  id BIGSERIAL PRIMARY KEY,
  plan_step_id BIGINT FK plans_steps.id,
  video_id VARCHAR(256), -- TikTok video ID
  creator_username VARCHAR(256),
  title TEXT,
  thumbnail_url TEXT,
  video_url TEXT,
  engagement_score FLOAT, -- likes/views ratio for ranking
  reason_text TEXT, -- "High engagement, matches your niche"
  created_at TIMESTAMPTZ
);

trending_videos (
  id BIGSERIAL PRIMARY KEY,
  category_id BIGINT FK categories.id,
  video_id VARCHAR(256) UNIQUE,
  creator_username VARCHAR(256),
  title TEXT,
  hashtags TEXT[], -- array of tags
  views BIGINT,
  likes BIGINT,
  engagement_score FLOAT,
  thumbnail_url TEXT,
  video_url TEXT,
  scraped_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ -- 24h cache TTL
);

user_actions (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT FK users.id,
  plan_step_id BIGINT FK plan_steps.id,
  step_item_id BIGINT FK step_items.id,
  action_type VARCHAR(32), -- "watched", "liked", "blocked", "followed"
  completed_at TIMESTAMPTZ
);
8. API Contracts (v2)
GET /api/plan?lang=en&category=personal_growth

Response:

json
{
  "plan_id": 123,
  "plan_date": "2025-12-07",
  "language": "en",
  "category_code": "personal_growth",
  "category_name": "Personal Growth",
  "steps": [
    {
      "step_id": 1,
      "order": 1,
      "action_type": "watch",
      "text": "Watch 3 high-quality videos on personal development",
      "items": [
        {
          "step_item_id": 101,
          "video_id": "tiktok_abc123",
          "creator": "@motivationcoach",
          "title": "5 Habits to Change Your Life",
          "thumbnail_url": "https://...",
          "video_url": "https://vm.tiktok.com/...",
          "reason": "High engagement, trending in Personal Growth",
          "is_completed": false
        },
        { ... },
        { ... }
      ]
    },
    { "step_id": 2, "order": 2, ... },
    ...
  ],
  "completion_progress": {
    "completed_steps": 0,
    "total_steps": 5,
    "percentage": 0
  }
}
POST /api/plan/{plan_id}/step/{step_id}/complete-action

Request:

json
{
  "step_item_id": 101,
  "action_type": "watched"
}
Response:

json
{
  "success": true,
  "action_recorded": {
    "user_id": 42,
    "step_item_id": 101,
    "action_type": "watched",
    "completed_at": "2025-12-07T14:30:00Z"
  }
}
9. Roles & Responsibilities (Unchanged)
You (founder): Product vision, roadmap, UX testing, deployment decisions.

I (AI): Architecture, code design, implementation, documentation, tooling guidance.

Shared: Git commits, schema design, decision logs.

10. Roadmap (v2, Updated)
Session 2–3 (Current):

✅ Docker infra (Postgres, Redis, web).

✅ Categories table + seed (8 categories, free/premium).

✅ /api/plan basic implementation (reading from categories).

🔄 Next: Add step_items table, design TikTok scraper, mock video data.

Session 4–5:

TikTok public video scraper (Firecrawl/Apify or manual parsing).

Populate trending_videos table with real data.

/api/plan returns actual video links (not mocked).

user_actions table + POST endpoint to track "watched/liked/blocked".

Session 6–7:

AI layer: LLM generates recommendations ("pick 5 videos for category X, language Y").

Qdrant + vector embeddings for semantic search.

n8n workflow for video recommendation pipeline.

Premium/free tier logic (2 vs 5–7 videos per step).

Session 8–9:

UI improvements: video preview cards, progress tracking, completion animations.

Mobile PWA features (offline, installable).

Analytics dashboard (completion rates, engagement, LTV).

Session 10+:

Cloud deployment (Hetzner / DigitalOcean).

Kubernetes setup.

Payment integration (Stripe).

Advanced: multi-language support, creator partnerships, affiliate links.

11. Key Documents (in Repo)
docs/architecture/c4-context.md — System Context (textual).

docs/domain-model.md — Domain Model (User, Plan, Step, Category, StepItem).

db_schema_v0.sql — Initial schema (users, categories, plans, plan_steps).

db_schema_categories_v0.sql — Categories table with is_premium.

db_seed_categories_v0.sql — 8 base categories seeded.

Dockerfile, docker-compose.yml, .env — Infrastructure.

requirements.txt — Python dependencies.

app/__init__.py, app/routes/health.py, app/routes/plan.py — Flask app.

app/models.py — SQLAlchemy models (Category, User, Plan, PlanStep).

12. Environment Setup (Both Locations: [translate:дача] & [translate:дом])
Minimal requirements:

Windows 10/11 (WSL2 support).

Git + GitHub desktop.

VS Code.

Docker Desktop (installed, tested).

Python 3.11+ (for local testing, optional for Docker dev).

Repository:

https://github.com/mefmax/fypfixer.git

Main branch: production-ready code.

All changes: git add + commit + push.

Local paths:

[translate:дача]: C:\Users\mefmax\OneDrive\!My Projects\FYPFixer

[translate:дом]: Same path (OneDrive synced).

Docker commands (standard):

powershell
docker compose up -d
docker compose ps
docker logs fypfixer-web
docker compose build web
docker compose down -v
🎯 Next Immediate Steps
Add step_items table to schema (video links, metadata).

Design TikTok scraper (what service? Firecrawl? manual?).

Mock video data for first 3 categories.

Update /api/plan to return videos instead of text.

Create UI component to display videos + action buttons.