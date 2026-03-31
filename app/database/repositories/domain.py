from app.database.models import Domain
from app.database.repositories.base_repo import BaseResourceRepo
from app.schemas.domain import DomainCreate

domain_repo = BaseResourceRepo(Domain, DomainCreate)
