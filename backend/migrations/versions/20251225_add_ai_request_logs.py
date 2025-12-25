"""Add ai_request_logs table

Revision ID: 20251225_ai_logs
Revises:
Create Date: 2025-12-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251225_ai_logs'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ai_request_logs',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('provider', sa.String(20), nullable=False),
        sa.Column('model', sa.String(50), nullable=False),
        sa.Column('prompt_tokens', sa.Integer(), nullable=True),
        sa.Column('completion_tokens', sa.Integer(), nullable=True),
        sa.Column('latency_ms', sa.Integer(), nullable=False),
        sa.Column('cost_usd', sa.Numeric(10, 6), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ai_request_logs_created_at', 'ai_request_logs', ['created_at'])
    op.create_index('ix_ai_request_logs_user_id', 'ai_request_logs', ['user_id'])


def downgrade():
    op.drop_index('ix_ai_request_logs_user_id', table_name='ai_request_logs')
    op.drop_index('ix_ai_request_logs_created_at', table_name='ai_request_logs')
    op.drop_table('ai_request_logs')
