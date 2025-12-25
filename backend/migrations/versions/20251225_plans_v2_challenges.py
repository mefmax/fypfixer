"""Add plans_v2 columns and challenges table

Revision ID: 20251225_plans_v2
Revises: 20251225_perf_idx
Create Date: 2025-12-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251225_plans_v2'
down_revision = '20251225_perf_idx'
branch_labels = None
depends_on = None


def upgrade():
    # Create challenges table first (plans will FK to it)
    op.create_table(
        'challenges',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('category_id', sa.BigInteger(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('current_day', sa.Integer(), default=1, nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_challenges_user_id', 'challenges', ['user_id'])
    op.create_index('ix_challenges_is_active', 'challenges', ['is_active'])

    # Add new columns to plans table for v2.0
    op.add_column('plans', sa.Column('day_of_challenge', sa.Integer(), nullable=True))
    op.add_column('plans', sa.Column('challenge_id', sa.BigInteger(), nullable=True))
    op.add_column('plans', sa.Column('step_clear_completed', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('plans', sa.Column('step_watch_completed', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('plans', sa.Column('step_reinforce_completed', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('plans', sa.Column('signals_count', sa.Integer(), server_default='0', nullable=False))

    # Add FK constraint for challenge_id
    op.create_foreign_key(
        'fk_plans_challenge_id',
        'plans', 'challenges',
        ['challenge_id'], ['id'],
        ondelete='SET NULL'
    )

    # Create blocked_creators table for toxic detection
    op.create_table(
        'blocked_creators',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('creator_username', sa.String(256), nullable=False),
        sa.Column('blocked_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'creator_username', name='unique_user_blocked_creator')
    )
    op.create_index('ix_blocked_creators_user_id', 'blocked_creators', ['user_id'])


def downgrade():
    op.drop_index('ix_blocked_creators_user_id', table_name='blocked_creators')
    op.drop_table('blocked_creators')

    op.drop_constraint('fk_plans_challenge_id', 'plans', type_='foreignkey')
    op.drop_column('plans', 'signals_count')
    op.drop_column('plans', 'step_reinforce_completed')
    op.drop_column('plans', 'step_watch_completed')
    op.drop_column('plans', 'step_clear_completed')
    op.drop_column('plans', 'challenge_id')
    op.drop_column('plans', 'day_of_challenge')

    op.drop_index('ix_challenges_is_active', table_name='challenges')
    op.drop_index('ix_challenges_user_id', table_name='challenges')
    op.drop_table('challenges')
