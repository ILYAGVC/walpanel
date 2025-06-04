"""add purchase history and modify payment gateway

Revision ID: 20240320
Revises: b0ff954b3d6a
Create Date: 2024-03-20 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "20240320"
down_revision = "b0ff954b3d6a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "Payment_gateway_keys",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("Intermediary_gateway_key", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "purchase_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("purchase_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default="pending"),
        sa.PrimaryKeyConstraint("id"),
    )

    conn = op.get_bind()

    # Get current data from settings table
    settings_data = conn.execute(text("SELECT * FROM settings")).fetchall()

    # Create new settings table with updated default
    op.create_table(
        "settings_new",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("language", sa.String(), nullable=False, server_default="en"),
        sa.Column(
            "card_payment_enabled", sa.Boolean(), nullable=False, server_default="true"
        ),
        sa.Column(
            "Intermediary_payment_gateway",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Copy data to new table
    for row in settings_data:
        conn.execute(
            text(
                "INSERT INTO settings_new (id, language, card_payment_enabled, Intermediary_payment_gateway) VALUES (:id, :lang, :card, :inter)"
            ),
            {
                "id": row[0],
                "lang": row[1],
                "card": row[2],
                "inter": row[3] if len(row) > 3 else False,
            },
        )

    # Drop old table and rename new one
    op.drop_table("settings")
    op.rename_table("settings_new", "settings")


def downgrade():
    op.drop_table("purchase_history")

    op.drop_table("Payment_gateway_keys")

    conn = op.get_bind()

    settings_data = conn.execute(text("SELECT * FROM settings")).fetchall()

    op.create_table(
        "settings_new",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("language", sa.String(), nullable=False, server_default="en"),
        sa.Column(
            "card_payment_enabled", sa.Boolean(), nullable=False, server_default="true"
        ),
        sa.Column(
            "Intermediary_payment_gateway",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    for row in settings_data:
        conn.execute(
            text(
                "INSERT INTO settings_new (id, language, card_payment_enabled, Intermediary_payment_gateway) VALUES (:id, :lang, :card, :inter)"
            ),
            {"id": row[0], "lang": row[1], "card": row[2], "inter": row[3]},
        )

    op.drop_table("settings")
    op.rename_table("settings_new", "settings")
