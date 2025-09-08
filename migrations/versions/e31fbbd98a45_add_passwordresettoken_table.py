"""Add PasswordResetToken table

Revision ID: e31fbbd98a45
Revises: a5136477f0db
Create Date: 2025-09-08 08:13:14.497962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e31fbbd98a45'
down_revision: Union[str, None] = 'a5136477f0db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'passwordresettoken',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('token', sa.String, nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime, nullable=True),
    )
    op.create_index(op.f('ix_passwordresettoken_user_id'), 'passwordresettoken', ['user_id'], unique=False)
    op.create_index(op.f('ix_passwordresettoken_token'), 'passwordresettoken', ['token'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_passwordresettoken_token'), table_name='passwordresettoken')
    op.drop_index(op.f('ix_passwordresettoken_user_id'), table_name='passwordresettoken')
    op.drop_table('passwordresettoken')
