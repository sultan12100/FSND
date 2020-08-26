"""empty message

Revision ID: 9c9dabdae17e
Revises: daaf819e8285
Create Date: 2020-08-24 22:18:01.284451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c9dabdae17e'
down_revision = 'daaf819e8285'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('title_release_date_constraint', 'Movie', ['title', 'release_date'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('title_release_date_constraint', 'Movie', type_='unique')
    # ### end Alembic commands ###