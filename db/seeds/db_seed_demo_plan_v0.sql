-- FYPFixer – demo plan with step_items

-- 1. Создаём демо-пользователя (если ещё нет)
INSERT INTO users (client_id, language, created_at, updated_at)
VALUES ('demo-client', 'en', NOW(), NOW())
ON CONFLICT (client_id) DO NOTHING;

-- 2. Берём любую бесплатную категорию (personal_growth)
WITH cat AS (
    SELECT id FROM categories WHERE code = 'personal_growth' LIMIT 1
),
u AS (
    SELECT id FROM users WHERE client_id = 'demo-client' LIMIT 1
)
INSERT INTO plans (user_id, category_id, plan_date, language, is_template, title, created_at, updated_at)
SELECT u.id, cat.id, CURRENT_DATE, 'en', FALSE, 'Demo Personal Growth Plan', NOW(), NOW()
FROM u, cat
ON CONFLICT DO NOTHING;

-- 3. Находим этот план
WITH p AS (
    SELECT id FROM plans
    WHERE title = 'Demo Personal Growth Plan'
      AND plan_date = CURRENT_DATE
    LIMIT 1
)
-- 4. Создаём один шаг
INSERT INTO plan_steps (plan_id, step_order, action_type, text_en, created_at)
SELECT p.id, 1, 'watch', 'Watch these 3 videos about personal growth', NOW()
FROM p;

-- 5. Находим созданный шаг
WITH s AS (
    SELECT id FROM plan_steps
    WHERE action_type = 'watch'
      AND text_en = 'Watch these 3 videos about personal growth'
    ORDER BY id DESC
    LIMIT 1
)
-- 6. Добавляем три mock-видео
INSERT INTO step_items (plan_step_id, video_id, creator_username, title, thumbnail_url, video_url, engagement_score, reason_text, created_at)
SELECT s.id,
       'demo_vid_1',
       '@growthcoach',
       '5 Habits to Change Your Life',
       'https://example.com/thumb1.jpg',
       'https://www.tiktok.com/@growthcoach/video/0000000000000000001',
       0.42,
       'High engagement, great for beginners',
       NOW()
FROM s
UNION ALL
SELECT s.id,
       'demo_vid_2',
       '@mindsetdaily',
       'Morning Routine That Actually Works',
       'https://example.com/thumb2.jpg',
       'https://www.tiktok.com/@mindsetdaily/video/0000000000000000002',
       0.38,
       'Trending in Personal Growth niche',
       NOW()
FROM s
UNION ALL
SELECT s.id,
       'demo_vid_3',
       '@focus_hacks',
       'How to Stay Focused for 2 Hours',
       'https://example.com/thumb3.jpg',
       'https://www.tiktok.com/@focus_hacks/video/0000000000000000003',
       0.35,
       'Good watch time and saves',
       NOW()
FROM s;
