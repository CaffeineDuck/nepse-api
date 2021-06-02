import asyncio

import httpx

import nepse
from nepse import Client


async def main():
    company_name = input("Enter company name: ")
    async with httpx.AsyncClient() as async_client:
        client = Client(httpx_client=async_client)
        data = await client.security_client.get_companies()

        filtered = nepse.utils.get(data, security_name=company_name)
        if not filtered:
            raise ValueError("The given company name was not found!")
        else:
            print(filtered)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
