from .unauthorized_exception import UnauthorizedException


class ForbiddenException(UnauthorizedException):
    def __init__(
        self,
        message: str,
        status_code: int = 403,
        extra: dict = None,
    ):
        super().__init__(
            message,
            status_code=status_code,
            extra=extra,
        )
