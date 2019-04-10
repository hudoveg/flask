"""empty message

Revision ID: cb14ba170ba7
Revises: 710099272ca3
Create Date: 2019-04-10 07:47:54.704392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb14ba170ba7'
down_revision = '710099272ca3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_items', sa.Column('book_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order_items', 'books', ['book_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.drop_column('order_items', 'book_id')
    # ### end Alembic commands ###
