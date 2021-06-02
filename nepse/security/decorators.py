import functools
from inspect import iscoroutinefunction
from typing import Callable, TypeVar

_T = TypeVar("_T")


def securities_are_cached(func: _T) -> _T:
    @functools.wraps(func)
    async def predicate(self, *args, **kwargs):
        if not self._securities_basic_cache:
            await self._fetch_securities_cache()
        if iscoroutinefunction(func):
            return await func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)

    return predicate
