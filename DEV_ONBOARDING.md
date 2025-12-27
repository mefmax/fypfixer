# FYPGLOW — DEV ONBOARDING
## Прочитай перед началом работы

---

# 🎯 МИССИЯ ПРОЕКТА

**FYPGlow** — помогаем пользователям изменить TikTok ленту за 7 дней.

**Проблема:** TikTok алгоритм засасывает в токсичный контент
**Решение:** 7-дневный челлендж с конкретными действиями

---

# 📊 ТЕКУЩИЙ СТАТУС

| Параметр | Значение |
|----------|----------|
| День разработки | Day 6 of 9 |
| MVP готовность | 55% |
| Backend API v2 | ✅ Готов |
| Frontend v2 | 🔄 В процессе |
| PROD deployed | Day 1-5 |

---

# 🏗️ АРХИТЕКТУРА

## Tech Stack

| Компонент | Технология |
|-----------|------------|
| Frontend | React + TypeScript + Zustand + TailwindCSS |
| Backend | Python Flask + SQLAlchemy |
| Database | PostgreSQL |
| Cache | Redis |
| AI | Claude Haiku API |
| Auth | TikTok OAuth (LIVE, не sandbox!) |
| Server | VPS Ubuntu + Docker + Nginx |

## Структура проекта

```
FYPFixer/
├── Frontend/           # React приложение
│   └── src/
│       ├── components/
│       │   └── plan/   # ← Day 5-6 работа здесь
│       ├── stores/     # Zustand stores
│       ├── pages/
│       └── lib/
│
├── backend/            # Flask API
│   └── app/
│       ├── routes/
│       │   ├── plans_v2.py      # API v2
│       │   └── oauth.py         # TikTok OAuth
│       ├── services/
│       │   ├── plan_service_v2.py
│       │   ├── toxic_detection_service.py
│       │   ├── curation_service.py
│       │   └── favorites_service.py
│       ├── models/
│       └── ai_providers/
│           ├── anthropic_provider.py
│           └── static_provider.py
│
└── deploy/
    └── fail2ban/       # Server configs
```

---

# 📋 PLAN v2.0 — Главная фича

## 3 шага ежедневного плана:

```
┌─────────────────────────────────────────┐
│ Step 1: CLEAR (Detox)                   │
│ - Показываем токсичных креаторов        │
│ - Кнопка BLOCK ALL                      │
│ - Сигналы: blocks                       │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ Step 2: WATCH (Mindful Watching)        │
│ - 4 видео carousel                      │
│ - Like / Follow кнопки                  │
│ - Сигналы: watches, likes, follows      │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ Step 3: REINFORCE                       │
│ - Пересмотр любимого видео              │
│ - Share (только Day 3+)                 │
│ - Сигналы: rewatches, shares            │
└─────────────────────────────────────────┘
```

---

# ✅ ЧТО УЖЕ СДЕЛАНО (Day 1-5)

## Backend:
- ✅ OAuth whitelist (только fypglow.com + localhost)
- ✅ Security headers (X-Frame, CSP, HSTS)
- ✅ Tiered rate limits (AUTH:10, WRITE:30, READ:120, HEAVY:5/min)
- ✅ AI retry (3x backoff) + fallback to StaticProvider
- ✅ Redis plan cache (TTL 24h)
- ✅ AI request logging (cost tracking)
- ✅ Token cleanup (max 5 per user)
- ✅ DB indexes (6 штук)
- ✅ ToxicDetectionService
- ✅ CurationService
- ✅ FavoritesService
- ✅ PlanServiceV2

## API v2 Endpoints:
- ✅ POST /api/v2/plan/generate
- ✅ GET /api/v2/toxic-creators
- ✅ POST /api/v2/toxic-creators/block
- ✅ GET /api/v2/curated-videos
- ✅ GET/POST /api/v2/favorites

## Frontend:
- ✅ planStoreV2.ts (Zustand store)
- ✅ ClearStep.tsx (Block toxic creators)
- ✅ WatchStep.tsx (Video carousel)

## Infrastructure:
- ✅ fail2ban (auth + ddos jails)
- ✅ Deployed to PROD

---

# 🔧 ЧТО ДЕЛАЕМ СЕЙЧАС

## Сначала: CLEANUP_TIKTOK_SANDBOX

TikTok одобрил приложение — sandbox больше не нужен.
Убрать любую логику dev/prod для выбора sandbox/live.

## Потом: Day 6 — Frontend Integration

| Компонент | Описание |
|-----------|----------|
| ReinforceStep.tsx | Rewatch favorite + Share button |
| ShareModal.tsx | Invite friends (Day 3+) |
| DailyPlanViewV2.tsx | Container для 3 шагов |
| ChallengeProgress.tsx | "Day X of 7" прогресс |

---

# ⚠️ ВЫУЧЕННЫЕ УРОКИ

## TikTok OAuth:
- PKCE flow обязателен
- state parameter проверять ВСЕГДА
- Sandbox больше НЕ используем — только LIVE
- Redirect URIs в whitelist

## AI:
- Всегда retry 3x с exponential backoff
- Fallback на StaticProvider
- Логировать cost для мониторинга
- Cache планы на 24h

## Security:
- Rate limit на всех endpoints
- OAuth callback — 10/min max
- Refresh tokens — max 5 per user
- fail2ban для brute force

## Code:
- Не хардкодить 'fitness' — использовать DEFAULT_CATEGORY_CODE
- N+1 queries проверять — использовать eager loading
- Индексы на часто queried columns

---

# 📁 ВАЖНЫЕ ФАЙЛЫ

| Файл | Зачем |
|------|-------|
| `backend/app/config/constants.py` | Все константы |
| `backend/app/routes/plans_v2.py` | API v2 endpoints |
| `backend/app/services/plan_service_v2.py` | Plan generation |
| `Frontend/src/stores/planStoreV2.ts` | Frontend state |
| `Frontend/src/components/plan/` | UI компоненты |

---

# 🚫 ЧЕГО НЕ ДЕЛАТЬ

1. **Не использовать TikTok Sandbox** — только LIVE API
2. **Не создавать отдельные CSS файлы** — TailwindCSS inline
3. **Не хардкодить значения** — использовать constants.py
4. **Не игнорировать rate limits** — они важны
5. **Не забывать про TypeScript типы** — строгая типизация

---

# 🔌 API КОНТРАКТЫ

## POST /api/v2/plan/generate

Request:
```json
{"category": "fitness"}
```

Response:
```json
{
  "success": true,
  "data": {
    "plan": {
      "plan_id": "uuid",
      "day_of_challenge": 3,
      "steps": {
        "clear": {
          "type": "CLEAR",
          "toxic_creators": [...],
          "completed": false
        },
        "watch": {
          "type": "WATCH",
          "videos": [...],
          "completed": false
        },
        "reinforce": {
          "type": "REINFORCE",
          "favorite_video": {...},
          "show_share": true,
          "completed": false
        }
      }
    }
  }
}
```

---

# 🎨 UI GUIDELINES

- Dark theme: `bg-gray-900`, `text-white`
- Cards: `rounded-xl`, `shadow-lg`
- Primary button: `bg-purple-600 hover:bg-purple-700`
- Progress bars: `bg-green-500`
- Use Lucide icons
- Mobile-first responsive

---

# 📞 WORKFLOW

1. Получаешь промпт с задачей
2. Читаешь задачу полностью
3. Выполняешь по шагам
4. Коммитишь с понятным message
5. Отчитываешься: что сделано, какие файлы

## Commit message format:
```
feat: add ReinforceStep component
fix: remove TikTok sandbox logic
refactor: centralize constants
```

---

# ✅ ГОТОВ К РАБОТЕ

После прочтения этого документа ты знаешь:
- Что такое FYPGlow и зачем он нужен
- Текущий статус и что уже сделано
- Архитектуру и tech stack
- Выученные уроки
- Что делать сейчас

**Жди промпт с конкретной задачей!**
