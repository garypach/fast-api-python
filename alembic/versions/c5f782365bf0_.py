"""add tag column to comments

Revision ID: c5f782365bf0
Revises: cdbb75360a69
Create Date: 2021-12-26 15:28:36.803464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5f782365bf0'
down_revision = 'cdbb75360a69'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('comments', sa.Column('tag',sa.String(),nullable=False,server_default='Enhancement'))
    pass


def downgrade():
    op.drop_column('comments','tag')
    pass
