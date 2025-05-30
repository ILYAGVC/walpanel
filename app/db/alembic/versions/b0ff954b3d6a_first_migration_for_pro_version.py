"""first migration for pro version

Revision ID: b0ff954b3d6a
Revises: ce955c93bf0e
Create Date: 2025-05-21 11:51:06.994154

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b0ff954b3d6a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create table panels
    op.create_table(
        "panels",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("sub", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create table admins
    op.create_table(
        "admins",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(), unique=True, nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("panel_id", sa.Integer(), sa.ForeignKey("panels.id"), nullable=False),
        sa.Column("inbound_id", sa.Integer(), default=1, nullable=False),
        sa.Column("traffic", sa.Integer(), default=0, nullable=False),
        sa.Column("expiry_time", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("is_banned", sa.Boolean(), default=False, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create table plans
    op.create_table(
        "plans",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("traffic", sa.Integer(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=True),
        sa.Column("days", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create table settings
    op.create_table(
        "settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("language", sa.String(), nullable=False, server_default="en"),
        sa.Column(
            "card_payment_enabled", sa.Boolean(), nullable=False, server_default="true"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create table news (lowercase tablename as per model)
    op.create_table(
        "news",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create table card_number
    op.create_table(
        "card_number",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("number", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create table help_message
    op.create_table(
        "help_message",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create table registering_message
    op.create_table(
        "registering_message",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create table bot_settings
    op.create_table(
        "bot_settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("start_notif", sa.Boolean(), nullable=False, default=True),
        sa.Column("create_notif", sa.Boolean(), nullable=False, default=True),
        sa.Column("delete_notif", sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Insert default row for bot_settings (optional)
    op.execute(
        "INSERT INTO bot_settings (start_notif, create_notif, delete_notif) VALUES (true, true, true)"
    )

    # Insert default row for settings
    op.execute(
        "INSERT INTO settings (language, card_payment_enabled) VALUES ('en', true)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("bot_settings")
    op.drop_table("registering_message")
    op.drop_table("help_message")
    op.drop_table("card_number")
    op.drop_table("news")
    op.drop_table("settings")
    op.drop_table("plans")
    op.drop_table("admins")
    op.drop_table("panels")
