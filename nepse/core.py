from typing import AsyncIterator, Optional

import httpx

from nepse.security.types import SecurityResponse
from nepse.utils import ClientWrapperHTTPX

from .security import SecurityClient


class Client:
    def __init__(self) -> None:
        self._session = httpx.AsyncClient()
        self._client_wrapper = ClientWrapperHTTPX(self._session)
        self._security_client = SecurityClient(self._client_wrapper)
        

    async def companies(self) -> AsyncIterator[SecurityResponse]:
        base_securities = self._security_client._securities_basic_cache.values()
        if not base_securities:
            await self._security_client.fetch_all_base_securities()

        for security in base_securities:
            yield await self._security_client.fetch_security_response(security.id)

    async def get_company(
        self, id: Optional[int] = None, symbol: Optional[str] = None
    ) -> SecurityResponse:
        model = await self._security_client.get_security_response(id, symbol)
        return model

    async def close(self) -> None:
        await self._session.aclose()
