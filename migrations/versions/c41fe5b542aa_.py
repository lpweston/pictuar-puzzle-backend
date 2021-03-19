"""empty message

Revision ID: c41fe5b542aa
Revises: 069939575466
Create Date: 2019-10-08 20:19:45.465802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c41fe5b542aa'
down_revision = '069939575466'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('num', sa.Integer(), nullable=True))
    op.drop_column('games', 'three')
    op.drop_column('games', 'two')
    op.drop_column('games', 'four')
    op.drop_column('games', 'one')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('one', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('games', sa.Column('four', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('games', sa.Column('two', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('games', sa.Column('three', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('games', 'num')
    # ### end Alembic commands ###