from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.core.security import hash_password
from app.core.db import get_session
from app.models.users import User
from app.schemas.users import UserCreate, UserRead, UserReadBasic
from app.utils import users as user_utils
from app.api.v1.auth import get_current_user

router = APIRouter()

# --- GET all users for a specific account ---
@router.get("/{account_unique_id}", response_model=List[UserReadBasic])
def list_users(
    account_unique_id: str, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)):
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
    Create a new user in the database and assign to multiple accounts.
    """
    existing_user = user_utils.get_user_by_email(email=user.email, session=session)
    if existing_user:
        user_utils.add_user_to_accounts(
            user=existing_user,
            account_ids=user.account_ids[0],  # assuming at least one account is provided
            session=session
        )
        return existing_user

    new_user = user_utils.create_new_user_in_db(
        email=user.email,
        password=hash_password(user.password),
        full_name=user.full_name,
        account_ids=user.account_ids,
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
