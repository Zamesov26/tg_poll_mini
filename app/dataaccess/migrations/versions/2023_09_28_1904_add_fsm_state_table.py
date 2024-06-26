"""add fsm state table

Revision ID: bb1b4ce5ec48
Revises: e9da1f90dd40
Create Date: 2023-09-28 19:04:20.091823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb1b4ce5ec48'
down_revision: Union[str, None] = 'e9da1f90dd40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fsm_state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bot_id', sa.BigInteger(), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('state', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('index_fsm_state_ids', 'fsm_state', ['bot_id', 'chat_id', 'user_id'], unique=False)
    op.drop_index('index_ids', table_name='fsm_data')
    op.create_index('index_fsm_data_ids', 'fsm_data', ['bot_id', 'chat_id', 'user_id'], unique=False)
    op.drop_column('fsm_data', 'state')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fsm_data', sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index('index_fsm_data_ids', table_name='fsm_data')
    op.create_index('index_ids', 'fsm_data', ['bot_id', 'chat_id', 'user_id'], unique=False)
    op.drop_index('index_fsm_state_ids', table_name='fsm_state')
    op.drop_table('fsm_state')
    # ### end Alembic commands ###
