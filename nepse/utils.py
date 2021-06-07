import json
from json import JSONDecodeError
from operator import attrgetter
from typing import Any, Iterable, Optional, TypeVar

import attr
import httpx

from nepse.errors import APIError

T = TypeVar("T")

PAYLOAD_ID_MARKET_ID_MAP = {
    5: 167,
    11: 318,
    12: 482,
    13: 574,
    14: 895,
    16: 620,
    17: 345,
    18: 326,
    19: 515,
    24: 662,
    25: 198,
    27: 511,
    28: 469,
    29: 537,
    30: 352,
    31: 407,
}


@attr.frozen
class _ClientWrapperHTTPX:
    _client: httpx.AsyncClient

    async def _get_json(self, url: str) -> object:
        try:
            return (await self._client.get(url)).json()
        except JSONDecodeError:
            raise APIError()

    # Created this cause NEPSE API requires POST request
    # with `{"id": <some number>}` in body.
    async def _post_json_defualt_body(self, url: str) -> object:
        payload_id = PAYLOAD_ID_MARKET_ID_MAP.get(
            (
                await self._get_json(
                    "https://newweb.nepalstock.com/api/nots/nepse-data/market-open"
                )
            ).get("id")
        )
        return (await self._client.post(url, json={"id": payload_id})).json()

    async def _post_json(self, url: str, body: dict) -> object:
        """[summary]

        Args:
            url (str): [description]
            body (dict): [description]

        Returns:
            object: [description]
        """
        return (await self._client.post(url, json=body)).json()


def get(iterable: Iterable[T], **attrs: Any) -> Optional[T]:
    """A helper that returns the first element in the iterable that meets
    all the traits passed in ``attrs``.

    Args:
        iterable (Iterable): An iterable to search through.
        **attrs (Any): Keyword arguments that denote attributes to search with.
    """
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
