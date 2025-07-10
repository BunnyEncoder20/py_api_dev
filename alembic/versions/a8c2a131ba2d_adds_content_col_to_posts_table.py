"""adds content col to posts table

Revision ID: a8c2a131ba2d
Revises: 0e552f25a5a8
Create Date: 2025-07-10 22:12:25.739397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8c2a131ba2d'
down_revision: Union[str, Sequence[str], None] = '0e552f25a5a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'Posts',
        sa.Column('content', sa.String(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('Posts', 'content')
