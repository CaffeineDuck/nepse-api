from typing import AsyncIterator, Optional

import httpx

from nepse.security.types import SecurityResponse
from nepse.utils import ClientWrapperHTTPX

from .security import SecurityClient


class Client:
    def __init__(self) -> None:
        self._session = httpx.AsyncClient()
        self._client_wrapper = ClientWrapperHTTPX(self._session)
        self.security_client = SecurityClient(self._client_wrapper)

    async def close(self) -> None:
        await self._session.aclose()
