from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.core.db import get_session
from app.models.accounts import Account
from app.models.users import User
from app.schemas.accounts import AccountCreate, AccountRead, AccountUpdate
from app.schemas.users import UserCreate, UserReadBasic
from app.utils import accounts as account_utils
from app.utils import users as user_utils
from app.api.v1.auth import get_current_user
from app.core.security import hash_password

router = APIRouter()

# --- GET all accounts for the current user ---
@router.get("/", response_model=List[AccountRead])
def list_accounts(
    current_user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    """
    Retrieve all accounts for the currently logged-in user.
    """
    # assuming a many-to-many relationship: user.accounts
    accounts = current_user.accounts  # this will already be a list of Account objects
    return accounts


# --- POST create a new account ---
@router.post("/", response_model=AccountRead)
def create_account(
    account: AccountCreate,
    user: UserCreate,
    session: Session = Depends(get_session)):
    """
    Create a new account in the database."""
    account = account_utils.create_new_account_in_db(
        account_organisation=account.account_organisation,
        session=session
    )

    user = user_utils.create_new_user_in_db(
        email=user.email,
        password=hash_password(user.password),
        full_name=user.full_name,
        account_ids=[account.id],
        session=session
    )

    return account


# --- Updte account ---
@router.put("/{account_unique_id}", response_model=AccountRead)
def update_account(
    account_unique_id: str,
    account_update: AccountUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing account's details."""
    account = account_utils.get_account_by_account_unique_id(
        account_unique_id=account_unique_id,
        session=session
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account = account_utils.update_account(
        account=account,
        account_organisation=account_update.account_organisation or account.account_organisation,
        session=session
    )
    
    return account


# --- GET single account by ID ---
@router.get("/{account_unique_id}", response_model=AccountRead)
def get_account(account_unique_id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Retrieve a single account by its account_unique_id."""
    account = account_utils.get_account_by_account_unique_id(
        account_unique_id=account_unique_id,
        session=session
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
