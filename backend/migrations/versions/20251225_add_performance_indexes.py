"""Add performance indexes for common queries

Revision ID: 20251225_perf_idx
Revises: 20251225_ai_logs
Create Date: 2025-12-25

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '20251225_perf_idx'
down_revision = '20251225_ai_logs'
branch_labels = None
depends_on = None


def upgrade():
    # 1. users table - partial index for active users
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_is_active
        ON users(is_active) WHERE is_active = true
    """)

    # 2. step_items table - foreign key index
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_step_items_plan_step
        ON step_items(plan_step_id)
    """)

    # 3. user_categories table - user lookup
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_categories_user
        ON user_categories(user_id)
    """)

    # 4. user_progress table - completed actions by date
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_progress_completed
        ON user_progress(completed_at DESC)
    """)

    # 5. plans table - user's plans by date
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_plans_user_date
        ON plans(user_id, plan_date DESC)
    """)

    # 6. actions table - plan actions in order
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_actions_plan_order
        ON actions(plan_id, sort_order)
    """)


def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_actions_plan_order")
    op.execute("DROP INDEX IF EXISTS idx_plans_user_date")
    op.execute("DROP INDEX IF EXISTS idx_user_progress_completed")
    op.execute("DROP INDEX IF EXISTS idx_user_categories_user")
    op.execute("DROP INDEX IF EXISTS idx_step_items_plan_step")
    op.execute("DROP INDEX IF EXISTS idx_users_is_active")
