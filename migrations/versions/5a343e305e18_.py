"""empty message

Revision ID: 5a343e305e18
Revises: 99ec73c5ec2e
Create Date: 2023-12-27 01:53:23.026424

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5a343e305e18'
down_revision = '99ec73c5ec2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('feed_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['feed_id'], ['feeds.id'], name='subscriptions_feed_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='subscriptions_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='subscriptions_pkey'),
    sa.UniqueConstraint('feed_id', 'user_id', name='user_feed_subscription_index')
    )
    # ### end Alembic commands ###
