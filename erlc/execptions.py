from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from erlc.client import ErlcServerClient


class ErlcExecption(Exception):
    def __init__(self, message: str, client: "ErlcServerClient") -> None:
        self.client = client
        super().__init__(message)


class InvalidApiKey(ErlcExecption):
    def __init__(
        self, message: str = "Invalid API key", client: "ErlcServerClient" = None
    ) -> None:
        super().__init__(message, client)

    def __str__(self) -> str:
        return f"Invalid API key: {self.client.api_key if self.client else 'Unknown'}"
