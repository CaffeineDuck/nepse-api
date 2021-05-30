import asyncio

from nepse.core import Client


async def main():
    client = Client()
    data = await client.get_company(symbol="UPPER")
    print(data.daily_trade.high_price)
    await client.close()

asyncio.run(main())