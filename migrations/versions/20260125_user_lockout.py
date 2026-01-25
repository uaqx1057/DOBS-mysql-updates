"""Add user lockout fields

Revision ID: 20260125_user_lockout
Revises: 20260125_decimal_indexes
Create Date: 2026-01-25 00:45:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260125_user_lockout'
down_revision = '20260125_decimal_indexes'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == "sqlite"
    inspector = sa.inspect(bind)

    def _has_column(table, column):
        return any(col.get("name") == column for col in inspector.get_columns(table))

    has_failed = _has_column('dobs_user', 'failed_logins')
    has_locked = _has_column('dobs_user', 'locked_until')

    if not has_failed:
        op.add_column('dobs_user', sa.Column('failed_logins', sa.Integer(), nullable=False, server_default='0'))
    if not has_locked:
        op.add_column('dobs_user', sa.Column('locked_until', sa.DateTime(), nullable=True))

    op.execute("UPDATE dobs_user SET failed_logins = 0 WHERE failed_logins IS NULL")

    if not is_sqlite:
        op.alter_column('dobs_user', 'failed_logins', server_default=None)


def downgrade():
    op.drop_column('dobs_user', 'locked_until')
    op.drop_column('dobs_user', 'failed_logins')
