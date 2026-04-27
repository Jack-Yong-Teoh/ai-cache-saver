from fastapi import APIRouter
from app.models.routes.api_route import InterceptorAPIRoute
from app.controllers.prompt_image import (
    create_prompt_image,
    lazyload_prompt_images,
)

router = APIRouter(route_class=InterceptorAPIRoute)

router.add_api_route(
    "/generate",
    create_prompt_image,
    methods=["POST"],
)

router.add_api_route(
    "s",
    lazyload_prompt_images,
    methods=["POST"],
    response_model_exclude_none=True,
)
