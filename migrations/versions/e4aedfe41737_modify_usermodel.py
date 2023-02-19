"""modify UserModel

Revision ID: e4aedfe41737
Revises: 4027cae1015c
Create Date: 2023-01-29 22:09:02.114903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4aedfe41737'
down_revision = '4027cae1015c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'my_reaction')


def downgrade() -> None:
    op.add_column('users', sa.Column('my_reaction', sa.Integer, nullable=False, default=5))
