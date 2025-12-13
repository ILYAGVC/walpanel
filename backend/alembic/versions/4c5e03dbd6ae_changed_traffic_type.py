"""changed traffic type

Revision ID: 4c5e03dbd6ae
Revises: 55d743570ead
Create Date: 2025-12-13 13:22:00.202954

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c5e03dbd6ae"
down_revision: Union[str, None] = "55d743570ead"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("admins") as batch_op:
        batch_op.alter_column(
            "traffic",
            existing_type=sa.FLOAT(),
            type_=sa.BigInteger(),
            existing_nullable=True,
        )


def downgrade() -> None:
    with op.batch_alter_table("admins") as batch_op:
        batch_op.alter_column(
            "traffic",
            existing_type=sa.BigInteger(),
            type_=sa.FLOAT(),
            existing_nullable=True,
        )
