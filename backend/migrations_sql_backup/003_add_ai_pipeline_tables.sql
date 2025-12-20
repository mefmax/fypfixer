-- Migration: add_ai_pipeline_tables
-- Date: 2025-12-18
-- Description: Create 4 new tables for AI pipeline

-- Table 1: user_behavior_stats
-- Tracks engagement, streaks, preferences, gamification
CREATE TABLE IF NOT EXISTS user_behavior_stats (
    user_id BIGINT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,

    -- Engagement metrics
    total_actions_completed INTEGER DEFAULT 0,
    total_days_active INTEGER DEFAULT 0,
    avg_completion_rate NUMERIC(5, 4) DEFAULT 0,

    -- Streaks (Psychology Stage 1 - habit building)
    current_streak_days INTEGER DEFAULT 0,
    max_streak_days INTEGER DEFAULT 0,
    last_completed_date DATE,

    -- Adaptive Difficulty (Flow State)
    current_difficulty INTEGER DEFAULT 5 CHECK (current_difficulty >= 3 AND current_difficulty <= 8),

    -- Content Preferences (learned from behavior)
    preferred_creators JSONB DEFAULT '{}',
    preferred_topics JSONB DEFAULT '{}',

    -- Gamification
    current_level VARCHAR(20) DEFAULT 'Beginner',
    total_xp INTEGER DEFAULT 0,
    achievements JSONB DEFAULT '[]',

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_behavior_streak ON user_behavior_stats(current_streak_days);


-- Table 2: tiktok_videos
-- Cache for scraped TikTok content (24h TTL)
CREATE TABLE IF NOT EXISTS tiktok_videos (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(50) NOT NULL UNIQUE,
    url TEXT NOT NULL,

    -- Creator info
    creator_username VARCHAR(100) NOT NULL,
    creator_display_name VARCHAR(200),
    creator_follower_count INTEGER,
    creator_verified BOOLEAN DEFAULT false,

    -- Video metadata
    description TEXT,
    hashtags JSONB DEFAULT '[]',
    duration_sec INTEGER,
    upload_date TIMESTAMPTZ,
    thumbnail_url TEXT,

    -- Engagement metrics
    views INTEGER,
    likes INTEGER,
    comments INTEGER,
    shares INTEGER,
    engagement_rate NUMERIC(7, 6),

    -- AI Analysis results
    topics JSONB DEFAULT '[]',
    quality_score NUMERIC(5, 4),
    category_scores JSONB DEFAULT '{}',

    -- Cache management
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    cache_expires_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '24 hours'
);

CREATE INDEX IF NOT EXISTS idx_videos_quality ON tiktok_videos(quality_score);
CREATE INDEX IF NOT EXISTS idx_videos_creator ON tiktok_videos(creator_username);
CREATE INDEX IF NOT EXISTS idx_videos_cache_expires ON tiktok_videos(cache_expires_at);


-- Table 3: user_recommendations
-- Logs each AI pipeline execution for analytics
CREATE TABLE IF NOT EXISTS user_recommendations (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    plan_date DATE NOT NULL,
    category_code VARCHAR(50) NOT NULL,

    -- AI Pipeline Data
    search_criteria JSONB NOT NULL,
    scraper_results JSONB,
    selected_actions JSONB NOT NULL,

    -- Pipeline Metadata
    ai_provider VARCHAR(50) NOT NULL,
    generation_time_ms INTEGER,
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    source VARCHAR(20) DEFAULT 'ai',

    -- Quality Metrics
    avg_quality_score NUMERIC(5, 4),
    diversity_score NUMERIC(5, 4),

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_recommendations_user_date ON user_recommendations(user_id, plan_date);


-- Table 4: message_templates
-- Psychology-based motivation messages
CREATE TABLE IF NOT EXISTS message_templates (
    id SERIAL PRIMARY KEY,
    template_key VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,

    -- Localized messages
    message_en TEXT NOT NULL,
    message_ru TEXT,
    message_es TEXT,

    -- Display conditions
    conditions JSONB DEFAULT '{}',

    -- Presentation
    emoji VARCHAR(20),
    tone VARCHAR(30),

    priority INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_templates_category ON message_templates(category, is_active);


-- Add columns to existing actions table
ALTER TABLE actions ADD COLUMN IF NOT EXISTS source VARCHAR(20) DEFAULT 'seed';
ALTER TABLE actions ADD COLUMN IF NOT EXISTS reason TEXT;
ALTER TABLE actions ADD COLUMN IF NOT EXISTS quality_score NUMERIC(5, 4);
