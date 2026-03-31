from uuid import UUID

from pydantic import BaseModel, Field


class BaseGetResourceById(BaseModel):
    id: UUID


class BaseGetResourceByName(BaseModel):
    name: str


class BaseCreateResource(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)


class BaseGetResourceResponse(BaseModel):
    id: UUID
    name: str = Field(..., min_length=3, max_length=20)
