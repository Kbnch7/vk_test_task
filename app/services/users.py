"""
Модуль для создания сервиса пользователей
"""
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repositories import users_repo
from app.schemas.users import UserCreate
from app.services import logger
from app.services.base_service import BaseResourceService
from app.services.exceptions import UserAlreadyExistsError
from app.utils.security import (
    decrypt_password,
    decrypt_users_password,
    encrypt_password,
)

from .exceptions import DatabaseError, NoAvailiableUserError


class UserService(BaseResourceService):
    async def get_by_id(self, *args, **kwargs):  # noqa: ARG002
        raise AttributeError("method not allowed")

    async def get_by_name(self, *args, **kwargs):  # noqa: ARG002
        raise AttributeError("method not allowed")

    async def create(
        self,
        session: AsyncSession,
        user_data: UserCreate,
    ) -> User:
        encrypted_password = encrypt_password(user_data.password)
        user_data.password = encrypted_password

        try:
            async with session.begin():
                user =  await users_repo.create(session, user_data)
            user.password = decrypt_password(user.password)
            return user
        except IntegrityError as e:
            raise self.integrity_error_exception("User already exists") from e
        except SQLAlchemyError as e:
            self.logger.error("Database connection failed")
            raise DatabaseError() from e

    async def get_users(
        self,
        session: AsyncSession,
        limit: int,
        skip: int,
    ) -> list[User]:
        try:
            users = await users_repo.get_users(session, limit, skip)
            users_with_decrypted_passwords = decrypt_users_password(users)
            return users_with_decrypted_passwords
        except SQLAlchemyError as e:
            self.logger.error("Database connection failed")
            raise DatabaseError() from e

    async def lock_first_avaliable_user(
            self,
            session: AsyncSession,
            days_to_lock: int = 0,
            hours_to_lock: int = 1,
        ) -> User:
        try:
            async with session.begin():
                user = await users_repo.lock_user(
                    session,
                    days_to_lock,
                    hours_to_lock
                )
                if user is None:
                    raise NoAvailiableUserError()
            user.password = decrypt_password(user.password)
            return user
        except SQLAlchemyError as e:
            self.logger.error("Database connection failed")
            raise DatabaseError() from e

    async def unlock_users(self, session: AsyncSession):
        try:
            async with session.begin():
                amount_of_users = await users_repo.unlock_users(session)
                return amount_of_users
        except SQLAlchemyError as e:
            self.logger.error("Database connection failed")
            raise DatabaseError() from e

user_service = UserService(users_repo, UserAlreadyExistsError, Exception, logger)
