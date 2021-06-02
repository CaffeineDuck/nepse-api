from typing import AsyncIterator, Optional

import httpx

from nepse.security.types import SecurityResponse
from nepse.utils import ClientWrapperHTTPX

from .security import SecurityClient


class Client:
    def __init__(
        self,
        httpx_client: Optional[httpx.AsyncClient] = None,
        use_cache: Optional[bool] = False,
        cache_retain_time: Optional[int] = 60,
    ) -> None:
        self._session = httpx_client or httpx.AsyncClient()
        self._client_wrapper = ClientWrapperHTTPX(self._session)
        self.security_client = SecurityClient(
            self._client_wrapper, cache_retain_time, use_cache
        )

    async def close(self) -> None:
        await self._session.aclose()
