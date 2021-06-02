from typing import AsyncIterator, Generator, List, Optional

import humps
from cachetools import LRUCache, TTLCache

from nepse.errors import NotFound, SymbolOrIdNotPassed
from nepse.security.decorators import is_cached
from nepse.security.types import BaseSecurity, SecurityResponse
from nepse.utils import ClientWrapperHTTPX

BASE_URL = "https://newweb.nepalstock.com/api/nots/security"


class SecurityClient:
    def __init__(
        self,
        client_wrapper: ClientWrapperHTTPX,
        cache_retain_time: Optional[int] = 60,
        use_cache: Optional[bool] = False,
    ) -> None:
        self._client_wrapper = client_wrapper
        self._securities_basic_cache = LRUCache(1000)
        self._securities_full_cache = TTLCache(100, cache_retain_time)
        self._use_cache = use_cache

    def _create_security_model(self, model: BaseSecurity) -> None:
        self._securities_basic_cache[model.symbol] = model

    def _get_security_model(self, symbol: str) -> BaseSecurity:
        return self._securities_basic_cache.get(symbol)

    def _create_security_cache(self, model: SecurityResponse) -> None:
        self._securities_full_cache[model.security_id] = model

    def _get_security_cache(self, security_id: int) -> SecurityResponse:
        return self._securities_full_cache.get(security_id)

    async def _update_basic_securities_cache(self) -> None:
        await self._fetch_all_base_securities()

    async def _fetch_all_base_securities(self) -> List[BaseSecurity]:
        securities = await self._client_wrapper.get_json(BASE_URL)

        def create_security_object(security: dict):
            data = humps.decamelize(security)
            model = BaseSecurity(**data)
            self._create_security_model(model)
            return model

        securities_objects = [
            create_security_object(security) for security in securities
        ]
        return securities_objects

    async def _fetch_company(self, id: int):
        data = await self._client_wrapper.get_json(f"{BASE_URL}/{id}")
        if not data:
            raise NotFound()

        data = humps.decamelize(data)

        model = SecurityResponse(**data)
        self._create_security_cache(model)
        return model

    @is_cached
    async def _get_or_fetch_company(
        self,
        id: Optional[int] = None,
        symbol: Optional[str] = None,
        use_cache: Optional[bool] = None,
    ) -> SecurityResponse:
        use_cache = use_cache or self._use_cache

        if not any(id or symbol):
            raise SymbolOrIdNotPassed()

        if not id:
            model = self._get_security_model(symbol)
            if not model:
                raise NotFound()
            id = model.id

        if use_cache:
            model = self._get_security_cache(id)
            if not model:
                model = await self._fetch_company(id)
        else:
            model = await self._fetch_company(id)

        return model

    # Used a different function for better type support
    # As the `@is_cached` decorator messes that up!
    async def get_company(
        self,
        id: Optional[int] = None,
        symbol: Optional[str] = None,
        use_cache: Optional[bool] = None,
    ) -> SecurityResponse:
        return await self._get_or_fetch_company(id, symbol, use_cache)

    async def get_full_companies(self) -> AsyncIterator[SecurityResponse]:
        base_securities = self._security_client._securities_basic_cache.values()
        if not base_securities:
            await self._fetch_all_base_securities()

        for security in base_securities:
            yield await self._fetch_company(security.id)

    @is_cached
    def get_companies(self) -> List[BaseSecurity]:
        base_securities = self._security_client._securities_basic_cache.values()
        return base_securities
