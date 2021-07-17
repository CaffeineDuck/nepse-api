import sys

sys.path.append("..")

import asyncio
from dataclasses import asdict

import httpx
import humps
import pytest

from nepse import Client
from nepse.utils import _ClientWrapperHTTPX


@pytest.mark.asyncio
async def test_all_companies():
    """This is a test for seeing if the all companies method works"""

    async with httpx.AsyncClient() as async_client:
        nepse_client = Client(httpx_client=async_client)
        api_data = await nepse_client.security_client.get_companies()
        assert api_data

    assert api_data


@pytest.mark.asyncio
async def test_right_detailed_security_data():
    """This is a test for seeing if the `get_company_detailed` method provides right data"""

    async with httpx.AsyncClient() as async_client:
        wrapper_client = _ClientWrapperHTTPX(async_client)
        data = await wrapper_client._post_json_defualt_body(
            "https://newweb.nepalstock.com/api/nots/security/2792"
        )
        api_data = humps.decamelize(data)

    async with httpx.AsyncClient() as async_client:
        nepse_client = Client(httpx_client=async_client)
        wrapper_data = asdict(
            await nepse_client.security_client.get_company_detailed(2792)
        )

    assert api_data == wrapper_data


@pytest.mark.asyncio
async def test_right_security_data():
    """This is a test for seeing if the `get_company` method provides right data"""

    async with httpx.AsyncClient() as async_client:
        wrapper_client = _ClientWrapperHTTPX(async_client)
        data = await wrapper_client._get_json(
            "https://newweb.nepalstock.com/api/nots/securityDailyTradeStat/58"
        )
        security = (
            list(filter(lambda company: company.get("symbol") == "UPPER", data))
        )[0]
        api_data = humps.decamelize(security)

    async with httpx.AsyncClient() as async_client:
        nepse_client = Client(httpx_client=async_client)
        wrapper_data = asdict(
            await nepse_client.security_client.get_company(symbol="UPPER")
        )

    assert api_data == wrapper_data


@pytest.mark.asyncio
async def test_company_history():
    """This is a test for seeing if the `get_company_history` method provides right data"""
    async with httpx.AsyncClient() as async_client:

        client = Client(httpx_client=async_client)
        wrapper_data = [
            asdict(date)
            for date in await client.security_client.get_company_history(2792)
        ]

    async with httpx.AsyncClient() as async_client:

        wrapper_client = _ClientWrapperHTTPX(async_client)
        response = await wrapper_client._post_json_defualt_body(
            "https://newweb.nepalstock.com/api/nots/market/graphdata/2792"
        )
        api_data = humps.decamelize(response)

    assert api_data == wrapper_data
