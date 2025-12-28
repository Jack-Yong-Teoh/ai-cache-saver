from fastapi import APIRouter
from app.models.routes.api_route import InterceptorAPIRoute
from app.controllers.authentication import signup, login, logout, refresh

router = APIRouter(route_class=InterceptorAPIRoute)

router.add_api_route(
    "/signup",
    signup,
    methods=["POST"],
)

router.add_api_route(
    "/login",
    login,
    methods=["POST"],
)

router.add_api_route(
    "/logout",
    logout,
    methods=["POST"],
)

router.add_api_route(
    "/refresh",
    refresh,
    methods=["POST"],
)
