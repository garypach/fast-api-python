"""add published and created at columns to posts table

Revision ID: 1a3dae40a04e
Revises: b360c1af8706
Create Date: 2021-12-16 19:52:23.471318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a3dae40a04e'
down_revision = 'b360c1af8706'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published',sa.Boolean(),nullable=False,server_default='True'))
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')

    pass
