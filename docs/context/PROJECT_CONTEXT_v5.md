FYPFixer – Project Context Snapshot 

наши роли
ты - мозг руководитель этого проекта, главный разработчик и архитектор + дизайнер
я - твой аватар в реальном мире, твои руки, подчиняюсь твоим командам, думать, выбирать не умею. могу тратить 2 часа в день, не больше. У меня win 10/11
когда я всё сделал я буду писать +

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

FYPFixer – Project Context Snapshot v5 (2025‑12‑08, 20:37 MSK)
1. Project Status & Current Sprint
Version: MVP v2 (backend ready, UI in progress)
Last updated: 2025‑12‑08, 20:37 MSK
Team: Founder (product, testing), AI (architecture, code, docs)

Current priority:

Finalize UI: connect video player iframe and "Open in TikTok" button to video_url

Prepare for closed beta test in 2–4 weeks (working ~1.5h/day)

Validate product-market fit with EN-speaking audience (18–35, personal growth/learning focus)

2. What FYPFixer Does (Quick Recap)
AI-powered daily checklists with concrete TikTok video links. User gets a structured plan (3–5 steps), taps through videos and actions (watch, like, follow, block), and their FYP gets trained without FYPFixer having direct account access.

Core value: "Train your TikTok feed in 10 minutes a day. No searching, no thinking—just tap and watch."

3. Architecture Overview
Backend
Flask + SQLAlchemy (Python 3.11)

/api/plan — returns structured plan with steps[] containing items[] (video metadata: url, title, creator, thumbnail, reason)

/api/health — DB/Redis connectivity check

Flask‑Babel for i18n (EN/RU/ES templates and content)

Database
PostgreSQL 16: users, categories, plans, plan_steps, step_items

For detailed schema, see db/schema/*.sql in project repo

Redis 7: caching, sessions, rate limits (future)

Frontend
Flask templates + vanilla JS + CSS

Mobile-first dark theme

Video player modal with embedded iframe + "Open in TikTok" button

Real-time video_url binding (JS function setCurrentVideo())

Infrastructure
Docker Compose (web, Postgres, Redis)

Local dev = prod (source of truth)

Run: git pull → docker compose build web → docker compose up -d

AI Layer (Future)
Two-stage: lightweight model formulates refined query → sonar-pro searches and curates videos

Wrapped in custom service (zero vendor lock; can swap Perplexity ↔ OpenAI)

Metrics: cost per plan generation, hallucination filters (min N sources before suggesting)

4. Where Code Lives
Component	File(s)	Purpose
App init	app/__init__.py	Flask setup, blueprint registration, DB/Redis init
API endpoints	app/routes/plan.py, app/routes/health.py	/api/plan, /api/health
Models	app/models.py	SQLAlchemy: User, Category, Plan, PlanStep, StepItem
Landing page	templates/index.html	Main UI: form, video player, checklist, "Your Plan" section
Infrastructure	docker-compose.yml, Dockerfile	Container definitions
Setup	README.md	Quick start guide (requirements, Docker commands)
Database	db/schema/*.sql	Latest schema files (not stored in context, too volatile)
For full SQL schemas, see db/schema/ directory in repo.

5. Current State (✅ done / 🔄 in progress / ❌ to do)
Aspect	Status	Notes
Backend API	✅	/api/plan returns steps + items with video URLs
Demo plan	✅	Multiple steps with descriptions; no undefined
Docker infra	✅	web + Postgres + Redis running stable
Database schema	✅	v3 with step_items table; 8 categories seeded
Liz page + form	✅	Works; shows plan on submission
Video player	🔄	iframe needs binding to video_url; "Open in TikTok" button needs href binding
UI polish	🔄	Video cards from items[], multi-video nav
User auth	🔄	Anon client_id (device-based); no login yet
Progress tracking	❌	user_actions table planned; step completion UI not implemented
Real TikTok scraper	❌	Currently mock URLs; light scraper needed for MVP
AI layer	❌	No LLM integration yet (planned Session 7–8)
Premium tier	❌	is_premium flag in DB; logic not implemented
6. Target Audience & Monetization
Primary: EN-speaking TikTok users (18–35), focus on personal growth, learning, wellness.
Secondary: ES-speaking Latam users (expand after EN MVP validation).

Monetization:

Free tier: 2 videos/step, 1x/day, basic categories

Premium: $4.99–$9.99/month, 5–7 videos/step, 6h refresh, premium categories (science_tech, food, travel), creator partnerships

7. User Journey (MVP)
Open FYPFixer → select interest + language

Submit → /api/plan returns day's checklist with video links

See embedded video in modal + "Open in TikTok" button

Tap → opens TikTok app (or web) on that exact video

User watches, likes, follows, hides—TikTok's algo learns from actions

Check off steps, see progress 0/5 → 5/5 (gamification)

Return tomorrow for fresh plan, no login needed (anonymous client_id in cookie)

8. Key Decisions & Rationale (Architecture Decision Records)
No TikTok OAuth Login
Why: TikTok restricts third-party account access; we don't need it (influence FYP via user's own actions)

How: Anonymous client_id + local storage; history stored in users table

Anon User ID (Device-Based)
Why: Zero friction MVP; can add email/social login later

How: Generate UUID on first visit, store in cookie/localStorage, link all plans/actions to that ID

Public TikTok links only
Why: Safer, legal, no deep linking tricks needed

How: Standard tiktok.com/@user/video/ID URLs auto-open TikTok app if installed

sonar-pro for AI (Future)
Why: Native search + web context; cheaper than GPT-4 for curation; two-stage (cheap model + sonar) minimizes costs

How: Wrapped in custom service; swappable provider via config

Embedded player (no external embed)
Why: Better UX than constant redirects; users see video inline

How: iframe with video_url; "Open in TikTok" for actual app interaction

9. Known Issues & Tech Debt
Video player binding: iframe src and button href not yet synced to current_video.video_url

Fix: Implement setCurrentVideo() JS function; test modal video switch

No user action tracking: Can't yet record what user watched/skipped/liked

Impact: Can't build personalization or analytics

Plan: Add user_actions table + /api/plan/{id}/complete-action endpoint (Session 3–4)

Real video source: Currently mock URLs in DB seed

Impact: Can't show real trending content

Plan: Light scraper or manual CSV import for MVP test (Session 5)

No error handling for DB/Redis: App crashes if Postgres/Redis unavailable

Fix: Add try/catch in Flask init + health checks (Session 3)

Multi-language is scaffolded but EN-only content

Impact: RU/ES templates exist but no translated plans yet

Plan: Focus MVP on EN; ES localization = Session 3–4+

10. Next Steps (Prioritized)
This Week
Bind video_url to iframe + button (1–2h): Implement setCurrentVideo(), test modal playback

Update PROJECT_CONTEXT in repo (1h): Sync AI decisions, architecture notes

Local smoke test: /api/plan → UI → modal → TikTok link → works

Next Week (Sessions 2–3)
Multiple video cards in UI (5h): Show all videos from items[], navigation buttons

Basic user actions tracking (5h): UI checkboxes for step completion, simple progress bar

Real or semi-real video data (7h): CSV seed or manual + light scraper for top TikTok trends

By Week 3 (Beta Launch)
Closed test with 5–10 real users (EN-speaking, personal growth interested)

Collect feedback: What hooks? What friction? Why churn?

Iterate: Polish UX, fix bugs, tweak category/video selection

11. Risks & Mitigations
Risk	Severity	Mitigation
TikTok blocks our scraper or user flow	High	Start with published links only; monitor ToS; pivot to YouTube Shorts if needed
Low user retention (>30% day-2 churn)	High	Focus on habit-forming: reminders, streak counter, perfect 10-min experience
Slow video curation = low quality	Medium	Combine manual seeds + light ML (sonar-pro) for selection; start narrow (2–3 categories)
DB/Redis failures crash app	Medium	Add health checks + graceful fallbacks; containerize + monitoring (Session 7+)
Can't differentiate from other FYP-trainers	High	Unique angle: Daily atomic plans (not infinite browse) + creator partnerships (later)
12. Communication & Sync

Всё на месте:

✅ Git репо (on branch main)

✅ .env файл

✅ app/ папка

✅ docker-compose.yml

✅ requirements.txt

✅ Полная структура проекта

Context updates: Every sprint end (weekly), or when major decisions made

Code: Git is truth; all decisions + schema changes logged in commits

Quick Q&A: Use this context as reference; no need to repeat architecture each session


