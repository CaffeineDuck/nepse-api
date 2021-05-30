import asyncio

from nepse.core import Client


async def main():
    client = Client()
    data = await client.get_company(symbol="UPPER")
    await client.close()

asyncio.run(main())