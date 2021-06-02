from nepse.market.core import MarketClient
from typing import  Optional

import httpx

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
        self._security_client = SecurityClient(
            self._client_wrapper, cache_retain_time, use_cache
        )
        self._market_client = MarketClient(self._client_wrapper)

    @property
    def security_client(self) -> SecurityClient:
        return self._security_client

    @property
    def market_client(self) -> MarketClient:
        return self._market_client

    async def close(self) -> None:
        await self._session.aclose()
