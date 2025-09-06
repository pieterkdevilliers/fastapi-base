from pydantic import BaseModel
from app.schemas.accounts import AccountRead

class UserCreate(BaseModel):
    email: str
    password: str
    account_unique_id: str
    full_name: str | None = None

class UserRead(BaseModel):
    id: int
    email: str
    account_unique_id: str
    account: AccountRead
    full_name: str | None = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str
