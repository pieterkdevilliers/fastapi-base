from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from datetime import datetime

class PasswordResetTokenBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

class PasswordResetToken(PasswordResetTokenBase, table=True):

    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)
    token: str = Field(unique=True,  index=True, nullable=False)
    expires_at: Optional[datetime] = Field(default=None)

    def is_expired(self):
        return datetime.now() > self.expires_at