"""Add Classifications

Revision ID: 118ce993aa3c
Revises: None
Create Date: 2013-03-28 06:43:30.082680

"""

# revision identifiers, used by Alembic.
revision = '118ce993aa3c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'classifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('key', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )


def downgrade():
    op.drop_table('classifications')
