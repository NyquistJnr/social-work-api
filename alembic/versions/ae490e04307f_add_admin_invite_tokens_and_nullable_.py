"""add admin invite tokens and nullable password

Revision ID: ae490e04307f
Revises: 94e98f28ceeb
Create Date: 2026-06-27 19:33:37.617315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae490e04307f'
down_revision: Union[str, None] = '94e98f28ceeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'hashed_password', existing_type=sa.String(length=255), nullable=True)

    op.create_table(
        'admin_invite_tokens',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('token_hash', sa.String(length=64), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('restored_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.UUID(), nullable=True),
        sa.Column('updated_by', sa.UUID(), nullable=True),
        sa.Column('deleted_by', sa.UUID(), nullable=True),
        sa.Column('restored_by', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_admin_invite_tokens_token_hash'), 'admin_invite_tokens', ['token_hash'], unique=True
    )
    op.create_index(
        op.f('ix_admin_invite_tokens_user_id'), 'admin_invite_tokens', ['user_id'], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_admin_invite_tokens_user_id'), table_name='admin_invite_tokens')
    op.drop_index(op.f('ix_admin_invite_tokens_token_hash'), table_name='admin_invite_tokens')
    op.drop_table('admin_invite_tokens')

    op.alter_column('users', 'hashed_password', existing_type=sa.String(length=255), nullable=False)
