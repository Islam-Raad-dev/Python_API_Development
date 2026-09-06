"""Creat Posts Table

Revision ID: 8a4e8f650ab2
Revises: 8435f2e792e8
Create Date: 2026-09-06 19:25:14.809114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a4e8f650ab2'
down_revision: Union[str, Sequence[str], None] = '8435f2e792e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
