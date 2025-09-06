from sqlmodel import Session
from sqlmodel.sql.expression import select
from app.models.users import User


def create_new_user_in_db(email: str, password: str, account_unique_id: str, full_name: str, session: Session):
    """
    Creates a new user and saves it to the database.
    """
    user = User(email=email,
                password=password,
                account_unique_id=account_unique_id,
                full_name=full_name)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user


def get_users_for_account(account_unique_id: str, session: Session):
    """
    Retrives all User objects based on account_unique_id
    """
    statement = select(User).filter(User.account_unique_id == account_unique_id)
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