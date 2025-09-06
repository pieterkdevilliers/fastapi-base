from pydantic import BaseModel

class AccountCreate(BaseModel):
    account_organisation: str

class AccountRead(BaseModel):
    id: int
    account_organisation: str
    account_unique_id: str
