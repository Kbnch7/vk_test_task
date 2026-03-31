from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas import UserResponse
from app.services.exceptions import (
    DatabaseError,
)
from app.services.users import user_service

from .users_router import users_router


@users_router.get(
    '/',
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK
)
async def get_users_handler(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: AsyncSession = Depends(get_db)
) -> list[UserResponse]:
    try:
        users = await user_service.get_users(session, limit, skip)
        return users
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        ) from e
