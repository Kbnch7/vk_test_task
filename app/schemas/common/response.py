from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class BaseResourceResponse(BaseModel):
    id: UUID
    name: str
