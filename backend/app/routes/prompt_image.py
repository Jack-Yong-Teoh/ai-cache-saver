from fastapi import APIRouter
from app.models.routes.api_route import InterceptorAPIRoute
from app.controllers.prompt_image import (
    create_prompt_image,
)

router = APIRouter(route_class=InterceptorAPIRoute)

router.add_api_route(
    "/generate",
    create_prompt_image,
    methods=["POST"],
)
