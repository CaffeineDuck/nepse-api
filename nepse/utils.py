from operator import attrgetter
from typing import Any, Iterable, Optional, TypeVar

import attr
import httpx

T = TypeVar("T")


@attr.frozen
class ClientWrapperHTTPX:
    _client: httpx.AsyncClient

    async def get_json(self, url) -> object:
        return (await self._client.get(url)).json()


def get(iterable: Iterable[T], **attrs: Any) -> Optional[T]:
    attrget = attrgetter

    # Special case the single element call
    if len(attrs) == 1:
        k, v = attrs.popitem()
        pred = attrget(k.replace("__", "."))
        for elem in iterable:
            if pred(elem) == v:
                return elem
        return None

    converted = [
        (attrget(attr.replace("__", ".")), value) for attr, value in attrs.items()
    ]

    for elem in iterable:
        if all(pred(elem) == value for pred, value in converted):
            return elem
    return None
