"""Initial tables

Revision ID: 45502a712dae
Revises: 
Create Date: 2024-12-28 12:30:55.162545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45502a712dae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exhibitions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exhibitions_id'), 'exhibitions', ['id'], unique=False)
    op.create_table('owners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_owners_id'), 'owners', ['id'], unique=False)
    op.create_table('exhibits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['owners.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exhibits_id'), 'exhibits', ['id'], unique=False)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exhibition_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('venue', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['exhibition_id'], ['exhibitions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    op.create_table('arrival_acts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('arrived_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_arrival_acts_id'), 'arrival_acts', ['id'], unique=False)
    op.create_table('order_exhibit_association',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('exhibit_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exhibit_id'], ['exhibits.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('order_id', 'exhibit_id')
    )
    op.create_table('return_acts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('returned_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_return_acts_id'), 'return_acts', ['id'], unique=False)
    op.create_table('transfer_acts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('transferred_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transfer_acts_id'), 'transfer_acts', ['id'], unique=False)
    op.create_table('arrival_exhibit_association',
    sa.Column('arrival_act_id', sa.Integer(), nullable=False),
    sa.Column('exhibit_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['arrival_act_id'], ['arrival_acts.id'], ),
    sa.ForeignKeyConstraint(['exhibit_id'], ['exhibits.id'], ),
    sa.PrimaryKeyConstraint('arrival_act_id', 'exhibit_id')
    )
    op.create_table('return_exhibit_association',
    sa.Column('return_act_id', sa.Integer(), nullable=False),
    sa.Column('exhibit_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exhibit_id'], ['exhibits.id'], ),
    sa.ForeignKeyConstraint(['return_act_id'], ['return_acts.id'], ),
    sa.PrimaryKeyConstraint('return_act_id', 'exhibit_id')
    )
    op.create_table('transfer_exhibit_association',
    sa.Column('transfer_act_id', sa.Integer(), nullable=False),
    sa.Column('exhibit_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exhibit_id'], ['exhibits.id'], ),
    sa.ForeignKeyConstraint(['transfer_act_id'], ['transfer_acts.id'], ),
    sa.PrimaryKeyConstraint('transfer_act_id', 'exhibit_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transfer_exhibit_association')
    op.drop_table('return_exhibit_association')
    op.drop_table('arrival_exhibit_association')
    op.drop_index(op.f('ix_transfer_acts_id'), table_name='transfer_acts')
    op.drop_table('transfer_acts')
    op.drop_index(op.f('ix_return_acts_id'), table_name='return_acts')
    op.drop_table('return_acts')
    op.drop_table('order_exhibit_association')
    op.drop_index(op.f('ix_arrival_acts_id'), table_name='arrival_acts')
    op.drop_table('arrival_acts')
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_exhibits_id'), table_name='exhibits')
    op.drop_table('exhibits')
    op.drop_index(op.f('ix_owners_id'), table_name='owners')
    op.drop_table('owners')
    op.drop_index(op.f('ix_exhibitions_id'), table_name='exhibitions')
    op.drop_table('exhibitions')
    # ### end Alembic commands ###
