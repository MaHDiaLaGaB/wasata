"""db init

Revision ID: 1f3f451eeb64
Revises: 
Create Date: 2023-06-22 21:22:32.549078

"""
from alembic import op
import sqlalchemy as sa
import type


# revision identifiers, used by Alembic.
revision = "1f3f451eeb64"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "admins",
        sa.Column("id", type.GUID(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=True),
        sa.Column("api_secret_key", sa.String(length=128), nullable=True),
        sa.Column("usdt_price", sa.Numeric(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(op.f("ix_admins_username"), "admins", ["username"], unique=True)
    op.create_table(
        "users",
        sa.Column("id", type.GUID(), nullable=False),
        sa.Column("invoice_id", type.GUID(), nullable=True),
        sa.Column("phone_number", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("tokens", sa.Numeric(precision=9, scale=4), nullable=True),
        sa.Column("price", sa.Numeric(precision=9, scale=4), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("admin_id", type.GUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["admin_id"],
            ["admins.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("invoice_id"),
        sa.UniqueConstraint("phone_number"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    op.drop_index(op.f("ix_admins_username"), table_name="admins")
    op.drop_table("admins")
    # ### end Alembic commands ###
