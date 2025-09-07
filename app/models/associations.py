from typing import Optional
from sqlmodel import SQLModel, Field
import sqlalchemy as sa
from sqlalchemy import ForeignKey

class UserAccountLink(SQLModel, table=True):
    """
    Association table for many-to-many relationship between Users and Accounts.
    """
    user_id: Optional[int] = Field(
        default=None,
        sa_column=sa.Column(
            sa.Integer,
            ForeignKey("user.id", ondelete="CASCADE"),
            primary_key=True
        )
    )
    
    account_id: Optional[int] = Field(
        default=None,
        sa_column=sa.Column(
            sa.Integer,
            ForeignKey("account.id"),
            primary_key=True
        )
    )
