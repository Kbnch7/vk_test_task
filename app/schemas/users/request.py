from uuid import UUID

from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    login: str = Field(..., min_length=3, max_length=15)
    password: str = Field(..., min_length=8, max_length=128)
    project_id: UUID
    env_id: UUID
    domain_id: UUID
