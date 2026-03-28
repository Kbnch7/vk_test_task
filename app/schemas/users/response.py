from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

class UserResponse(BaseModel):
    id: UUID
    login: str
    password: str
    locktime: datetime


class UnlockUsersResponse(BaseModel):
    users_unlocked: int
