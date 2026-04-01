"""
Модуль для создания сервиса доменов
"""
from app.database.repositories import domain_repo
from app.services import logger
from app.services.base_service import BaseResourceService
from app.services.exceptions import DomainAlreadyExists, DomainNotFound

domain_service = BaseResourceService(
    domain_repo,
    DomainAlreadyExists,
    DomainNotFound,
    logger
)
