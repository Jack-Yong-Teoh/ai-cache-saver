from app.models.exceptions import (
    LogicException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    ConflictException,
)


def responses(exceptions: list[Exception]):
    template = {
        "content": {
            "application/json": {
                "example": {
                    "message": "string",
                    "result": "error",
                }
            }
        }
    }
    # pylint: disable-next=redefined-outer-name
    responses = {}
    if Exception in exceptions:
        status_code = 500
        responses[status_code] = template
    if LogicException in exceptions:
        status_code = 400
        responses[status_code] = template
    if NotFoundException in exceptions:
        status_code = 404
        responses[status_code] = template
    if UnauthorizedException in exceptions:
        status_code = 401
        responses[status_code] = template
    if ForbiddenException in exceptions:
        status_code = 403
        responses[status_code] = template
    if ConflictException in exceptions:
        status_code = 409
        responses[status_code] = template
    return responses
