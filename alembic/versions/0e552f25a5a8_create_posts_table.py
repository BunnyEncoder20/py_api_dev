"""create posts table

Revision ID: 0e552f25a5a8
Revises:
Create Date: 2025-07-10 21:49:02.668183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e552f25a5a8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('Posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('Posts')
