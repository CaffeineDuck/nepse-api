import json
from json import JSONDecodeError
from operator import attrgetter
from typing import Any, Iterable, Optional, TypeVar

import attr
import httpx

from nepse.errors import APIError

T = TypeVar("T")


@attr.frozen
class _ClientWrapperHTTPX:
    _client: httpx.AsyncClient

    async def _get_json(self, url: str) -> object:
        try:
            return (await self._client.get(url)).json()
        except JSONDecodeError:
            raise APIError()

    # Created this cause NEPSE API requires POST request
    # with `{"id": 678}` in body.
    async def _post_json_defualt_body(self, url: str) -> object:
        body = {"id": 678}
        return (await self._client.post(url, json=body)).json()

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
