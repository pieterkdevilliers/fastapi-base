from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .accounts import Account

class UserBase(SQLModel):
    """
    User Model Base
    """
    email: str
    password: str
    account_unique_id: str = Field(foreign_key="account.account_unique_id")
    full_name: Optional[str] = None


class User(UserBase, table=True):
    """
    User Model
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    account: Account = Relationship(back_populates="users")