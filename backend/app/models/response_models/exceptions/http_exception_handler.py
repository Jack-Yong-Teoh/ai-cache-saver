from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from app.models.exceptions import LogicException
from app.utilities.logger import logger


class HTTPExceptionHandler(HTTPException):
    @staticmethod
    # pylint: disable-next=unused-argument
    async def handler(request: Request, e: HTTPException):
        logger.error(e.detail)
        if e.status_code == 422 and "message" in e.detail:
            return JSONResponse(
                content={**e.detail, "result": "error"},
                status_code=e.status_code,
            )

        return JSONResponse(
            content={"message": e.detail, "result": "error"},
            status_code=e.status_code,
        )


class RequestValidationErrorHandler(RequestValidationError):
    @staticmethod
    # pylint: disable-next=unused-argument
    async def handler(request: Request, e: RequestValidationError):
        logger.error(str(e))
        return JSONResponse(
            content={"message": str(e), "result": "error", "detail": e.errors()},
            status_code=422,
        )


class LogicExceptionHandler:
    @staticmethod
    # pylint: disable-next=unused-argument
    async def handler(request: Request, e: LogicException):
        logger.error(str(e), extra={"extra": e.extra if hasattr(e, "extra") else None})
        return JSONResponse(
            content={"message": str(e), "result": "error"},
            status_code=e.status_code,
        )


class ExceptionHandler:
    @staticmethod
    # pylint: disable-next=unused-argument
    async def handler(request: Request, e: Exception):
        if isinstance(e, HTTPException):
            logger.error(e.detail)
            if e.status_code == 422:
                message = e.detail.get("message") if "message" in e.detail else ""
                detail = e.detail.get("detail") if "detail" in e.detail else e.detail
                return JSONResponse(
                    content={
                        "message": message,
                        "result": "error",
                        "detail": detail,
                    },
                    status_code=e.status_code,
                )
            return JSONResponse(
                content="e.detail",
                status_code=e.status_code,
            )

        try:
            traceback = e.__traceback__
        except:
            traceback = None

        logger.error(str(e), extra={"traceback": traceback})
        return JSONResponse(
            content={"message": "Something went wrong!", "result": "error"},
            status_code=500,
        )
