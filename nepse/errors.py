class SymbolOrIdNotPassed(Exception):
    def __str__(self) -> str:
        return "Neither symbol nor ID was passed for fetching the security!"
