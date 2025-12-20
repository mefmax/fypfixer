# FYPGlow — Day 8 Context Handoff

**Дата:** 20 декабря 2025  
**Продукт:** FYPGlow (бывший FYPFixer)  
**Слоган:** "Glow up your life. Detox your feed."

---

## 🎯 Что это за проект

FYPGlow — веб-приложение для улучшения TikTok FYP (For You Page).
- Пользователь выбирает категорию интересов
- AI генерирует ежедневный план действий
- План включает: follow, like, not_interested actions
- Цель: улучшить рекомендации TikTok

**Целевая аудитория:** US Gen Z (18-35), self-improvement focused

---

## 📁 Расположение проекта

```
C:\Projects\FYPGlow
```

**GitHub:** https://github.com/mefmax/fypfixer

---

## 🛠 Tech Stack

| Компонент | Технология |
|-----------|------------|
| Backend | Flask + SQLAlchemy + PostgreSQL |
| Frontend | React + TypeScript + Vite + Tailwind |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Container | Docker Compose |
| AI | Local (Ollama) / OpenAI / Anthropic (планируется) |

---

## 🐳 Docker Containers

```powershell
# Запуск
cd C:\Projects\FYPGlow
docker-compose up -d

# Проверка
docker ps
```

| Container | Port | Image |
|-----------|------|-------|
| fypfixer-backend | 8000 | fypglow-backend |
| fypfixer-frontend | 5173 | fypglow-frontend |
| fypfixer-db | 5432 | postgres:16-alpine |
| fypfixer-redis | 6379 | redis:7-alpine |

---

## ✅ Выполнено на День 8

### Security Fixes (все 9 применены):

**Critical (3):**
- C1: Убраны дефолтные JWT/SECRET keys
- C2: Добавлен Flask-Limiter rate limiting
- C3: Проверка token type в JWT

**High (6):**
- H1: CORS whitelist для production
- H2: JWT lifetime 15min access / 7d refresh
- H3: Password validation (8+ chars, letter + number)
- H5: Скрыты exception details
- H6: Security headers в nginx
- H7: Redis backend для rate limiter

### Ребрендинг:
- FYPFixer → FYPGlow
- Новый слоган
- Логотипы добавлены
- Favicon обновлён

### Инфраструктура (День 7):
- Сервер: BitLaunch, New York, $28/mo
- IP: 149.28.235.95
- Домены: fypglow.com + fypglow.app (NameSilo)
- DNS настроен на сервер
- WHOIS Privacy включён

---

## ⏳ TODO (что осталось)

### Production Deploy:
- [ ] SSH подключение к серверу
- [ ] Установка Docker на сервер
- [ ] SSL сертификаты (Let's Encrypt)
- [ ] Deploy приложения
- [ ] Настройка production .env

### Функционал:
- [ ] Real TikTok scraper (Apify integration)
- [ ] OpenAI/Anthropic AI providers
- [ ] Refresh token flow на frontend
- [ ] Email verification (опционально)

### Качество:
- [ ] E2E тесты (Cypress)
- [ ] Lighthouse audit
- [ ] Mobile testing

---

## 🔐 Production Secrets (нужно сгенерировать)

```bash
# Для .env на production сервере
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
JWT_SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
DATABASE_URL=postgresql://fypglow:STRONG_PASSWORD@localhost:5432/fypglow
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=https://fypglow.com,https://www.fypglow.com
FLASK_ENV=production
```

---

## 📊 Бюджет потрачено

| Статья | Сумма |
|--------|-------|
| BitLaunch сервер | $51 |
| Домены (NameSilo) | $33.28 |
| **Итого** | **$84.28** |

---

## 🔗 Полезные URLs

- Frontend local: http://localhost:5173
- Backend API: http://localhost:8000/api/health
- Production (после deploy): https://fypglow.com

---

## 📝 Команды для работы

```powershell
# Перейти в проект
cd C:\Projects\FYPGlow

# Запустить Docker
docker-compose up -d

# Логи backend
docker-compose logs backend --tail=50

# Инициализировать БД (если пустая)
docker exec fypfixer-backend python init_db.py

# Пересобрать после изменений
docker-compose build
docker-compose up -d
```

---

## 🎭 Роли Claude

Используется multi-role подход:
- **System Architect** — архитектура, security
- **Project Manager** — координация, статусы
- **Backend Developer** — Flask, API
- **Frontend Developer** — React, UI
- **Code Reviewer** — качество кода

Инструкции в файле: `CLAUDE_ROLES_INSTRUCTIONS.md` в project knowledge.

---

## ⏭️ Рекомендуемый следующий шаг

**Вариант A:** Скрипты синхронизации БД (db-save.ps1, db-restore.ps1)
**Вариант B:** Production deploy на сервер
**Вариант C:** Тестирование полного flow (регистрация → план → actions)

---

**Этот файл загрузи в project knowledge нового диалога!**
