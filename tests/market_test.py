from http import client
import sys

from nepse.utils import _ClientWrapperHTTPX

sys.path.append("..")

import httpx
import pytest

from nepse import Client


@pytest.mark.asyncio
async def test_market_open():
    async with httpx.AsyncClient() as async_client:

        client = Client(httpx_client=async_client)
        market_wrapper_data = await client.market_client.market_is_open()

    async with httpx.AsyncClient() as async_client:

        wrapper_client = _ClientWrapperHTTPX(async_client)
        response = await wrapper_client._get_json(
            "https://newweb.nepalstock.com/api/nots/nepse-data/market-open"
        )
        if response["isOpen"] != "CLOSE":
            real_data = True
        real_data = False

    assert real_data == market_wrapper_data


@pytest.mark.asyncio
async def test_IPO():
    async with httpx.AsyncClient() as async_client:

        client = Client(httpx_client=async_client)
        ipo_result = await client.market_client.check_IPO("MLBSL", 1301310000123606)

    assert ipo_result == False


@pytest.mark.asyncio
async def test_market_summaries():
    async with httpx.AsyncClient() as async_client:

        client = Client(httpx_client=async_client)
        market_summaries = await client.market_client.get_market_summaries()

    assert market_summaries
