from pydantic import BaseModel
from typing import List, Optional
from app.schemas.accounts import AccountRead

class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    email: str
    password: Optional[str] = None
    full_name: Optional[str] = None
    account_ids: Optional[List[int]] = []  # IDs of accounts to assign on creation

class UserReadBasic(BaseModel):
    """
    Basic schema for reading user details.
    """
    id: int
    email: str
    full_name: Optional[str] = None

    class Config:
        """
        Enable ORM mode for compatibility with ORM objects.
        """
        orm_mode = True

class UserRead(UserReadBasic):
    """
    Schema for reading user details with associated accounts.
    """
    accounts: List[AccountRead] = []  # many-to-many accounts

class UserLogin(BaseModel):
    """
    Schema for user login."""
    email: str
    password: str

class UserUpdate(BaseModel):
    """
    Schema for updating user details."""
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserToAccount(BaseModel):
    """
    Schema for adding a user to an account.
    """
    email: str
    password: str
    full_name: Optional[str] = None

class MessageResponse(BaseModel):
    """
    Generic message response schema.
    """
    message: str