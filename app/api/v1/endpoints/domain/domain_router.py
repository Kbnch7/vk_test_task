from fastapi.routing import APIRouter

from app.api.v1.base_router import BaseResourceHandler
from app.schemas import DomainCreate, DomainResponse
from app.services.domain import domain_service

domain_router_object = BaseResourceHandler(
    "Domain",
    domain_service,
    DomainResponse,
    DomainCreate
)

domain_router = APIRouter(prefix="/domain")
domain_router.add_api_route(
    "/",
    domain_router_object.create,
    methods=["POST",],
    response_model=DomainResponse
)
domain_router.add_api_route(
    "/{resource_id}",
    domain_router_object.get_by_id,
    methods=["GET",],
    response_model=DomainResponse
)
domain_router.add_api_route(
    "/",
    domain_router_object.get_by_name,
    methods=["GET",],
    response_model=DomainResponse
)
