from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse

class InterceptorAPIRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
                
            except HTTPException as http_exc:
                return JSONResponse(
                    status_code=http_exc.status_code,
                    content={
                        "detail": http_exc.detail,
                        "message": "Request failed", 
                    },
                )
            
            except Exception as e:
                # Only catch unexpected crashes as 500
                return JSONResponse(
                    status_code=500,
                    content={
                        "detail": str(e),
                        "message": "An internal error occurred.",
                    },
                )

        return custom_route_handler