from typing import List, Optional

import humps
from cachetools import LRUCache, TTLCache

from nepse.errors import NotFound, SymbolOrIdNotPassed
from nepse.security.decorators import is_cached
from nepse.security.types import BaseSecurity, SecurityResponse
from nepse.utils import ClientWrapperHTTPX

BASE_URL = "https://newweb.nepalstock.com/api/nots/security"


class SecurityClient:
    def __init__(self, client_wrapper: ClientWrapperHTTPX) -> None:
        self._client_wrapper = client_wrapper
        self._securities_basic_cache = LRUCache(1000)
        self._securities_full_cache = TTLCache(100, 500)

    def create_security_model(self, model: BaseSecurity) -> None:
        self._securities_basic_cache[model.symbol] = model

    def get_security_model(self, symbol: str) -> BaseSecurity:
        return self._securities_basic_cache.get(symbol)

    def create_security_cache(self, model: SecurityResponse) -> None:
        self._securities_full_cache[model.security_id] = model

    def get_security_cache(self, security_id: int) -> SecurityResponse:
        return self._securities_full_cache.get(security_id)

    async def _update_basic_securities_cache(self) -> None:
        await self.fetch_all_base_securities()

    async def fetch_all_base_securities(self) -> List[BaseSecurity]:
        securities = await self._client_wrapper.get_json(BASE_URL)

        def create_security_object(security: dict):
            data = humps.decamelize(security)
            model = BaseSecurity(**data)
            self.create_security_model(model)
            return model

        securities_objects = [
            create_security_object(security) for security in securities
        ]
        return securities_objects

    @is_cached
    async def get_security_response(
        self, id: Optional[int], symbol: Optional[str]
    ) -> SecurityResponse:
        if not any(id or symbol):
            raise SymbolOrIdNotPassed()

        if not id:
            model = self.get_security_model(symbol)
            if not model:
                raise NotFound()
            id = model.id

        model = self.get_security_cache(id)
        if not model:
            model = await self.fetch_security_response(id)

        return model

    async def fetch_security_response(self, id: int):
        data = await self._client_wrapper.get_json(f"{BASE_URL}/{id}")
        if not data:
            raise NotFound()

        data = humps.decamelize(data)

        model = SecurityResponse(**data)
        self.create_security_cache(model)
        return model
