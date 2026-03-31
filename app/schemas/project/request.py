from app.schemas.common import (
    BaseCreateResource,
    BaseGetResourceById,
    BaseGetResourceByName,
)


class ProjectCreate(BaseCreateResource):
    ...


class GetDomainById(BaseGetResourceById):
    ...


class GetDomainByName(BaseGetResourceByName):
    ...
