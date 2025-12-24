# FYPGlow — Бэклог

> Задачи на будущее. Обновлять по мере выполнения.

**Последнее обновление:** 24 декабря 2025

---

## 🔴 Высокий приоритет

### Build args в docker-compose.yml
**Проблема:** При `docker compose build` без `--build-arg` используются дефолтные значения (localhost).

**Решение:**
```yaml
frontend:
  build:
    context: ./Frontend
    args:
      VITE_API_URL: ${VITE_API_URL:-https://fypglow.com/api}
      VITE_TIKTOK_CLIENT_KEY: ${VITE_TIKTOK_CLIENT_KEY}
```

---

## 🟡 Средний приоритет

### Унифицировать TikTok OAuth
**Сейчас:**
- DEV: HEX PKCE, localhost redirect
- PROD: Base64URL PKCE, fypglow.com redirect

**После:** Один код для всех (TikTok LIVE одобрен 24.12.2025)

---

### Переименовать `Frontend` → `frontend`
Case-sensitive пути в Linux.

---

## 🟢 Низкий приоритет

- fail2ban от WordPress сканеров
- API rate limiting
- Вариативность в StaticProvider

---

## ✅ Выполнено (24.12.2025)

- TikTok OAuth LIVE одобрен
- Новые TikTok ключи на PROD
- AI-ядро (StaticProvider, AnthropicProvider, OllamaProvider)
- Фикс /api/plans/today
