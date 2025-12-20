# 🔧 FYPFixer — ПЛАН ЗАВЕРШЕНИЯ BACKEND

**Для:** Claude Code (Backend Sonnet) в VS Code  
**Статус:** Продолжение после основной миграции  
**Время:** ~1 час

---

## 📋 ЧТО ОСТАЛОСЬ СДЕЛАТЬ

Backend Sonnet создал структуру, но не выполнил:
1. ❌ Создание `.env` файла
2. ❌ Seed данные для категорий и демо-плана
3. ❌ Инициализация Flask-Migrate
4. ❌ Обновление корневого `docker-compose.yml`
5. ❌ Тестирование запуска

---

## Фаза B9: Завершение настройки (60 мин)

### 9.1 Создать `backend/.env`

```bash
cd backend
cp .env.example .env
```

Отредактировать `.env`:
```bash
FLASK_ENV=development
SECRET_KEY=fypfixer-dev-secret-key-change-in-production
DATABASE_URL=postgresql://fypfixer:fypfixer@db:5432/fypfixer
REDIS_URL=redis://redis:6379/0
JWT_SECRET_KEY=jwt-super-secret-key-change-in-production
APIFY_API_KEY=
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 9.2 Создать seed данные `backend/seeds/seed_data.py`

```python
"""
Seed data for FYPFixer database.
Run: python -m seeds.seed_data
"""
from datetime import date
from app import create_app, db
from app.models import Category, Plan, PlanStep, StepItem

def seed_categories():
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


def seed_demo_plan():
    """Seed demo plan for personal_growth category"""
    category = Category.query.filter_by(code='personal_growth').first()
    if not category:
        print("  ✗ Category 'personal_growth' not found!")
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
        items = step_data.pop('items')
        step = PlanStep(plan_id=plan.id, **step_data)
        db.session.add(step)
        db.session.flush()
        
        for item_data in items:
            item = StepItem(plan_step_id=step.id, **item_data)
            db.session.add(item)
        
        print(f"  ✓ Added step {step_data['step_order']}: {step_data['action_type']}")
    
    db.session.commit()
    print(f"  ✓ Created demo plan (id={plan.id})")
    return plan


def run_seeds():
    """Run all seed functions"""
    app = create_app('development')
    
    with app.app_context():
        print("\n🌱 Seeding database...")
        
        print("\n📁 Categories:")
        seed_categories()
        
        print("\n📋 Demo Plan:")
        seed_demo_plan()
        
        print("\n✅ Seeding complete!\n")


if __name__ == '__main__':
    run_seeds()
```

### 9.3 Создать папку seeds и __init__.py

```bash
mkdir -p backend/seeds
touch backend/seeds/__init__.py
```

### 9.4 Обновить корневой `docker-compose.yml`

**Файл: `docker-compose.yml` (в корне репозитория)**

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

### 9.5 Создать скрипт инициализации БД `backend/init_db.py`

```python
"""
Initialize database: create tables and seed data.
Run: python init_db.py
"""
from app import create_app, db

def init_database():
    app = create_app('development')
    
    with app.app_context():
        print("🗄️  Creating database tables...")
        db.create_all()
        print("✅ Tables created!\n")
        
        # Run seeds
        from seeds.seed_data import run_seeds
        run_seeds()

if __name__ == '__main__':
    init_database()
```

### 9.6 Добавить команду seed в `backend/main.py`

Обновить `backend/main.py`:

```python
import os
import sys
from app import create_app, db

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

@app.cli.command('init-db')
def init_db_command():
    """Create tables and seed data."""
    db.create_all()
    print("✅ Tables created!")
    
    from seeds.seed_data import run_seeds
    run_seeds()

@app.cli.command('seed')
def seed_command():
    """Seed the database with demo data."""
    from seeds.seed_data import run_seeds
    run_seeds()

if __name__ == '__main__':
    # Check for init-db argument
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        with app.app_context():
            db.create_all()
            print("✅ Tables created!")
            from seeds.seed_data import run_seeds
            run_seeds()
    else:
        app.run(host='0.0.0.0', port=8000, debug=True)
```

---

## Фаза B10: Тестирование (20 мин)

### 10.1 Запуск через Docker Compose

```bash
# В корне репозитория
cd fypfixer

# Поднять только БД и Redis сначала
docker compose up -d db redis

# Подождать 5 секунд
sleep 5

# Проверить что БД работает
docker compose exec db psql -U fypfixer -c "SELECT 1"
```

### 10.2 Инициализация БД

```bash
# Запустить backend и инициализировать БД
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
  ...

📋 Demo Plan:
  ✓ Added step 1: watch
  ✓ Added step 2: like
  ✓ Added step 3: follow
  ✓ Created demo plan (id=1)

✅ Seeding complete!
```

### 10.3 Запуск backend

```bash
# Поднять backend
docker compose up -d backend

# Проверить логи
docker compose logs -f backend
```

### 10.4 Тест эндпоинтов

```bash
# Health check
curl http://localhost:8000/api/health
# Ожидаемо: {"status": "healthy", "services": {"database": "connected"}, ...}

# Categories
curl http://localhost:8000/api/categories
# Ожидаемо: {"success": true, "data": {"categories": [...]}}

# Daily plan
curl "http://localhost:8000/api/plan?category=personal_growth&lang=en"
# Ожидаемо: {"success": true, "data": {"id": 1, "title": "Daily Personal Growth Plan", "steps": [...]}}
```

---

## ✅ ЧЕК-ЛИСТ ЗАВЕРШЕНИЯ

### Фаза B9: Настройка
- [ ] Создать `backend/.env` из `.env.example`
- [ ] Создать `backend/seeds/__init__.py`
- [ ] Создать `backend/seeds/seed_data.py`
- [ ] Создать `backend/init_db.py`
- [ ] Обновить `backend/main.py` с CLI командами
- [ ] Обновить корневой `docker-compose.yml`

### Фаза B10: Тестирование
- [ ] `docker compose up -d db redis` — БД и Redis запущены
- [ ] `docker compose run --rm backend python init_db.py` — таблицы созданы, seed данные загружены
- [ ] `docker compose up -d backend` — backend запущен
- [ ] `curl http://localhost:8000/api/health` — возвращает `{"status": "healthy"}`
- [ ] `curl http://localhost:8000/api/categories` — возвращает 8 категорий
- [ ] `curl http://localhost:8000/api/plan?category=personal_growth` — возвращает план с видео

---

## ⚠️ ВАЖНО

1. **Если БД не создаётся через `db.create_all()`**, проверить что все модели импортируются в `app/__init__.py`
2. **Если seed падает**, проверить что Category уже существует перед созданием Plan
3. **JWT_SECRET_KEY** должен быть разным для dev и production
4. **CORS_ORIGINS** должен включать адрес frontend (localhost:5173)

---

## 🔗 После завершения

Когда backend полностью работает:
1. Сообщи мне результат
2. Я дам команду Frontend Sonnet начать работу
3. Frontend будет использовать эти эндпоинты

---

**Время на завершение: ~1 час**
