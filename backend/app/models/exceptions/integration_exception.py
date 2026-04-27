from .general_exception import GeneralException


class IntegrationException(GeneralException):
    def __init__(
        self,
        message: str,
        extra: dict = None,
    ):
        super().__init__(
            message,
            extra=extra,
        )
