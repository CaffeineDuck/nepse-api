from typing import Optional

import aiohttp

from nepse.security.types import SecurityResponse

from .security import SecurityClient


class Client:
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()
        self._security_client = SecurityClient(self._session)

    async def get_company(
        self, id: Optional[int] = None, symbol: Optional[str] = None
    ) -> SecurityResponse:
        model = await self._security_client.get_security_response(id, symbol)
        return model

    async def close(self) -> None:
        await self._session.close()
