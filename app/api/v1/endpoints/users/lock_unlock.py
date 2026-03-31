from fastapi import Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import logger
from app.database.session import get_db
from app.schemas import Message, UnlockUsersResponse, UserResponse
from app.services.exceptions import (
    DatabaseError,
    NoAvailiableUserError,
)
from app.services.users import user_service

from .users_router import users_router


@users_router.patch('/lock', response_model=UserResponse)
async def lock_first_availible_user_handler(
    days_to_lock: int = Body(0, ge=0),
    hours_to_lock: int = Body(1, ge=0),
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        user = await user_service.lock_first_avaliable_user(
            session,
            days_to_lock,
            hours_to_lock
        )
        return user
    except NoAvailiableUserError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No availible user found"
        ) from e
    except DatabaseError as e:
        logger.error("Database connection failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        ) from e

@users_router.patch('/unlock', response_model=UnlockUsersResponse)
async def unlock_users_handler(session: AsyncSession = Depends(get_db)) -> Message:
    try:
        amount_of_users = await user_service.unlock_users(session)
        return UnlockUsersResponse(users_unlocked=amount_of_users)
    except DatabaseError as e:
        logger.error("Database connection failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        ) from e
