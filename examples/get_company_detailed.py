import asyncio

import httpx

from nepse import Client


async def main():
    async with httpx.AsyncClient() as async_client:
        client = Client(async_client)

        # 2919 is code for NIFRA(Nepal Infrastructre Bank Limited)
        company = await client.security_client.get_company_detailed(2919)
        print(company.security.symbol)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
