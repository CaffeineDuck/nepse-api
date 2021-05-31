import functools


def is_cached(func):
    @functools.wraps(func)
    async def predicate(self, *args, **kwargs):
        if not self._securities_basic_cache:
            await self._update_basic_securities_cache()
        return await func(self, *args, **kwargs)

    return predicate
