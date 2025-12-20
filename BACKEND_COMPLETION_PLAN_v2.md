# 🔧 FYPFixer — ПЛАН ЗАВЕРШЕНИЯ BACKEND (ИСПРАВЛЕННЫЙ)

**Для:** Claude Code (Backend Sonnet) в VS Code  
**Статус:** Продолжение после основной миграции  
**Время:** ~1 час

---

## 📋 ЧТО ОСТАЛОСЬ СДЕЛАТЬ

Backend Sonnet создал структуру, но не выполнил:
1. ❌ Создание `.env` файла
2. ❌ Seed данные для категорий и демо-плана
3. ❌ Скрипт инициализации БД
4. ❌ Обновление корневого `docker-compose.yml`
5. ❌ Тестирование запуска

---

## Фаза B9: Завершение настройки (60 мин)

### 9.1 Создать `backend/.env`

```bash
cd backend
```

Создать файл `backend/.env` с содержимым:

```env
FLASK_ENV=development
SECRET_KEY=fypfixer-dev-secret-key-change-in-production
DATABASE_URL=postgresql://fypfixer:fypfixer@db:5432/fypfixer
REDIS_URL=redis://redis:6379/0
JWT_SECRET_KEY=jwt-super-secret-key-change-in-production
APIFY_API_KEY=
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

### 9.2 Создать папку seeds

```bash
mkdir -p backend/seeds
```

---

### 9.3 Создать `backend/seeds/__init__.py`

```python
# Seeds package
```

---

### 9.4 Создать `backend/seeds/seed_data.py`

```python
"""
Seed data for FYPFixer database.
Run from backend folder: python -m seeds.seed_data
Or via init_db.py: python init_db.py
"""
from datetime import date


def seed_categories(db, Category):
    """Seed 8 categories (5 free + 3 premium)"""
    categories = [
        # Free categories
        {'code': 'personal_growth', 'name_en': 'Personal Growth', 'name_ru': 'Личное развитие', 'name_es': 'Crecimiento Personal', 'icon': '🎯', 'display_order': 1, 'is_premium': False},
        {'code': 'entertainment', 'name_en': 'Entertainment', 'name_ru': 'Развлечение', 'name_es': 'Entretenimiento', 'icon': '🎬', 'display_order': 2, 'is_premium': False},
        {'code': 'wellness', 'name_en': 'Wellness & Lifestyle', 'name_ru': 'Здоровье и Образ жизни', 'name_es': 'Bienestar y Estilo de vida', 'icon': '🧘', 'display_order': 3, 'is_premium': False},
        {'code': 'creative', 'name_en': 'Creative & Arts', 'name_ru': 'Творчество и Искусство', 'name_es': 'Creatividad y Arte', 'icon': '🎨', 'display_order': 4, 'is_premium': False},
        {'code': 'learning', 'name_en': 'Learning & Education', 'name_ru': 'Обучение и Образование', 'name_es': 'Aprendizaje y Educación', 'icon': '📚', 'display_order': 5, 'is_premium': False},
        # Premium categories
        {'code': 'science_tech', 'name_en': 'Science & Technology', 'name_ru': 'Наука и Технология', 'name_es': 'Ciencia y Tecnología', 'icon': '🔬', 'display_order': 6, 'is_premium': True},
        {'code': 'food', 'name_en': 'Food & Cooking', 'name_ru': 'Еда и Кулинария', 'name_es': 'Comida y Cocina', 'icon': '🍳', 'display_order': 7, 'is_premium': True},
        {'code': 'travel', 'name_en': 'Travel & Adventure', 'name_ru': 'Путешествия и Приключения', 'name_es': 'Viajes y Aventura', 'icon': '✈️', 'display_order': 8, 'is_premium': True},
    ]
    
    for cat_data in categories:
        existing = Category.query.filter_by(code=cat_data['code']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
            print(f"  ✓ Added category: {cat_data['code']}")
        else:
            print(f"  - Category exists: {cat_data['code']}")
    
    db.session.commit()
    return Category.query.all()


def seed_demo_plan(db, Category, Plan, PlanStep, StepItem):
    """Seed demo plan for personal_growth category"""
    category = Category.query.filter_by(code='personal_growth').first()
    if not category:
        print("  ✗ Category 'personal_growth' not found! Run seed_categories first.")
        return None
    
    # Check if demo plan exists
    existing = Plan.query.filter_by(
        category_id=category.id,
        is_template=True,
        language='en'
    ).first()
    
    if existing:
        print(f"  - Demo plan already exists (id={existing.id})")
        return existing
    
    # Create demo plan
    plan = Plan(
        category_id=category.id,
        plan_date=date.today(),
        language='en',
        is_template=True,
        title='Daily Personal Growth Plan',
        is_active=True
    )
    db.session.add(plan)
    db.session.flush()  # Get plan.id
    
    # Create steps with videos
    steps_data = [
        {
            'step_order': 1,
            'action_type': 'watch',
            'text_en': 'Watch these videos about personal growth',
            'text_ru': 'Посмотри эти видео о личном развитии',
            'text_es': 'Mira estos videos sobre crecimiento personal',
            'duration_minutes': 5,
            'items': [
                {
                    'video_id': '7288965558730713349',
                    'creator_username': '@growthcoach',
                    'title': '5 Habits to Change Your Life',
                    'thumbnail_url': 'https://p16-sign.tiktokcdn.com/obj/tos-maliva-p-0068/thumb1.jpg',
                    'video_url': 'https://www.tiktok.com/@growthcoach/video/7288965558730713349',
                    'engagement_score': 0.85,
                    'reason_text': 'High engagement, great for beginners'
                },
                {
                    'video_id': '7300442445678901234',
                    'creator_username': '@mindsetmastery',
                    'title': 'Morning Routine of Successful People',
                    'thumbnail_url': 'https://p16-sign.tiktokcdn.com/obj/tos-maliva-p-0068/thumb2.jpg',
                    'video_url': 'https://www.tiktok.com/@mindsetmastery/video/7300442445678901234',
                    'engagement_score': 0.78,
                    'reason_text': 'Practical tips, highly rated'
                },
                {
                    'video_id': '7295123456789012345',
                    'creator_username': '@lifeoptimizer',
                    'title': 'How to Set Goals That Stick',
                    'thumbnail_url': 'https://p16-sign.tiktokcdn.com/obj/tos-maliva-p-0068/thumb3.jpg',
                    'video_url': 'https://www.tiktok.com/@lifeoptimizer/video/7295123456789012345',
                    'engagement_score': 0.72,
                    'reason_text': 'Science-backed strategies'
                },
            ]
        },
        {
            'step_order': 2,
            'action_type': 'like',
            'text_en': 'Like your favorite video from the list',
            'text_ru': 'Лайкни своё любимое видео из списка',
            'text_es': 'Dale me gusta a tu video favorito',
            'duration_minutes': 1,
            'items': []
        },
        {
            'step_order': 3,
            'action_type': 'follow',
            'text_en': 'Follow 2 creators who inspire you',
            'text_ru': 'Подпишись на 2 авторов, которые тебя вдохновляют',
            'text_es': 'Sigue a 2 creadores que te inspiren',
            'duration_minutes': 2,
            'items': []
        },
    ]
    
    for step_data in steps_data:
        # Сохраняем step_order до pop
        step_order = step_data['step_order']
        action_type = step_data['action_type']
        items = step_data.pop('items')
        
        step = PlanStep(plan_id=plan.id, **step_data)
        db.session.add(step)
        db.session.flush()
        
        for item_data in items:
            item = StepItem(plan_step_id=step.id, **item_data)
            db.session.add(item)
        
        print(f"  ✓ Added step {step_order}: {action_type} ({len(items)} videos)")
    
    db.session.commit()
    print(f"  ✓ Created demo plan (id={plan.id})")
    return plan


def run_seeds(app, db):
    """Run all seed functions within app context"""
    from app.models import Category, Plan, PlanStep, StepItem
    
    with app.app_context():
        print("\n🌱 Seeding database...")
        
        print("\n📁 Categories:")
        seed_categories(db, Category)
        
        print("\n📋 Demo Plan:")
        seed_demo_plan(db, Category, Plan, PlanStep, StepItem)
        
        print("\n✅ Seeding complete!\n")


if __name__ == '__main__':
    # Standalone execution
    from app import create_app, db
    app = create_app('development')
    run_seeds(app, db)
```

---

### 9.5 Создать `backend/init_db.py`

```python
"""
Initialize database: create tables and seed data.
Run from backend folder: python init_db.py
"""
import os
import sys

# Add backend to path if running from backend folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db


def init_database():
    """Initialize database with tables and seed data"""
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("🗄️  Creating database tables...")
        db.create_all()
        print("✅ Tables created!\n")
    
    # Run seeds (has its own app_context)
    from seeds.seed_data import run_seeds
    run_seeds(app, db)
    
    print("🎉 Database initialization complete!")


if __name__ == '__main__':
    init_database()
```

---

### 9.6 Обновить `backend/main.py`

**Заменить полностью файл `backend/main.py`:**

```python
"""
FYPFixer Backend Entry Point
Run: python main.py
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)


# CLI Commands
@app.cli.command('init-db')
def init_db_command():
    """Create tables and seed data."""
    db.create_all()
    print("✅ Tables created!")
    
    from seeds.seed_data import run_seeds
    run_seeds(app, db)


@app.cli.command('seed')
def seed_command():
    """Seed the database with demo data."""
    from seeds.seed_data import run_seeds
    run_seeds(app, db)


@app.cli.command('drop-db')
def drop_db_command():
    """Drop all tables (DANGEROUS!)."""
    confirm = input("Are you sure you want to drop all tables? (yes/no): ")
    if confirm.lower() == 'yes':
        db.drop_all()
        print("🗑️  All tables dropped!")
    else:
        print("Cancelled.")


if __name__ == '__main__':
    # Handle init-db argument for Docker
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        with app.app_context():
            db.create_all()
            print("✅ Tables created!")
        from seeds.seed_data import run_seeds
        run_seeds(app, db)
    else:
        # Run development server
        debug = config_name == 'development'
        app.run(host='0.0.0.0', port=8000, debug=debug)
```

---

### 9.7 Обновить корневой `docker-compose.yml`

**Файл: `docker-compose.yml` (в КОРНЕ репозитория, НЕ в backend/)**

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: fypfixer-backend
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://fypfixer:fypfixer@db:5432/fypfixer
      - REDIS_URL=redis://redis:6379/0
      - JWT_SECRET_KEY=dev-jwt-secret-change-in-production
      - SECRET_KEY=dev-secret-key-change-in-production
      - CORS_ORIGINS=http://localhost:5173,http://localhost:3000
    volumes:
      - ./backend:/app
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    command: python main.py

  frontend:
    build: ./frontend
    container_name: fypfixer-frontend
    ports:
      - "5173:80"
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    container_name: fypfixer-db
    environment:
      POSTGRES_USER: fypfixer
      POSTGRES_PASSWORD: fypfixer
      POSTGRES_DB: fypfixer
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U fypfixer"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: fypfixer-redis
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data
    restart: unless-stopped

volumes:
  pgdata:
  redisdata:
```

---

## Фаза B10: Тестирование (20 мин)

### 10.1 Запуск БД и Redis

```bash
# В корне репозитория (где docker-compose.yml)
cd /path/to/fypfixer

# Остановить старые контейнеры если есть
docker compose down

# Поднять БД и Redis
docker compose up -d db redis

# Подождать 10 секунд для старта PostgreSQL
sleep 10

# Проверить что БД работает
docker compose exec db psql -U fypfixer -c "SELECT 1"
```

Ожидаемый вывод:
```
 ?column?
----------
        1
(1 row)
```

---

### 10.2 Инициализация БД и Seed данных

```bash
# Запустить init_db.py через Docker
docker compose run --rm backend python init_db.py
```

Ожидаемый вывод:
```
🗄️  Creating database tables...
✅ Tables created!

🌱 Seeding database...

📁 Categories:
  ✓ Added category: personal_growth
  ✓ Added category: entertainment
  ✓ Added category: wellness
  ✓ Added category: creative
  ✓ Added category: learning
  ✓ Added category: science_tech
  ✓ Added category: food
  ✓ Added category: travel

📋 Demo Plan:
  ✓ Added step 1: watch (3 videos)
  ✓ Added step 2: like (0 videos)
  ✓ Added step 3: follow (0 videos)
  ✓ Created demo plan (id=1)

✅ Seeding complete!

🎉 Database initialization complete!
```

---

### 10.3 Запуск Backend

```bash
# Поднять backend
docker compose up -d backend

# Проверить статус
docker compose ps

# Проверить логи (Ctrl+C для выхода)
docker compose logs -f backend
```

Ожидаемые логи:
```
 * Running on http://0.0.0.0:8000
 * Restarting with stat
 * Debugger is active!
```

---

### 10.4 Тест эндпоинтов

```bash
# 1. Health check
curl http://localhost:8000/api/health
```
Ожидаемо:
```json
{"status": "healthy", "timestamp": "...", "services": {"database": "connected"}}
```

```bash
# 2. Categories
curl http://localhost:8000/api/categories
```
Ожидаемо:
```json
{"success": true, "data": {"categories": [{"id": 1, "code": "personal_growth", "name": "Personal Growth", ...}, ...]}}
```

```bash
# 3. Daily plan
curl "http://localhost:8000/api/plan?category=personal_growth&lang=en"
```
Ожидаемо:
```json
{"success": true, "data": {"id": 1, "title": "Daily Personal Growth Plan", "steps": [{"id": 1, "step_order": 1, "action_type": "watch", "items": [...]}]}}
```

---

## ✅ ЧЕК-ЛИСТ ЗАВЕРШЕНИЯ

### Фаза B9: Настройка
- [ ] Создать `backend/.env` (скопировать содержимое выше)
- [ ] Создать папку `backend/seeds/`
- [ ] Создать `backend/seeds/__init__.py`
- [ ] Создать `backend/seeds/seed_data.py`
- [ ] Создать `backend/init_db.py`
- [ ] Обновить `backend/main.py`
- [ ] Обновить корневой `docker-compose.yml`

### Фаза B10: Тестирование
- [ ] `docker compose down` — остановить старые контейнеры
- [ ] `docker compose up -d db redis` — БД и Redis запущены
- [ ] `docker compose exec db psql -U fypfixer -c "SELECT 1"` — БД отвечает
- [ ] `docker compose run --rm backend python init_db.py` — таблицы созданы, seed загружен
- [ ] `docker compose up -d backend` — backend запущен
- [ ] `curl http://localhost:8000/api/health` — возвращает `{"status": "healthy"}`
- [ ] `curl http://localhost:8000/api/categories` — возвращает 8 категорий
- [ ] `curl "http://localhost:8000/api/plan?category=personal_growth&lang=en"` — возвращает план с 3 видео

---

## 🔧 TROUBLESHOOTING

### Ошибка: "No module named 'app'"
```bash
# Убедиться что WORKDIR в Dockerfile = /app
# И что volumes монтирует ./backend:/app
docker compose exec backend pwd  # должно быть /app
docker compose exec backend ls   # должны быть app/, main.py, etc.
```

### Ошибка: "connection refused" к БД
```bash
# Проверить что db контейнер работает
docker compose ps db
# Проверить логи
docker compose logs db
# Подождать и попробовать снова
sleep 10
docker compose run --rm backend python init_db.py
```

### Ошибка: "relation does not exist"
```bash
# Таблицы не созданы, запустить init заново
docker compose run --rm backend python init_db.py
```

### Сбросить всё и начать заново
```bash
docker compose down -v  # -v удалит volumes (данные БД)
docker compose up -d db redis
sleep 10
docker compose run --rm backend python init_db.py
docker compose up -d backend
```

---

## ⚠️ ВАЖНО

1. **Файлы создавать В ПАПКЕ `backend/`**, а `docker-compose.yml` в корне репозитория
2. **Порядок важен**: сначала db и redis, потом init_db.py, потом backend
3. **Если seed уже был** — он НЕ создаст дубликаты (проверяет existing)
4. **JWT_SECRET_KEY** должен быть надёжным в production

---

## 🔗 После завершения

Когда все curl команды работают правильно:
1. Сообщи мне результат тестов
2. Можно запускать Frontend Sonnet
3. Frontend будет использовать эти эндпоинты

---

**Время на завершение: ~1 час**
