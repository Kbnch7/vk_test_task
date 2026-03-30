from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: UUID
    login: EmailStr
    password: str
    locktime: datetime


class UnlockUsersResponse(BaseModel):
    users_unlocked: int
