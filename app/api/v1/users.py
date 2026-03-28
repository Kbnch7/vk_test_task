from typing import List

from fastapi import APIRouter, Depends, status, Query, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.users import create_user_service, get_users_service, lock_first_avaliable_user_service, unlock_users_service
from app.database import get_db
from app.schemas.users import UserResponse, UserCreate, UnlockUsersResponse
from app.schemas.common import Message
from app.services.exceptions import UserAlreadyExistsError, DatabaseError, NoAvailiableUserError

'''
POST /users/
GET /users/
POST /users/lock/
POST /users/unlock/
'''

users_router = APIRouter()

@users_router.post(
    '/',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user_handler(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        user = await create_user_service(db, user_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
    else:
        return user

@users_router.get(
    '/',
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK    
)
async def get_users_handler(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
) -> List[UserResponse]:
    try:
        users = await get_users_service(db, limit, skip)
        return users
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )

@users_router.patch('/lock/', response_model=UserResponse)
async def lock_first_availible_user_handler(
    days_to_lock: int = Body(0, ge=0),
    hours_to_lock: int = Body(1, ge=0),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        user = await lock_first_avaliable_user_service(db, days_to_lock, hours_to_lock)
        return user
    except NoAvailiableUserError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No availible user found"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )

@users_router.post('/unlock/', response_model=UnlockUsersResponse)
async def unlock_users_handler(
    db: AsyncSession = Depends(get_db)
) -> Message:
    try:
        amount_of_users = await unlock_users_service(db)
        return UnlockUsersResponse(users_unlocked=amount_of_users)
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
