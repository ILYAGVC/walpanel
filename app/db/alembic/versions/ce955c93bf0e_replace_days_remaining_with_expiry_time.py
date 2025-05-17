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


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("admins", "expiry_time")
