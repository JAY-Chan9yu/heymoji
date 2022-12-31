"""Initialize heymoji

Revision ID: 4027cae1015c
Revises: 
Create Date: 2022-10-10 16:02:21.240316

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4027cae1015c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('slack_id', sa.String(50), nullable=False, unique=True),
        sa.Column('my_reaction', sa.Integer, nullable=False, default=5),
        sa.Column('avatar_url', sa.String(500), nullable=False),
        sa.Column('department', sa.String(50), nullable=False),
        sa.Column('is_display', sa.Boolean, nullable=False)
    )

    op.create_table(
        'reactions',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('to_user_id', sa.Integer, sa.ForeignKey("users.id")),
        sa.Column('from_user_id', sa.Integer, sa.ForeignKey("users.id")),
        sa.Column('year', sa.Integer, nullable=False),
        sa.Column('month', sa.Integer, nullable=False),
        sa.Column('emoji', sa.String(50), nullable=True),
        sa.Column('count', sa.Integer, default=0)
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('reactions')
