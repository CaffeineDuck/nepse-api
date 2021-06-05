from typing import List, Mapping, Optional

import humps
from cachetools import TTLCache

import nepse
from nepse.broker.decorators import brokers_are_cached
from nepse.broker.types import BrokerResponse
from nepse.utils import _ClientWrapperHTTPX

BASE_URL = "https://newweb.nepalstock.com/api/nots/member?&size=500"


class BrokerClient:
    def __init__(
        self,
        client_wrapper: _ClientWrapperHTTPX,
        use_cache: bool,
        cache_retain_time: int,
    ):
        self._client_wrapper = client_wrapper
        self._use_cache = use_cache
        self._cache_retain_time = cache_retain_time

        self._brokers_cache: Mapping[int, BrokerResponse] = TTLCache(
            1000, cache_retain_time
        )

    def _create_broker_cache(self, model: BrokerResponse) -> None:
        self._brokers_cache[model.id] = model

    def _get_broker_cache(self, id: int) -> BrokerResponse:
        return self._brokers_cache.get(id)

    def _create_broker_model(self, data: dict):
        data = humps.decamelize(data)
        model = BrokerResponse(**data)
        self._create_broker_cache(model)
        return model

    async def _fetch_brokers(self) -> List[BrokerResponse]:
        brokers = (await self._client_wrapper._get_json(BASE_URL)).get("content")
        return [self._create_broker_model(data) for data in brokers]

    async def _fetch_broker(self, **attrs) -> BrokerResponse:
        models = await self._fetch_brokers()
        return nepse.utils.get(models, **attrs)

    @brokers_are_cached
    def _get_brokers(self) -> List[BrokerResponse]:
        return self._brokers_cache.values()

    @brokers_are_cached
    def _get_broker(self, **attrs) -> BrokerResponse:
        models = self._brokers_cache.values()
        return nepse.utils.get(models, **attrs)

    async def get_broker(
        self, use_cache: Optional[bool] = None, **attrs
    ) -> BrokerResponse:
        """Get the broker by its attributes

        Args:
            use_cache (Optional[bool]): To use or not to use cache while getting broker data.
                Defaults to `nepse.Client.use_cache`

        Returns:
            BrokerResponse: The response about the broker

        Examples:
            Getting Broker by member_code:

            .. code-block:: python

                imperial = client.broker_client.get_broker(member_code=45)


            Getting Broker by name:

            .. code-block:: python

                imperial = client.broker_client.get_broker(member_name="Imperial Securities Company Pvt. Ltd.")

        """
        use_cache = use_cache or self._use_cache

        if use_cache:
            broker = await self._get_broker(**attrs)
        else:
            broker = await self._fetch_broker(**attrs)

        return broker

    async def get_brokers(
        self, use_cache: Optional[bool] = None
    ) -> List[BrokerResponse]:
        """Returns the list of every broker

        Args:
            use_cache (Optional[bool]): To use or not to use cache while getting broker data.
                    Defaults to `nepse.Client.use_cache`

        Returns:
            List[BrokerResponse]: List of all the brokers in Nepal.
        """
        use_cache = use_cache or self._use_cache

        if use_cache:
            brokers = await self._get_brokers()
        else:
            brokers = await self._fetch_brokers()

        return brokers
