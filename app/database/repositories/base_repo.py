from typing import TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BaseTable
from app.schemas.common import BaseCreateResource

T_Table = TypeVar('T_Table', bound=BaseTable)
T_CreateSchema = TypeVar('T_CreateSchema', bound=BaseCreateResource)


class BaseResourceRepo:
    """
    Класс базового репозитория (Repositery Layer)

    Предоставляет основные методы (создать, получить по id/name)

    Attributes:
    - table: Объект таблицы, в которой будет создан ресурс
    """
    def __init__(
        self,
        table: BaseTable,
    ):
        self.table = table

    async def create(
        self,
        session: AsyncSession,
        env_data: T_CreateSchema
    ) -> T_Table:
        """
        Выполняет создание ресурса

        Args:
            session: Объект сессии через который будет происходить создание ресурса
            create_schema: Схема с данными, на основе которых будет создан ресурс
        Returns:
            Объект созданного ресурса
        Raises:
            IntegrityError: при нарушении схемы бд при создании ресурса
            SQLAlchemyError: при неудачной попытке подключиться к бд
        """
        new_object = self.table(**env_data.model_dump())
        session.add(new_object)
        await session.flush()
        await session.refresh(new_object)
        return new_object

    async def get_by_id(
        self,
        session: AsyncSession,
        id: UUID
    ) -> T_Table:
        """
        Выполняет получение ресурса по id

        Args:
            session: Объект сессии через который будет происходить получение ресурса
            id: Идентификатор ресурса, который хотим получить
        Returns:
            Объект полученного ресурса
        Raises:
            SQLAlchemyError: при неудачной попытке подключиться к бд
        """
        result = await session.execute(
            select(self.table)
            .where(self.table.id == id)
        )
        env = result.scalar_one_or_none()
        return env

    async def get_by_name(
        self,
        session: AsyncSession,
        name: str
    ) -> T_Table:
        """
        Выполняет получение ресурса по name

        Args:
            session: Объект сессии через который будет происходить получение ресурса
            name: name ресурса, который хотим получить
        Returns:
            Объект полученного ресурса
        Raises:
            SQLAlchemyError: при неудачной попытке подключиться к бд
        """
        result = await session.execute(
            select(self.table)
            .where(self.table.name == name)
        )
        env = result.scalar_one_or_none()
        return env
