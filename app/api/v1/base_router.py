from typing import TypeVar
from uuid import UUID

from fastapi import Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BaseTable
from app.database.session import get_db
from app.schemas.common import BaseCreateResource, BaseResourceResponse
from app.services.base_service import BaseResourceService
from app.services.exceptions import BaseAlreadyExists, BaseNotFound, DatabaseError

T_Table = TypeVar('T_Table', bound=BaseTable)
T_GetSchema = TypeVar('T_CreateSchema', bound=BaseResourceResponse)
T_CreateSchema = TypeVar('T_CreateSchema', bound=BaseCreateResource)

class BaseResourceHandler:
    def __init__(
        self,
        resource_name: str,
        service: BaseResourceService,
        get_schema: BaseResourceResponse,
        create_schema: BaseCreateResource
    ):
        self.service = service
        self.get_schema = get_schema
        self.resource_name = resource_name
        self.create_schema = create_schema

    async def get_by_id(
        self,
        resource_id: UUID,
        session: AsyncSession = Depends(get_db)
    ) -> T_GetSchema:
        try:
            resource = await self.service.get_by_id(session, resource_id)
            return resource
        except BaseNotFound as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.resource_name} not found"
            ) from e
        except DatabaseError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed"
            ) from e

    async def get_by_name(
        self,
        name: str = Query(..., alias="name"),
        session: AsyncSession = Depends(get_db),
    ) -> T_GetSchema:
        resource_name = name
        try:
            resource = await self.service.get_by_name(session, resource_name)
            return resource
        except BaseNotFound as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.resource_name} not found"
            ) from e
        except DatabaseError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed"
            ) from e

    async def create(
        self,
        resource_data: T_CreateSchema = Body(...),
        session: AsyncSession = Depends(get_db)
    ) -> T_GetSchema:
        try:
            resource = await self.service.create(session, resource_data)
            return resource
        except BaseAlreadyExists as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{self.resource_name} already exists"
            ) from e
        except DatabaseError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed"
            ) from e
