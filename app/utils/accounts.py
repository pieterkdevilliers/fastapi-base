from secrets import token_hex
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import select
from app.models.accounts import Account

async def create_new_account_in_db(account_organisation: str, session: AsyncSession):
    """
    Generates a new account with a unique account ID and saves it to the database.
    """
    account_unique_id = token_hex(8)
    account = Account(account_organisation=account_organisation,
                      account_unique_id=account_unique_id)
    session.add(account)
    await session.commit()
    await session.refresh(account)
    
    return account


async def get_account_by_account_unique_id(account_unique_id: str,session: AsyncSession):
    """
    Retrives the Account object based on account_unique_id
    """
    statement = select(Account).filter(Account.account_unique_id == account_unique_id)
    result = await session.exec(statement)
    account = result.first()

    return account


async def update_account(account: Account, account_organisation: str, session: AsyncSession):
    """
    Updates the account's organisation name.
    """
    account.account_organisation = account_organisation
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account