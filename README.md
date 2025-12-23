FYPFixer — планировщик для улучшения TikTok‑ленты.

Требования
Требования:

Docker Desktop

Git

Windows 10/11 (опционально WSL2)

VS Code (рекомендуется в качестве редактора)

Локальный запуск
Local setup:

bash
git pull
docker compose build web
docker compose up -d
curl http://localhost:8000/api/plan
Интерфейс доступен в браузере по адресу http://localhost:8000/?lang=ru

Статус проекта
Статус:

Бэкенд и /api/plan уже работают, отдают демо‑план из базы

UI показывает демо‑план на лендинге

В планах — карточки нескольких видео и трекинг выполнения шагов пользователем

## Documentation

- [Architecture v4.2](docs/FYPGLOW_ARCHITECTURE_v4.2.md) — Current architecture (API contracts, DB schema, roadmap)
- [TikTok OAuth PKCE — Lessons Learned](docs/TIKTOK_OAUTH_PKCE_LESSONS_LEARNED.md) — Критически важно для OAuth!