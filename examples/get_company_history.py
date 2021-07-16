import asyncio

import httpx

from nepse import Client


async def main():
    async with httpx.AsyncClient() as async_client:
        client = Client(async_client)

        # 2919 is code for NIFRA(Nepal Infrastructre Bank Limited)
        history = await client.security_client.get_company_history(2919)

        # Returns a list of all the details about the company.
        print(history)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
