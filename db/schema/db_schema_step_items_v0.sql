-- FYPFixer – step_items table v0

CREATE TABLE IF NOT EXISTS step_items (
    id               BIGSERIAL PRIMARY KEY,
    plan_step_id     BIGINT NOT NULL REFERENCES plan_steps(id) ON DELETE CASCADE,
    video_id         VARCHAR(256),        -- TikTok video ID (если есть)
    creator_username VARCHAR(256),
    title            TEXT,
    thumbnail_url    TEXT,
    video_url        TEXT NOT NULL,
    engagement_score DOUBLE PRECISION,    -- likes/views ratio или иной скор
    reason_text      TEXT,                -- почему именно это видео
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_step_items_plan_step
    ON step_items(plan_step_id);
