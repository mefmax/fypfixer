-- Seed data for FYPFixer MVP (personal_growth category)

-- 1. Создаём пользователя (если ещё нет)
INSERT INTO users (client_id, language, created_at, updated_at)
VALUES ('demo-user-001', 'en', NOW(), NOW())
ON CONFLICT (client_id) DO NOTHING;

-- 2. Создаём категорию personal_growth (если нет)
INSERT INTO categories (code, name_en, name_ru, name_es, is_premium, created_at)
VALUES ('personal_growth', 'Personal Growth', 'Личное развитие', 'Crecimiento Personal', false, NOW())
ON CONFLICT (code) DO NOTHING;

-- 3. Создаём план для demo user
INSERT INTO plans (user_id, category_id, plan_date, language, is_template, title, created_at, updated_at)
SELECT u.id, c.id, CURRENT_DATE, 'en', false, 'Personal Growth Plan', NOW(), NOW()
FROM users u, categories c
WHERE u.client_id = 'demo-user-001' AND c.code = 'personal_growth'
ON CONFLICT (user_id, plan_date, language) DO NOTHING;

-- 4. Добавляем шаги плана
INSERT INTO plan_steps (plan_id, step_order, action_type, text_en, text_ru, text_es, created_at)
SELECT p.id, 1, 'watch', 'Identify Your Goal', 'Определи цель', 'Identifica tu objetivo', NOW()
FROM plans p
WHERE p.is_template = false AND p.title = 'Personal Growth Plan'
LIMIT 1;

-- 5. Добавляем видео для первого шага
INSERT INTO step_items (plan_step_id, video_id, creator_username, title, thumbnail_url, video_url, engagement_score, reason_text, created_at)
SELECT ps.id, '7288965558730713349', 'tiktok', '5 Habits to Change Your Life', 'https://via.placeholder.com/300x200?text=Growth', 'https://www.tiktok.com/@tiktok/video/7288965558730713349', 0.85, 'High engagement, great for beginners', NOW()
FROM plan_steps ps
WHERE ps.step_order = 1
LIMIT 1;

INSERT INTO step_items (plan_step_id, video_id, creator_username, title, thumbnail_url, video_url, engagement_score, reason_text, created_at)
SELECT ps.id, '7300442445678901234', 'tiktok', 'Morning Routine for Success', 'https://via.placeholder.com/300x200?text=Routine', 'https://www.tiktok.com/@tiktok/video/7300442445678901234', 0.78, 'Practical daily habits', NOW()
FROM plan_steps ps
WHERE ps.step_order = 1
LIMIT 1;
