"""Alter car model

Revision ID: c39d47e32bad
Revises: 6e48ae8c35e1
Create Date: 2025-12-10 14:08:49.210205

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c39d47e32bad"
down_revision: Union[str, Sequence[str], None] = "6e48ae8c35e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("cars", "user_id", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("cars", "user_id", nullable=True)
