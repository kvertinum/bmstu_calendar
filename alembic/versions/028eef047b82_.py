"""

Revision ID: 028eef047b82
Revises: 7a65b0f53426
Create Date: 2024-09-23 10:59:38.401747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '028eef047b82'
down_revision: Union[str, None] = '7a65b0f53426'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('telegram_name', sa.String(length=255)))
    op.create_unique_constraint(None, 'user', ['id'])
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'telegram_name')
    # ### end Alembic commands ###
