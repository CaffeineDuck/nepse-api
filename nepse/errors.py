class NepseException(Exception):
    def __init__(self) -> None:
        self._stop_code = True

    def __str__(self) -> str:
        raise NotImplementedError()


class NotFound(NepseException):
    def __str__(self) -> str:
        return "The Company name Provided was not found !"


class APIError(NepseException):
    def __str__(self) -> str:
        return "The data couldn't be fetched from the NEPSE API for this"
