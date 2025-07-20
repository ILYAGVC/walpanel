"""
Remove help_message, registering_message, and bot_settings tables

Revision ID: 20240601
Revises: 
Create Date: 2024-06-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20240601'
down_revision = '20240320'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('admins', sa.Column('inbound_flow', sa.String, nullable=True))
    op.drop_table('help_message')
    op.drop_table('registering_message')
    op.drop_table('bot_settings')


def downgrade():
    op.drop_column('admins', 'inbound_flow')
    op.create_table(
        'help_message',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('message', sa.String, nullable=False)
    )
    op.create_table(
        'registering_message',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('message', sa.String, nullable=False)
    )
    op.create_table(
        'bot_settings',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('start_notif', sa.Boolean, default=True),
        sa.Column('create_notif', sa.Boolean, default=True),
        sa.Column('delete_notif', sa.Boolean, default=True)
    ) 