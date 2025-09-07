"""Add cascade delete for user_id in UserAccountLink

Revision ID: a5136477f0db
Revises: 
Create Date: 2025-09-07 10:07:15.521548
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a5136477f0db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Use batch mode to alter SQLite table safely
    with op.batch_alter_table("useraccountlink", recreate="always") as batch_op:
        batch_op.create_foreign_key(
            "fk_useraccountlink_user_id_user",
            "user",
            ["user_id"],
            ["id"],
            ondelete="CASCADE"
        )
        batch_op.create_foreign_key(
            "fk_useraccountlink_account_id_account",
            "account",
            ["account_id"],
            ["id"]
        )


def downgrade() -> None:
    # Recreate table without cascade
    with op.batch_alter_table("useraccountlink", recreate="always") as batch_op:
        batch_op.create_foreign_key(
            "fk_useraccountlink_user_id_user",
            "user",
            ["user_id"],
            ["id"]
        )
        batch_op.create_foreign_key(
            "fk_useraccountlink_account_id_account",
            "account",
            ["account_id"],
            ["id"]
        )
