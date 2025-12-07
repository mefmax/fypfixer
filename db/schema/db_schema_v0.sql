-- FYPFixer – PostgreSQL schema v0

CREATE TABLE users (
    id              BIGSERIAL PRIMARY KEY,
    client_id       VARCHAR(64) UNIQUE NOT NULL, -- uuid-like from cookie/localStorage
    language        VARCHAR(5) NOT NULL DEFAULT 'en', -- en, ru, es
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE categories (
    id              BIGSERIAL PRIMARY KEY,
    code            VARCHAR(32) UNIQUE NOT NULL, -- 'it', 'fitness', 'fashion', 'default'
    name_en         TEXT NOT NULL,
    name_ru         TEXT,
    name_es         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE plans (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT REFERENCES users(id) ON DELETE CASCADE,
    category_id     BIGINT REFERENCES categories(id),
    plan_date       DATE NOT NULL,
    language        VARCHAR(5) NOT NULL DEFAULT 'en',
    is_template     BOOLEAN NOT NULL DEFAULT FALSE, -- true for generic templates
    title           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, plan_date, language)
);

CREATE TABLE plan_steps (
    id              BIGSERIAL PRIMARY KEY,
    plan_id         BIGINT NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    step_order      INT NOT NULL, -- 1..5
    action_type     VARCHAR(32),  -- 'watch', 'like', 'block', 'search', etc.
    text_en         TEXT NOT NULL,
    text_ru         TEXT,
    text_es         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_client_id ON users(client_id);
CREATE INDEX idx_plans_user_date ON plans(user_id, plan_date);
CREATE INDEX idx_plan_steps_plan_order ON plan_steps(plan_id, step_order);
