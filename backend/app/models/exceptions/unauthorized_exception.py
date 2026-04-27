from .logic_exception import LogicException


class UnauthorizedException(LogicException):
    def __init__(
        self,
        message: str,
        status_code: int = 401,
        extra: dict = None,
    ):
        super().__init__(
            message,
            status_code=status_code,
            extra=extra,
        )
