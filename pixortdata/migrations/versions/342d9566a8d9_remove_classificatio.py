"""remove classifications

Revision ID: 342d9566a8d9
Revises: 118ce993aa3c
Create Date: 2013-03-29 16:57:45.040614

"""

# revision identifiers, used by Alembic.
revision = '342d9566a8d9'
down_revision = '118ce993aa3c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table(u'classifications')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('key', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )
    ### end Alembic commands ###
