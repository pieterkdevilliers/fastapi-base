import secrets
from datetime import datetime, timedelta, timezone
from sqlmodel import select, Session
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings
from app.models.security import PasswordResetToken
from app.models.users import User


# Setup the bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a plain password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_password_reset_token(user_id: int, session) -> str:
    """
    Creates a JWT token for password reset.
    """
    # 1. Generate a secure token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours=1) # Token valid for 1 hour

    # 2. Store the token in the database
    password_reset_token = PasswordResetToken(user_id=user_id, token=token, expires_at=expires_at)
    session.add(password_reset_token)
    session.commit()
    session.refresh(password_reset_token)

    return token


def get_reset_token(token: str, session: Session):
    """
    Retrieve a password reset token record from the database.
    """
    token_record = select(PasswordResetToken).filter(PasswordResetToken.token == token)
    result = session.exec(token_record)
    token_record = result.first()

    return token_record


def update_user_password(user_id: int, password: str, session: Session):
    """
    Update user password in password reset process
    """
    user = session.get(User, user_id)
    
    if not user:
        return {"error": "User not found"}
    
    user.password = hash_password(password)
        
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

def delete_reset_token(token_record: PasswordResetToken, session: Session):
    """
    Deletes a password reset token from the database.
    """
    session.delete(token_record)
    session.commit()