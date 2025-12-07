-- FYPFixer – seed categories v0

INSERT INTO categories (code, name_en, name_ru, name_es, is_premium, created_at)
VALUES
  ('personal_growth', 'Personal Growth', 'Личное развитие', 'Crecimiento Personal', FALSE, NOW()),
  ('entertainment', 'Entertainment', 'Развлечение', 'Entretenimiento', FALSE, NOW()),
  ('wellness', 'Wellness & Lifestyle', 'Здоровье и Образ жизни', 'Bienestar y Estilo de vida', FALSE, NOW()),
  ('creative', 'Creative & Arts', 'Творчество и Искусство', 'Creatividad y Arte', FALSE, NOW()),
  ('learning', 'Learning & Education', 'Обучение и Образование', 'Aprendizaje y Educación', FALSE, NOW()),
  ('science_tech', 'Science & Technology', 'Наука и Технология', 'Ciencia y Tecnología', TRUE, NOW()),
  ('food', 'Food & Cooking', 'Еда и Кулинария', 'Comida y Cocina', TRUE, NOW()),
  ('travel', 'Travel & Adventure', 'Путешествия и Приключения', 'Viajes y Aventura', TRUE, NOW());
