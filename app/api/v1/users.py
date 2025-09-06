from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.core.security import hash_password
from app.core.db import get_session
from app.models.users import User
from app.schemas.users import UserCreate, UserRead
from app.utils import users as user_utils

router = APIRouter()

# --- GET all users for a specific account ---
@router.get("/{account_unique_id}", response_model=List[UserRead])
def list_users(account_unique_id: str, session: Session = Depends(get_session)):
    """
    Retrieve all users for a specific account from the database."""
    users = user_utils.get_users_for_account(
        account_unique_id=account_unique_id,
        session=session
    )
    return users

# --- POST create a new user ---
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    Create a new user in the database."""
    existing_user = user_utils.get_user_by_email(
        email=user.email,
        session=session
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = user_utils.create_new_user_in_db(
        email = user.email,
        password = hash_password(user.password),
        account_unique_id = user.account_unique_id,
        full_name = user.full_name,
        session=session
    )
    return new_user


# # --- GET single account by ID ---
# @router.get("/{account_unique_id}", response_model=AccountRead)
# def get_account(account_unique_id: str, session: Session = Depends(get_session)):
#     """
#     Retrieve a single account by its account_unique_id."""
#     account = account_utils.get_account_by_account_unique_id(
#         account_unique_id=account_unique_id,
#         session=session
#     )
#     if not account:
#         raise HTTPException(status_code=404, detail="Account not found")
#     return account
