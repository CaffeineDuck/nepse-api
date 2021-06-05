from typing import Optional

import httpx

from nepse.broker.core import BrokerClient
from nepse.market.core import MarketClient
from nepse.utils import _ClientWrapperHTTPX

from .security import SecurityClient


class Client:
    def __init__(
        self,
        httpx_client: Optional[httpx.AsyncClient] = None,
        use_cache: Optional[bool] = False,
        cache_retain_time: Optional[int] = 60,
    ) -> None:
        self._session = httpx_client or httpx.AsyncClient()
        self._client_wrapper = _ClientWrapperHTTPX(self._session)
        self._security_client = SecurityClient(
            self._client_wrapper, cache_retain_time, use_cache
        )
        self._market_client = MarketClient(self._client_wrapper)
        self._broker_client = BrokerClient(
            self._client_wrapper, use_cache, cache_retain_time
        )

    @property
    def broker_client(self) -> BrokerClient:
        """Returns the initialized `BrokerClient`

        Returns:
            BrokerClient: It is the module through which you can interact with
            API's brokers.
        """
        return self._broker_client

    @property
    def security_client(self) -> SecurityClient:
        """Returns the initialized `SecurityClient`

        Returns:
            SecurityClient: It is the module through which you can interact with
            API's securities and its data.
        """
        return self._security_client

    @property
    def market_client(self) -> MarketClient:
        """Returns the initialized `MarketClient`

        Returns:
            MarketClient: It is the module through which you can interact with
            NEPSE's Market.
        """
        return self._market_client

    async def close(self) -> None:
        """Properly disposes the session"""
        await self._session.aclose()
