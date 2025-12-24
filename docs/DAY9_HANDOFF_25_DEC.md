# FYPGlow — Day 9 Handoff (24→25 декабря 2025)

## 🎯 СТАТУС: РАБОТАЕТ!

- **PROD:** https://fypglow.com
- **TikTok:** LIVE (одобрен 24.12.2025)
- **AI:** StaticProvider (бесплатный fallback)

## 🔑 CREDENTIALS

```
TIKTOK_CLIENT_KEY=awvyb17mzijy09je
TIKTOK_CLIENT_SECRET=nmFI6fUIVcibVn7o3gjqZmr61w1OOQix
AI_PROVIDER=static
```

## ✅ ВЫПОЛНЕНО 24 ДЕКАБРЯ

- TikTok LIVE одобрен
- Ротация ключей
- AI-ядро (Static/Anthropic/Ollama providers)
- OAuth исправлен
- Документация в репо

## 📋 БЭКЛОГ

### 🔴 Высокий
- Build args в docker-compose.yml

### 🟡 Средний
- Унифицировать TikTok OAuth
- Переименовать Frontend → frontend

### 🟢 Низкий
- fail2ban
- API rate limiting

## 🚨 ОШИБКИ (docs/LESSONS_LEARNED.md)

10 записанных ошибок — читать перед деплоем!

## 🔧 КОМАНДЫ

```bash
# Деплой frontend
docker compose build \
  --build-arg VITE_TIKTOK_CLIENT_KEY=awvyb17mzijy09je \
  --build-arg VITE_API_URL=https://fypglow.com/api \
  --no-cache frontend && docker compose up -d frontend

# Переключить на Anthropic
sed -i 's/AI_PROVIDER=static/AI_PROVIDER=anthropic/g' .env
docker compose restart backend
```

## 👥 КОМАНДА

- Founder — координация
- PM Claude — архитектура
- DEV Claude — код
- PROD Claude — сервер 149.28.235.95
