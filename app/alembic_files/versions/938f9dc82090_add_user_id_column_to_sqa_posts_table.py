"""Add user_id column to sqa_posts table

Revision ID: 938f9dc82090
Revises: 
Create Date: 2024-08-29 16:56:24.817766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '938f9dc82090'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sqa_posts', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('posts_users_fk', source_table='sqa_posts', referent_table='Users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='sqa_posts')
    op.drop_column('sqa_posts', 'user_id')
    pass
