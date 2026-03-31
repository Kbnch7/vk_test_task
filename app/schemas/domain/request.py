from app.schemas.common import (
    BaseCreateResource,
    BaseGetResourceById,
    BaseGetResourceByName,
)


class DomainCreate(BaseCreateResource):
    ...


class GetDomainById(BaseGetResourceById):
    ...


class GetDomainByName(BaseGetResourceByName):
    ...
