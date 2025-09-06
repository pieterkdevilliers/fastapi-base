from pydantic import BaseModel
from typing import List, Optional

class AccountCreate(BaseModel):
    """
    Schema for creating a new account.
    """
    account_organisation: str

class AccountRead(BaseModel):
    """
    Schema for reading account details.
    """
    id: int
    account_organisation: str
    account_unique_id: str

    class Config:
        orm_mode = True

class AccountReadWithUsers(AccountRead):
    """
    Schema for reading account details with associated users.
    """
    users: List["UserReadBasic"] = []  # optional for nested read


class AccountUpdate(BaseModel):
    """
    Schema for updating account details.
    """
    account_organisation: Optional[str] = None
