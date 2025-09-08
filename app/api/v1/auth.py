from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from jose import jwt, JWTError
from app.schemas.token import Token
from app.schemas.users import UserLogin
from app.schemas.security import ForgotPasswordRequest, TokenValidateRequest, ResetPasswordRequest
from app.models.users import User
from app.core.db import get_session
import app.core.security as security
from app.core.aws_ses_service import EmailService, get_email_service
from app.core.config import settings
from app.utils import users as user_utils
import boto3

router = APIRouter(tags=["auth"])
# Initialize the S3 client
s3 = boto3.client('s3')


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Authenticate user and return a JWT token.
    """
    statement = select(User).where(User.email == form_data.username)
    result = await session.exec(statement)
    db_user = result.first()
    if not db_user or not await security.verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = await security.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    request: ForgotPasswordRequest,
    email_service: EmailService = Depends(get_email_service),
    session: Session = Depends(get_session)):
    """
    Handle forgot password requests.
    """
    user = await user_utils.get_user_by_email(email=request.email, session=session)
    if user:
        token = await security.create_password_reset_token(user.id, session=session)

        reset_link = f"{settings.FE_BASE_URL}/reset-password?token={token}"
        print(f"Password reset link for {user.email}: {reset_link}")

        try:
            await email_service.send_password_reset_email(
                to_email=user.email,
                reset_link=reset_link
            )
        except Exception as e:
            print(f"ERROR: Could not send password reset email to {user.email}. Error: {e}")
            return {"message": "If an account with that email exists, a password reset link has been sent."}

    return {"message": "If an account with that email exists, a password reset link has been sent."}


@router.post("/validate-token", status_code=status.HTTP_200_OK)
async def validate_reset_token(
    request_data: TokenValidateRequest,
    session: Session = Depends(get_session),
    ):
    """
    Serves the Password Reset Step 2"""
    token_record = await security.get_reset_token(token=request_data.token, session=session)
    if not token_record or token_record.is_expired():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is invalid or has expired.",
        )
    return {"message": "Token is valid."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    request: ResetPasswordRequest,
    session: Session = Depends(get_session),
    ):
    token_record = await security.get_reset_token(token=request.token, session=session)

    # 1. Re-validate the token
    if not token_record or token_record.is_expired():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is invalid or has expired.",
        )

    # 2. Get the user and update their password
    user_id = token_record.user_id
    await security.update_user_password(user_id=user_id, password=request.new_password, session=session)

    # 3. Invalidate the token by deleting it
    await security.delete_reset_token(token_record=token_record, session=session)

    return {"message": "Password has been successfully reset."}