"""rev2 creates user table

Revision ID: 39327bc8a954
Revises: 0e552f25a5a8
Create Date: 2025-07-11 18:55:06.927338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP


# revision identifiers, used by Alembic.
revision: str = '39327bc8a954'
down_revision: Union[str, Sequence[str], None] = '0e552f25a5a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id',sa.Integer(), nullable=False),
        sa.Column('email',sa.String(), nullable=False),
        sa.Column('password',sa.String(), nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),                      # constraint: primary key
        sa.UniqueConstraint('email')                        # constraint: email must be unique
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
