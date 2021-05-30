class SymbolOrIdNotPassed(Exception):
    def __str__(self) -> str:
        return "Neither symbol nor ID was passed for fetching the security!"


class NotFound(Exception):
    def __str__(self) -> str:
        return "The given details was not found!"
