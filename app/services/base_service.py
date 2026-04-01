from logging import Logger
from typing import TypeVar
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BaseTable
from app.database.repositories import BaseResourceRepo
from app.schemas.common import BaseCreateResource
from app.services.exceptions import DatabaseError

T_Table = TypeVar('T_Table', bound=BaseTable)
T_CreateSchema = TypeVar('T_CreateSchema', bound=BaseCreateResource)

class BaseResourceService:
    """
    Класс базового сервиса (Service Layer)

    Предоставляет основные методы (создать, получить по id/name)

    Attributes:
    - repo: Объект репозитория, который используется в сервисе
    - integrity_error_exception: Объект ошибки, вызываемый при IntegrityError
    - resource_not_found_error: Объект ошибки, вызываемый при ненахождении ресурса в get_by_id/get_by_name
    - logger: Объект Logger для логирования
    """  # noqa: E501
    def __init__(
        self,
        repo: BaseResourceRepo,
        integrity_error_exception: Exception,
        resource_not_found_exception: Exception,
        logger: Logger
    ):
        self.repo = repo
        self.integrity_error_exception = integrity_error_exception
        self.resource_not_found_exception = resource_not_found_exception
        self.logger = logger

    async def create(
        self,
        session: AsyncSession,
        create_schema: T_CreateSchema,
    ) -> T_Table:
        """
        Выполняет создание ресурса

        Args:
            session: Объект сессии через который будет происходить создание ресурса
            create_schema: Схема с данными, на основе которых будет создан ресурс
        Returns:
            Объект созданного ресурса
        Raises:
            integrity_error_exception: при нарушении схемы бд при создании ресурса
            DatabaseError: при неудачной попытке подключиться к бд
        """
        try:
            new_object = await self.repo.create(session, create_schema)
            await session.commit()
            await session.refresh(new_object)
            return new_object
        except IntegrityError as e:
            self.logger.error("Resource already exists")
            raise self.integrity_error_exception() from e
        except SQLAlchemyError as e:
            self.logger.error(f"Database error: {e}")
            raise DatabaseError() from e

    async def get_by_id(self, session: AsyncSession, id: UUID):
        """
        Выполняет получение ресурса по id

        Args:
            session: Объект сессии через который будет происходить получение ресурса
            id: Id ресурса, который хотим получить
        Returns:
            Объект полученного ресурса
        Raises:
            DatabaseError: при неудачной попытке подключиться к бд
        """
        try:
            resource = await self.repo.get_by_id(session, id)
            if resource is None:
                raise self.resource_not_found_exception()
            return resource
        except SQLAlchemyError as e:
            self.logger.error(f"Database error: {e}")
            raise DatabaseError() from e

    async def get_by_name(self, session: AsyncSession, name: str):
        """
        Выполняет получение ресурса по name

        Args:
            session: Объект сессии через который будет происходить получение ресурса
            id: Name ресурса, который хотим получить
        Returns:
            Объект полученного ресурса
        Raises:
            DatabaseError: при неудачной попытке подключиться к бд
        """
        try:
            resource = await self.repo.get_by_name(session, name)
            if resource is None:
                raise self.resource_not_found_exception()
            return resource
        except SQLAlchemyError as e:
            self.logger.error(f"Database error: {e}")
            raise DatabaseError() from e
