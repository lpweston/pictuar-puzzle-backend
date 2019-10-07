"""empty message

Revision ID: 225cb855fe63
Revises: fd7e741aeaec
Create Date: 2019-10-05 16:52:44.194598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '225cb855fe63'
down_revision = 'fd7e741aeaec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pieces_hard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['img_id'], ['images.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pieces_intermediate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['img_id'], ['images.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pieces_intermediate')
    op.drop_table('pieces_hard')
    # ### end Alembic commands ###