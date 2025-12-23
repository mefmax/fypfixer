# FYPGlow Architecture v4.2
## Guided Watching Edition — Production Ready

**Дата:** 23 декабря 2025
**Версия:** 4.2
**Статус:** ✅ Ready for Development
**Changes:** QA fixes, scope reduction, API contracts

---

## 🎯 Миссия

Помочь пользователям **реально изменить** свою TikTok ленту за 5-7 дней через конкретные, выполнимые действия.

---

## 🔄 Ключевое изменение: Guided Watching

### Было (v1-v3):
```
"Подпишись на 3 аккаунта в категории Fitness"
→ Юзер сам ищет, не знает на кого
→ Слабый эффект на алгоритм
→ Юзер уходит через 2 дня
```

### Стало (v4+):
```
"Посмотри @chriswillx до конца и подпишись"
→ Конкретный аккаунт с описанием
→ Кнопка "Открыть в TikTok"
→ Сильный эффект (watch time!)
→ Юзер видит результат
```

---

## 🏗️ Системная архитектура

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL SERVICES                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │   TikTok    │    │   Apify     │    │  Anthropic  │                     │
│  │   OAuth     │    │  Scraper    │    │   Claude    │                     │
│  │             │    │  (Schedule) │    │   Haiku     │                     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                     │
│         │                  │                  │                             │
└─────────┼──────────────────┼──────────────────┼─────────────────────────────┘
          │                  │                  │
          │ OAuth            │ Webhook          │ API
          │ Callback         │ (accounts)       │ (filter/enrich)
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               BACKEND (Flask)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ Auth Service │ │   Curated    │ │  AI Service  │ │  Analytics   │       │
│  │              │ │   Service    │ │              │ │   Service    │       │
│  │ • OAuth      │ │ • Import     │ │ • Filter     │ │ • Events     │       │
│  │ • JWT        │ │ • Get/Rank   │ │ • Enrich     │ │ (MVP: 3)     │       │
│  │ • Sessions   │ │ • Anti-repeat│ │ • Motivate   │ │              │       │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘       │
│         │                │                │                │                │
│         └────────────────┴────────────────┴────────────────┘                │
│                                   │                                         │
│                    ┌──────────────▼──────────────┐                          │
│                    │      Plan Generator         │                          │
│                    │  • Guided Watching          │                          │
│                    │  • Streak calculation       │                          │
│                    │  • Daily limit (1 plan)     │                          │
│                    └──────────────┬──────────────┘                          │
│                                   │                                         │
│  ┌────────────────────────────────┼────────────────────────────────────┐   │
│  │                          REDIS (Cache)                              │   │
│  │  • categories (TTL: 1h)                                             │   │
│  │  • curated:{category} (TTL: 10min)                                  │   │
│  │  • plan:{user_id}:{date} (TTL: 24h)                                 │   │
│  └────────────────────────────────┼────────────────────────────────────┘   │
│                                   │                                         │
│  ┌────────────────────────────────┼────────────────────────────────────┐   │
│  │                         PostgreSQL                                  │   │
│  │  users | categories | curated_accounts | user_shown_accounts        │   │
│  │  plans | plan_step_completions | analytics_events                   │   │
│  │  apify_import_logs                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
          │
          │ REST API
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React)                                │
└─────────────────────────────────────────────────────────────────────────────┘
          │
          │ HTTPS (Cloudflare)
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            INFRASTRUCTURE                                    │
│  Nginx | Docker Compose | Let's Encrypt | Cloudflare                        │
│  VPS: 149.28.235.95 (Vultr) | Domains: fypglow.com, fypglow.app            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📜 API Contracts (NEW in v4.2)

### TypeScript Interfaces

```typescript
// ============================================
// PLAN TYPES
// ============================================

interface CuratedAccount {
  id: string;
  username: string;
  display_name: string;
  bio: string | null;
  description_ru: string | null;  // AI-generated
  follower_count: number;
  avatar_url: string | null;
  profile_url: string;            // https://tiktok.com/@username
}

interface PlanStep {
  order: number;                  // 1, 2, 3
  type: 'detox' | 'watch' | 'browse';
  title: string;
  description: string;
  instruction: string | null;
  duration_minutes: number;
  target_count?: number;          // для detox: сколько видео
  accounts?: CuratedAccount[];    // для watch: список аккаунтов
  completed: boolean;
}

interface GuidedPlanResponse {
  id: string;
  steps: PlanStep[];
  total_duration_minutes: number;
  completion_rate: number;        // 0.0 - 1.0
  motivation: {
    greeting: string;             // "Привет! Готов прокачать ленту? 🔥"
    tip: string;                  // "Досматривай видео до конца..."
    encouragement: string;        // "Ты на 3-дневном streak!"
  };
  streak: {
    current: number;
    best: number;
  };
  generated_at: string;           // ISO timestamp
}

interface StepCompletionRequest {
  time_spent_seconds?: number;    // optional: сколько времени потратил
}

interface StepCompletionResponse {
  success: boolean;
  step_order: number;
  plan_completion_rate: number;   // обновлённый
  streak_updated: boolean;
}

// ============================================
// ANALYTICS TYPES (MVP: только 3 события)
// ============================================

type AnalyticsEventType =
  | 'plan_generated'           // план создан
  | 'step_completed'           // шаг выполнен
  | 'account_opened';          // нажал "Открыть в TikTok"

interface AnalyticsEvent {
  type: AnalyticsEventType;
  data?: {
    step_order?: number;
    step_type?: string;
    account_id?: string;
    account_username?: string;
  };
}
```

---

## 🔌 API Endpoints v4.2

### Auth
```
POST /api/auth/tiktok              # Initiate OAuth
GET  /api/auth/tiktok/callback     # OAuth callback
GET  /api/auth/me                  # Current user
POST /api/auth/logout              # Logout
```

### Categories
```
GET  /api/categories               # All categories (cached)
POST /api/categories/select        # User selects categories
     Body: { category_ids: string[] }
```

### Plan ⚠️ UNIFIED IN v4.2
```
GET  /api/plan/guided
     # Возвращает план на сегодня (создаёт если нет)
     # Категории берутся из user.selected_categories
     Response: GuidedPlanResponse

POST /api/plan/step/:order/complete    # ← unified: используем order (1,2,3)
     Body: StepCompletionRequest
     Response: StepCompletionResponse

GET  /api/plan/history
     Query: ?days=7
     Response: { plans: [...], streak_current, streak_best }
```

### Curated (Internal)
```
POST /api/curated/import           # Webhook from Apify
GET  /api/curated/accounts/:slug   # Get accounts by category
GET  /api/curated/stats            # Import stats
```

### Analytics (MVP: simplified)
```
POST /api/analytics/event
     Body: AnalyticsEvent
```

### Health
```
GET  /api/health                   # Basic health
GET  /api/health/ready             # Dependencies check
```

---

## 🧭 Onboarding Flow (SIMPLIFIED in v4.2)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER JOURNEY (MVP)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

1️⃣ LANDING PAGE
   │  "Надоело листать мусор в TikTok?"
   │  CTA: "Начать бесплатно"
   ▼
2️⃣ TIKTOK OAUTH
   │  Редирект → TikTok → Callback
   │  Backend создаёт user + JWT
   ▼
3️⃣ CATEGORY SELECTION
   │  "Что хочешь видеть в ленте?"
   │  Выбор 1-3 категорий
   ▼
4️⃣ WELCOME MODAL (вместо 7-step tutorial)
   │  ┌────────────────────────────────────────┐
   │  │  🎯 Как это работает                   │
   │  │                                        │
   │  │  1. Мы даём конкретные задания         │
   │  │  2. Ты выполняешь их в TikTok          │
   │  │  3. За 5-7 дней лента изменится        │
   │  │                                        │
   │  │  [Понятно, начинаем!]                  │
   │  └────────────────────────────────────────┘
   ▼
5️⃣ FIRST DAILY PLAN
   │  Сразу показываем план с 3 шагами
   ▼
6️⃣ EXECUTION & DAILY RETURN
```

**Email/Push:** Отложено на v5 (после валидации retention).

---

## 📊 Feedback Loop & Completion

### Философия: Trust but Verify (Lite)

- Юзер сам отмечает шаги как выполненные
- Мы логируем для аналитики
- Не пытаемся верифицировать (нет доступа к TikTok)

### Что логируем

```sql
INSERT INTO plan_step_completions (
    user_id, plan_id, step_order, step_type,
    shown_accounts,           -- UUID[] для watch шага
    completed_at,
    time_spent_seconds
);
```

### Streak Policy

```
День completed = хотя бы 1 шаг выполнен
Streak = последовательные дни с активностью
Grace period: можно пропустить сегодня, streak сохраняется до завтра
```

---

## ⏰ Apify Scheduling

### Стратегия: Apify-native scheduling

```
Schedule: Every Sunday 03:00 UTC
Actor: clockworks/tiktok-scraper
Categories: 12 задач (по одной на категорию)
On Success → POST /api/curated/import
On Failure → POST /api/curated/import-failed (логируем)
```

### Error Handling

```python
# Три сценария:
1. Success      → import all, AI enrich
2. AI Failed    → import without AI, quality_score = 0.5
3. Apify Failed → log error, alert if 3+ failures
```

---

## 🎯 Quality Score

### Формула v1

```python
quality_score = (
    followers_score(0-0.3) +      # log scale, cap 10M
    ai_relevance(0-0.4) +          # от Claude
    freshness(0.1) +               # placeholder
    manual_boost(0-0.1)            # admin override
)
# Range: 0.0 - 1.0
# Default without AI: 0.5
```

### Selection Algorithm

```sql
SELECT * FROM curated_accounts
WHERE category_id = ANY(user_categories)
  AND is_active = true
  AND quality_score >= 0.4
  AND id NOT IN (shown in last 7-14 days)
ORDER BY quality_score * 0.7 + RANDOM() * 0.3 DESC
LIMIT 4;
```

---

## 🔄 Anti-Repeat Logic

| Action | Cooldown |
|--------|----------|
| followed (self-reported) | Never show again |
| opened / completed | 14 days |
| shown / skipped | 7 days |

---

## 🤖 AI Fallback

| Scenario | Action |
|----------|--------|
| AI down on import | Import all, quality_score=0.5, is_ai_enriched=false |
| AI partial failure | Process successful, skip failed |
| AI down on plan | Use precomputed description_ru, default motivation |

**Default Motivation:**
```python
{
    "greeting": "Привет! Вот твой план на сегодня 🔥",
    "tip": "Досматривай видео до конца — главный сигнал для алгоритма.",
    "encouragement": "Каждый день приближает тебя к идеальной ленте!"
}
```

---

## 🚀 Caching Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  REDIS KEYS                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  categories              TTL: 1 hour                                        │
│  curated:{slug}          TTL: 10 minutes                                    │
│  plan:{user_id}:{date}   TTL: 24 hours                                      │
│  rate_limit:{ip}         TTL: 1 minute                                      │
└─────────────────────────────────────────────────────────────────────────────┘

Fallback: Если Redis недоступен → запросы идут в DB напрямую.
          Логируем warning, система продолжает работать.
```

---

## 📈 Analytics (MVP Scope)

### 3 Event Types (достаточно для MVP)

```python
class EventType(Enum):
    PLAN_GENERATED = "plan_generated"
    STEP_COMPLETED = "step_completed"
    ACCOUNT_OPENED = "account_opened"
```

### Key Metrics (SQL queries)

```sql
-- D7 Retention
-- Plan Completion Rate
-- Average steps per day
```

**Deferred to v5:** Full 10-event taxonomy, Sentry, dashboards.

---

## 🗄️ Database Schema v4.2

### Plans Table (с комментарием про JSONB)

```sql
CREATE TABLE plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_ids UUID[] NOT NULL,

    -- steps: массив PlanStep объектов
    -- Format: [
    --   { "order": 1, "type": "detox", "title": "...", "target_count": 15, ... },
    --   { "order": 2, "type": "watch", "accounts": [...], ... },
    --   { "order": 3, "type": "browse", ... }
    -- ]
    steps JSONB NOT NULL,

    total_duration_minutes INTEGER,
    completion_rate FLOAT DEFAULT 0,

    -- AI-generated motivation texts
    motivation JSONB,  -- { greeting, tip, encouragement }

    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE INDEX idx_plans_user_date ON plans(user_id, DATE(created_at) DESC);
```

### Полная схема (остальные таблицы)

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tiktok_id VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200),
    avatar_url TEXT,
    selected_categories UUID[] DEFAULT '{}',
    streak_current INTEGER DEFAULT 0,
    streak_best INTEGER DEFAULT 0,
    onboarding_completed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Categories
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    emoji VARCHAR(10),
    description TEXT,
    hashtags TEXT[],
    is_premium BOOLEAN DEFAULT false,
    display_order INTEGER DEFAULT 0
);

-- Curated Accounts
CREATE TABLE curated_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tiktok_username VARCHAR(100) UNIQUE NOT NULL,
    category_id UUID REFERENCES categories(id),
    display_name VARCHAR(200),
    follower_count INTEGER DEFAULT 0,
    bio TEXT,
    avatar_url TEXT,
    profile_url TEXT GENERATED ALWAYS AS ('https://www.tiktok.com/@' || tiktok_username) STORED,
    description_ru TEXT,
    quality_score FLOAT DEFAULT 0.5,
    manual_boost FLOAT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    is_ai_enriched BOOLEAN DEFAULT false,
    source VARCHAR(20) DEFAULT 'apify',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_curated_category_score ON curated_accounts(category_id, quality_score DESC)
    WHERE is_active = true;

-- User Shown Accounts
CREATE TABLE user_shown_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES curated_accounts(id) ON DELETE CASCADE,
    plan_id UUID REFERENCES plans(id),
    shown_at TIMESTAMP DEFAULT NOW(),
    action_taken VARCHAR(20) DEFAULT 'shown',  -- shown, opened, completed, followed, skipped

    UNIQUE(user_id, account_id, DATE(shown_at))
);

CREATE INDEX idx_shown_user_recent ON user_shown_accounts(user_id, shown_at DESC);

-- Plan Step Completions
CREATE TABLE plan_step_completions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    step_order INTEGER NOT NULL,
    step_type VARCHAR(20) NOT NULL,
    shown_accounts UUID[],
    completed_at TIMESTAMP DEFAULT NOW(),
    time_spent_seconds INTEGER,

    UNIQUE(plan_id, step_order)
);

-- Analytics Events (MVP: 3 types)
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_user ON analytics_events(user_id, created_at DESC);

-- Apify Import Logs
CREATE TABLE apify_import_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_slug VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    accounts_received INTEGER DEFAULT 0,
    accounts_imported INTEGER DEFAULT 0,
    accounts_filtered INTEGER DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

---

## 🔐 Environment Variables

```bash
# App
FLASK_ENV=production
SECRET_KEY=xxx
JWT_SECRET_KEY=xxx

# Database
DATABASE_URL=postgresql://user:pass@db:5432/fypglow
POSTGRES_USER=fypglow
POSTGRES_PASSWORD=xxx
POSTGRES_DB=fypglow

# Redis (documented format)
REDIS_URL=redis://:password@redis:6379/0
REDIS_PASSWORD=xxx

# TikTok OAuth
TIKTOK_CLIENT_KEY=xxx
TIKTOK_CLIENT_SECRET=xxx
TIKTOK_REDIRECT_URI=https://fypglow.com/auth/tiktok/callback

# AI
ANTHROPIC_API_KEY=xxx

# CORS
CORS_ORIGINS=https://fypglow.com,https://www.fypglow.com
```

---

## 📅 MVP vs Deferred

### ✅ MVP (v4.2)

- TikTok OAuth
- Category selection
- Guided Watching UI (3 steps)
- Apify integration
- AI enrichment
- Basic analytics (3 events)
- Redis caching
- Welcome modal (1 screen)

### 📦 Deferred (v5+)

| Feature | When |
|---------|------|
| Full analytics (10 events) | After launch |
| Sentry integration | After launch |
| Push notifications | After retention validated |
| Email reminders | After retention validated |
| FYP feedback surveys | v5 |
| Admin panel | v5 |
| Premium subscription | v6 |

---

## 📅 Roadmap

### Phase 1: MVP ← МЫ ЗДЕСЬ
- [x] TikTok OAuth
- [x] Category selection
- [ ] Guided Watching UI
- [ ] Apify integration
- [ ] AI enrichment
- [ ] TikTok Web App approval

### Phase 2: Retention (after launch)
- [ ] Sentry monitoring
- [ ] Full analytics
- [ ] Push notifications
- [ ] Streak achievements

### Phase 3: Growth
- [ ] Referral program
- [ ] Premium categories

### Phase 4: Monetization
- [ ] Subscription ($4.99/mo)

---

## ✅ QA Checklist

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Feedback loop | ✅ Trust but verify |
| 2 | Apify scheduling | ✅ Native + error handling |
| 3 | Quality score | ✅ Formula documented |
| 4 | Anti-repeat | ✅ 7-14 day cooldown |
| 5 | AI fallback | ✅ 3 scenarios |
| 6 | Onboarding | ✅ Simplified to modal |
| 7 | Plan refresh | ✅ 1/day policy |
| 8 | Analytics | ✅ MVP: 3 events |
| 9 | Caching | ✅ Redis + fallback |
| 10 | Monitoring | ✅ Health endpoints |
| 11 | TikTok context | ✅ External site + deep links |
| 12 | DB indexes | ✅ Hot-path covered |
| 13 | API contracts | ✅ TypeScript interfaces |
| 14 | Endpoint consistency | ✅ :order unified |

---

**Last Updated:** 23 декабря 2025
**Authors:** PM Opus + Founder + QA Review
**Version:** 4.2 — Production Ready 🚀
