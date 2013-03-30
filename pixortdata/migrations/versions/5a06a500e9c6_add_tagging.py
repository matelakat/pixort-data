"""add tagging

Revision ID: 5a06a500e9c6
Revises: 342d9566a8d9
Create Date: 2013-03-30 08:37:38.611866

"""

# revision identifiers, used by Alembic.
revision = '5a06a500e9c6'
down_revision = '342d9566a8d9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'classifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('classification_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['classification_id'], ['classifications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('raw_id', sa.Integer(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['raw_id'], ['raw.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('categories')
    op.drop_table('classifications')
    ### end Alembic commands ###
