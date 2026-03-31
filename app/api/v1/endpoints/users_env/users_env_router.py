from fastapi.routing import APIRouter

from app.api.v1.base_router import BaseResourceHandler
from app.schemas import EnvCreate, EnvResponse
from app.services.users_env import env_service

users_env_router_object = BaseResourceHandler(
    "Env",
    env_service,
    EnvResponse,
    EnvCreate
)

users_env_router = APIRouter(prefix="/env")
users_env_router.add_api_route(
    "/",
    users_env_router_object.create,
    methods=["POST",],
    response_model=EnvResponse
)
users_env_router.add_api_route(
    "/{resource_id}",
    users_env_router_object.get_by_id,
    methods=["GET",],
    response_model=EnvResponse
)
users_env_router.add_api_route(
    "/",
    users_env_router_object.get_by_name,
    methods=["GET",],
    response_model=EnvResponse
)
