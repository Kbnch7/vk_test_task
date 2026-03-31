from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas import UserCreate, UserResponse
from app.services.exceptions import (
    DatabaseError,
    UserAlreadyExistsError,
)
from app.services.users import user_service

from .users_router import users_router


@users_router.post(
    '/',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user_handler(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        user = await user_service.create(session, user_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        ) from e
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        ) from e
    else:
        return user
