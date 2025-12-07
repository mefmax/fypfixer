-- FYPFixer – categories table v0

CREATE TABLE IF NOT EXISTS categories (
    id              BIGSERIAL PRIMARY KEY,
    code            VARCHAR(32) UNIQUE NOT NULL, -- 'it', 'fitness', 'fashion', 'default'
    name_en         TEXT NOT NULL,
    name_ru         TEXT,
    name_es         TEXT,
    is_premium      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
