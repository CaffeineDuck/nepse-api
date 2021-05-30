from typing import List, Optional

from aiohttp import ClientSession
from cachetools import LRUCache, TTLCache

from nepse.errors import NotFound, SymbolOrIdNotPassed
from nepse.security.converters import create_reponse_object
from nepse.security.decorators import is_cached
from nepse.security.types import BaseSecurity, SecurityResponse

BASE_URL = "https://newweb.nepalstock.com/api/nots/security/"


class SecurityClient:
    def __init__(self, session: ClientSession) -> None:
        self._session = session
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
        securities = await (await self._session.get(BASE_URL)).json()

        def create_security_object(security: dict):
            model = BaseSecurity(
                id=security.get("id"),
                symbol=security.get("symbol"),
                active_status=security.get("activeStatus"),
                name=security.get("name"),
            )
            self.create_security_model(model)
            return model

        securities_objects = [
            create_security_object(security) for security in securities
        ]
        return securities_objects

    # TODO: work with the decorator for checks!
    # @is_cached
    async def get_security_response(
        self, id: Optional[int], symbol: Optional[str]
    ) -> SecurityResponse:
        if not self._securities_basic_cache:
            await self._update_basic_securities_cache()

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
        data = await (await self._session.get(f"{BASE_URL}/{id}")).json()
        if not data:
            raise NotFound()

        model = create_reponse_object(data)
        self.create_security_cache(model)
        return model
