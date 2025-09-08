from pydantic import BaseModel, EmailStr

class ForgotPasswordRequest(BaseModel):
    """
    Schema for forgot password request.
    """
    email: EmailStr

class TokenValidateRequest(BaseModel):
    """
    Schema for validating a token.
    """
    token: str

class ResetPasswordRequest(BaseModel):
    """
    Schema for resetting password."""
    token: str
    new_password: str