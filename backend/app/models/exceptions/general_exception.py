class GeneralException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        extra: dict = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.extra = {} if extra is None else extra
