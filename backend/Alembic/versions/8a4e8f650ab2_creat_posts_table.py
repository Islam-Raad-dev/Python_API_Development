"""Creat Posts Table

Revision ID: 8a4e8f650ab2
Revises: 8435f2e792e8
Create Date: 2026-09-06 19:25:14.809114

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8a4e8f650ab2'
down_revision: Union[str, Sequence[str], None] = '8435f2e792e8'  # noqa: UP007
branch_labels: Union[str, Sequence[str], None] = None  # noqa: UP007
depends_on: Union[str, Sequence[str], None] = None  # noqa: UP007


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', sa.column('id', sa.Integer(), nullable=False, primary_key=True), sa.column('title', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')

