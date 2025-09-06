from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.associations import UserAccountLink

class UserBase(SQLModel):
    """
    Base model for User with common fields.
    """
    email: str
    password: str
    full_name: Optional[str] = None

class User(UserBase, table=True):
    """
    User model representing a user entity.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    accounts: List["Account"] = Relationship(
        back_populates="users",
        link_model=UserAccountLink
    )
