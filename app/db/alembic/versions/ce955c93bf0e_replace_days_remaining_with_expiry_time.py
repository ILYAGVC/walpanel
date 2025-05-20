"""replace_days_remaining_with_expiry_time

Revision ID: ce955c93bf0e
Revises: 147102cd297e
Create Date: 2025-05-16 23:23:21.689284

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ce955c93bf0e"
down_revision: Union[str, None] = "147102cd297e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("admins", sa.Column("expiry_time", sa.Date(), nullable=True))

    op.create_table(
        "settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("language", sa.String(), server_default="en"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("admins", "expiry_time")

    op.drop_table("settings")
