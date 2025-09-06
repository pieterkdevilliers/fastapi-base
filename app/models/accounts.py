from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.associations import UserAccountLink


class AccountBase(SQLModel):
    """
    Base model for Account with common fields.
    """
    account_organisation: str
    account_unique_id: str = Field(unique=True)

class Account(AccountBase, table=True):
    """
    Account model representing an account entity.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    users: List["User"] = Relationship(
        back_populates="accounts",
        link_model=UserAccountLink  # reference the association table
    )
