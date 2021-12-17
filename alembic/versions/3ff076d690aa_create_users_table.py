"""create users table

Revision ID: 3ff076d690aa
Revises: 82c5ac274c60
Create Date: 2021-12-16 19:49:03.381582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ff076d690aa'
down_revision = '82c5ac274c60'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id',sa.Integer(),nullable=False), 
        sa.Column('email',sa.String(),nullable=False),
        sa.Column('password',sa.String(),nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )
    pass


def downgrade():
    op.drop_table('users')
    pass