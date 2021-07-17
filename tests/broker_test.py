import sys

sys.path.append("..")

import httpx
import pytest

from nepse import Client


@pytest.mark.asyncio
async def test_broker():
    async with httpx.AsyncClient() as async_client:

        client = Client(httpx_client=async_client)
        wrapper_broker = await client.broker_client.get_broker(id=116)

    assert wrapper_broker.member_name == "Ashutosh Brokerage & Securities (PVT) Ltd."


@pytest.mark.asyncio
async def test_brokers():
    async with httpx.AsyncClient() as async_client:

        client = Client(httpx_client=async_client)
        wrapper_broker = await client.broker_client.get_brokers()

    assert wrapper_broker
