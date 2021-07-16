import asyncio

import httpx

from nepse import Client


async def main():
    async with httpx.AsyncClient() as async_client:
        client = Client(async_client)

        # check_IPO takes in two parameters, company scrip and BOID
        result = await client.market_client.check_IPO("MSLBSL", 130110000000000)

        # This returns a boolean value
        print(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
