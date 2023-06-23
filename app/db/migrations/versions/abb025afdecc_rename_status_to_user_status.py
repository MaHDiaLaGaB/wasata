"""rename status to user_status

Revision ID: abb025afdecc
Revises: ab07bb77af38
Create Date: 2023-06-23 17:04:05.422179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abb025afdecc'
down_revision = 'ab07bb77af38'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_status', sa.String(), nullable=True))
    op.drop_column('users', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'user_status')
    # ### end Alembic commands ###
