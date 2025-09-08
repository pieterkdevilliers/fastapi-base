from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from app.core.security import hash_password
from app.core.db import get_session
from app.models.users import User
from app.schemas.users import UserCreate, UserRead, UserReadBasic, UserUpdate, UserToAccount, MessageResponse
from app.utils import users as user_utils
from app.utils.auth import get_current_user

router = APIRouter()

# --- GET all users for a specific account ---
@router.get("/{account_unique_id}", response_model=List[UserReadBasic])
async def list_users(
    account_unique_id: str, 
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)):
    """
    Retrieve all users for a specific account from the database."""
    users = await user_utils.get_users_for_account(
        account_unique_id=account_unique_id,
        session=session
    )
    return users


# --- GET user by ID ---
@router.get("/get-user/{user_id}", response_model=UserReadBasic)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieve a user by ID from the database."""
    user = await session.get(User, user_id)
    print("User fetched:", user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- POST create a new user ---
@router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_user), 
    session: AsyncSession = Depends(get_session)):
    """
    Create a new user in the database and assign to multiple accounts.
    """
    existing_user = await user_utils.get_user_by_email(email=user.email, session=session)
    if existing_user:
        await user_utils.add_user_to_accounts(
            user=existing_user,
            account_ids=user.account_ids[0],  # assuming at least one account is provided
            session=session
        )
        return existing_user

    new_user = await user_utils.create_new_user_in_db(
        email=user.email,
        password=hash_password(user.password),
        full_name=user.full_name,
        account_ids=user.account_ids,
        session=session
    )
    return new_user


# --- PUT update user ---
@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update an existing user's details."""
    user = await user_utils.get_user_with_accounts(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = await user_utils.update_user_in_db(
        user=user,
        email=user_update.email,
        full_name=user_update.full_name,
        session=session
    )
    return user


# ---PUT add user to account ---
@router.put("/add-user-to-account/", response_model=UserRead)
async def add_user_to_account(
    account_id: List[int],
    user: UserToAccount,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Add a user to an existing account.
    If the user does not exist, create a new user and add to the account.
    """
    existing_user = await user_utils.get_user_with_accounts_by_email(email=user.email, session=session)
    if existing_user:
        await user_utils.add_user_to_accounts(
            user=existing_user,
            account_ids=account_id,  # assuming at least one account is provided
            session=session
        )
        return await user_utils.get_user_with_accounts_by_id(existing_user.id, session)

    new_user = await user_utils.create_new_user_in_db(
        email=user.email,
        password=hash_password(user.password),
        full_name=user.full_name,
        account_ids=account_id,
        session=session
    )
    return await user_utils.get_user_with_accounts_by_id(new_user.id, session)


# ---PUT remove user from account ---
@router.put("/remove-user-from-account/", response_model=MessageResponse)
async def remove_user_from_account(
    user_id: int,
    account_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Remove a user from an account.
    """
    user = await user_utils.get_user_with_accounts_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user_utils.remove_user_from_account(
        user=user,
        account_id=account_id,
        session=session
    )

    if len(user.accounts) == 0:
        await user_utils.delete_user_in_db(user=user, session=session)

    return {"message": "User removed from account successfully"}



# --- DELETE user ---
@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a user from the database."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user_utils.delete_user_in_db(user=user, session=session)
    
    return {"detail": "User deleted successfully"}
