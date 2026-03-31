
from app.database.repositories import env_repo
from app.services import logger
from app.services.base_service import BaseResourceService
from app.services.exceptions import EnvAlreadyExists, EnvNotFound

env_service = BaseResourceService(
    env_repo,
    EnvAlreadyExists,
    EnvNotFound,
    logger
)
