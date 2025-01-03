"""empty message

Revision ID: 019c645d7f9b
Revises: 6d1414726602
Create Date: 2025-01-03 01:39:59.401042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '019c645d7f9b'
down_revision = '6d1414726602'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('people_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.alter_column('people_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
