"""
Remove order_id and chat_id from purchase_history

Revision ID: 20240602
Revises: 20240601
Create Date: 2024-06-02 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20240602'
down_revision = '20240601'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('purchase_history') as batch_op:
        batch_op.add_column(sa.Column('payer', sa.String(), nullable=False))
        batch_op.drop_column('order_id')
        batch_op.drop_column('chat_id')

def downgrade():
    op.add_column('purchase_history', sa.Column('order_id', sa.String(), nullable=False, unique=True))
    op.add_column('purchase_history', sa.Column('chat_id', sa.Integer(), nullable=False)) 