"""add reset token table

Revision ID: 20260125_add_reset_token
Revises: 7e1367b61cd1
Create Date: 2026-01-25 00:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260125_add_reset_token'
down_revision = '7e1367b61cd1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'password_resets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('token', sa.String(length=128), nullable=False, unique=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['dobs_user.id']),
    )
    op.create_index('ix_password_resets_user_id', 'password_resets', ['user_id'])


def downgrade():
    op.drop_index('ix_password_resets_user_id', table_name='password_resets')
    op.drop_table('password_resets')
