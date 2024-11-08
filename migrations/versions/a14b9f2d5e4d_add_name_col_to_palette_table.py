"""Add name col to palette table

Revision ID: a14b9f2d5e4d
Revises: 989e4283cb15
Create Date: 2024-11-07 23:47:40.413370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a14b9f2d5e4d'
down_revision = '989e4283cb15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('palette', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=200), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('palette', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
