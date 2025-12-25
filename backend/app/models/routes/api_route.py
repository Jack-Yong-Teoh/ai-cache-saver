from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute


class InterceptorAPIRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                # Executes the actual controller logic
                return await original_route_handler(request)
            except Exception as e:
                # Minimal error handling to keep the project simple
                from fastapi.responses import JSONResponse

                return JSONResponse(
                    status_code=500,
                    content={
                        "detail": str(e),
                        "message": "An internal error occurred.",
                    },
                )

        return custom_route_handler
