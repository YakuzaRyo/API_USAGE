"""initial

Revision ID: 9428951d372e
Revises:
Create Date: 2026-04-29 11:02:37.659727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9428951d372e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('providers', sa.Column('billing_mode', sa.String(length=16), nullable=True, server_default='api'))
    op.execute("UPDATE providers SET billing_mode = 'api' WHERE billing_mode IS NULL")
    op.add_column('providers', sa.Column('monthly_fee', sa.Float(), nullable=True))
    op.add_column('providers', sa.Column('sub_start_date', sa.String(length=16), nullable=True))


def downgrade() -> None:
    op.drop_column('providers', 'sub_start_date')
    op.drop_column('providers', 'monthly_fee')
    op.drop_column('providers', 'billing_mode')
