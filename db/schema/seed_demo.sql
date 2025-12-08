-- Очистить старые данные (если есть)
TRUNCATE TABLE step_items, plan_steps, plans, categories RESTART IDENTITY CASCADE;

-- Вставить 8 категорий
INSERT INTO categories (code, name_en, name_ru, name_es, is_premium, created_at) VALUES
('personal_growth', 'Personal Growth', 'Личное развитие', 'Crecimiento Personal', false, NOW()),
('entertainment', 'Entertainment', 'Развлечение', 'Entretenimiento', false, NOW()),
('wellness', 'Wellness & Lifestyle', 'Здоровье и Образ жизни', 'Bienestar y Estilo de vida', false, NOW()),
('creative', 'Creative & Arts', 'Творчество и Искусство', 'Creatividad y Arte', false, NOW()),
('learning', 'Learning & Education', 'Обучение и Образование', 'Aprendizaje y Educación', false, NOW()),
('science_tech', 'Science & Technology', 'Наука и Технология', 'Ciencia y Tecnología', true, NOW()),
('food', 'Food & Cooking', 'Еда и Кулинария', 'Comida y Cocina', true, NOW()),
('travel', 'Travel & Adventure', 'Путешествия и Приключения', 'Viajes y Aventura', true, NOW());

-- Вставить демо-план для personal_growth
INSERT INTO plans (user_id, category_id, plan_date, language, is_template, title, created_at, updated_at) VALUES
(NULL, 1, '2025-12-08', 'en', true, 'Demo Personal Growth Plan', NOW(), NOW());

-- Вставить 3 шага для плана
INSERT INTO plan_steps (plan_id, step_order, action_type, text_en, text_ru, text_es, created_at) VALUES
(1, 1, 'watch', 'Watch these 3 videos about personal growth', 'Посмотри эти 3 видео о личном развитии', 'Mira estos 3 videos sobre crecimiento personal', NOW()),
(1, 2, 'like', 'Like your favorite video from the list', 'Лайкни любимое видео из списка', 'Dale me gusta a tu video favorito', NOW()),
(1, 3, 'follow', 'Follow 2 creators who inspire you', 'Подпишись на 2 авторов', 'Sigue a 2 creadores', NOW());

-- Вставить 3 видео для первого шага
INSERT INTO step_items (plan_step_id, video_id, creator_username, title, thumbnail_url, video_url, engagement_score, reason_text, created_at) VALUES
(1, 'demo_vid_1', '@growthcoach', '5 Habits to Change Your Life', 'https://p16-sign-sg.tiktokcdn.com/thumb1.jpg', 'https://www.tiktok.com/@growthcoach/video/7000000000000000001', 95.5, 'High engagement, great for beginners', NOW()),
(1, 'demo_vid_2', '@mindsetmastery', 'Morning Routine of Successful People', 'https://p16-sign-sg.tiktokcdn.com/thumb2.jpg', 'https://www.tiktok.com/@mindsetmastery/video/7000000000000000002', 92.3, 'Practical tips, highly rated', NOW()),
(1, 'demo_vid_3', '@lifeoptimizer', 'How to Set Goals That Stick', 'https://p16-sign-sg.tiktokcdn.com/thumb3.jpg', 'https://www.tiktok.com/@lifeoptimizer/video/7000000000000000003', 89.1, 'Science-backed strategies', NOW());
