"""
Модуль для создания сервиса проектов
"""
from app.database.repositories import project_repo
from app.services import logger
from app.services.base_service import BaseResourceService
from app.services.exceptions import ProjectAlreadyExists, ProjectNotFound

project_service = BaseResourceService(
    project_repo,
    ProjectAlreadyExists,
    ProjectNotFound,
    logger
)
