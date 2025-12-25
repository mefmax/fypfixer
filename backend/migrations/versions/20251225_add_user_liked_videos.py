"""Add user_liked_videos table for favorites tracking.

Revision ID: 20251225_add_user_liked_videos
Revises: 20251225_plans_v2_challenges
Create Date: 2025-12-25
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '20251225_add_user_liked_videos'
down_revision = '20251225_plans_v2'
branch_labels = None
depends_on = None


def upgrade():
    """Create user_liked_videos table for favorites tracking."""

    # Create user_liked_videos table
    op.create_table(
        'user_liked_videos',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('video_id', sa.String(50), nullable=False),
        sa.Column('liked_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),

        # Prevent duplicate favorites
        sa.UniqueConstraint('user_id', 'video_id', name='uq_user_liked_videos_user_video'),
    )

    # Indexes for common queries
    op.create_index('idx_user_liked_videos_user', 'user_liked_videos', ['user_id'])
    op.create_index('idx_user_liked_videos_liked_at', 'user_liked_videos', ['user_id', 'liked_at'], postgresql_using='btree')


def downgrade():
    """Drop user_liked_videos table."""
    op.drop_index('idx_user_liked_videos_liked_at', table_name='user_liked_videos')
    op.drop_index('idx_user_liked_videos_user', table_name='user_liked_videos')
    op.drop_table('user_liked_videos')
