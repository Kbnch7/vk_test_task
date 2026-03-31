from fastapi.routing import APIRouter

from app.api.v1.base_router import BaseResourceHandler
from app.schemas import ProjectCreate, ProjectResponse
from app.services.project import project_service

project_router_object = BaseResourceHandler(
    "Project",
    project_service,
    ProjectResponse,
    ProjectCreate
)

project_router = APIRouter(prefix="/project")
project_router.add_api_route(
    "/",
    project_router_object.create,
    methods=["POST",],
    response_model=ProjectResponse
)
project_router.add_api_route(
    "/{resource_id}",
    project_router_object.get_by_id,
    methods=["GET",],
    response_model=ProjectResponse
)
project_router.add_api_route(
    "/",
    project_router_object.get_by_name,
    methods=["GET",],
    response_model=ProjectResponse
)
