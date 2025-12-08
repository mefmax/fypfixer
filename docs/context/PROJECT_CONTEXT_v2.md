FYPFixer – Project Context Snapshot v3 (2025‑12‑07, 18:14 MSK)
1. Purpose & Vision (Final)
Идея:
FYPFixer — это AI‑помощник, который генерирует ежедневные конкретные действия с готовыми ссылками на TikTok видео. Пользователь только жмёт кнопки; FYPFixer — мозг, пользователь — руки.

Миссия:

Give users simple, AI-powered daily checklists with concrete TikTok video links. No searching, no thinking — just tap and watch. Train your FYP in 10 minutes a day.

Видение:

Стать стандартом "управляемого FYP" на TikTok (позже — Instagram, YouTube Shorts).

Вводить оба варианта: free (2 видео/шаг, 1x/день) и premium ($4.99–$9.99/месяц, 5–7 видео/шаг, обновление 6ч).

Международная аудитория (EN основной, RU/ES локализованы).

2. Target Audience (Final)
Primary ЦА: Вариант A

Демография: 18–35 лет, пользователи TikTok.

Психография: хотят "чистый, качественный контент без мусора".

Боль: мусор в FYP, потеря времени на поиск, информационный хаос.

Решение: FYPFixer даёт готовые действия с конкретными видео.

Категории (8 штук, 5 free + 3 premium):

## 6. Пользовательский путь (MVP)

FYPFixer не логинит пользователя в TikTok, а даёт чек‑лист действий и публичные ссылки;
влияние на FYP происходит через осознанные действия пользователя по этим ссылкам.

1. Пользователь открывает лендинг FYPFixer на телефоне и видит поле для ввода интересов и большую кнопку «Получить план». [file:159][image:1]  
2. Вводит пару ключевых слов (например, «personal_growth, fitness, education…») и жмёт кнопку; фронтенд вызывает `/api/plan` с категорией и языком. [file:159]  
3. Бэкенд выбирает демо‑план для категории (сейчас personal_growth), возвращает JSON с шагами и списком видео для первого шага. [file:159]  
4. Интерфейс показывает блок «Today’s Video» с обложкой и описанием ролика, а ниже — чек‑лист шагов в секции «Your Plan». [file:159][image:1]  
5. Пользователь нажимает «Open in TikTok», ролик открывается в приложении TikTok по прямой ссылке `video_url`; пользователь смотрит и таким образом «обучает» свою ленту. [file:159]  
6. После просмотра пользователь может вернуться и пройти следующие шаги (например, подписаться на экспертов или применить выученное), пока весь чек‑лист не будет выполнен. [file:159]

#	Code	EN	RU	ES	is_premium
1	personal_growth	Personal Growth	Личное развитие	Crecimiento Personal	FALSE
2	entertainment	Entertainment	Развлечение	Entretenimiento	FALSE
3	wellness	Wellness & Lifestyle	Здоровье и Образ жизни	Bienestar y Estilo de vida	FALSE
4	creative	Creative & Arts	Творчество и Искусство	Creatividad y Arte	FALSE
5	learning	Learning & Education	Обучение и Образование	Aprendizaje y Educación	FALSE
6	science_tech	Science & Technology	Наука и Технология	Ciencia y Tecnología	TRUE
7	food	Food & Cooking	Еда и Кулинария	Comida y Cocina	TRUE
8	travel	Travel & Adventure	Путешествия и Приключения	Viajes y Aventura	TRUE
3. Product Values & Principles
Safety & Compliance: Only public TikTok videos, no account access, transparent scraping.

Simplicity: User taps button → action completed (watch, like, block, follow, search).

Concrete Value: Not advice, but ready-to-use actions with video links.

AI‑Powered: LLM + Vector DB generates recommendations, not manual templates.

Engagement Over Friction: Minimize user thinking; maximize button‑tapping.

4. Current Product State (MVP v2, Actual Status)
✅ Implemented (Session 1 complete):

Landing page (Flask + Jinja2, 3 languages EN/RU/ES).

/api/health — health check with DB connectivity (✓ working).

/api/plan — returns plan with steps and items[] containing concrete TikTok video links (✓ working).

Each item: video_url, title, creator, thumbnail_url, reason.

Demo plan with 3 mock videos for testing (✓ in DB).

Categories table with is_premium flag (8 base categories seeded) (✓ working).

Docker Compose infrastructure (web, Postgres 16, Redis 7) (✓ working).

SQLAlchemy models: Category, PlanStep, StepItem with relations (✓ defined).

Status: MVP v2 backend is ALIVE. /api/plan already returns video items, not generic advice.

5. Tech Stack (Target, Refined)
Backend

Python 3.11 + Flask + Flask‑SQLAlchemy.

REST API (/api/plan, /api/plan/{id}/step, /api/plan/{id}/complete-action, /api/recommendations).

Flask‑Babel for i18n (UI + Plan content).

Database

PostgreSQL 16:

users (client_id, language).

categories (code, names_en/ru/es, is_premium).

plans (user_id, category_id, plan_date, language, is_template, title).

plan_steps (plan_id, step_order, action_type, text_en/ru/es).

step_items (NEW) (plan_step_id, video_id, creator_username, title, thumbnail_url, video_url, engagement_score, reason_text).

trending_videos (planned: category cache).

user_actions (planned: tracking).

Redis 7 (cache, sessions, rate limits).

AI & Data

Двухэтапная схема AI: лёгкая модель AI формирует уточнённый запрос к цели/категории, sonar‑pro — поиск и отбор видео + короткое обоснование.​​

Отдельный клиент для AI: таймауты, ретраи, логирование, возможность сменить провайдера без переписывания бэкенда.

TikTok Scraper: Firecrawl.dev or manual parsing (planned, currently mock).

LLM: Ollama (local, llama3) or OpenAI (fallback/premium).

Vector DB: Qdrant — embed videos, semantic search.

Data Pipeline: n8n or cron job for trending videos refresh.

Frontend

Flask templates + vanilla JS + CSS (mobile‑first, dark theme).

PWA approach (offline, installable).

Video card components (thumbnail, title, creator, action buttons).

Infrastructure

Docker Compose (local dev): web, Postgres, Redis, Ollama, Qdrant, n8n, Grafana, Prometheus, Nginx.

Production: Hetzner / DigitalOcean + Kubernetes (later).

Observability: Prometheus, Grafana, Loki, Sentry.

Backups: Daily Postgres snapshots to S3‑compatible storage.

6. Database Schema (v3, Current State)
Created tables:

sql
-- users
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  client_id VARCHAR(64) UNIQUE NOT NULL,
  language VARCHAR(5) NOT NULL DEFAULT 'en',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- categories
CREATE TABLE categories (
  id BIGSERIAL PRIMARY KEY,
  code VARCHAR(32) UNIQUE NOT NULL,
  name_en TEXT NOT NULL,
  name_ru TEXT,
  name_es TEXT,
  is_premium BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- plans
CREATE TABLE plans (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
  category_id BIGINT REFERENCES categories(id),
  plan_date DATE NOT NULL,
  language VARCHAR(5) NOT NULL DEFAULT 'en',
  is_template BOOLEAN NOT NULL DEFAULT FALSE,
  title TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, plan_date, language)
);

-- plan_steps
CREATE TABLE plan_steps (
  id BIGSERIAL PRIMARY KEY,
  plan_id BIGINT NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
  step_order INT NOT NULL,
  action_type VARCHAR(32),
  text_en TEXT NOT NULL,
  text_ru TEXT,
  text_es TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- step_items (NEW!)
CREATE TABLE step_items (
  id BIGSERIAL PRIMARY KEY,
  plan_step_id BIGINT NOT NULL REFERENCES plan_steps(id) ON DELETE CASCADE,
  video_id VARCHAR(256),
  creator_username VARCHAR(256),
  title TEXT,
  thumbnail_url TEXT,
  video_url TEXT NOT NULL,
  engagement_score DOUBLE PRECISION,
  reason_text TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_step_items_plan_step ON step_items(plan_step_id);
Seeded data:

8 categories (5 free: personal_growth, entertainment, wellness, creative, learning; 3 premium: science_tech, food, travel).

1 demo plan ("Demo Personal Growth Plan") with 1 step ("watch 3 videos") and 3 mock video items.

7. API Contracts (v3, Current)
GET /api/plan?lang=en&category=personal_growth

Response (actual from production):

json
{
  "plan_date": "2025-12-07",
  "language": "en",
  "category_code": "personal_growth",
  "category_name": "Personal Growth",
  "steps": [
    {
      "step_id": 1,
      "order": 1,
      "action_type": "watch",
      "text": "Watch these 3 videos about personal growth",
      "items": [
        {
          "step_item_id": 1,
          "video_id": "demo_vid_1",
          "creator": "@growthcoach",
          "title": "5 Habits to Change Your Life",
          "thumbnail_url": "https://example.com/thumb1.jpg",
          "video_url": "https://www.tiktok.com/@growthcoach/video/0000000000000000001",
          "reason": "High engagement, great for beginners"
        },
        { ... },
        { ... }
      ]
    }
  ]
}
Observed: Each items[] contains video_url, title, creator, thumbnail_url, reason — ready for frontend to display and link.

8. Repository Structure
text
FYPFixer/
├── db/
│   ├── schema/
│   │   ├── db_schema_v0.sql               (users, plans, plan_steps)
│   │   ├── db_schema_categories_v0.sql    (categories table + is_premium)
│   │   └── db_schema_step_items_v0.sql    (step_items table)
│   ├── migrations/
│   │   └── (planned: future ALTER migrations)
│   └── seeds/
│       ├── db_seed_categories_v0.sql      (8 categories)
│       └── db_seed_demo_plan_v0.sql       (demo plan + 3 videos)
├── docs/
│   ├── architecture/
│   │   └── c4-context.md
│   ├── context/
│   │   ├── PROJECT_CONTEXT_v3.md (this file)
│   │   └── README.md
│   └── domain-model.md
├── app/
│   ├── __init__.py          (Flask app init, blueprint registration)
│   ├── models.py            (Category, PlanStep, StepItem)
│   └── routes/
│       ├── __init__.py
│       ├── health.py        (/api/health)
│       └── plan.py          (/api/plan with items[])
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── index.html           (landing)
│   └── plan.html            (plan display — to be enhanced)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── main.py
├── .gitignore
└── README.md
9. Roles & Responsibilities
You (founder): Product vision, UX decisions, roadmap, deployment, testing on real users.

I (AI): Architecture, code design, implementation, documentation, debugging.

Shared: Git discipline, decision logs (C4 updates, ADRs).

10. Roadmap (Sessions 2–10+)
Session 2 (Current focus — next steps):

✅ Database schema with step_items.

✅ /api/plan returns video items.

🔄 UI enhancement: Display video cards from items[] on frontend (thumbnail, title, creator, "Open in TikTok" button).

🔄 Expand demo plan to 5 steps (not just 1 step).

Session 3–4:

Mock more video data for different categories.

Add "Step completion tracking" (user marks video as watched).

Build /api/plan/{plan_id}/complete-action endpoint.

Session 5–6:

TikTok public video scraper (Firecrawl or manual).

trending_videos table + refresh job.

Replace mock URLs with real TikTok video links.

Session 7–8:

AI layer: LLM generates recommendations.

Qdrant integration for semantic search of videos.

Premium/free tier restrictions.

Session 9–10:

User analytics: completion rates, engagement, LTV.

Cloud deployment (Hetzner / DigitalOcean).

Payment integration (Stripe).

Session 11+:

Kubernetes setup, auto-scaling.

Multi-language polish.

Creator partnerships, referral system.

11. Key Development Principles
One artifact at a time: Changes committed to main, one feature per PR/commit.

Documentation first: C4 diagrams, schema changes, API contracts updated before/after code.

No hardcoded data: All templates and lists go to DB (categories, plans, steps, items).

Testing locally: Docker Compose is source of truth; dev = prod (as much as possible).

Git is truth: All decisions, context, code live in the repo.

12. Environment Setup (Both Locations)
Locations:

дача﻿: C:\Users\mefmax\OneDrive\!My Projects\FYPFixer

дом﻿: Same path (OneDrive synced).

Requirements:

Windows 10/11 + WSL2.

Docker Desktop (latest stable).

Git + GitHub CLI.

VS Code + Python extension.

Python 3.11+ (for local testing).

Commands (standard):

bash
git pull
docker compose build web
docker compose up -d
curl http://localhost:8000/api/plan
13. Current Status Summary (2025‑12‑07, 18:14 MSK)
Aspect	Status	Evidence
Infrastructure	✅ Ready	Docker + Postgres + Redis running, all 5 tables exist.
Backend Core	✅ Ready	Flask app + /api/health + /api/plan working.
Database	✅ Ready	Schema v3 with step_items; 8 categories seeded; 1 demo plan with 3 videos.
API Response	✅ Ready	/api/plan returns steps[].items[] with video_url, title, creator, reason.
UI Layer	🔄 WIP	Templates exist, but not yet displaying video cards from items[].
Real Video Scraper	❌ Todo	Currently mock TikTok URLs.
AI Recommendations	❌ Todo	No LLM integration yet.
Premium/Free Logic	❌ Todo	All categories accessible (no tier restrictions).
Next action (Session 2): Upgrade frontend to display video items as clickable cards with thumbnails and "Open in TikTok" buttons.