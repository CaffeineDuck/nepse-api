from json import JSONDecodeError

import attr
import httpx


@attr.frozen
class ClientWrapperHTTPX:
    _client: httpx.AsyncClient

    async def get_json(self, url) -> object:
        return (await self._client.get(url)).json()
      