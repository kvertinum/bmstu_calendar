"""

Revision ID: 11f096e9d2c9
Revises: 84b72fad1f79
Create Date: 2024-10-08 12:53:19.099691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11f096e9d2c9'
down_revision: Union[str, None] = '84b72fad1f79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('chats_user_id_fkey', 'chats', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('chats_user_id_fkey', 'chats', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
