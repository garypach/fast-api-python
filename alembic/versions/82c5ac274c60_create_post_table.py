"""create post table

Revision ID: 82c5ac274c60
Revises: 
Create Date: 2021-12-16 19:47:29.959251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82c5ac274c60'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(),nullable=False,primary_key=True), sa.Column('title', sa.String(),nullable=False),sa.Column('content', sa.String(),nullable=False)) 
    pass


def downgrade():
    op.drop_table('posts')
    pass
