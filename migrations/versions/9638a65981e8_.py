"""empty message

Revision ID: 9638a65981e8
Revises: 5a343e305e18
Create Date: 2023-12-27 02:32:14.442744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9638a65981e8'
down_revision = '5a343e305e18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feeds', schema=None) as batch_op:
        batch_op.drop_constraint('feeds_created_by_id_fkey', type_='foreignkey')
        batch_op.drop_column('created_by_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feeds', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('feeds_created_by_id_fkey', 'users', ['created_by_id'], ['id'])

    # ### end Alembic commands ###