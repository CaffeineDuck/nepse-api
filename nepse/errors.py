class NepseException(Exception):
    def __init__(self) -> None:
        self.stop_code = True

    def __str__(self) -> str:
        raise NotImplementedError()


class SymbolOrIdNotPassed(NepseException):
    def __str__(self) -> str:
        return "Neither symbol nor ID was passed for fetching the security!"


class NotFound(NepseException):
    def __str__(self) -> str:
        return "The given details was not found!"
