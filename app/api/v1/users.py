from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.core.security import hash_password
from app.core.db import get_session
from app.models.users import User
from app.schemas.users import UserCreate, UserRead, UserReadBasic, UserUpdate
from app.utils import users as user_utils
from app.utils.auth import get_current_user

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
def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)):
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


# --- PUT update user ---
@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing user's details."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = user_utils.update_user_in_db(
        user=user,
        email=user_update.email,
        full_name=user_update.full_name,
        session=session
    )
    return user


# --- DELETE user ---
@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a user from the database."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_utils.delete_user_in_db(user=user, session=session)
    
    return {"detail": "User deleted successfully"}
