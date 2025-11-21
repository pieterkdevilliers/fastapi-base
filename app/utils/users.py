from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.users import User
from app.models.accounts import Account
from app.models.associations import UserAccountLink


async def create_new_user_in_db(
        email: str,
        password: str,
        full_name: str,
        account_ids: Optional[List[int]],
        session: AsyncSession):
    """
    Creates a new user and assigns it to multiple accounts.
    """
    user = User(email=email, password=password, full_name=full_name)
    
    if account_ids:
        # fetch accounts from DB
        accounts = await session.exec(select(Account).where(Account.id.in_(account_ids)))
        user.accounts = accounts.all()

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def add_user_to_accounts(user: User, account_ids: list[int], session: AsyncSession):
    """
    Adds an existing user to multiple accounts."""
    if isinstance(account_ids, int):
        account_ids = [account_ids]
    result = await session.exec(select(Account).where(Account.id.in_(account_ids)))
    accounts = result.all()
    for account in accounts:
        user.accounts.append(account)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def remove_user_from_account(user: User, account_id: int, session: AsyncSession):
    """
    Removes a user from a specific account by ID.
    """
    account = await session.get(Account, account_id)
    if account and account in user.accounts:
        user.accounts.remove(account)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user




async def get_users_for_account(account_unique_id: str, session: AsyncSession):
    """
    Retrieves all User objects related to a given account_unique_id.
    """
    statement = (
        select(User)
        .join(UserAccountLink, UserAccountLink.user_id == User.id)
        .join(Account, UserAccountLink.account_id == Account.id)
        .where(Account.account_unique_id == account_unique_id)
        .options(selectinload(User.accounts))  # eager load accounts if needed
    )

    result = await session.exec(statement)
    users = result.all()
    return users


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    """
    Retrieve a user object by email, eagerly loading their accounts.
    """
    statement = select(User).options(selectinload(User.accounts)).where(User.email == email)
    result = await session.exec(statement)
    user = result.first()
    return user


async def get_user_with_accounts_by_email(email: str, session: AsyncSession) -> User | None:
    """
    Retrieve a user by email, eagerly loading their associated accounts."""
    statement = (
        select(User)
        .options(selectinload(User.accounts))
        .where(User.email == email)
    )
    result = await session.exec(statement)
    return result.first()


async def get_user_with_accounts_by_id(user_id: int, session: AsyncSession) -> User | None:
    """
    Retrieve a user by ID, eagerly loading their associated accounts.
    """
    statement = (
        select(User)
        .options(selectinload(User.accounts))
        .where(User.id == user_id)
    )
    result = await session.exec(statement)
    return result.first()


async def get_user_with_accounts(user_id: int, session: AsyncSession) -> User | None:
    """
    Retrieve a user by ID, eagerly loading their associated accounts.
    """
    statement = select(User).options(selectinload(User.accounts)).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()
    return user


async def update_user_in_db(user: User, email: Optional[str], full_name: Optional[str], session: AsyncSession):
    """
    Update user details in the database."""
    if email:
        user.email = email
    if full_name:
        user.full_name = full_name

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user_in_db(user: User, session: AsyncSession):
    """
    Deletes a user from the database."""
    await session.delete(user)
    await session.commit()
    return


async def get_orphaned_users_to_delete(account: Account, session: AsyncSession):
    """
    Retrieves users who would be orphaned when an account is deleted.
    """
    statement = select(Account).options(selectinload(Account.users)).where(Account.id == account.id)
    result = await session.exec(statement)
    account = result.one_or_none()

    if not account:
        return []
    orphaned_users = []
    for user in account.users:
        if len(user.accounts) == 1 and user.accounts[0].id == account.id:
            orphaned_users.append(user)
    return orphaned_users