import functools
from inspect import iscoroutinefunction


def securities_are_cached(func):
    @functools.wraps(func)
    async def predicate(self, *args, **kwargs):
        if not self._securities_basic_cache:
            await self._update_basic_securities_cache()
        if iscoroutinefunction(func):
            return await func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)

    return predicate
