"""add foreign key to post table

Revision ID: 06386a2e6f13
Revises: a4e003e5f85f
Create Date: 2026-11-11 09:26:52.629647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06386a2e6f13'
down_revision: Union[str, Sequence[str], None] = 'a4e003e5f85f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_posts_owner_id_users', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_posts_owner_id_users', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
