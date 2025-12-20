-- Migration: Add index for user_progress performance
-- Date: 2025-12-17
-- Status: APPLIED (indexes created during schema setup)

-- Index for faster lookups by action_id
CREATE INDEX IF NOT EXISTS idx_user_progress_action
ON user_progress(action_id);

-- Composite index for (user_id, action_id) queries
-- Note: unique_user_action constraint already provides this index
CREATE INDEX IF NOT EXISTS idx_user_progress_user_action
ON user_progress(user_id, action_id);

-- Verify indexes:
-- SELECT indexname FROM pg_indexes WHERE tablename = 'user_progress';
