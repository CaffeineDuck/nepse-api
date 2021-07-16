import asyncio
import httpx
from nepse import Client


async def main():
    async with httpx.AsyncClient() as async_client:
        client = Client(async_client)

        """Using this method may take upto 200 seconds, and may take upto 350 MB of memory.
            This returns a list.
        """
        floorsheet = await client.market_client.get_floorsheets()

        print(floorsheet[0])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
