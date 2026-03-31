from typing import TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BaseTable
from app.schemas.common import BaseCreateResource

T_Table = TypeVar('T_Table', bound=BaseTable)
T_CreateSchema = TypeVar('T_CreateSchema', bound=BaseCreateResource)


class BaseResourceRepo:
    def __init__(
        self,
        table: BaseTable,
        create_schema: BaseCreateResource,
    ):
        self.table = table
        self.create_schema = create_schema

    async def create(
        self,
        session: AsyncSession,
        env_data: T_CreateSchema
    ) -> T_Table:
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
        result = await session.execute(
            select(self.table)
            .where(self.table.name == name)
        )
        env = result.scalar_one_or_none()
        return env
