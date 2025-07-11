"""rev 3 adds users.id foreign key into posts table

Revision ID: 7fc0dd20789d
Revises: 39327bc8a954
Create Date: 2025-07-11 19:30:20.148657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fc0dd20789d'
down_revision: Union[str, Sequence[str], None] = '39327bc8a954'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )

    # setting up the foreign key constraint
    op.create_foreign_key(
        'posts_users_fk',           # name of constraint
        source_table='posts',       # on which we putting FK
        referent_table='users',     # from which table we bring FK
        local_cols=['owner_id'],    # Col of local table
        remote_cols=['id'],         # Col of remote table
        ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
