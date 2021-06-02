import asyncio

from nepse import Client


async def main():
    client = Client()
    data = await client.security_client.get_company(symbol="UPPER")
    print(data.security_daily_trade_dto.high_price)
    await client.close()


asyncio.run(main())
