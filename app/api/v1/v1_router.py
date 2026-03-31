from fastapi.routing import APIRouter

from .endpoints.domain import domain_router
from .endpoints.project import project_router
from .endpoints.users import users_router
from .endpoints.users_env import users_env_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(users_router)
v1_router.include_router(domain_router)
v1_router.include_router(project_router)
v1_router.include_router(users_env_router)
