import asyncio
from dataclasses import asdict
from textwrap import wrap

import httpx
import humps
import pytest

from nepse import Client
from nepse.utils import ClientWrapperHTTPX


@pytest.mark.asyncio
async def test_all_companies():
    async with httpx.AsyncClient() as async_client:
        await asyncio.sleep(0.1)
        nepse_client = Client(httpx_client=async_client)
        api_data = await nepse_client.security_client.get_companies()
        assert api_data

    assert api_data


@pytest.mark.asyncio
async def test_right_detailed_security_data():
    async with httpx.AsyncClient() as async_client:
        await asyncio.sleep(0.1)
        wrapper_client = ClientWrapperHTTPX(async_client)
        data = await wrapper_client.get_json(
            "https://newweb.nepalstock.com/api/nots/security/2792"
        )
        api_data = humps.decamelize(data)

    async with httpx.AsyncClient() as async_client:
        await asyncio.sleep(0.1)
        nepse_client = Client(httpx_client=async_client)
        wrapper_data = asdict(
            await nepse_client.security_client.get_company_detailed(2792)
        )

    assert api_data == wrapper_data


@pytest.mark.asyncio
async def test_right_security_data():
    async with httpx.AsyncClient() as async_client:
        await asyncio.sleep(0.1)
        wrapper_client = ClientWrapperHTTPX(async_client)
        data = await wrapper_client.get_json(
            "https://newweb.nepalstock.com/api/nots/securityDailyTradeStat/58"
        )
        security = (
            list(filter(lambda company: company.get("symbol") == "UPPER", data))
        )[0]
        api_data = humps.decamelize(security)

    async with httpx.AsyncClient() as async_client:
        await asyncio.sleep(0.1)
        nepse_client = Client(httpx_client=async_client)
        wrapper_data = asdict(
            await nepse_client.security_client.get_company(symbol="UPPER")
        )

    assert api_data == wrapper_data

@pytest.mark.asyncio
async def test_market_open():
    async with httpx.AsyncClient() as async_client:
        await asyncio.sleep(0.1)

        client = Client(httpx_client=async_client)
        market_wrapper_data = await client.market_client.market_is_open()

    async with httpx.AsyncClient() as async_client:
        await asyncio.sleep(0.1)

        wrapper_client = ClientWrapperHTTPX(async_client)
        response = await wrapper_client.get_json('https://newweb.nepalstock.com/api/nots/nepse-data/market-open')
        if response['isOpen'] !='CLOSE':
            real_data = True
        real_data = False

    assert real_data == market_wrapper_data
