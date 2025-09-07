from sqlmodel import Session
from sqlmodel.sql.expression import select
from typing import List, Optional
from app.models.users import User
from app.models.accounts import Account


def create_new_user_in_db(email: str, password: str, full_name: str,
                          account_ids: Optional[List[int]], session: Session):
    """
    Creates a new user and assigns it to multiple accounts.
    """
    user = User(email=email, password=password, full_name=full_name)
    
    if account_ids:
        # fetch accounts from DB
        accounts = session.exec(select(Account).where(Account.id.in_(account_ids))).all()
        user.accounts = accounts  # link many-to-many

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def add_user_to_accounts(user: User, account_ids: list[int], session: Session):
    """
    Adds an existing user to multiple accounts."""
    if isinstance(account_ids, int):
        account_ids = [account_ids]
    accounts = session.exec(select(Account).where(Account.id.in_(account_ids))).all()
    for account in accounts:
        user.accounts.append(account)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user



def get_users_for_account(account_unique_id: str, session: Session):
    """
    Retrives all User objects based on account_unique_id
    """
    statement = select(User).filter(Account.account_unique_id == account_unique_id)
    result = session.exec(statement)
    users = result.all()

    return users


def get_user_by_email(email: str, session: Session):
    """
    Retrieve user object by email_address
    """
    statement = select(User).filter(User.email == email)
    result = session.exec(statement)
    user = result.first()

    return user


def update_user_in_db(user: User, email: Optional[str], full_name: Optional[str], session: Session):
    """
    Update user details in the database."""
    if email:
        user.email = email
    if full_name:
        user.full_name = full_name

    session.add(user)
    session.commit()
    session.refresh(user)
    return user