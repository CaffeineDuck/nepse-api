from nepse.errors import NotFound
from nepse.security.types import (
    LiveSecurityTrade,
    SecurityResponse,
    SecurityResponseDetailed,
)
from typing import List, Mapping, Optional

import humps
from cachetools import TTLCache
from nepse.utils import ClientWrapperHTTPX
from nepse.utils import get

from .decorators import securities_are_cached

BASE_URL = "https://newweb.nepalstock.com/api/nots/security"
BASE_SECURITIES_URL = "https://newweb.nepalstock.com/api/nots/securityDailyTradeStat/58"
BASE_LIVE_TRADE_URL = (
    "https://newweb.nepalstock.com/api/nots/nepse-data/today-price?&size=500&sort=true"
)


class SecurityClient:
    def __init__(
        self,
        client_wrapper: ClientWrapperHTTPX,
        cache_retain_time: Optional[int] = 60,
        use_cache: Optional[bool] = False,
    ) -> None:
        self._client_wrapper = client_wrapper
        self._cache_retain_time = cache_retain_time
        self._use_cache = use_cache

        self._securities_cache: Mapping[str, SecurityResponse] = TTLCache(
            1000, cache_retain_time
        )

    def _create_security_cache(self, model: SecurityResponse) -> None:
        self._securities_cache[model.symbol] = model

    def _get_security_cache(self, symbol: str) -> SecurityResponse:
        self._securities_cache.get(symbol)

    async def _fetch_security(self, symbol: str) -> SecurityResponse:
        securities = await self._client_wrapper.get_json(BASE_SECURITIES_URL)

        try:
            security = (
                list(
                    filter(lambda company: company.get("symbol") == symbol, securities)
                )
            )[0]
        except IndexError:
            raise NotFound()

        security = humps.decamelize(security)

        return SecurityResponse(**security)

    async def _fetch_securities(self) -> List[SecurityResponse]:
        securities = await self._client_wrapper.get_json(BASE_SECURITIES_URL)

        def handle_security(data: dict):
            model = SecurityResponse(**(humps.decamelize(data)))
            self._create_security_cache(model)

        securities_model = [handle_security(security) for security in securities]
        return securities_model

    @securities_are_cached
    async def _get_security(self, symbol: str) -> SecurityResponse:
        return self._get_security_cache(symbol)

    @securities_are_cached
    async def _get_securities(self) -> List[SecurityResponse]:
        return self._securities_cache.values()

    async def get_company(
        self, symbol: str, use_cache: Optional[bool] = None
    ) -> SecurityResponse:
        use_cache = use_cache if use_cache == None else self._use_cache

        if use_cache:
            company = await self._get_security(symbol)
        else:
            company = await self._fetch_security(symbol)

        return company

    async def get_companies(
        self, use_cache: Optional[bool] = None
    ) -> List[SecurityResponse]:
        use_cache = use_cache if use_cache == None else self._use_cache

        if use_cache:
            companies = await self._get_securities()
        else:
            companies = await self._fetch_securities()

        return companies

    async def get_company_detailed(self, security_id: int) -> SecurityResponseDetailed:
        detailed_company = await self._client_wrapper.get_json(
            f"{BASE_URL}/{security_id}"
        )

        if not detailed_company:
            raise NotFound()

        detailed_company = humps.decamelize(detailed_company)
        return SecurityResponseDetailed(**detailed_company)

    async def get_company_live_price(self, symbol: str) -> LiveSecurityTrade:
        live_prices = humps.decamelize(
            (await self._client_wrapper.get_json(BASE_LIVE_TRADE_URL)).get("content")
        )

        try:
            security = (
                list(
                    filter(lambda company: company.get("symbol") == symbol, live_prices)
                )
            )[0]
        except IndexError:
            raise NotFound()

        return LiveSecurityTrade(**security)

    async def get_companies_live_prices(self) -> List[LiveSecurityTrade]:
        live_prices = humps.decamelize(
            (await self._client_wrapper.get_json(BASE_LIVE_TRADE_URL)).get("content")
        )
        return [LiveSecurityTrade(**model) for model in live_prices]
