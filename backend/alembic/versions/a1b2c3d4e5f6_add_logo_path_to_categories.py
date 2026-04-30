"""add logo_path to categories

Revision ID: a1b2c3d4e5f6
Revises: cd5b2a14347e
Create Date: 2026-04-30 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'cd5b2a14347e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('categories', sa.Column('logo_path', sa.String(length=512), nullable=True))


def downgrade() -> None:
    op.drop_column('categories', 'logo_path')
