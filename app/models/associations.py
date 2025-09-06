from sqlmodel import SQLModel, Field
from typing import Optional

class UserAccountLink(SQLModel, table=True):
    """
    Association table for many-to-many relationship between Users and Accounts.
    """
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    account_id: Optional[int] = Field(default=None, foreign_key="account.id", primary_key=True)