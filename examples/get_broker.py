import asyncio

import httpx

from nepse import Client


async def main():
    async with httpx.AsyncClient() as async_client:
        client = Client(async_client)

        # Getting broker by Broker number.
        get_by_id = await client.broker_client.get_broker(member_code=42)

        # Getting broker by Broker name.
        get_by_name = await client.broker_client.get_broker(
            member_name="Sani Securities Company Ltd."
        )

        # Returns details about a broker.
        print(get_by_id)
        print(get_by_name)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
