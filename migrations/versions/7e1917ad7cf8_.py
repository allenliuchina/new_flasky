"""empty message

Revision ID: 7e1917ad7cf8
Revises: 9943558db952
Create Date: 2018-09-05 14:19:01.906047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e1917ad7cf8'
down_revision = '9943558db952'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('comments_sum', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'comments_sum')
    # ### end Alembic commands ###