from .logic_exception import LogicException


class MissingCriteriaException(LogicException):
    def __init__(
        self,
        message: str,
        extra: dict = None,
    ):
        super().__init__(
            message,
            extra=extra,
        )
