from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.schemas.users import UserCreate
from app.database.models import User
from app.database.repositories import create_user_repo, get_users_repo, lock_user_repo, unlock_users_repo
from app.utils.security import encrypt_password, decrypt_password, decrypt_users_password
from .exceptions import UserAlreadyExistsError, DatabaseError, NoAvailiableUserError
from app.services import logger


async def create_user_service(db: AsyncSession, user_data: UserCreate) -> User:
    encrypted_password = encrypt_password(user_data.password)
    user_data.password = encrypted_password
    
    try:
        async with db.begin():
            user =  await create_user_repo(db, user_data)
        user.password = decrypt_password(user.password)
        return user
    except IntegrityError:
        raise UserAlreadyExistsError("User already exists")
    except SQLAlchemyError:
        logger.error("Database connection failed")
        raise DatabaseError()

async def get_users_service(db: AsyncSession, limit: int, skip: int) -> List[User]:
    try:
        users = await get_users_repo(db, limit, skip)
        users_with_decrypted_passwords = decrypt_users_password(users)
        return users_with_decrypted_passwords
    except SQLAlchemyError:
        raise DatabaseError()

async def lock_first_avaliable_user_service(db: AsyncSession, days_to_lock: int = 0, hours_to_lock: int = 1) -> User:
    try:
        async with db.begin():
            user = await lock_user_repo(db, days_to_lock, hours_to_lock)
            if user is None:
                raise NoAvailiableUserError()
        user.password = decrypt_password(user.password)
        return user
    except SQLAlchemyError:
        logger.error("Database connection failed")
        raise DatabaseError()
    
async def unlock_users_service(db: AsyncSession):
    try:
        async with db.begin():
            amount_of_users = await unlock_users_repo(db)
            return amount_of_users
    except SQLAlchemyError:
        logger.error("Database connection failed")
        raise DatabaseError()
