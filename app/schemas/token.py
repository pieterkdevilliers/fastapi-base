from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    account_unique_id: str | None = None
    account_organisation: str | None = None

class TokenData(BaseModel):
    email: str | None = None
