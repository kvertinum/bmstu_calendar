"""

Revision ID: 84b72fad1f79
Revises: a757849b60b9
Create Date: 2024-10-08 12:28:48.463053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84b72fad1f79'
down_revision: Union[str, None] = 'a757849b60b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    op.create_unique_constraint(None, 'user', ['id'])
    op.create_unique_constraint(None, 'user_settings', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_settings', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_table('chats')
    # ### end Alembic commands ###
